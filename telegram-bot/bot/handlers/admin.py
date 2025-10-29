import logging
import random
import string

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.fsm.states import Form
from bot.keyboards.inline import get_main_keyboard, get_role_keyboard
from bot.api.planka import create_planka_user

from aiogram.utils.markdown import hcode

# --- Router and Filter Setup ---
router = Router()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# --- Utility Functions ---
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for i in range(length))


# --- Command Handlers ---
# Admin start handler (only for admins)
@router.message(CommandStart())
async def admin_start_handler(message: Message) -> None:
    await message.answer(
        f"Your user ID: {message.from_user.id}\nHello, admin {message.from_user.full_name}!",
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Action cancelled.", reply_markup=types.ReplyKeyboardRemove())


# --- FULL USER CREATION FLOW ---
@router.callback_query(F.data == "full_create_user")
async def process_full_create_callback(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await state.set_state(Form.full_creation_data)
    await callback_query.message.answer(
        "Enter data for the new user in the format:\n"
        "`email;Full Name;username;password`\n\n"
        "Or just `email;Full Name;username` and the password will be generated automatically."
    )
    await callback_query.answer()


@router.message(Form.full_creation_data, F.text)
async def process_full_creation_data(message: Message, state: FSMContext):
    parts = [p.strip() for p in message.text.split(";")]
    if len(parts) < 3 or len(parts) > 4:
        await message.answer(
            "Invalid format. Please use the format: `email;Full Name;username;[password]`"
        )
        return

    email, name, username = parts[:3]
    password = parts[3] if len(parts) == 4 else generate_random_password()

    await state.update_data(
        email=email, name=name, username=username, password=password
    )
    await state.set_state(Form.full_creation_role)
    await message.answer(
        "Data accepted. Now select a role for the user:",
        reply_markup=get_role_keyboard(),
    )


@router.callback_query(Form.full_creation_role, F.data.startswith("set_role_"))
async def process_full_creation_role(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    planka_token: str,
    planka_api_url: str,
):
    role = callback_query.data.split("_")[-1]
    user_data = await state.get_data()
    await state.clear()

    await callback_query.message.edit_text(
        "All data collected. Creating user in Planka..."
    )

    payload = {
        "email": user_data["email"],
        "name": user_data["name"],
        "username": user_data["username"],
        "password": user_data["password"],
        "role": role,
    }

    try:
        response = create_planka_user(planka_api_url, planka_token, payload)
        if response.status_code == 200:
            await callback_query.message.answer(
                f"User {payload['username']} successfully created!",
                reply_markup=get_main_keyboard(),
            )
        else:
            await callback_query.message.answer(
                f"Error: {response.status_code} - {response.text}",
                reply_markup=get_main_keyboard(),
            )
    except Exception as e:
        await callback_query.message.answer(
            f"API connection error: {e}", reply_markup=get_main_keyboard()
        )

    await callback_query.answer()


# --- QUICK USER CREATION FLOW ---
@router.callback_query(F.data == "quick_create_user")
async def process_quick_create_callback(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await state.set_state(Form.quick_creation_username)
    await callback_query.message.answer("Enter `username` for the new user:")
    await callback_query.answer()


@router.message(Form.quick_creation_username, F.text)
async def process_quick_creation_username(
    message: Message, state: FSMContext, planka_token: str, planka_api_url: str
):
    username = message.text.strip()
    await state.clear()

    await message.answer(f"Generating data for `{username}` and creating user...")

    password = generate_random_password()
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    payload = {
        "email": f"{username}_{random_suffix}@example.com",
        "name": username,
        "username": username,
        "password": password,
        "role": "boardUser",
    }

    try:
        response = create_planka_user(planka_api_url, planka_token, payload)
        if response.status_code == 200:
            await message.answer(
                f"User <b>{hcode(username)}</b> successfully created!\n\n"
                f"<b>Login:</b> {hcode(username)}\n"
                f"<b>Password:</b> {hcode(password)}",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(
                f"Error: {response.status_code} - {response.text}",
                reply_markup=get_main_keyboard(),
            )
    except Exception as e:
        await message.answer(
            f"API connection error: {e}", reply_markup=get_main_keyboard()
        )
