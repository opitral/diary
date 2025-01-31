from aiogram.filters import BaseFilter
from aiogram.types import Message

from pkg.config import settings


class IsAdminFilter(BaseFilter):
    def __init__(self) -> None:
        self.admins_telegram_id = settings.ADMINS_TELEGRAM_ID

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins_telegram_id
