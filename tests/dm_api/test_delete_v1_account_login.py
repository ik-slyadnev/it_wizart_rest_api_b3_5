import pytest
from requests.exceptions import HTTPError


class TestDeleteV1AccountLogin:
    def test_delete_v1_account_login(self, auth_user, login_helper):
        """
        Тест выхода из аккаунта с использованием авторизованного пользователя

        Шаги:
        1. Используем авторизованного пользователя (из фикстуры auth_user)
        2. Выполняем выход из системы через login_helper
        3. Проверяем успешность выхода
        """
        response = login_helper.logout()
        assert response.status_code == 204, "Неверный код ответа при выходе из системы"

        # Проверяем что пользователь не авторизован через обработку исключения
        with pytest.raises(HTTPError) as exc_info:
            auth_user.helper.get_current_user()

        assert exc_info.value.response.status_code == 401, "Пользователь все еще авторизован после выхода"
