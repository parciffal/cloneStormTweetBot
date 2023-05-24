from aiogram.fsm.state import StatesGroup, State


class ChgCommentState(StatesGroup):
    change_comment = State()
    remove_comment = State()
