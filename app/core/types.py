from enum import Enum, auto


class StrEnum(str, Enum):

    def __new__(cls, value, *args, **kwargs):
        if not isinstance(value, (str, auto)):
            raise TypeError(f"Values of StrEnum must be of type str: ${repr(value)} is {type(value)}")
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self):
        return str(self.value)

    def _generate_next_value_(name, *_):
        return name

    @classmethod
    def __members__(cls):
        return cls.list()

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class FileStorageType(StrEnum):
    SBER = "SBER"
    LOCAL = "LOCAL"
