import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.handlers import admin
from bot.api.planka import get_planka_token

async def main():
    # --- Environment Variables ---
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    ADMIN_IDS_STR = os.getenv("TELEGRAM_ADMIN_IDS")
    PLANKA_API_URL = os.getenv("PLANKA_API_URL")
    PLANKA_ADMIN_EMAIL = os.getenv("PLANKA_ADMIN_EMAIL")
    PLANKA_ADMIN_PASSWORD = os.getenv("PLANKA_ADMIN_PASSWORD")

    if not all([TOKEN, ADMIN_IDS_STR, PLANKA_API_URL, PLANKA_ADMIN_EMAIL, PLANKA_ADMIN_PASSWORD]):
        logging.critical("One or more environment variables are missing.")
        sys.exit(1)

    ADMIN_IDS = [int(admin_id) for admin_id in ADMIN_IDS_STR.split(',')]

    # --- Dispatcher and Bot Setup ---
    # Authenticate with Planka on startup to get the token
    logging.info("Authenticating with Planka API on startup...")
    planka_token = get_planka_token(PLANKA_API_URL, PLANKA_ADMIN_EMAIL, PLANKA_ADMIN_PASSWORD)

    if not planka_token:
        logging.critical("Could not authenticate with Planka API. Please check credentials and API URL.")
        sys.exit(1)
    
    logging.info("Successfully authenticated with Planka API.")

    # Pass token and other data to all handlers through the dispatcher
    dp = Dispatcher(planka_token=planka_token, planka_api_url=PLANKA_API_URL)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # --- Register handlers ---
    # Apply admin filter to all handlers in the admin router
    admin.router.message.filter(admin.IsAdmin(ADMIN_IDS))
    admin.router.callback_query.filter(admin.IsAdmin(ADMIN_IDS))
    dp.include_router(admin.router)

    # --- Start Polling ---
    logging.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
