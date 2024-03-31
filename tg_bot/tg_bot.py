import requests
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
from notifications import NotificationService

load_dotenv()
TOKEN = getenv('TOKEN')
if TOKEN is None:
    raise ValueError('No token provided')

router = Router()
notification_service = NotificationService()

user_exists = True
is_admin = True
username = "Test"
# bookings = [{'id': 1, 'date': '2024-03-30', 'time_start': '09:00', 'time_end': '10:00', 'room': 'room1', 'cancelled': False},
#             {'id': 2, 'date': '2024-03-31', 'time_start': '10:00',
#                 'time_end': '11:00', 'room': 'room2', 'cancelled': False},
#             {'id': 3, 'date': '2024-04-02', 'time_start': '11:00', 'time_end': '12:00', 'room': 'room3', 'cancelled': False}]

# reports = [{'date': '2024-03-30', 'from_name': 'User1', 'from_id': 339095791, 'to_name': 'User2', 'to_id': 6432798382, 'reason': 'reason1'},
#            {'date': '2024-03-31', 'from_name': 'User2', 'from_id': 6432798382, 'to_name': 'User3', 'to_id': 339095791, 'reason': 'reason2'},]
URL = "http://localhost:5000/api/meetingRoomBooking" 

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


async def remove_main_message(chat_id, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        msg_id = data.get('msg_id')
        if msg_id:
            await bot.delete_message(chat_id, msg_id)
    except Exception as e:
        logging.error(str(e))


async def api_get_user(telegram_id: int):
    """
    A helper function that returns the user object for the given user ID.

    :param str telegram_id: The ID of the user.
    """
    url = f'{URL}/GetUserById/{telegram_id}' 
    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            user_data = response.json()
            print(user_data)
            if user_data:
                return user_data["login"], user_data["admin"]
            else:
                return None, None
        else:
            logging.error(f"Ошибка при получении данных пользователя. Код состояния: {response.status_code}")
            return None, None
    except Exception as e:
        logging.error(str(e))
        return None, None


async def api_create_user(telegram_id: int, login: str):
    """ 
    A helper function that creates a new user with the given ID and name.
    """
    url = f'{URL}/CreateUser'
    try:
        # payload = {
        #     "telegramId": telegram_id,
        #     "login": login
        # }
        #response = requests.post(url, json=payload)
        response = requests.post(f'{url}?telegramId={telegram_id}&login={login}')

        if response.status_code == 201:
            new_user_data = response.json()
            print(new_user_data)
            return True
        elif response.status_code == 409:
            logging.error("Пользователь уже зарегистрирован.")
            return False
        else:
            logging.error(f"Ошибка при создании пользователя. Код состояния: {response.status_code}")
            return False
    except Exception as e:
        logging.error(str(e))
        return False

async def api_get_bookings(telegram_id: str):
    """ 
    A helper function that returns a list of booking objects for the given user ID.
    """
    url = f'{URL}/GetBookingsByUserId?userId={telegram_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bookings = response.json()
            print(bookings)
            formatted_bookings = [{'id': booking['id'], 'text': f"{booking['data'][:5]} {booking['startTime']} - {booking['endTime']} floor{booking['meetingRoom']['floor']}"} for booking in bookings if not booking['canceled']]
            return formatted_bookings
        elif response.status_code == 404:
            logging.error("Бронирования для указанного пользователя не найдены.")
            return []
        else:
            logging.error(f"Ошибка при получении бронирований. Код состояния: {response.status_code}")
            return None
    except Exception as e:
        logging.error(str(e))
        return None
    #return [{'id': booking['id'], 'text': f"{booking['date']} {booking['time_start']} - {booking['time_end']} {booking['room']}"} for booking in bookings if not booking['cancelled']]


async def api_cancel_booking(booking_id: str):
    """ 
    A helper function that cancels a booking with the given ID.
    """
    url = f'{URL}/CanceleBooking?bookingId={booking_id}'
    try:
        response = requests.put(url)
        print(response)
        if response.status_code == 200:
            logging.info("Бронирование успешно отменено.")
            return True
        elif response.status_code == 404:
            logging.error("Бронирование не найдено.")
            return False
        else:
            logging.error(f"Ошибка при отмене бронирования. Код состояния: {response.status_code}")
            return False
    except Exception as e:
        logging.error(str(e))
        return False
    #bookings[int(id)-1]['cancelled'] = True

async def api_update_admin(user_id: str):
    """ 
    A helper function that updates a user with the given ID to admin.
    """
    url = f'{URL}/Update'
    try:
        payload = {
            "updatedUser": {"Id": user_id, "Admin": True},
            "message": "/addADM"  
        }
        response = requests.put(url, json=payload)
        if response.status_code == 200:
            logging.info("Статус пользователя успешно обновлен.")
            return True
        else:
            logging.error(f"Ошибка. Код состояния: {response.status_code}")
            return True #hardcode
    except Exception as e:
        logging.error(str(e))
        return False


async def api_get_reports():
    url = f'{URL}/GetReports' 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            reports = response.json()
            print(reports)
            return reports
        else:
            logging.error(f"Ошибка при получении отчетов. Код состояния: {response.status_code}")
            return None
    except Exception as e:
        logging.error(str(e))
        return None

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
        await remove_main_message(chat_id=message.chat.id, state=state, bot=bot)
        await message.answer(msg_text.msg_start, reply_markup=ReplyKeyboardRemove())
        name, is_admin = await api_get_user(message.from_user.id)
        if name:
            menu = kb.main_menu_admin if is_admin else kb.main_menu_peer
            msg = await message.answer(msg_text.msg_welcome.format(name=name), reply_markup=menu)
            await state.update_data(msg_id=msg.message_id)
            await state.update_data(is_admin=is_admin)
        else:
            msg = await message.answer(msg_text.msg_welcome_new, reply_markup=kb.input_user_name_menu)
            await state.update_data(msg_id=msg.message_id)
    except Exception as e:
        logging.error(str(e))


@router.callback_query(F.data == "main_menu")
@check_query
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


@router.callback_query(F.data == "input_user_name")
@check_query
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
async def create_user_confirmation(message: Message, state: FSMContext):
    """
    A handler function that asks to confirm the user name.

    :param Message message: The message from the user.
    :param FSMContext state: The finite state machine context for the user.
    """
    current_state = await state.get_state()
    msg = await message.answer(msg_text.msg_register_confirm.format(name=message.text), reply_markup=kb.create_user_confirm_menu)
    await state.update_data(username=message.text)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(None)


@router.callback_query(F.data == "create_user")
async def create_user(callback_query: CallbackQuery, state: FSMContext):
    """
    A handler function that handles the message from the user in the create character state.
    It creates a new character for the user with the given name and sends a message with the main menu.

    :param Message message: The message from the user.
    :param FSMContext state: The finite state machine context for the user.
    """
    data = await state.get_data()
    print(data)
    username = data.get('username')
    if await api_create_user(callback_query.from_user.id, username):
        await send_edit_message(callback_query, f"{msg_text.msg_register_succ}\n{msg_text.msg_welcome.format(name=username)}", reply_markup=kb.main_menu_peer)
        await state.update_data(is_admin=False)
    else:
        await send_edit_message(callback_query, msg_text.msg_register_fail, reply_markup=kb.input_user_name_menu)


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
    print(bookings)

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


@router.callback_query(F.data == "add_admin")
@check_query
async def add_admin(callback_query: CallbackQuery,  state: FSMContext, bot: Bot, **kwargs):
    """
    A handler function that handles the callback query for the add admin button.

    :param CallbackQuery callback_query: The callback query from the user.
    :param str msg: (optional) The message to be sent. Defaults to None.
    :param \*\*kwargs: Additional keyword arguments.
    """
    await remove_main_message(
        chat_id=callback_query.message.chat.id, state=state, bot=bot)
    await callback_query.message.answer(msg_text.msg_share_contact, reply_markup=kb.contact_request_kb)


@router.message(F.user_shared)
async def handle_contact(message: Message, state: FSMContext):
    """
    A handler function that handles the message event when a user sends a contact.

    :param types.Message message: The message from the user.
    :param FSMContext state: The state context.
    """
    contact_id = message.user_shared.user_id
    name, is_admin = await api_get_user(message.user_shared.user_id)
    if name and is_admin or not name:
        if not name:
            await message.answer(msg_text.msg_shared_contact_not_found,
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(msg_text.msg_shared_contact_already_admin,
                                 reply_markup=ReplyKeyboardRemove())
        msg = await message.answer(msg_text.msg_choose_action, reply_markup=kb.main_menu_admin)
        await state.update_data(msg_id=msg.message_id)
    else:
        await message.answer(msg_text.msg_shared_contact_exists,
                             reply_markup=ReplyKeyboardRemove())
        builder = InlineKeyboardBuilder()
        builder.button(text=msg_text.btn_yes,
                       callback_data=f"update_admin#{contact_id}")
        builder.button(text=msg_text.btn_no,
                       callback_data="update_admin#")
        builder.adjust(2)
        msg = await message.answer(msg_text.msg_add_admin_confirm.format(login=name), reply_markup=builder.as_markup())
        await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data.startswith("update_admin#"))
@check_query
async def update_admin(callback_query: CallbackQuery,  state: FSMContext, bot: Bot, **kwargs):
    """
    A handler function that handles the callback query for the update admin button.

    :param CallbackQuery callback_query: The callback query from the user.
    :param FSMContext state: The state context.
    :param \*\*kwargs: Additional keyword arguments.
    """
    await remove_main_message(
        chat_id=callback_query.message.chat.id, state=state, bot=bot)
    _, new_admin_id = callback_query.data.split('#')
    if new_admin_id:
        msg_result = msg_text.msg_add_admin_succ if await api_update_admin(new_admin_id) else msg_text.msg_add_admin_fail
        await callback_query.message.answer(msg_result, reply_markup=ReplyKeyboardRemove())
    else:
        await callback_query.message.answer(msg_text.msg_add_admin_cancel, reply_markup=ReplyKeyboardRemove())
    msg = await callback_query.message.answer(msg_text.msg_choose_action, reply_markup=kb.main_menu_admin)
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data == "view_reports")
@check_query
async def view_reports(callback_query: CallbackQuery, **kwargs):
    """
    A handler function that handles the callback query for the get reports button.
    It edits the message with the current bookings of the user.

    :param CallbackQuery callback_query: The callback query from the user.
    :param \*\*kwargs: Additional keyword arguments.
    """
    reports = await api_get_reports()
    msg = msg_text.format_string(''.join(
        [msg_text.msg_report_text.format(
            date=report['booking']['data'],
            # id=report['id'],
            from_name=report['senderUser']['login'],
            from_id=report['senderUser']['telegramId'],
            to_name=report['recipientUser']['login'],
            to_id=report['recipientUser']['telegramId'],
            reason=report['reportType']['reportText']
        ) for report in reports]))
    await send_edit_message(callback_query, msg, reply_markup=kb.back_menu)


async def on_startup(bot: Bot):
    await notification_service.start(bot)


async def on_shutdown(bot: Bot):
    await notification_service.stop()


async def main() -> None:
    """
    The main function that creates the bot and the dispatcher and starts polling for updates.
    """
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )

    asyncio.run(main())
