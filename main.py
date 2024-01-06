# main.py

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from gemini_pro import generate_response, handle_photo_processing

# Rest of your code...

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6917224699:AAFNxlwiqLluR0gGbVqtBx-vkVUWoWHrBqQ")
dp = Dispatcher(bot)


class ChatStates(StatesGroup):
  CHATTING = State()


class UserData:

  def __init__(self):
    self.chat_history = []


user_data_dict = {}


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
  await message.reply(
      "Hi! I'm Gemini Pro. (You can use free) How can I help you?")
  user_data_dict[message.from_user.id] = UserData()


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
  # Handle the photo processing logic using gemini vision pro
  user_message = message.caption or "What's in the picture? Watch carefully and describe all details."

  # Assuming you have a function in gemini_pro.py to handle photo processing
  response, user_data_dict[
      message.from_user.id].chat_history = handle_photo_processing(
          user_message, message.photo)

  parse_mode = types.ParseMode.MARKDOWN if any(
      markdown_chars in response
      for markdown_chars in ['*', '_', '`']) else types.ParseMode.HTML
  await message.reply(response, parse_mode=parse_mode)


@dp.message_handler()
async def message_handler(message: types.Message):
  await bot.send_chat_action(message.chat.id, 'typing')

  user_id = message.from_user.id
  user_data = user_data_dict.get(user_id)
  if not user_data:
    user_data = UserData()
    user_data_dict[user_id] = user_data

  response, user_data.chat_history = generate_response(message.text,
                                                       user_data.chat_history)
  parse_mode = types.ParseMode.MARKDOWN if any(
      markdown_chars in response
      for markdown_chars in ['*', '_', '`']) else types.ParseMode.HTML

  await message.reply(response, parse_mode=parse_mode)


if __name__ == '__main__':
  storage = MemoryStorage()
  dp.storage = storage
  executor.start_polling(dp, skip_updates=True)
