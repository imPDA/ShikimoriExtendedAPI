from .utils import EndpointURL

SHIKIMORI_URL = 'https://shikimori.one'

AUTH_ENDPOINT = SHIKIMORI_URL + '/oauth/authorize'
TOKEN_ENDPOINT = SHIKIMORI_URL + '/oauth/token'
API_ROOT = SHIKIMORI_URL + '/api'
GRAPHQL_ENDPOINT = API_ROOT + '/graphql'

auth_endpoint = EndpointURL(AUTH_ENDPOINT)
token_endpoint = EndpointURL(TOKEN_ENDPOINT)

api_endpoint = EndpointURL(API_ROOT)
graphql_endpoint = EndpointURL(GRAPHQL_ENDPOINT)

__all__ = [
    'api_endpoint',
    'graphql_endpoint'
]
