import uuid

import pytest
from datetime import datetime

from app.services.user.db_models import UserDBModel
from app.services.user.schemas import User, UserUpdateForm


@pytest.fixture
def user_form():
    return User(
        id='00000000-0000-0000-0000-000000000000',
        login='testuser123',
        avatar="lore",
        gender='female',
        first_name='Test',
        last_name='User',
        full_name='Test User',
        birthday=datetime.now(),
        bio='test user bio',
        role='testrole',
        city='TestCity',
        country_code='RU',
        email='testuser123@test.com',
        phone='1234567890',
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )


def test_user_create(db_session, user_form):
    user = UserDBModel.create(db_session, user_form)
    assert str(user.id) == '00000000-0000-0000-0000-000000000000'


def test_user_get(db_session):
    user_id = '00000000-0000-0000-0000-000000000000'
    user = UserDBModel.get(db_session, user_id)
    assert str(user.id) == user_id


def test_user_update(db_session):
    user_id = '00000000-0000-0000-0000-000000000000'
    form = UserUpdateForm(login='updated_testuser')
    user = UserDBModel.update(db_session, user_id, form)
    assert user.login == 'updated_testuser'


def test_user_delete(db_session):
    user_id = '00000000-0000-0000-0000-000000000000'
    result = UserDBModel.delete(db_session, user_id)
    assert result == True


def test_user_get_list(db_session):
    users = UserDBModel.get_list(db_session)
    assert isinstance(users, list)
