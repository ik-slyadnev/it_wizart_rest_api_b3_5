

class TestPostV1AccountLogin:
    def test_post_v1_account_login(self, account_helper, login_helper, prepare_user):
        # Регистрация и активация пользователя через хелпер
        user = account_helper.register_new_user(prepare_user)

        # Авторизация пользователя через login_helper
        response = login_helper.login(
            login=user.login,
            password=user.password
        )
        assert response.status_code == 200, "Не удалось авторизоваться"
