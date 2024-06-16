import pytest
from unittest.mock import MagicMock

from app.services.reply_activity.const import ACTIVITY_TYPE
from app.services.reply_activity.schemas import ReplyActivityForm
from app.services.reply_activity.db_models import ActivityDBModel
from sqlalchemy.orm import Session


@pytest.fixture
def db_session():
    session = MagicMock(spec=Session)
    yield session
    session.close.assert_called_once()


@pytest.fixture
def form_data():
    data = {
        'type': ACTIVITY_TYPE.EVENT_STATUS,
        'text': 'Test text',
        'external_id': 'test_external_id',
        'owner_id': 'test_owner_id',
        'owner_type': 'APPLICANT'
    }
    return ReplyActivityForm(**data)


def test_create_method(db_session, form_data):
    activity = ActivityDBModel.create(form_data, db_session)

    db_session.add.assert_called_once()
    db_session.add.assert_called_with(activity)

    db_session.commit.assert_called_once()

    db_session.refresh.assert_called_once()
    db_session.refresh.assert_called_with(activity)


def test_get_list_method(db_session):
    reply_id = 'test_reply_id'

    results = ActivityDBModel.get_list(db_session, reply_id)

    db_session.execute.assert_called_once()
    query = db_session.execute.call_args[0][0]
    assert f'external_id == {reply_id}' in str(query)
