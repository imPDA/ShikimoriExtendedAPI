import pytest

from src.shikimoriextendedapi.shikimoriextendedapi.endpoints import (
    SHIKIMORI_URL,
    URL,
    api_endpoint
)

from tests.utils.results import expected


TESTCASES_1 = [
    # start endpoint
    (api_endpoint, *expected(URL(f"{SHIKIMORI_URL}/api"))),
]


@pytest.mark.parametrize('path, expected_result, error', TESTCASES_1)
def test_success_creation(path, expected_result, error):
    with error:
        assert type(path) is URL
        assert path.url == expected_result.url
        assert str(path) == str(expected_result)


TESTCASES_2 = [
    # start endpoint
    (api_endpoint, *expected(f"{SHIKIMORI_URL}/api")),

    # test id(), paste() and __getitem__
    (api_endpoint.animes.id(555555), *expected(f"{SHIKIMORI_URL}/api/animes/555555")),
    (api_endpoint.animes.paste(555555), *expected(f"{SHIKIMORI_URL}/api/animes/555555")),
    (api_endpoint.animes[555555], *expected(f"{SHIKIMORI_URL}/api/animes/555555")),

    # test simple endpoint
    (api_endpoint.v2.user_rates, *expected(f"{SHIKIMORI_URL}/api/v2/user_rates")),
]


@pytest.mark.parametrize('path, expected_result, error', TESTCASES_2)
def test_success_string_representation(path, expected_result, error):
    with error:
        assert str(path) == expected_result
