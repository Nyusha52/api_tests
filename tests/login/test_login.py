import pytest

from fixtures.constants import ResponseText
from fixtures.register.model import RegisterUser, RegisterUserResponse
from fixtures.auth.model import AuthUser


class TestLoginUser:
    def test_login_user_with_valid_data(self, app):
        """
        Steps.
            1. Try to login user with valid data
            2. Check that status code is 200
            3. Check response
        """
        data = RegisterUser.random()
        res = app.register.register(data=data, type_response=RegisterUserResponse)
        assert res.status_code == 201
        assert res.data.message == ResponseText.MESSAGE_REGISTER_USER
        res_auth = app.auth.login(data=data, type_response=None)
        assert res_auth.status_code == 200

    def test_login_user_with_not_registred_data(self, app):
        """
        Steps.
            1. Try to login user with invalid data
            2. Check that status code is 401
            3. Check response
        """
        data = AuthUser.random()
        res = app.auth.login(data=data)
        assert res.status_code == 401

    @pytest.mark.parametrize("field", ["username", "password"])
    def test_auth_empty_data(self, app, field):
        """
        Steps.
            1. Try to login user with empty data
            2. Check that status code is 401
            3. Check response
        """
        data = AuthUser.random()
        setattr(data, field, None)
        res = app.auth.login(data)
        assert res.status_code == 401