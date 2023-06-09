import contextlib
import logging

import aerich.exceptions
from tortoise import Tortoise
from app.db.models import UserModel

from aerich import Command
from click import Abort


async def create_models(tortoise_config: dict):
    # Create the database tables for the defined models

    command = Command(tortoise_config=tortoise_config, app="models")
    await command.init()
    await command.init_db(safe=True)
    await command.upgrade()
    """await Tortoise.init(db_url="sqlite://production-database.sqlite3", modules={"models": [
        "app.db.models"
    ]})
    await Tortoise.generate_schemas()"""


async def migrate_models(tortoise_config: dict):
    command = Command(tortoise_config=tortoise_config, app="models")
    await command.init()
    try:
        with contextlib.suppress(Abort):
            await command.migrate()
        await command.upgrade()
    except aerich.exceptions.NotSupportError as e:
        logging.error(e)
    """# Perform database migrations for the defined models
    await Tortoise.init(db_url="sqlite://production-database.sqlite3", modules={"models": [
        "app.db.models"
    ]})
    await Tortoise.generate_schemas()"""


async def init_orm(tortoise_config: dict) -> None:
    await Tortoise.init(config=tortoise_config)
    logging.info(f"Tortoise-ORM started, {Tortoise.apps}")


async def close_orm():
    # Close the Tortoise ORM connection
    await Tortoise.close_connections()
    logging.info("Tortoise-ORM shutdown")