import pytest

from fixtures.userinfo.model import UserInfo, UpdateUserInfoResponse, UserInfoResponse


class TestUserInfo:
    def test_add_user_info(self, app, auth_user):
        """
        Steps.
            1. Try to login user with valid data
            2. Check that status code is 200
            3. Check response
        """
        data = UserInfo.random()
        res = app.userinfo.add_user_info(user_id=auth_user.uuid, data=data, header=auth_user.header,  type_response=UserInfoResponse)
        assert res.status_code == 200

class TestEditUserInfo:
    def test_edit_user_info(self, app, user_info):
        """
        Steps.
            1. Try to login user with valid data
            2. Check that status code is 200
            3. Check response
        """
        data = UserInfo.random()
        res = app.userinfo.edit_user_info(user_id=user_info.uuid, data=data, header=user_info.header,
                                          type_response=UpdateUserInfoResponse)
        assert res.status_code == 200

    @pytest.mark.parametrize("uuid", ["ffddass", "@/&", -55, True])
    def test_update_invalid_id_userinfo(self, app, user_info, uuid):
        """
        Steps.
            1. Try to login user with valid data
            2. Add user info
            3. Change user data
            4. Check that status code is 200
            5. Check response
        """
        data = UserInfo.random()

        res = app.userinfo.edit_user_info(
            user_id=uuid,
            data=data,
            type_response=UpdateUserInfoResponse,
            header=user_info.header,
        )
        assert res.status_code == 404

    def test_none_exist_id_userinfo(self, app, user_info, uuid=1000):
        """
        Steps.
            1. Try to login user with valid data
            2. Add user info
            3. Change user data
            4. Check that status code is 200
            5. Check response
        """
        data = UserInfo.random()

        res = app.userinfo.edit_user_info(
            user_id=uuid,
            data=data,
            type_response=None,
            header=user_info.header,
        )
        assert res.status_code == 404

    @pytest.mark.xfail(reason="Ожидается 400 ошибка")
    def test_invalid_phone_userinfo(self, app, user_info, phone="1" * 10000):
        """
        Steps.
            1. Try to login user with valid data
            2. Add user info
            3. Change user data
            4. Check that status code is 200
            5. Check response
        """
        data = UserInfo.random()
        setattr(data, "phone", phone)
        res = app.userinfo.edit_user_info(
            user_id=user_info.uuid,
            data=data,
            type_response=None,
            header=user_info.header,
        )
        assert res.status_code == 400

    def test_update_userinfo_wo_header(self, app, user_info):
        """
        Steps.
            1. Try to login user with valid data
            2. Add user info
            3. Change user data
            4. Check that status code is 200
            5. Check response
        """
        data = UserInfo.random()
        res = app.userinfo.edit_user_info(
            user_id=user_info.uuid,
            data=data,
            type_response=None,
            header=None,
        )
        assert res.status_code == 401

    def test_update_userinfo_invalid_header(self, app, user_info):
        """
        Steps.
            1. Try to login user with valid data
            2. Add user info
            3. Change user data
            4. Check that status code is 200
            5. Check response
        """
        data = UserInfo.random()
        header = {"Authorization": "JWT 895241"}
        res = app.userinfo.edit_user_info(
            user_id=user_info.uuid, data=data, type_response=None, header=header
        )
        assert res.status_code == 401
