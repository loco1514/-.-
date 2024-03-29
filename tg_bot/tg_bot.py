import asyncio
import logging
from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv
import kb
import msg_text
import html
from functools import wraps

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()

user_exists = False
is_admin = False
username = "Test"
bookings = [{'id': 1, 'date': '2024-03-30', 'time_start': '09:00', 'time_end': '10:00', 'room': 'room1', 'cancelled': False},
            {'id': 2, 'date': '2024-03-31', 'time_start': '10:00',
                'time_end': '11:00', 'room': 'room2', 'cancelled': False},
            {'id': 3, 'date': '2024-04-02', 'time_start': '11:00', 'time_end': '12:00', 'room': 'room3', 'cancelled': False}]


def check_query(func):
    """
    A decorator that checks if the callback query is from the same message as the user menu.

    :param function func: The function to be decorated.

    :returns:
        function: The wrapper function that performs the check.
    """
    @wraps(func)
    async def wrapper(callback_query: CallbackQuery, state: FSMContext, **kwargs):
        data = await state.get_data()
        msg_id = data.get('msg_id')
        try:
            if callback_query.message.message_id != msg_id:
                await send_edit_message(callback_query, msg_text.msg_check_query_fail,)
            else:
                return await func(callback_query=callback_query, state=state, **kwargs)
        except Exception as e:
            logging.error(str(e))
    return wrapper


class MenuStates(StatesGroup):
    """
    A class that represents the states of the user creation menu.
    """
    create_user = State()


async def send_edit_message(callback_query: CallbackQuery, msg: str, reply_markup: types.InlineKeyboardMarkup = None):
    """
    A helper function that edits the message with the given text and reply markup, if they are different from the current ones.

    :param CallbackQuery callback_query: The callback query from the user.
    :param srt msg: The text to be sent.
    :param types.InlineKeyboardMarkup reply_markup: (optional) The reply markup to be sent. Defaults to None.
    """
    current_btns = [
        btn.text for row in reply_markup.inline_keyboard for btn in row] if reply_markup else []
    msg_btns = [
        btn.text for row in callback_query.message.reply_markup.inline_keyboard for btn in row]
    if html.unescape(msg) != html.unescape(callback_query.message.html_text) \
            or current_btns != msg_btns:
        try:
            await callback_query.message.edit_text(msg, reply_markup=reply_markup)
        except Exception as e:
            logging.error(str(e))


async def api_get_user(id: str):
    """
    A helper function that returns the user object for the given user ID.

    :param str id: The ID of the user.
    """
    # TODO API request
    if user_exists:
        return username, is_admin
    else:
        return None, None


async def api_create_user(id: str, name: str):
    """ 
    A helper function that creates a new user with the given ID and name.
    """
    # TODO API request
    global user_exists
    global username
    user_exists = True
    username = name
    return True


async def api_get_bookings(id: str):
    """ 
    A helper function that returns a list of booking objects for the given user ID.
    """
    # TODO API request
    return [{'id': booking['id'], 'text': f"{booking['date']} {booking['time_start']} - {booking['time_end']} {booking['room']}"} for booking in bookings if not booking['cancelled']]


async def api_cancel_booking(id: str):
    """ 
    A helper function that cancels a booking with the given ID.
    """
    # TODO API request
    global bookings
    bookings[int(id)-1]['cancelled'] = True
    return True


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext, bot: Bot):
    """
    A handler function that handles the /start command from the user.
    It checks if the user exists, and if not, it prompts them to create one.

    :param Message message: The message from the user.
    :param FSMContext state: The finite state machine context for the user.
    :param Bot bot: The bot instance.
    """
    try:
        data = await state.get_data()
        msg_id = data.get('msg_id')
        if msg_id:
            if not await bot.delete_message(message.chat.id, msg_id):
                return
        name, is_admin = await api_get_user(message.from_user.id)
        if name:
            menu = kb.main_menu_admin if is_admin else kb.main_menu_peer
            msg = await message.answer(msg_text.msg_welcome.format(name=name), reply_markup=menu)
            await state.update_data(msg_id=msg.message_id)
            await state.update_data(is_admin=is_admin)
        else:
            await message.answer(msg_text.msg_welcome_new, reply_markup=kb.create_user_menu)
    except Exception as e:
        logging.error(str(e))


@router.callback_query(F.data == "main_menu")
async def main_menu(callback_query: CallbackQuery, state: FSMContext):
    """
    A handler function that handles the callback query for the main menu button.
    It edits the message with the main menu text and reply markup.

    :param CallbackQuery callback_query: The callback query from the user.
    """
    data = await state.get_data()
    is_admin = data.get('is_admin')
    menu = kb.main_menu_admin if is_admin else kb.main_menu_peer
    await send_edit_message(callback_query, msg_text.msg_choose_action, reply_markup=menu)


@router.callback_query(F.data == "create_user")
async def input_user_name(callback_query: CallbackQuery, state: FSMContext):
    """
    A handler function that handles the callback query for the create user button.
    It sets the state to the create user state and edits the message with the prompt for the user name.

    :param CallbackQuery callback_query: The callback query from the user.
    :param FSMContext state: The finite state machine context for the user.
    """
    await state.set_state(MenuStates.create_user)
    await send_edit_message(callback_query, msg_text.msg_enter_name)


@router.message(MenuStates.create_user)
async def create_user(message: Message, state: FSMContext):
    """
    A handler function that handles the message from the user in the create character state.
    It creates a new character for the user with the given name and sends a message with the main menu.

    :param Message message: The message from the user.
    :param FSMContext state: The finite state machine context for the user.
    """
    await state.set_state(None)
    if await api_create_user(message.from_user.id, message.text):
        msg = await message.answer(f"{msg_text.msg_register_succ}\n{msg_text.msg_welcome.format(name=message.text)}", reply_markup=kb.main_menu_peer)
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(is_admin=False)
    else:
        msg = await message.answer(msg_text.msg_register_fail, reply_markup=kb.create_user_menu)


@router.callback_query(F.data == "get_bookings")
@check_query
async def get_bookings(callback_query: CallbackQuery, msg: str = None, **kwargs):
    """
    A handler function that handles the callback query for the get bookings button.
    It edits the message with the current bookings of the user.

    :param CallbackQuery callback_query: The callback query from the user.
    :param str msg: (optional) The message to be sent. Defaults to None.
    :param \*\*kwargs: Additional keyword arguments.
    """
    bookings = await api_get_bookings(callback_query.from_user.id)
    builder = InlineKeyboardBuilder()
    for booking in bookings:
        builder.button(text=booking['text'],
                       callback_data=f"hangle_booking#{booking['id']}#{booking['text']}")
    builder.add(kb.back_to_menu_btn)
    builder.adjust(2)

    await send_edit_message(callback_query, msg if msg else msg_text.msg_select_booking, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("hangle_booking#"))
@check_query
async def hangle_booking(callback_query: CallbackQuery, msg: str = None, **kwargs):
    _, booking_id, booking_text = callback_query.data.split('#')
    builder = InlineKeyboardBuilder()
    builder.button(text=msg_text.btn_cancel_booking,
                   callback_data=f"cancel_booking:{booking_id}")
    builder.button(text=msg_text.btn_back, callback_data=f"get_bookings")
    builder.button(text=msg_text.btn_menu, callback_data=f"main_menu")
    builder.adjust(1, 2)
    await send_edit_message(callback_query,  msg_text.format_string(booking_text), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("cancel_booking:"))
@check_query
async def cancel_booking(callback_query: CallbackQuery, **kwargs):
    _, booking_id = callback_query.data.split(':')
    if await api_cancel_booking(booking_id):
        msg = msg_text.msg_cancel_booking_succ
    else:
        msg = msg_text.msg_cancel_booking_fail
    await get_bookings(callback_query=callback_query, msg=msg, **kwargs)


async def main() -> None:
    """
    The main function that creates the bot and the dispatcher and starts polling for updates.
    """
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )

    asyncio.run(main())
