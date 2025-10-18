from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    # Full creation flow
    full_creation_data = State()
    full_creation_role = State()

    # Quick creation flow
    quick_creation_username = State()
