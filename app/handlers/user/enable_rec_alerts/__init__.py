from aiogram import Router


def get_enable_router() -> Router:
    from . import enable_alert_cmd

    router = Router()
    router.include_router(enable_alert_cmd.router)

    return router
