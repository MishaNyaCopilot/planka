import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

from bot.handlers import admin, public
from bot.api.planka import get_planka_token


async def notify_handler(request):
    bot = request.app["bot"]
    try:
        data = await request.json()
        chat_id = data.get("chat_id")
        message = data.get("message")

        if not chat_id or not message:
            return web.Response(status=400, text="Missing chat_id or message")

        await bot.send_message(
            chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN
        )
        return web.Response(text="OK")
    except Exception as e:
        logging.error(f"Error in notify_handler: {e}")
        return web.Response(status=500, text="Internal Server Error")


async def main():
    # --- Environment Variables ---
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    ADMIN_IDS_STR = os.getenv("TELEGRAM_ADMIN_IDS")
    PLANKA_API_URL = os.getenv("PLANKA_API_URL")
    PLANKA_ADMIN_EMAIL = os.getenv("PLANKA_ADMIN_EMAIL")
    PLANKA_ADMIN_PASSWORD = os.getenv("PLANKA_ADMIN_PASSWORD")

    if not all(
        [
            TOKEN,
            ADMIN_IDS_STR,
            PLANKA_API_URL,
            PLANKA_ADMIN_EMAIL,
            PLANKA_ADMIN_PASSWORD,
        ]
    ):
        logging.critical("One or more environment variables are missing.")
        sys.exit(1)

    ADMIN_IDS = [int(admin_id) for admin_id in ADMIN_IDS_STR.split(",")]

    # --- Dispatcher and Bot Setup ---
    logging.info("Authenticating with Planka API on startup...")
    planka_token = get_planka_token(
        PLANKA_API_URL, PLANKA_ADMIN_EMAIL, PLANKA_ADMIN_PASSWORD
    )

    if not planka_token:
        logging.critical(
            "Could not authenticate with Planka API. Please check credentials and API URL."
        )
        sys.exit(1)

    logging.info("Successfully authenticated with Planka API.")

    dp = Dispatcher(planka_token=planka_token, planka_api_url=PLANKA_API_URL)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # --- Register handlers ---
    # Public handlers (no filter)
    dp.include_router(public.router)

    # Admin handlers (filtered)
    admin.router.message.filter(admin.IsAdmin(ADMIN_IDS))
    admin.router.callback_query.filter(admin.IsAdmin(ADMIN_IDS))
    dp.include_router(admin.router)

    # --- Web App Setup ---
    app = web.Application()
    app.add_routes([web.post("/notify", notify_handler)])
    app["bot"] = bot  # Make bot instance available to handlers

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logging.info("Web server started on port 8080")

    # --- Start Polling ---
    logging.info("Starting bot polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
