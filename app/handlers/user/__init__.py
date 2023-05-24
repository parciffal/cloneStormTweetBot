from aiogram import Router


def get_user_router() -> Router:
    from .start_cmd import get_start_router
    from .enable_rec_alerts import get_enable_router
    from .disable_rec_alerts import get_disable_router
    from .close_cmd import get_close_router

    start_router = get_start_router()
    enable_router = get_enable_router()
    disable_router = get_disable_router()
    close_router = get_close_router()

    router = Router()
    router.include_router(start_router)
    router.include_router(enable_router)
    router.include_router(disable_router)
    router.include_router(close_router)
    return router
