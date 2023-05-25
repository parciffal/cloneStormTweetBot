from aiogram import Router


def get_start_router() -> Router:
    from . import from_group_start, group_start_cmd, private_start_cmd

    router = Router()
    from_group_router = from_group_start.get_from_group_start_router()
    router.include_router(group_start_cmd.router)
    router.include_router(from_group_router)
    router.include_router(private_start_cmd.router)

    return router
