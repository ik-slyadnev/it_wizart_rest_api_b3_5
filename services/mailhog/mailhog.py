from common.rest_client import RestClient


class MailhogApi(RestClient):
    def get_api_v2_messages(self, limit: str = '2') -> dict:
        """
        Получение писем пользователей из Mailhog

        :param limit: Количество писем (по умолчанию '2')
        :return: Словарь с сообщениями
        """
        response = self.get(
            path="/api/v2/messages",
            params={'limit': limit}
        )
        assert response.status_code == 200, "Не удалось получить письма"
        return response.json()