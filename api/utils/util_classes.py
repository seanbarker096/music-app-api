
class Singleton:
    _instance = None
    __create_key = object()

    def __init__(self, create_key) -> None:
        assert(create_key == Singleton.__create_key), \
            "You must use Singleton.instance() to create a Singleton instance"

    @classmethod
    def instance(cls, classname, *args, **kwargs) -> object:
        if (cls._instance is None):
            cls._instance = classname(create_key=Singleton.__create_key, *args, **kwargs)

        return cls._instance