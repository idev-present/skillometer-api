from enum import Enum


class CURRENCY(Enum):
    RUR = "₽"
    USD = "$"
    EUR = "€"
    UAH = "₴"
    KZT = "₸"


class REPLY_STATUS(Enum):
    NEW = "NEW"
