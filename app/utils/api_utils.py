from enum import Enum
from typing import TypeVar, Type

from fastapi.routing import APIRoute
from pydantic import BaseModel


def api_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def prepare_errors(errors) -> dict:
    data = {}
    for error in errors:
        key = error['loc'][0]
        if key not in data:
            data[key] = []
        data[key].append(error['msg'])
    return data


T = TypeVar('T', bound=Enum)


def create_enum_model(enum: Type[T]) -> Type[BaseModel]:
    class EnumModel(BaseModel):
        key: str
        value: str

        @property
        def key(self) -> str:
            return self.__dict__['key'].name

        @property
        def value(self) -> str:
            return self.__dict__['key'].value

    return EnumModel
