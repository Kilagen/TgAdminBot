import typing as tp
from dataclasses import dataclass

GENERAL_ADMINS = [310571541]


@dataclass
class AdminConfig:
    general_admins: tp.List[int]

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.general_admins


admin_config = AdminConfig(GENERAL_ADMINS)
