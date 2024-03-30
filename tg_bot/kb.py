from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers, ReplyKeyboardRemove

back_to_menu_btn = InlineKeyboardButton(
    text="🔙 Назад", callback_data='main_menu')
"""A button that takes the user back to the main menu.

    :meta hide-value:
"""

back_menu = InlineKeyboardMarkup(inline_keyboard=[[back_to_menu_btn]])
"""A keyboard markup that contains the back to menu button.

    :meta hide-value:
"""

input_user_name_button = [
    [InlineKeyboardButton(text="Зарегистрироваться",
                          callback_data="input_user_name")],
]
"""A list of lists of buttons that allows to create a user.

    :meta hide-value:
"""

input_user_name_menu = InlineKeyboardMarkup(
    inline_keyboard=input_user_name_button)
"""A keyboard markup that contains the create user button.

    :meta hide-value:
"""

create_user_confirm_button = [
    [InlineKeyboardButton(text="Да", callback_data="create_user"),
     InlineKeyboardButton(text="Нет", callback_data="input_user_name")],
]
"""A list of lists of buttons that allows to confirm a user name input.
    :meta hide-value:
"""

create_user_confirm_menu = InlineKeyboardMarkup(
    inline_keyboard=create_user_confirm_button)
"""A keyboard markup that contains the create user confirm buttons.

    :meta hide-value:
"""

update_admin_confirm_button = [
    [InlineKeyboardButton(text="Да", callback_data="update_admin"),
     InlineKeyboardButton(text="Нет", callback_data="main_menu")],
]
"""A list of lists of buttons that allows to confirm an admin update.
    :meta hide-value:
"""

update_admin_confirm_menu = InlineKeyboardMarkup(
    inline_keyboard=update_admin_confirm_button)
"""A keyboard markup that contains the update admin confirm buttons.

    :meta hide-value:
"""

main_menu_peer_buttons = [
    [InlineKeyboardButton(text="Мои брони", callback_data="get_bookings")]
]
"""A list of lists of buttons that allows a peer to access various features of the bot.

    :meta hide-value:
"""

main_menu_peer = InlineKeyboardMarkup(inline_keyboard=main_menu_peer_buttons)
"""A keyboard markup that contains the main menu buttons for a peer.

    :meta hide-value:
"""
main_menu_admin_buttons = [
    [InlineKeyboardButton(text="Мои брони", callback_data="get_bookings")],
    [InlineKeyboardButton(text="Добавить администратора",
                          callback_data="add_admin")],
    [InlineKeyboardButton(text="Посмотреть жалобы",
                          callback_data="view_reports")],
]
"""A list of lists of buttons that allows an admin to access various features of the bot.

    :meta hide-value:
"""

main_menu_admin = InlineKeyboardMarkup(inline_keyboard=main_menu_admin_buttons)
"""A keyboard markup that contains the main menu buttons for an admin.

    :meta hide-value:
"""

contact_request_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📞 Отправить контакт", request_users=KeyboardButtonRequestUsers(request_id=1, max_quantity=1))]], resize_keyboard=True)
