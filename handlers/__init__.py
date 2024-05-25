from .admin import admin_router
from .commands import command_router
from .dm import dm_router
from .groups import group_router

__all__ = ['admin_router', 'command_router', 'group_router', 'dm_router']