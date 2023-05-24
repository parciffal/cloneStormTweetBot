from app.db.models import GroupModel, TemplateModel, AccountModel



states_def = {
    True: "Enabled",
    False: "Disabled"
}


async def get_user_data(user_id: int) -> dict:
    group = await GroupModel.get(telegram_id=user_id)
    template_count = await TemplateModel.filter(group=group)
    account_count = await AccountModel.filter(group=group)

    return {
        "group_id": group.telegram_id,
        "raid_msg": group.influencers_tweets,
        "retweets/replies": group.retweets_replies,
        "comment_raid_msg": True if group.comments else False,
        "current_comment": group.comments if group.comments else "No comment",
        "templates_count": len(template_count),
        "delay": group.delay,
        "account_count": len(account_count)
    }
