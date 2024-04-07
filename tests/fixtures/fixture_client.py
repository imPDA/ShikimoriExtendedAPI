import pytest as pytest
from src.shikimoriextendedapi.shikimoriextendedapi.client import ShikimoriExtendedAPI


@pytest.fixture(scope="session")
def client():
    client = ShikimoriExtendedAPI(
        application_name='test_application_name',
        client_id='test_client_id',
        client_secret='test_client_secret',
        redirect_uri='http://test/redirect/url'
    )

    yield client
