import asyncio
import logging

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.arguments import parse_arguments
from app.config import parse_config, Config
from app.handlers import get_handlers_router
from app.commands import setup_bot_commands
from app import db


async def on_startup(dispatcher: Dispatcher, bot: Bot, config: Config):

    dispatcher.include_router(get_handlers_router())
    await setup_bot_commands(bot)

    bot_info = await bot.get_me()
    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    await db.init_orm(config.database.get_tortoise_config())

    states = {
        True: "Enabled",
        False: "Disabled",
    }

    logging.debug(f"Groups Mode - {states[bool(bot_info.can_join_groups)]}")
    logging.debug(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.info("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning("Stopping bot...")
    # await remove_bot_commands(bot)
    await dispatcher.fsm.storage.close()
    await bot.session.close()
    await db.close_orm()


async def main():

    coloredlogs.install(level=logging.INFO)
    logging.info("Starting bot...")

    arguments = parse_arguments()
    config = parse_config(arguments.config)

    tortoise_config = config.database.get_tortoise_config()
    try:
        await db.create_models(tortoise_config)
    except FileExistsError:
        await db.migrate_models(tortoise_config)
    token = config.bot.token
    bot = Bot(token)
    bot_info = await bot.get_me()
    config.bot.username = str(bot_info.username)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    context_kwargs = {"config": config}

    await dp.start_polling(bot, **context_kwargs)


if __name__ == "__main__":
    try:

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
