from .utils import URL

SHIKIMORI_URL = 'https://shikimori.me'

AUTH_ENDPOINT = SHIKIMORI_URL + '/oauth/authorize'
TOKEN_ENDPOINT = SHIKIMORI_URL + '/oauth/token'
API_ROOT = SHIKIMORI_URL + '/api'

auth_endpoint = URL(AUTH_ENDPOINT)
token_endpoint = URL(TOKEN_ENDPOINT)
api_endpoint = URL(API_ROOT)
