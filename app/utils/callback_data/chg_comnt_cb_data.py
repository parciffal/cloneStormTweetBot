import enum

from aiogram.filters.callback_data import CallbackData


class CommentActions(str, enum.Enum):
    CHANGE_COMMENT = "change_comment"
    REMOVE_COMMENT = "remove_comment"


class ChgCommentCbData(CallbackData, prefix="comment"):
    action: CommentActions
    group_id: int
