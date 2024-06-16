from pydantic import BaseModel, Field
from typing import Optional


class KeyValueDict(BaseModel):
    key: str
    value: str


class City(BaseModel):
    """ Словарь городов"""
    id: str = Field(description='ID')
    fias_id: Optional[str] = Field(description='Фиас ID населенного пункта')
    habr_id: Optional[int] = Field(description='ID населенного пункта на habr.ru')
    habr_alias: Optional[str] = Field(description='Название населенного пункта на habr.ru')
    name: Optional[str] = Field(description='Название населенного пункта')
    country_name: Optional[str] = Field(description='Название страны')
    region_name: Optional[str] = Field(description='Название региона')


class EmploymentType(BaseModel):
    """Словарь типов занятостей"""
    id: str = Field(description='ID')
    name: Optional[str] = Field(description='Название')
    habr_id: Optional[str] = Field(description='ID на habr.ru')
    hh_id: Optional[str] = Field(description='ID на hh.ru')


class Division(BaseModel):
    id: str
    name: Optional[str]
    habr_id: Optional[int]


class Qualification(BaseModel):
    id: str
    name: Optional[str]
    habr_id: Optional[int]


class SearchStatus(BaseModel):
    id: Optional[str]
    name: Optional[str]
    habr_id: Optional[int]


class Skill(BaseModel):
    """Словарь навыков"""
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    qualification_id: Optional[str]
    division_id: Optional[str]
    habr_id: Optional[int]


class ReplyStatusCount(BaseModel):
    status: str
    count: int

    @classmethod
    def from_row(cls, row) -> 'ReplyStatusCount':
        return cls(status=row[0], count=row[1])
