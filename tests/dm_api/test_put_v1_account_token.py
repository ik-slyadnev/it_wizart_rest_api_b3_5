

class TestPutV1AccountToken:
    def test_put_v1_account_token(self, dm_api_facade, mailhog_facade, prepare_user, account_helper):
        """
        Тест проверяет активацию аккаунта по токену

        Шаги:
        1. Регистрация нового пользователя без автоматической активации
        2. Получение письма с токеном активации
        3. Активация аккаунта с помощью токена
        """
        # Регистрация пользователя без активации
        response = dm_api_facade.account_api.post_v1_account(
            login=prepare_user.login,
            email=prepare_user.email,
            password=prepare_user.password
        )
        assert response.status_code == 201, "Регистрация пользователя не прошла"

        # Получение токена активации
        token = account_helper.get_registration_token(prepare_user.login)
        assert token is not None, f"Токен для пользователя {prepare_user.login} не был получен"

        # Активация аккаунта
        response = dm_api_facade.account_api.put_v1_account_token(token)
        assert response.status_code == 200, "Не удалось активировать аккаунт"
