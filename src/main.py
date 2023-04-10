from aiogram import executor
from loader import dp, db
from handlers.start_handler import register_start_handler
from handlers.dialog_handler import register_dialog_handlers
from handlers.settings_handler import register_settings_handlers
from handlers.any_message_handler import register_any_message_handler


async def on_startup(dsip):
    register_start_handler(dsip)
    register_dialog_handlers(dsip)
    register_settings_handlers(dsip)
    register_any_message_handler(dsip)
    await db.init_db()


async def on_shutdown(dip):
    await db.close_db()
    await dip.storage.close()
    await dip.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=False)
