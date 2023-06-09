import enum

from aiogram.filters.callback_data import CallbackData


class MenuActions(str, enum.Enum):
    BACK_TO_MENU = "back_to_menu"
    FINISH = "finish"
    CH_INF_TWEETS = "change_influencers_tweets"
    RETWEETS_REPLIES = "retweets_replies"
    ADD_COMMENT = "add_comment"
    SET_TEMPLATE = "set_template"
    CHANGE_DELAY = "change_delay"
    SHOW_MEDIA = "show_media"
    ADD_ACCOUNT = "add_account"


class MainMenuCbData(CallbackData, prefix="menu"):
    action: MenuActions
    group_id: int
