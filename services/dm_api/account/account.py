from requests import Response
from services.dm_api.account.models.requests.registration import Registration
from services.dm_api.account.models.requests.change_email import ChangeEmail
from services.dm_api.account.models.requests.reset_password import ResetPassword
from services.dm_api.account.models.requests.change_password import ChangePassword
from services.dm_api.account.models.responses.user_envelope import UserEnvelope
from common.rest_client import RestClient



class AccountApi(RestClient):
    def post_v1_account(self, login: str, email: str, password: str):
        """
        Регистрация нового аккаунта.

        :param login: Логин пользователя
        :param email: Email пользователя
        :param password: Пароль пользователя
        :return: Response
        """
        registration = Registration(
            login=login,
            email=email,
            password=password
        )
        response = self.post(
            path="/v1/account",
            json=registration.model_dump(by_alias=True)
        )
        return response

    def put_v1_account_token(self, token: str):
        """
        Активация аккаунта по токену.

        :param token: Токен активации
        :return: Response
        """
        response = self.put(
            path=f"/v1/account/{token}"
        )
        return response

    def put_v1_account_email(self, login: str, new_email: str, password: str) -> Response:
        """
        Смена email пользователя.

        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param new_email: Новый email пользователя
        :return: Response
        """
        change_email = ChangeEmail(
            login=login,
            email=new_email,
            password=password
        )
        response = self.put(
            path="/v1/account/email",
            json=change_email.model_dump(by_alias=True)
        )
        UserEnvelope.model_validate(response.json())
        return response

    def get_v1_account(self):
        """
        Получение информации о текущем пользователе
        """
        response = self.get(
            path="/v1/account"
        )
        return response

    def post_v1_account_password(self, login: str, email: str) -> None:
        """
        Запрос на сброс пароля

        :param login: Логин пользователя
        :param email: Email пользователя
        :return: Response
        """
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        response = self.post(
            path="/v1/account/password",
            json=reset_password.model_dump(by_alias=True)
        )
        return response

    def put_v1_account_password(self, old_password: str, new_password: str, reset_token: str = None) -> Response:
        """
        Смена пароля пользователя

        :param old_password: Текущий пароль
        :param new_password: Новый пароль
        :param reset_token: Токен сброса пароля (опционально)
        :return: Response
        """
        change_password = ChangePassword(
            old_password=old_password,
            new_password=new_password,
            reset_token=reset_token
        )
        response = self.put(
            path="/v1/account/password",
            json=change_password.model_dump(by_alias=True)
        )
        UserEnvelope.model_validate(response.json())
        return response