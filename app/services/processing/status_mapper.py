from typing import Optional

from pydantic import BaseModel, Field

from app.services.dict.const import REPLY_STATUS


class FlowConfig(BaseModel):
    status: str
    is_required_reason: Optional[bool] = Field(False)


available_status_flow = {
    REPLY_STATUS.NEW.name: [
        FlowConfig(status=REPLY_STATUS.CV_REVIEW.name)
    ],
    REPLY_STATUS.CV_REVIEW.name: [
        FlowConfig(status=REPLY_STATUS.HR_INTERVIEW.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.HR_INTERVIEW.name: [
        FlowConfig(status=REPLY_STATUS.CV_AGREEMENT.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.CV_AGREEMENT.name: [
        FlowConfig(status=REPLY_STATUS.JOB_INTERVIEW.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.JOB_INTERVIEW.name: [
        FlowConfig(status=REPLY_STATUS.REQUIRED_TASK.name),
        FlowConfig(status=REPLY_STATUS.WAITING.name),
        FlowConfig(status=REPLY_STATUS.RESERVE.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.REQUIRED_TASK.name: [
        FlowConfig(status=REPLY_STATUS.WAITING.name),
        FlowConfig(status=REPLY_STATUS.RESERVE.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.WAITING.name: [
        FlowConfig(status=REPLY_STATUS.OFFER_POSTED.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.OFFER_POSTED.name: [
        FlowConfig(status=REPLY_STATUS.OFFER_ACCEPTED.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.OFFER_ACCEPTED.name: [
        FlowConfig(status=REPLY_STATUS.DONE.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.RESERVE.name: [
        FlowConfig(status=REPLY_STATUS.DONE.name),
        FlowConfig(status=REPLY_STATUS.DECLINED.name, is_required_reason=True)
    ],
    REPLY_STATUS.DECLINED.name: [],
}