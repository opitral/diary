import asyncio
import datetime

from aiogram import Bot

from internal.models import Record
from pkg.database import session_factory
from pkg.config import settings
from pkg.logger import get_logger

logger = get_logger(__name__)


async def remind_admins(bot: Bot):
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=settings.NOTIFICATION_TIME.hour, minute=settings.NOTIFICATION_TIME.minute,
                                  second=0, microsecond=0)

        if now >= target_time:
            target_time += datetime.timedelta(days=1)

        sleep_duration = (target_time - now).total_seconds()
        logger.debug(f"Notifying admins in {sleep_duration / 3600:.2f} hours")
        await asyncio.sleep(sleep_duration)

        with session_factory() as session:
            record = session.query(Record).filter(Record.date == datetime.date.today()).first()

        if not record:
            logger.debug("Notifying admins about missing record")
            for admin_telegram_id in settings.ADMINS_TELEGRAM_ID:
                await bot.send_message(admin_telegram_id, "Don't forget to create a record for today")

        else:
            logger.debug("Record already exists for today")
