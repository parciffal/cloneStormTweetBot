from ctypes import Union

from app.db.models import AdminModel, AdsModel

states_def = {
    True: "Enabled",
    False: "Disabled"
}


async def get_admin_data(telegram_id: int) -> dict:
    admin = await AdminModel.get(telegram_id=telegram_id)
    ads = await AdsModel.filter(admin=admin)
    return {
        "admin": admin,
        "ads": ads
    }

