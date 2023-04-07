
class Singleton:
    # _instance = None
    _instances = {}
    __create_key = object()

    def __init__(self, create_key) -> None:
        assert(create_key == Singleton.__create_key), \
            "You must use Singleton.instance() to create a Singleton instance"

    @classmethod
    def instance(cls, classname, instance_key: str, *args, **kwargs) -> object:
        if (cls._instances.get(instance_key, None) is None):
            cls._instances[instance_key] = classname(create_key=Singleton.__create_key, *args, **kwargs)

        return cls._instances[instance_key]
    
    @classmethod
    def remove_instance(cls, instance_key: str) -> None:
        del cls._instances[instance_key]

    @classmethod
    def has_instance(cls, instance_key: str) -> bool:
        return cls._instances.get(instance_key, None) is not None