import pytest

from shikimoriextendedapi.endpoints import SHIKIMORI_URL
from tests.common import BASE_DIR


# IGNORED_PATHS = [
#     "/api/users/whoami",
# ]


# def scrub_string_for_paths(paths: list['str']) -> Callable:
#     def before_record_response(response):
#         print(dir())
#         print(response)
#
#         return response
#     return before_record_response


def is_shikimori_url(r1, r2):
    assert r1.uri == r2.uri and SHIKIMORI_URL in r1.uri


# @pytest.fixture
# def vcr(vcr):
#     vcr.register_matcher('shikimori_matcher', is_shikimori_url)
#     vcr.match_on = ['method', 'shikimori_matcher']
#
#     # vcr.before_record_response = scrub_string_for_paths(IGNORED_PATHS)
#
#     return vcr


def pytest_recording_configure(config, vcr):
    vcr.register_matcher('shikimori_matcher', is_shikimori_url)
    vcr.match_on = ['method', 'shikimori_matcher']


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "record_mode": "new_episodes",
        "filter_headers": [
            ('Authorization', 'DUMMY'),
            ('User-Agent', 'DUMMY')
        ],
        "filter_query_parameters": [
            # none
        ],
        "filter_post_data_parameters": [
            ('client_id', 'DUMMY'),
            ('client_secret', 'DUMMY'),
            ('code', 'DUMMY'),
            ('redirect_uri', 'DUMMY')
        ]
    }


@pytest.fixture
def vcr_cassette_dir(request):
    return str(BASE_DIR / 'vcr_cassettes' / request.module.__name__)


# @pytest.fixture(scope="module")
# def vcr_cassette_name(request):
#     return "shikimori_shared_cassette"
