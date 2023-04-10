from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔎 Начать поиск')
    markup.add('⭐ Интересы поиска')
    return markup
