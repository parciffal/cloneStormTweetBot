from aiogram import Router


def get_admin_menu_router() -> Router:
    from . import admin_main_menu, change_show_ads, add_ads_cb, change_name_cb, show_ads_cb, view_ads
    router = Router()
    router.include_router(view_ads.router)
    router.include_router(show_ads_cb.router)
    router.include_router(change_name_cb.router)
    router.include_router(admin_main_menu.router)
    router.include_router(add_ads_cb.router)
    router.include_router(change_show_ads.router)
    return router
