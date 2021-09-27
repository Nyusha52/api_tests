from fixtures.userinfo.model import UserInfo


class TestUserInfo:
    def test_add_user_info(self, app, auth_user):
        """
        Steps.
            1. Try to login user with valid data
            2. Check that status code is 200
            3. Check response
        """
        data = UserInfo.random()
        res = app.userinfo.add_user_info(user_id=auth_user.uuid, data=data, header=auth_user.header)
        assert res.status_code == 200
