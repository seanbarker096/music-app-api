import functools


def mock_decorator(func):
    @functools.wraps(func)
    def wrapped_f(*args, **kwargs):
        print("running mock")
        return func(*args, **kwargs)

    return wrapped_f
