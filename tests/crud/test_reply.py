import uuid
from datetime import datetime

import pytest

from app.services.dict.const import REPLY_STATUS
from app.services.reply.db_models import ReplyDBModel

# Assuming Reply and ReplyUpdateForm classes are from form_models.py.
from app.services.reply.schemas import Reply, ReplyUpdateForm


@pytest.fixture
def new_reply_form():
    form = Reply(
        id='00000000-0000-0000-0000-000000000000',
        status=REPLY_STATUS.NEW.name,
        vacancy_id="vac_000",
        applicant_id="app_000",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        updated_by='00000000-0000-0000-0000-000000000000',
        updated_by_role='applicant'
    )
    return form


@pytest.fixture
def update_reply_form():
    form = ReplyUpdateForm(status=REPLY_STATUS.CV_REVIEW.name)
    return form


def test_create_reply(db_session, new_reply_form):
    new_reply_form.id = uuid.uuid4()
    reply = ReplyDBModel.create(db=db_session, form=new_reply_form)
    
    assert isinstance(reply, ReplyDBModel)
    assert reply is not None
    assert reply.id is not None


def test_get_reply(db_session, new_reply_form):
    new_reply_form.id = uuid.uuid4()
    reply = ReplyDBModel.create(db=db_session, form=new_reply_form)
    obtained_reply = ReplyDBModel.get(db=db_session, item_id=str(reply.id))

    assert isinstance(obtained_reply, ReplyDBModel)
    assert obtained_reply.id == reply.id


def test_update_reply(db_session, new_reply_form, update_reply_form):
    new_reply_form.id = uuid.uuid4()
    reply = ReplyDBModel.create(db=db_session, form=new_reply_form)

    updated_reply = ReplyDBModel.update(db=db_session, item_id=reply.id, form=update_reply_form)

    assert isinstance(updated_reply, ReplyDBModel)
    assert updated_reply.id == reply.id

    # verify that the updated fields are same as provided in upated_reply_form
    for field in update_reply_form.dict():
        assert getattr(updated_reply, field) == update_reply_form.dict().get(field)


def test_get_list(db_session, new_reply_form):
    # TODO: Creating multiple replies
    new_reply_form.id = uuid.uuid4()
    result_replies = ReplyDBModel.get_list(db=db_session)

    assert isinstance(result_replies, list)