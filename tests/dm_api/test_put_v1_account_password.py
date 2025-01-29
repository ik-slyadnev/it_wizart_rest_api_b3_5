

class TestPutV1AccountPassword:
    def test_put_v1_account_password(self, account_helper, prepare_user):
        """
        Тест смены пароля пользователя через старый пароль

        Шаги:
        1. Регистрация и активация пользователя
        2. Авторизация со старым паролем
        3. Смена пароля
        4. Проверка авторизации с новым паролем
        """
        user = account_helper.register_new_user(prepare_user)
        assert account_helper.auth_client(
            login=user.login,
            password=user.password
        ).status_code == 200, "Не удалось авторизоваться со старым паролем"

        new_password = "NewPassword123!"
        response = account_helper.change_password(
            password=user.password,
            new_password=new_password
        )
        assert response.status_code == 200, f"Не удалось сменить пароль: {response.text}"

        assert account_helper.auth_client(
            login=user.login,
            password=new_password
        ).status_code == 200, "Не удалось авторизоваться с новым паролем"
