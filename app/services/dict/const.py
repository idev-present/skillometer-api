from enum import Enum


class CURRENCY(Enum):
    RUR = "₽"
    USD = "$"
    EUR = "€"
    UAH = "₴"
    KZT = "₸"


class REPLY_STATUS(Enum):
    NEW = "Новый"
    CV_REVIEW = "Проверка резюме"
    HR_INTERVIEW = "Первичное интервью"
    CV_AGREEMENT = "Согласование кандидата"
    JOB_INTERVIEW = "Собеседование"
    REQUIRED_TASK = "Техническое задание"
    WAITING = "Принятие решения"
    OFFER_POSTED = "Выставлен оффер"
    OFFER_ACCEPTED = "Оффер принят"
    RESERVE = "Резерв"
    DECLINED = "Отказ"
