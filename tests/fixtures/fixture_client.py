import datetime
from urllib.parse import urlencode

import environ
import pytest as pytest
import pytest_asyncio

from shikimoriextendedapi.client import Client
from shikimoriextendedapi.datatypes import ShikimoriToken
from shikimoriextendedapi.endpoints import auth_endpoint

from tests.common import BASE_DIR

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')


@pytest.fixture
def client() -> Client:
    shiki_client = Client(
        application_name=env('APPLICATION_NAME', default='test_application_name'),
        client_id=env('CLIENT_ID', default='test_client_id'),
        client_secret=env('CLIENT_SECRET', default='test_client_secret')
    )

    yield shiki_client


@pytest.fixture
def auth_url() -> str:
    q = {
        'client_id': env('CLIENT_ID', default='test_client_id'),
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'response_type': 'code',
        'scope': ''
    }

    return f"{auth_endpoint}?{urlencode(q)}"


@pytest_asyncio.fixture
async def token() -> ShikimoriToken:
    expires_in = env('EXPIRES_IN', lambda x: datetime.timedelta(seconds=int(x)))
    expires_at = env(
        'EXPIRES_AT',
        cast=lambda x: datetime.datetime(*[int(a) for a in x.split(',')])
    )

    return ShikimoriToken(
        access_token=env('ACCESS_TOKEN'),
        refresh_token=env('REFRESH_TOKEN'),
        expires_in=expires_in,
        expires_at=expires_at
    )


@pytest_asyncio.fixture
async def user_id() -> int:
    return env('USER_ID', cast=int, default=None)
