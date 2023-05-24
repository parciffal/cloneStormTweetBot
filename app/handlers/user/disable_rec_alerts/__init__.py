from aiogram import Router


def get_disable_router() -> Router:
    from . import disable_alert_cmd

    router = Router()
    router.include_router(disable_alert_cmd.router)

    return router
