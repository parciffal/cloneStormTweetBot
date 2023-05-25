from tortoise import Tortoise
from app.db.models import UserModel


async def create_models():
    # Create the database tables for the defined models
    await Tortoise.init(db_url="sqlite://production-database.sqlite3", modules={"models": [
        "app.db.models"
    ]})
    await Tortoise.generate_schemas()


async def migrate_models():
    # Perform database migrations for the defined models
    await Tortoise.init(db_url="sqlite://production-database.sqlite3", modules={"models": [
        "app.db.models"
    ]})
    await Tortoise.generate_schemas()


async def init_orm():
    # Initialize the Tortoise ORM connection
    await Tortoise.init(db_url="sqlite://production-database.sqlite3", modules={"models": [
        "app.db.models"
    ]})


async def close_orm():
    # Close the Tortoise ORM connection
    await Tortoise.close_connections()
