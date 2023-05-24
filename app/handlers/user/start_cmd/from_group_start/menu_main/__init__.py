from aiogram import Router


def get_menu_main_router() -> Router:
    from . import back_button_cb, finish_cb, inf_tweets_cb, retweets_replies_cb, add_comment_cb

    router = Router()
    router.include_router(back_button_cb.router)
    router.include_router(add_comment_cb.router)
    router.include_router(finish_cb.router)
    router.include_router(retweets_replies_cb.router)
    router.include_router(inf_tweets_cb.router)
    return router
