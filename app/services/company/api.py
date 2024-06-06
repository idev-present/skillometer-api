from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def company_list():
    return [
        {
            "alias_name": "yandex",
            "href": "https://career.habr.com/companies/yandex",
            "title": "Яндекс",
            "accredited": True,
            "logo": {
                "src": "https://habrastorage.org/getpro/moikrug/uploads/company/548/669/435/logo/medium_586e9aeb81f9123e31337c951432b4ba.png"
            },
            "rating": {
                "title": "Средняя оценка компании в 2023 году",
                "value": "4.26",
                "href": "https://career.habr.com/companies/yandex/scores/2023"
            }
        }
    ]
