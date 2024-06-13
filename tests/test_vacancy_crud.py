import pytest


@pytest.mark.asyncio
async def test_example(db_session):
    # тестовый код здесь
    vacancy_id = 'vac_test'
    assert vacancy_id == 'vac_test'