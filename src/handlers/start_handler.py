from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from loader import bot, config, db
from markups import main_markup


async def start_handler(message: Message):
    chat_id = message.chat.id
    await db.query("INSERT OR IGNORE INTO users VALUES (?, ?)", [chat_id, " ".join(['0'] * len(config.interests))])
    await bot.send_message(chat_id, 'Привет', reply_markup=main_markup())


def register_start_handler(disp: Dispatcher):
    disp.register_message_handler(start_handler, commands=['start'])
