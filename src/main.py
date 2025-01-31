import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from internal.handlers import router
from internal.utils import remind_admins
from pkg.database import create_db
from pkg.config import settings
from pkg.logger import get_logger

logger = get_logger(__name__)


async def on_startup(bot: Bot):
    logger.info("Bot started")
    create_db()
    for admin_telegram_id in settings.ADMINS_TELEGRAM_ID:
        await bot.send_message(admin_telegram_id, "Bot started")


async def on_shutdown(bot: Bot):
    logger.info("Bot stopped")
    for admin_telegram_id in settings.ADMINS_TELEGRAM_ID:
        await bot.send_message(admin_telegram_id, "Bot stopped")


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_API_TOKEN.get_secret_value())
    dp = Dispatcher()

    commands = [
        BotCommand(command="/new_record", description="Create new record")
    ]
    await bot.set_my_commands(commands)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(router)

    _ = asyncio.create_task(remind_admins(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
