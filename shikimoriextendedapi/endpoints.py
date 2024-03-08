from .utils import URL

SHIKIMORI_URL = 'https://shikimori.one'

AUTH_ENDPOINT = SHIKIMORI_URL + '/oauth/authorize'
TOKEN_ENDPOINT = SHIKIMORI_URL + '/oauth/token'
API_ROOT = SHIKIMORI_URL + '/api'
GRAPHQL_ENDPOINT = API_ROOT + '/graphql'

auth_endpoint = URL(AUTH_ENDPOINT)
token_endpoint = URL(TOKEN_ENDPOINT)

api_endpoint = URL(API_ROOT)
graphql_endpoint = URL(GRAPHQL_ENDPOINT)

__all__ = [
    'api_endpoint',
    'graphql_endpoint'
]
