

class TestDeleteV1AccountLoginAll:
    def test_delete_v1_account_login_all(self, auth_user, login_helper):
        """
        Тест выхода из аккаунта на всех устройствах с использованием авторизованного пользователя

        Шаги:
        1. Используем авторизованного пользователя (из фикстуры auth_user)
        2. Выполняем выход из системы на всех устройствах через login_helper
        3. Проверяем успешность выхода
        """

        response = login_helper.logout_all()
        assert response.status_code == 204, "Неверный код ответа при выходе из системы на всех устройствах"

        # Проверяем что пользователь действительно вышел из системы
        check_auth = auth_user.helper.get_current_user()
        assert check_auth.status_code == 401, "Пользователь все еще авторизован после выхода"
