from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from loader import bot, dp, db
from state_groups import UserStates
from markups import main_markup
from aiogram.dispatcher.filters import Text

import datetime
import asyncio


loners = {}


async def search_companion_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    # Получаем интересы пользователя
    res = await db.fetchone("SELECT interests FROM users WHERE tg_id=?", [chat_id])
    user_interests = list(map(int, res[0].split(' ')))
    # Добавляем в кучу одиночек
    loners[chat_id] = user_interests
    msg = await bot.send_message(chat_id, 'Поиск собеседника 10 сек.')
    for i in range(1, 11):
        await asyncio.sleep(1)
        # Если пользователя нет в списке значит его уже кто-то забрал
        if not (chat_id in loners):
            await msg.edit_text('Используйте /stop чтобы остановить диалог')
            return None
        second = 10 - i
        await msg.edit_text(f'Поиск собеседника {second} сек.')
        for loner_id, loner_interests in loners.items():
            if loner_id == chat_id:
                continue
            # Вычисляем процент совпадения интересов
            co = sum(map(lambda x: x[0] == x[1], zip(user_interests, loner_interests))) / len(user_interests)
            # Планка совпадения снижается с каждой секундой
            if co >= second / 10:
                loners.pop(loner_id)
                loners.pop(chat_id)
                # Сохраняем id абонента в хранилище каждого собеседника и устанавливаем состояние коммутации
                await UserStates.commutation.set()
                async with state.proxy() as data:
                    data['last_activity'] = datetime.datetime.now()
                    data['commute_id'] = loner_id
                await dp.storage.set_state(chat=loner_id, state=UserStates.commutation)
                await dp.storage.update_data(chat=loner_id, commute_id=chat_id, last_activity=datetime.datetime.now())
                await msg.edit_text('Используйте /stop чтобы остановить диалог')
                return None
    # Если никого не нашлось убираем id из списка одиночек и завершаем поиск
    loners.pop(chat_id)
    await bot.send_message(chat_id, 'Никого не нашлось попробуйте попозже', reply_markup=main_markup())


async def stop_dialog_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await bot.send_message(data['commute_id'], 'Диалог завершён')
        await dp.storage.finish(chat=data['commute_id'])
        await bot.send_message(chat_id, 'Диалог завершён', reply_markup=main_markup())
        await state.finish()


async def commute_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        # Если сообщения не отправлялись больше часа завершаем сеанс
        if data['last_activity'] + datetime.timedelta(hours=1) < datetime.datetime.now():
            await bot.send_message(chat_id, 'Вы не общались слишком долго, диалог уже завершён.')
            await state.reset_state(with_data=False)
            return None
        data['last_activity'] = datetime.datetime.now()
        await bot.send_message(data['commute_id'], message.text)


def register_dialog_handlers(disp: Dispatcher):
    disp.register_message_handler(search_companion_handler, text=['🔎 Начать поиск'])
    disp.register_message_handler(search_companion_handler, commands=['search'])
    disp.register_message_handler(stop_dialog_handler, commands=['stop'], state=UserStates.commutation)
    disp.register_message_handler(commute_handler, state=UserStates.commutation)
