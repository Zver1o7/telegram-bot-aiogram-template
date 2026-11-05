from aiogram import Router

from .common import router as common_router
from .echo import router as echo_router


def get_routers() -> list[Router]:
    return [common_router, echo_router]
