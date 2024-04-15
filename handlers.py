import logging
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import config
import os
import db
import kb
import text
import states

bot = Bot(token = config.BOT_TOKEN)
router = Router()
# admin_id = os.getenv("admin_id")
admin_id = "740905109"
print(admin_id)


@router.message(Command("start"))
async def start_handler(msg: types.Message):
    user_id = msg.from_user.id
    print(user_id)
    print(admin_id)
    if int(user_id) == int(admin_id):
        await msg.answer(text.hello_polya)
    elif not db.check_user(user_id = user_id):
        db.add_user_id(user_id)
        await msg.answer(text.hello_message, reply_markup=kb.new_question)
    elif  db.check_quest_wait(user_id = user_id)[0] == 0:
        await msg.answer(text.hello_message, reply_markup=kb.new_question)
    else:
        await msg.answer(text.send_question)


@router.callback_query(F.data == "new_question")
async def new_question_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        print(callback.message.chat.id)
        print(callback.message.message_id)
        if db.check_quest_wait(user_id = callback.from_user.id)[0] == 0:
            if callback.message.text == text.hello_message or callback.message == text.send_question:
                await callback.message.delete()
                await callback.message.answer(text.ask_question)
                await state.set_state(states.QuestState.question_wait)
            else:
                print(callback.message.chat.id)
                await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                await callback.message.answer(text.ask_question)
                await state.set_state(states.QuestState.question_wait)
        else:
            await callback.message.answer(text.send_question)
    except Exception as er:logging.error(er)


@router.message(states.QuestState.question_wait)
async def ask_handler(msg: types.Message):
    question = msg.text
    user_id = msg.from_user.id
    answer_button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Ответить", callback_data=f"answer:{user_id}")],
    ])
    if not db.check_user(user_id=user_id):
        db.update_quest_await (user_id=user_id, question_wait=1)
        await msg.answer(text.send_question, reply_markup=answer_button)
    else:
        db.update_quest_await(user_id=user_id, question_wait=1)
        await bot.send_message(admin_id, f"Внимание вопрос: {question}", reply_markup=answer_button)
        await msg.answer(text.send_question)
        

@router.callback_query(lambda c: c.data.startswith("answer:"))
async def callback_answer_button(callback: types.CallbackQuery, state: FSMContext):
    try:
        question_id = callback.data[len('answer:'):]
        await state.set_state(states.QuestState.answer_wait)
        await state.update_data(question_id=question_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer(text.answer)
    except Exception as er:logging.error(er)

@router.message(states.QuestState.answer_wait)
async def answer_process(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data = data["question_id"]
    await state.clear()
    answer = msg.text
    await bot.send_message(data, f"Ваш ответ: {answer}", reply_markup = kb.new_question)
    db.update_quest_await(user_id=data, question_wait=0)
    await msg.answer(text.send_answer)