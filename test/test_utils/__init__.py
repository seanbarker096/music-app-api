import functools
from unittest.mock import MagicMock, patch


def mock_decorator(func):
    @functools.wraps(func)
    def wrapped_f(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapped_f


def set_up_patches():
    patcher = patch("api.utils.rest_utils.auth", MagicMock(side_effect=mock_decorator))
    mock = patcher.start()
