from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.files import PickleStorage
from config import load_config
from utils.database_manager import DatabaseManager


config = load_config('../.env')
bot = Bot(token=config.token, parse_mode='HTML')
storage = PickleStorage('../storage.pickle')
dp = Dispatcher(bot, storage=storage)
db = DatabaseManager('../storage.db')
