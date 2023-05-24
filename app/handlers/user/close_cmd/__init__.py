from aiogram import Router


def get_close_router() -> Router:
    from . import (close_cmd)

    router = Router()
    router.include_router(close_cmd.router)
    return router
