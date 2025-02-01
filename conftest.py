import pytest
from faker import Faker
from collections import namedtuple
from common.logger import setup_logging
from configs.configuration import Configuration
from services.dm_api.dm_api_facade import DMApiAccount
from services.mailhog.mailhog_facade import MailHogAPI
from helpers.account_helper import AccountHelper
from helpers.login_helper import LoginHelper

# Инициализация логгера при старте тестов
setup_logging()

# Инициализация Faker
fake = Faker()


@pytest.fixture
def prepare_user():
    """
    Фикстура для генерации тестового пользователя
    Returns:
        namedtuple: User с полями login, password, email
    """
    login = fake.user_name()
    password = fake.password()
    email = f"{login}@{fake.free_email_domain()}"

    User = namedtuple("User", ["login", "password", "email"])
    return User(login=login, password=password, email=email)


@pytest.fixture
def auth_user(account_helper, prepare_user):
    """
    Фикстура для создания и авторизации пользователя

    Returns:
        namedtuple: AuthUserData с полями user и helper, где:
            - user: данные пользователя (login, password, email)
            - helper: авторизованный account_helper
    """

    user = account_helper.register_new_user(user=prepare_user)
    auth_response = account_helper.auth_client(
        login=user.login,
        password=user.password
    )
    assert auth_response.status_code == 200, "Ошибка авторизации пользователя"

    AuthUserData = namedtuple('AuthUserData', ['user', 'helper'])
    return AuthUserData(user=user, helper=account_helper)

@pytest.fixture
def config_data():
    """
    Конфигурация для API endpoints
    """
    return {
        'host': 'http://5.63.153.31:5051',
        'mailhog_host': 'http://5.63.153.31:5025'
    }

@pytest.fixture
def main_config(config_data):
    """
    disable_log:
        False - логирование запросов и ответов включено
        True - логирование запросов и ответов выключено
        По умолчанию установлено в True
    """
    return Configuration(
        host=config_data['host'],
        headers={
            'Content-Type': 'application/json'
        },
        disable_log=True
    )

@pytest.fixture
def mailhog_config(config_data):
    return Configuration(
        host=config_data['mailhog_host'],
        disable_log=True  # логи отключены для mailhog
    )

# Фикстуры для фасадов
@pytest.fixture
def dm_api_facade(main_config):
    """
    Фасад для работы с DM API
    """
    return DMApiAccount(configuration=main_config)

@pytest.fixture
def mailhog_facade(mailhog_config):
    """
    Фасад для работы с Mailhog
    """
    return MailHogAPI(configuration=mailhog_config)

# Фикстуры хелперов
@pytest.fixture
def account_helper(dm_api_facade, mailhog_facade):
    """
    Хелпер для работы с аккаунтом, использует фасады
    """
    return AccountHelper(dm_api_facade, mailhog_facade)

@pytest.fixture
def login_helper(dm_api_facade):
    return LoginHelper(dm_api_facade)
