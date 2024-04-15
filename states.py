from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class QuestState(StatesGroup):
    question_wait = State()
    answer_wait = State()