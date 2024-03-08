import asyncio
from functools import partial
from typing import List

import httpx

from .endpoints import auth_endpoint, token_endpoint, api_endpoint, graphql_endpoint
from .utils import Limiter
from .enums import AnimeStatus
from .datatypes import ShikimoriToken


class ShikimoriExtendedAPI:
    limiter_5rps = Limiter(5, 1, name="5rps")
    limiter_90rpm = Limiter(90, 60, name="90rpm")

    def __init__(
            self,
            *,
            application_name: str,
            client_id: str = None,
            client_secret: str = None,
            redirect_uri: str = 'urn:ietf:wg:oauth:2.0:oob'
    ):
        self.application_name = application_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @property
    def auth_url(self):  # TODO add scopes
        q = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ''
        }

        return auth_endpoint(**q)

    @limiter_5rps
    @limiter_90rpm
    async def _request(self, method: str, url: str, **kwargs) -> dict:
        # print(f"[{datetime.now()}] {method} {url} {headers} {kwargs}")  # TODO logging

        headers = kwargs.pop('headers', None) or {}
        headers.update({'User-Agent': self.application_name})  # this header is required according to API documentation

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, **kwargs)

            if response.status_code != 200:
                raise response.raise_for_status()  # TODO exception handling

            return response.json()

    def get(self, url: str, *, token: ShikimoriToken = None, **kwargs):
        if token:
            kwargs.setdefault('headers', {}).update({'Authorization': f'Bearer {token.access_token}'})
        return self._request('get', url, **kwargs)

    def post(self, url: str, *, token: ShikimoriToken = None, **kwargs):
        if token:
            kwargs.setdefault('headers', {}).update({'Authorization': f'Bearer {token.access_token}'})
        return self._request('post', url, **kwargs)

    async def get_access_token(self, auth_code: str) -> ShikimoriToken:
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        return ShikimoriToken(**await self.post(token_endpoint(), data=data))

    async def get_current_user_info(self, token: ShikimoriToken) -> dict:
        try:
            info = await self.get(api_endpoint.users.whoami(), token=token)
        except httpx.HTTPStatusError as err:
            if err.response.status_code != 401:
                raise

            await self.refresh_tokens()
            info = await self.get(api_endpoint.users.whoami(), token=token)

        return info

    async def get_user_info(self, user_id: int) -> dict:
        return await self.get(api_endpoint.users.id(user_id).info())

    async def get_all_user_rates(
            self,
            user_id: int,
            *,
            status: List[AnimeStatus] | AnimeStatus = None,
            censored: bool = False
    ) -> list:
        if not isinstance(status, list):
            status = [status, ]

        rates = []
        for particular_status in status:
            limit, page = 100, 1  # limit per request, current page
            while True:
                r_ = await self.get(
                    api_endpoint.users.id(user_id).anime_rates(
                        limit=limit,
                        status=particular_status and particular_status.value,
                        censored=str(censored).lower(),
                        page=page
                    )
                )
                rates.extend(r_[:limit])
                if len(r_) <= limit:
                    break
                page += 1
        return rates

    async def get_anime(self, anime_id: int):
        return await self.get(api_endpoint.animes.id(anime_id))

    async def _get_titles(self, titles_ids: List[int]) -> List[dict]:
        tasks = []
        async with asyncio.TaskGroup() as group:
            for title_id in titles_ids:
                anime_info = group.create_task(
                    self.__request_again_on_2_many_requests_ex(
                        partial(self.get, api_endpoint.animes.id(title_id)())),
                    name=f"ID:{title_id}"
                )
                tasks.append(anime_info)
        return [task.result() for task in tasks]

    # TODO rework with any library
    @staticmethod
    def _build_graphql_query_for_total_watch_time(user_id: int, status: AnimeStatus, page: int) -> str:
        return f"""
        {{
          userRates(userId: "{user_id}", targetType: Anime, status: {status.value}, limit: 50, page: {page}) {{
            score
            status
            episodes
            rewatches
            anime {{
              english
              duration
              episodes
            }}
          }}
        }}
        """

    async def fetch_total_watch_time_graphql(self, user_id: int) -> float:
        statuses = [
            AnimeStatus.WATCHING,
            AnimeStatus.COMPLETED,
            AnimeStatus.DROPPED,
            AnimeStatus.ON_HOLD,
            AnimeStatus.REWATCHING
        ]

        scores = []

        for status in statuses:
            page = 1
            while True:
                graph_query = self._build_graphql_query_for_total_watch_time(user_id, status, page)
                response = await self.post(graphql_endpoint(), data={'query': graph_query})
                scores.extend(response['data']['userRates'])

                if not response['data']['userRates']:
                    break

                page += 1

        return sum([score['episodes'] * score['anime']['duration'] * (score['rewatches'] + 1) for score in scores])

    # It can take a super long time to be executed!!! TODO rework with graphql
    async def fetch_total_watch_time(self, user_id: int, *, accurate: bool = False) -> float:
        # get all user rates
        user_rates = await self.get_all_user_rates(
            user_id,
            status=[  # get all rates w/o `planned` titles, because planned have 0 finished episodes
                AnimeStatus.WATCHING,
                AnimeStatus.COMPLETED,
                AnimeStatus.DROPPED,
                AnimeStatus.ON_HOLD,
                AnimeStatus.REWATCHING
            ]
        )

        if accurate:
            # get complete info about all titles watched (including accurate duration)
            titles_info = await self._get_titles([rate['anime']['id'] for rate in user_rates])
            durations = [title['duration'] or 23 for title in titles_info]  # 23min - standard duration of an episode
            finished_episodes = [rate['episodes'] for rate in user_rates]
            return sum([dur * episodes for dur, episodes in zip(durations, finished_episodes)])
        else:
            # assume every episode = 23min, so we get coarse total watch time
            finished_episodes = [rate['episodes'] for rate in user_rates]
            return sum(map(lambda x: x * 23, finished_episodes))

    async def __request_again_on_2_many_requests_ex(self, request, retries: int = 0) -> dict:
        MAX_RETRIES = 3
        if retries >= MAX_RETRIES:
            raise Exception(f"Too Many Requests: {MAX_RETRIES} retries")  # TODO implement custom exception

        try:
            return await request()
        except httpx.HTTPStatusError as err:
            if err.response.status_code != 429:
                raise

            return await self.__request_again_on_2_many_requests_ex(request, retries + 1)

    async def refresh_tokens(self):
        raise NotImplementedError


Client = ShikimoriExtendedAPI
