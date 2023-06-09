from aiogram import Router


def get_admin_router() -> Router:
    from .admin_menu import get_admin_menu_router

    admin_menu_router = get_admin_menu_router()

    router = Router()
    router.include_router(admin_menu_router)
    return router
