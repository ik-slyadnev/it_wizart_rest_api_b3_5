

class TestPutV1AccountEmail:
    def test_put_v1_account_email(self, account_helper, dm_api_facade, mailhog_facade, login_helper, prepare_user):
        """
        Тест на смену email пользователя

        Шаги:
        1. Регистрация и активация пользователя
        2. Логин в систему
        3. Смена email
        4. Проверка невозможности входа до подтверждения
        5. Получение и активация токена подтверждения
        6. Проверка возможности входа после подтверждения
        """
        # Регистрация пользователя
        user = account_helper.register_new_user(prepare_user)

        response = login_helper.login(user.login, user.password)
        assert response.status_code == 200

        # Смена email
        new_email = f"new_{user.login}@example.com"
        response = dm_api_facade.account_api.put_v1_account_email(
            login=user.login,
            password=user.password,
            new_email=new_email
        )
        assert response.status_code == 200

        # Проверка невозможности входа до подтверждения
        response = login_helper.login(user.login, user.password)
        assert response.status_code == 403

        # Получение токена и активация нового email
        email_change_token = account_helper.get_registration_token(user.login)
        account_helper.activate_account(email_change_token)

        # Проверка возможности входа после подтверждения
        response = login_helper.login(user.login, user.password)
        assert response.status_code == 200
