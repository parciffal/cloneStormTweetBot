from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

users_commands = {
    "start": "Settings",
    "enable": "Start receiving alerts",
    "disable": "Stop receiving alerts",
}

owner_commands = {**users_commands, "ping": "Check bot ping", "stats": "Show bot stats"}


async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove_bot_commands(bot: Bot):
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
