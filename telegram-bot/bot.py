import asyncio
import logging
import os
import sys
import requests

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.client.default import DefaultBotProperties

# --- Environment Variables & Constants ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_IDS_STR = os.getenv("TELEGRAM_ADMIN_IDS")
PLANKA_API_URL = os.getenv("PLANKA_API_URL")
PLANKA_ADMIN_EMAIL = os.getenv("PLANKA_ADMIN_EMAIL")
PLANKA_ADMIN_PASSWORD = os.getenv("PLANKA_ADMIN_PASSWORD")

if not all([TOKEN, ADMIN_IDS_STR, PLANKA_API_URL, PLANKA_ADMIN_EMAIL, PLANKA_ADMIN_PASSWORD]):
    raise ValueError("One or more environment variables are missing.")

ADMIN_IDS = [int(admin_id) for admin_id in ADMIN_IDS_STR.split(',')]

# --- FSM States ---
class Form(StatesGroup):
    creating_user_email = State()
    creating_user_name = State()
    creating_user_username = State()
    creating_user_password = State()

# --- Admin Filter ---
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMIN_IDS

# --- Bot and Dispatcher Setup ---
dp = Dispatcher()

# --- Keyboard Builder ---
def get_main_keyboard():
    keyboard = [[InlineKeyboardButton(text="Создать пользователя", callback_data="create_user")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- Command Handlers ---
@dp.message(CommandStart(), IsAdmin())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, админ {message.from_user.full_name}!", reply_markup=get_main_keyboard())

@dp.message(CommandStart())
async def command_start_non_admin(message: Message) -> None:
    await message.answer("Access Denied.")

@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=types.ReplyKeyboardRemove())

# --- Callback & FSM for User Creation ---
@dp.callback_query(F.data == "create_user", IsAdmin())
async def process_create_user_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if not dp.workflow_data.get('planka_token'):
        await callback_query.message.answer("Ошибка: Не удалось получить токен Planka при старте. Проверьте лог контейнера бота.")
        await callback_query.answer()
        return

    await state.set_state(Form.creating_user_email)
    await callback_query.message.answer("Введите email для нового пользователя:")
    await callback_query.answer()

@dp.message(Form.creating_user_email, F.text)
async def process_email(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(Form.creating_user_name)
    await message.answer("Отлично. Теперь введите полное имя пользователя (например, John Doe):")

@dp.message(Form.creating_user_name, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.creating_user_username)
    await message.answer("Хорошо. Теперь введите username (логин латиницей, например, jdoe):")

@dp.message(Form.creating_user_username, F.text)
async def process_username(message: Message, state: FSMContext) -> None:
    await state.update_data(username=message.text)
    await state.set_state(Form.creating_user_password)
    await message.answer("Принято. И последнее - введите пароль для нового пользователя:")

@dp.message(Form.creating_user_password, F.text)
async def process_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    planka_token = dp.workflow_data.get('planka_token')
    await state.clear()

    await message.answer("Все данные собраны. Создаю пользователя в Planka...")

    try:
        headers = {
            "Authorization": f"Bearer {planka_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": user_data['email'],
            "name": user_data['name'],
            "username": user_data['username'],
            "password": user_data['password'],
            "role": "boardUser",
        }
        
        response = requests.post(f"{PLANKA_API_URL}/users", headers=headers, json=payload)

        if response.status_code == 200:
            await message.answer(f"Пользователь {user_data['username']} успешно создан!", reply_markup=get_main_keyboard())
        else:
            await message.answer(f"Ошибка при создании пользователя. Сервер ответил: {response.status_code} - {response.text}", reply_markup=get_main_keyboard())
    
    except Exception as e:
        await message.answer(f"Произошла ошибка при подключении к API Planka: {e}", reply_markup=get_main_keyboard())

# --- Main Bot Logic ---
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Authenticate with Planka on startup
    try:
        logging.info("Authenticating with Planka API...")
        auth_payload = {"emailOrUsername": PLANKA_ADMIN_EMAIL, "password": PLANKA_ADMIN_PASSWORD}
        response = requests.post(f"{PLANKA_API_URL}/access-tokens", json=auth_payload)
        if response.status_code == 200:
            access_token = response.json().get("item")
            if access_token:
                dp.workflow_data['planka_token'] = access_token
                logging.info("Successfully authenticated with Planka API.")
            else:
                logging.error("Planka API token not found in response.")
        else:
            logging.error(f"Failed to authenticate with Planka API. Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
        logging.error(f"Exception during Planka authentication: {e}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())