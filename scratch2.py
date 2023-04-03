
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
    

class MyClass(Singleton):
    def __init__(self, *args, **kwargs) -> None:
        # Call parent to ensure MyClass only being instantiated from inside Singleton
        create_key = kwargs.pop('create_key', None)
        super().__init__(create_key)

        self.test = kwargs.pop('test')
        self.config = kwargs.pop('config')

        # Do other stuff

        

    

a = MyClass.instance(MyClass, test='asdjasdjsa', config={'a': 7} )

print(a.test)
print(a.config)

b = MyClass.instance(MyClass)

# c = MyClass('key')

print(a)

print(b)

#b = MyClass()

