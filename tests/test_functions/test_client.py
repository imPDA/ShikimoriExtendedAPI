import datetime

import pytest

from shikimoriextendedapi.endpoints import api_endpoint
from tests.utils import Catchtime


def test_auth_url(client, auth_url):
    assert client.auth_url == auth_url


@pytest.mark.vcr
@pytest.mark.default_cassette("users.yaml")
@pytest.mark.asyncio
@pytest.mark.parametrize('user_id', [1, 272747])
async def test_success_get_request(client, user_id):
    result = await client.get(api_endpoint.users.id(user_id))

    assert type(result) is dict
    assert "id" in result
    assert result.get("id") == user_id


# @pytest.mark.vcr()
# @pytest.mark.asyncio
# async def test_success_post_request(client, vcr_cassette):
#     ... TODO


@pytest.mark.vcr
@pytest.mark.default_cassette("whoami.yaml")
@pytest.mark.asyncio
async def test_success_get_request_with_token(client, token, user_id):
    user_info = await client.get(api_endpoint.users.whoami, token=token)

    assert type(user_info) is dict
    assert "id" in user_info
    if user_id:
        assert user_info["id"] == user_id


@pytest.mark.vcr
@pytest.mark.default_cassette("animes.yaml")
@pytest.mark.asyncio
@pytest.mark.parametrize('anime_id', [52991, ])
async def test_success_get_anime_by_id(client, anime_id):
    result = await client.get_anime(anime_id)
    expectation = await client.get(api_endpoint.animes.id(anime_id))

    assert result == expectation
    assert type(result) is dict
    assert "id" in result
    assert result.get("id") == anime_id


@pytest.mark.vcr
@pytest.mark.default_cassette("whoami.yaml")
@pytest.mark.asyncio
async def test_success_get_current_user_info(client, token, user_id):
    user_info = await client.get_current_user_info(token)

    assert type(user_info) == dict
    assert "id" in user_info
    if user_id:
        assert user_info["id"] == user_id


@pytest.mark.vcr
@pytest.mark.default_cassette("users.yaml")
@pytest.mark.asyncio
@pytest.mark.parametrize('user_id', [1, 272747, ])
async def test_success_get_user_info(client, user_id):
    user_info = await client.get_user_info(user_id)

    keys = [
        "id", "nickname", "avatar", "image", "last_online_at", "url", "name",
        "sex", "website", "birth_on", "full_years", "locale"
    ]

    assert type(user_info) == dict
    for key in keys:
        assert key in user_info
    assert user_info.get("id") == user_id


@pytest.mark.vcr("users.yaml", "animes.yaml", record_mode="none")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'url_builder_object', [
        api_endpoint.animes.id(52991),
        api_endpoint.users.id(1)
    ]
)
async def test_success_integration_get_with_url_builder(client, url_builder_object):
    result = await client.get(url_builder_object)

    url_string = str(url_builder_object)
    result_with_string = await client.get(url_string)

    assert result == result_with_string


# @pytest.mark.vcr(allow_playback_repeats=True)
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'url_builder_object', [...]
# )
# async def test_success_integration_get_with_url_builder(
#         client, vcr_cassette, url_builder_object
# ):
#     ... TODO


@pytest.mark.vcr
@pytest.mark.default_cassette("users.yaml")
@pytest.mark.asyncio
@pytest.mark.parametrize('requests_amount', [1, 2, 5, 6, 10, 11])
async def test_success_limiter_5rps(client, requests_amount):
    client.limiter_5rps.history.clear()
    client.limiter_5rps.history.append(datetime.datetime.min)

    client.limiter_90rpm.history.clear()
    client.limiter_90rpm.history.append(datetime.datetime.min)

    with Catchtime() as timer:
        for _ in range(requests_amount):
            await client.get(api_endpoint.users.id(1))

    excepted_duration = (requests_amount - 1) // 5 + 1
    # print(f" {timer.time=}")

    assert timer.time < excepted_duration, "Too slow"
    assert timer.time > excepted_duration - 1, "Too fast"
