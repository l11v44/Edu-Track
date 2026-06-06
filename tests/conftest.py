import os
import pytest


def pytest_configure(config):
    os.environ['PYTEST_RUNNING'] = '1'
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']