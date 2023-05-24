import dataclasses

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, ChatEvent
from aiogram_dialog.widgets.kbd import (Button, Column, Row, Checkbox,
                                        ManagedCheckboxAdapter, Group,
                                        Back, Cancel)
from aiogram_dialog.widgets.text import Const, Format

from app.db import UserModel
from app.db.models import TemplateModel, AccountModel


class MenuDialog(StatesGroup):
    start = State()
    influencers_tweets = State()
    retweets_replies = State()
    custom_comment = State()
    show_templates = State()
    change_delay = State()
    show_media = State()
    add_account = State()


@dataclasses.dataclass
class CheckBoxBools:
    raid_msg_check: bool
    comment_check: bool

    def __init__(self, raid=False, comment=False):
        self.raid_msg_check = raid
        self.comment_check = comment

    def set_raid_msg_check(self, raid: bool):
        self.raid_msg_check = raid

    def set_comment_check(self, comm: bool):
        self.comment_check = comm


checkBoxBool = CheckBoxBools()


async def show_alert(c: CallbackQuery, _: Button, manager: DialogManager):
    await c.answer("❗️ Тестовое уведомление", show_alert=True, cache_time=0)
    await c.message.delete()
    await manager.done()


async def check_changed(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    print("Check status changed:", checkbox.is_checked())


async def get_solution_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    user = await UserModel.get(telegram_id=user_id)
    template_count = await TemplateModel.filter(user=user)
    account_count = await AccountModel.filter(user=user)
    raid_msg_check = True if user.comments else False
    comment_check = True if user.comments else False

    checkBoxBool.set_raid_msg_check(raid_msg_check)
    checkBoxBool.set_comment_check(comment_check)

    return {
        "user": user,
        "raid_msg": user.influencers_tweets,
        "comment_raid_msg": True if user.comments else False,
        "current_comment": user.comments if user.comments else "No comment",
        "templates_count": len(template_count),
        "delay": user.delay,
        "account_count": len(account_count)
    }


async def influencers_tweets_change(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    checkbox.is_checked()
    await manager.switch_to(MenuDialog.influencers_tweets)

menu_ui = Dialog(
    Window(
        Const("⚒️ Group Settings\n"),
        Format("Raid Message:\n {raid_msg}\n"),
        Format("Comment in raid message:\n {comment_raid_msg}\n"),
        Format("Templates: \n {templates_count}/20 \n"),
        Format("Delay: \n {delay} Minutes \n"),
        Format("Custom Twitter Account:\n {account_count} Account Added\n"),
        Const("Select an option below to change settings"),
        Group(
            Row(Checkbox(
                Const("✅ Influencers Tweets"),
                Const("❌ Influencers Tweets"),
                id="infuencers_tweets",
                default=checkBoxBool.raid_msg_check,
                on_state_changed=influencers_tweets_change),
                Checkbox(
                    Const("✅ Retweets/Replies"),
                    Const("❌ Retweets/Replies"),
                    id="retweets_replies",
                    default=checkBoxBool.comment_check,
                    on_state_changed=check_changed)),
            Row(Button(Const("➕ comment"), id="add_comment", on_click=show_alert),
                Button(Const("Set Template"), id="set_template", on_click=show_alert)),
            Row(Button(Const("Change delay"), id="change_delay", on_click=show_alert),
                Button(Const("Show media"), id="show_media", on_click=show_alert)),
            Row(Button(Const("➕ account"), id="add_account", on_click=show_alert),
                Button(Const("Finish"), id="finish", on_click=show_alert))
        ),
        state=MenuDialog.start,
        getter=get_solution_data
    ),
    Window(
        Const("🎉Awesome, you're all set to receive alerts from now on.\nPlease Choose an option below"),
        Column(Back(Const("Back to Main Menu")),
               Button(Const("Finish"), id="finish", on_click=show_alert)),
        state=MenuDialog.influencers_tweets
    ),
)
