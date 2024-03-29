from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_menu_btn = InlineKeyboardButton(
    text="🔙 Back", callback_data='main_menu')
"""A button that takes the user back to the main menu.

    :meta hide-value:
"""

back_menu = InlineKeyboardMarkup(inline_keyboard=[[back_to_menu_btn]])
"""A keyboard markup that contains the back to menu button.

    :meta hide-value:
"""

create_user_button = [
    [InlineKeyboardButton(text="Create", callback_data="create_user")],
]
"""A list of lists of buttons that allows to create a user.

    :meta hide-value:
"""

create_user_menu = InlineKeyboardMarkup(
    inline_keyboard=create_user_button)
"""A keyboard markup that contains the create user button.

    :meta hide-value:
"""

main_menu_peer_buttons = [
    [InlineKeyboardButton(text="My bookings", callback_data="get_bookings")]
]
"""A list of lists of buttons that allows a peer to access various features of the bot.

    :meta hide-value:
"""

main_menu_peer = InlineKeyboardMarkup(inline_keyboard=main_menu_peer_buttons)
"""A keyboard markup that contains the main menu buttons for a peer.

    :meta hide-value:
"""
main_menu_admin_buttons = [
    [InlineKeyboardButton(text="My bookings", callback_data="get_bookings")],
    [InlineKeyboardButton(text="Add admin", callback_data="add_admin")],
    [InlineKeyboardButton(text="View reports", callback_data="view_reports")],
]
"""A list of lists of buttons that allows an admin to access various features of the bot.

    :meta hide-value:
"""

main_menu_admin = InlineKeyboardMarkup(inline_keyboard=main_menu_admin_buttons)
"""A keyboard markup that contains the main menu buttons for an admin.

    :meta hide-value:
"""
