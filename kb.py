from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

new_question = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Задать вопрос", callback_data = 'new_question')]])

