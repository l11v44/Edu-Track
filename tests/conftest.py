import os
import pytest


def pytest_configure(config):
    # Указываем Django, что мы в режиме тестов
    os.environ['PYTEST_RUNNING'] = '1'

    # Полностью удаляем старую переменную, чтобы она не конфликтовала
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']