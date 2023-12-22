import asyncio
import re
from datetime import datetime
from functools import partial
from urllib.parse import urlencode

import httpx

from shikimori_extended_api.utils.url_builder import auth_endpoint, token_endpoint, api_endpoint
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

    async def get_all_user_anime_rates(
            self,
            user_id: int,
            *,
            status: AnimeStatus | str = None,
            censored: bool = None
    ) -> list:
        if not isinstance(status, AnimeStatus):
            status = AnimeStatus(status)

        L, p, rates = 100, 1, []  # limit per request, current page, list of rates
        while True:
            r_ = await self.get(
                api_endpoint.users.id(user_id).anime_rates(limit=L, status=status.value, censored=censored, page=p)
            )
            rates.extend(r_[:L])
            if len(r_) <= L:
                return rates
            p += 1

    async def get_anime(self, anime_id: int):
        return await self.get(api_endpoint.animes.id(anime_id))

    async def __request_again_on_2_many_requests_ex(self, request, retries: int = 0) -> dict:
        MAX_RETRIES = 3
        if retries >= MAX_RETRIES:
            raise Exception(f"Too Many Requests: {MAX_RETRIES} retries")

        try:
            return await request()
        except httpx.HTTPStatusError as err:
            if err.response.status_code != 429:
                raise

            return await self.__request_again_on_2_many_requests_ex(request, retries + 1)

    # It can take a super long time to be executed!!! TODO think how it can be speed up
    async def fetch_total_watch_time(self, user_id: int) -> float:
        titles = await self.get_all_user_anime_rates(user_id)
        tasks = []
        async with asyncio.TaskGroup() as group:
            for title in titles:
                anime_info = group.create_task(
                    self.__request_again_on_2_many_requests_ex(partial(self.get, api_endpoint.animes.id(title['anime']['id']))),
                    name=f"ID{title['anime']['id']}"
                )
                tasks.append(anime_info)

        durations = [task.result()['duration'] or 23 for task in tasks]  # 23mim - standard duration of an anime episode
        amount_of_episodes = [title['episodes'] for title in titles]
        return sum([duration * episodes for duration, episodes in zip(durations, amount_of_episodes)])

    def log_in(self, login: str, password: str):
        raise NotImplementedError

    async def refresh_tokens(self):
        raise NotImplementedError


Client = ShikimoriExtendedAPI
