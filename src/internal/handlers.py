import datetime
from typing import cast

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import Date

from internal.filters import IsAdminFilter
from internal.models import Record
from pkg.database import session_factory
from pkg.logger import get_logger

logger = get_logger(__name__)
router = Router()
router.message.filter(IsAdminFilter())


class CreateRecordState(StatesGroup):
    content = State()


@router.message(Command("new_record"))
async def new_record(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} wants to create a new record")
    with session_factory() as session:
        record = session.query(Record).filter(Record.date == datetime.date.today()).first()

    if record:
        await message.answer("Record already exists for today")

    else:
        await message.answer("Send me the content of the record")
        await state.set_state(CreateRecordState.content)


@router.message(StateFilter(CreateRecordState.content))
async def create_record(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent the content of the record")
    if len(message.text) < 10:
        return await message.answer("Content is too short")
    record = Record(content=message.text, date=cast(Date, datetime.date.today()))
    with session_factory() as session:
        session.add(record)
        session.commit()
        session.refresh(record)

    await message.answer(f"Record created with id {record.id}")
    await state.clear()
    logger.info(f"User {message.from_user.id} created record with id {record.id}")


@router.message()
async def unknown_command(message: Message):
    await message.answer("Unknown command")
