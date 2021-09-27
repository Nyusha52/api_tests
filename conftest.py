import logging

import pytest

from fixtures.app import StoreApp
from fixtures.auth.model import AuthUserResponse, AuthUserType
from fixtures.register.model import RegisterUser, RegisterUserResponse

logger = logging.getLogger("api")


@pytest.fixture(scope="session")
def app(request):
    url = request.config.getoption("--api-url")
    logger.info(f"Start api tests, url is {url}")
    return StoreApp(url)


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        help="enter api url",
        default="https://stores-tests-api.herokuapp.com",
    ),


@pytest.fixture
def auth_user(app):
    data = RegisterUser.random()
    res_register = app.register.register(data=data, type_response=RegisterUserResponse)
    res_auth = app.auth.login(data=data, type_response=AuthUserResponse)
    token = res_auth.data.access_token
    header = {"Authorization": f"JWT {token}"}
    user_uuid = res_register.data.uuid
    return AuthUserType(header, user_uuid)