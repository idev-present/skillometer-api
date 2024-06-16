from typing import Optional, List

from pydantic import Field, field_validator, BaseModel

from app.services.dict.const import REPLY_STATUS
from app.services.dict.schemas import KeyValueDict
from app.services.processing.status_mapper import FlowConfig


class ReplyStatusFlow(FlowConfig):
    status: Optional[KeyValueDict] = Field(None)

    @field_validator('status', mode='before')
    @classmethod
    def prepare_status(cls, v):
        # todo: check valid key
        for key in REPLY_STATUS:
            if key.name == v:
                return KeyValueDict(key=key.name, value=key.value)
        return v


class MatchingResult(BaseModel):
    missed_skills: Optional[List[str]] = Field([], description="Недостающие скиллы")
    additional_skills: Optional[List[str]] = Field([], description="Лишние скиллы")
    coverage: Optional[float] = Field(0, description="Процент")