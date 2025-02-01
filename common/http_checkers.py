import requests
from contextlib import contextmanager
from requests import HTTPError


@contextmanager
def check_status_code(
    expected_status_code: requests.codes = requests.codes.OK,
    expected_message: str = "User must be authenticated"
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть == {expected_status_code}")
        if expected_message != requests.codes.OK:
            raise AssertionError(f"Ожидаемое сообщение == {expected_message}, но запрос прошел успешно")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message
