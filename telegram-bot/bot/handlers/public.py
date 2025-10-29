import logging

from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.api.planka import create_planka_user
from bot.keyboards.inline import get_main_keyboard

# --- Router Setup ---
router = Router()


# --- Command Handlers ---
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    full_name = message.from_user.full_name or "Unknown"

    # Register user for notifications (store chat_id)
    # Assuming we have a way to register users for notifications
    # For now, just acknowledge the start
    await message.answer(
        f"Your user ID: {user_id}\nHello, {full_name}! You can now receive notifications from the project.",
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "This bot sends notifications when you are mentioned in the project.\n"
        "Use /start to register for notifications."
    )
