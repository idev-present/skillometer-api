import pytest
from sqlalchemy.orm import Session

from app.services.dict.const import CURRENCY
from app.services.vacancy.db_models import VacancyDBModel
from app.services.vacancy.schemas import VacancyForm, VacancyUpdateForm


@pytest.fixture(scope="module")
def vacancy_form():
    return VacancyForm(
        name='Test Vacancy',
        currency=CURRENCY.RUR.name,
        is_remote=True,
        description='Test Description',
        team='Test Team',
        todo='Test Todo',
        city_id='moscow',
        employment_type_id='full_time',
        division_id='frontend_developer',
        qualification_id='middle',
        skill_set='html,js,css'
    )


def test_create_vacancy(db_session: Session, vacancy_form: VacancyForm):
    vacancy = VacancyDBModel.create(db_session, vacancy_form)

    assert vacancy is not None
    assert vacancy.name == 'Test Vacancy'
    assert vacancy.description == 'Test Description'
    assert vacancy.is_remote is True


def test_get_vacancy(db_session: Session, vacancy_form: VacancyForm):
    new_vacancy = VacancyDBModel.create(db_session, vacancy_form)
    got_vacancy = VacancyDBModel.get(db_session, new_vacancy.id)

    assert new_vacancy.id == got_vacancy.id
    assert new_vacancy.name == got_vacancy.name


def test_update_vacancy(db_session: Session, vacancy_form: VacancyForm):
    new_vacancy = VacancyDBModel.create(db_session, vacancy_form)
    update_form = VacancyUpdateForm(name='Updated Vacancy')
    updated_vacancy = VacancyDBModel.update(db_session, new_vacancy.id, update_form)

    assert updated_vacancy.name == 'Updated Vacancy'
    assert updated_vacancy.id == new_vacancy.id


def test_delete_vacancy(db_session: Session, vacancy_form: VacancyForm):
    new_vacancy = VacancyDBModel.create(db_session, vacancy_form)
    result = VacancyDBModel.delete(db_session, new_vacancy.id)

    assert result is True
    assert db_session.query(VacancyDBModel).filter_by(id=new_vacancy.id).first() is None


def test_get_list_vacancy(db_session: Session):
    vacancies = VacancyDBModel.get_list(db_session)

    assert isinstance(vacancies, list)
