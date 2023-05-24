from aiogram import Router


def get_from_group_start_router() -> Router:
    from . import from_group_start_cmd
    from .menu_main import get_menu_main_router

    main_menu_router = get_menu_main_router()

    router = Router()
    router.include_router(from_group_start_cmd.router)
    router.include_router(main_menu_router)
    return router
