import json


class AccountHelper:
    def __init__(self, dm_api_facade, mailhog_facade):
        self.dm_api_facade = dm_api_facade
        self.mailhog_facade = mailhog_facade

    def auth_client(self, login: str, password: str):
        """
        Авторизация пользователя

        :param login: Логин пользователя
        :param password: Пароль пользователя
        :return: Response
        """
        response = self.dm_api_facade.login_api.post_v1_account_login(
            login=login,
            password=password
        )

        auth_token = response.headers["x-dm-auth-token"]
        headers = {
            "X-Dm-Auth-Token": auth_token
        }

        self.dm_api_facade.account_api.session.headers.update(headers)
        self.dm_api_facade.login_api.session.headers.update(headers)

        return response

    def register_new_user(self, user):
        """
        Регистрация нового пользователя с активацией аккаунта через email

        :param user: фикстура prepare_user с полями login, email, password
        :return: данные пользователя из фикстуры
        """
        self.register_account(
            login=user.login,
            email=user.email,
            password=user.password
        )
        token = self.get_registration_token(user.login)
        self.activate_account(token)

        return user

    def register_account(self, login: str, email: str, password: str):
        """
        Регистрация аккаунта пользователя

        :param login: Логин пользователя
        :param email: Email пользователя
        :param password: Пароль пользователя
        """
        response = self.dm_api_facade.account_api.post_v1_account(
            login=login,
            email=email,
            password=password
        )
        assert response.status_code == 201, f"Не удалось зарегистрировать пользователя {login}"

    def get_registration_token(self, login: str):
        """
        Получение токена активации из почты

        Args:
            login: логин пользователя
        Returns:
            str: токен для активации аккаунта
        """

        messages = self.mailhog_facade.mailhog_api.get_api_v2_messages(limit=1)
        token = None
        for item in messages['items']:
            message_data = json.loads(item['Content']['Body'])
            user_login = message_data['Login']
            if user_login == login:
                token = message_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        assert token is not None, f"Токен для пользователя {login} не был получен"
        return token

    def activate_account(self, token: str):
        """
        Активация аккаунта по токену

        Args:
            token: токен для активации аккаунта
        Returns:
            Response: ответ сервера
        """
        response = self.dm_api_facade.account_api.put_v1_account_token(token)
        assert response.status_code == 200, f"Не удалось активировать аккаунт"

    def get_current_user(self):
        """
        Получение информации о текущем пользователе

        Returns:
            Response: информация о текущем пользователе
        """
        response = self.dm_api_facade.account_api.get_v1_account()
        return response

    def reset_password(self, login: str, email: str):
        """
        Запрос на сброс пароля и получение reset token

        Args:
            login: логин пользователя
            email: email пользователя

        Returns:
            str: токен для сброса пароля
        """
        response = self.dm_api_facade.account_api.post_v1_account_password(
            login=login,
            email=email
        )
        assert response.status_code == 200, "Ошибка запроса на сброс пароля"

        messages = self.mailhog_facade.mailhog_api.get_api_v2_messages(limit=1)
        reset_token = None
        for item in messages['items']:
            message_data = json.loads(item['Content']['Body'])
            user_login = message_data['Login']
            if user_login == login:
                reset_token = message_data['ConfirmationLinkUri'].split('/')[-1]
                break

        assert reset_token is not None, f"Токен сброса пароля для пользователя {login} не был получен"
        return reset_token

    def change_password(self, password: str, new_password: str):
        """
        Смена пароля пользователя

        Args:
            password: текущий пароль
            new_password: новый пароль

        Returns:
            Response: ответ сервера
        """
        response = self.dm_api_facade.account_api.put_v1_account_password(
            old_password=password,
            new_password=new_password
        )

        assert response.status_code == 200, \
            f"Ошибка при смене пароля. Код ответа: {response.status_code}"

        return response
