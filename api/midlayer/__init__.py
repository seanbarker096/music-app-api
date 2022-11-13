class BaseMidlayerMixin:
    """This class is here to avoid other midlayer mixins calling the constrcutor of object with arguements provided from the previous mixin the the MRO e.g. conns object or config object. This results a TypeError: object.__init__() takes exactly one argument (the instance to initialize)."""

    def __init__(self, *args, **kwargs):
        pass
