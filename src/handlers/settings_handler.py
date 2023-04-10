from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from loader import bot, config, db


def gen_interests_markup(user_interests: list[bool | int]) -> InlineKeyboardMarkup:
    """ Генерирует клавиатуру интересов с галочками перед теми которые пользователь уже выбрал """
    markup = InlineKeyboardMarkup()
    for i in range(len(config.interests)):
        text = ''
        if user_interests[i]:
            text += '✅ '
        text += config.interests[i]
        markup.add(InlineKeyboardButton(text, callback_data=f'interest_{i}'))
    markup.add(InlineKeyboardButton('🗑 Сбросить интересы', callback_data='throw_off'))
    return markup


async def interests_handler(message: Message):
    chat_id = message.chat.id
    res = await db.fetchone("SELECT interests FROM users WHERE tg_id=?", [chat_id])
    interests = list(map(int, res[0].split(' ')))
    markup = gen_interests_markup(interests)
    await bot.send_message(
        chat_id,
        'Мы попытаемся соединить вас с собеседником который выберет похожие интересы.\n\nВыберите ваши интересы:',
        reply_markup=markup)


async def interests_callback(query: CallbackQuery):
    qdata = query.data
    chat_id = query.message.chat.id
    # Получаем интересы пользователя из БД
    res = await db.fetchone("SELECT interests FROM users WHERE tg_id=?", [chat_id])
    interests = list(map(int, res[0].split(' ')))
    # Если пользователь нажал на кнопку с интересом
    if qdata.startswith('interest_'):
        # Меняем значение интереса на противоположное
        interest_id = int(qdata.split('_')[1])
        interests[interest_id] = int(not interests[interest_id])
    else:
        interests = [0] * len(interests)
    # Обновляем интересы пользователя в базе данных
    await db.query("UPDATE users SET interests=? WHERE tg_id=?", [" ".join(map(str, interests)), chat_id])
    markup = gen_interests_markup(interests)
    # Отправляем обновлённую клавиатуру
    await query.message.edit_reply_markup(markup)
    await query.answer()


def register_settings_handlers(disp: Dispatcher):
    disp.register_message_handler(interests_handler, text=['⭐ Интересы поиска'])
    disp.register_message_handler(interests_handler, commands=['interests'])
    disp.register_callback_query_handler(interests_callback,
                                         lambda x: x.data.startswith('interest_') or x.data == 'throw_off')

