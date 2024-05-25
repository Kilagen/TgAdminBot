from dataclasses import dataclass
from enum import Enum

class UserStatus(Enum):
    BLACKLIST = -1
    WAITLIST = 1
    WHITELIST = 0
    NOT_FOUND = 13