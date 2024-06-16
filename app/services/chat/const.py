from enum import Enum


class MESSAGE_TYPE(Enum):
    TEXT = 'TEXT'
    LINK = 'LINK'
    FILE = 'FILE'
    IMAGE = 'IMAGE'


class MESSAGE_STATUS(Enum):
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'
    READ = 'READ'
    ERROR = 'ERROR'


class CHAT_ROOM_TYPE(Enum):
    REPLY = 'REPLY'
    P2P = 'P2P'
