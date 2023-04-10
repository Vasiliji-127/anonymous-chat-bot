from aiogram.types import Message
from aiogram import Dispatcher
from markups import main_markup
from loader import bot


async def any_message_handler(message: Message):
    await bot.send_message(message.chat.id, 'Напишите /search чтобы искать собеседника',
                           reply_markup=main_markup())


def register_any_message_handler(disp: Dispatcher):
    disp.register_message_handler(any_message_handler)
