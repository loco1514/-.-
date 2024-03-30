MAX_LINE_WIDTH = 200
"""A constant that defines the maximum line width for the messages.

    :meta hide-value:
"""

SPEC_MSG_END = '&#x200D;'
"""A constant that defines the special character to mark the end of a message.

    :meta hide-value:
"""

msg_start = "👋 Добро пожаловать в Meeting Room бота!"
"""A start message of the bot.

    :meta hide-value:
"""

msg_welcome_new = "Для дальнейшего пользования, пожалуйста, зарегистрируйтесь."
"""A message that welcomes a new user and prompts them to create a user.

    :meta hide-value:
"""

msg_welcome = "Здравствуй, {name}!"
"""A message that welcomes an existing user by their name.

    :meta hide-value:
"""

msg_enter_name = "Введите ваш логин:"
"""A message that asks the user to enter their login.

    :meta hide-value:
"""

msg_register_succ = "Регистрация прошла успешно."
"""A message that confirms the successful creation of a user.

    :meta hide-value:
"""

msg_register_fail = "Не удалось зарегистрировать пользователя."
"""A message that reports the failed creation of a user.

    :meta hide-value:
"""

msg_register_confirm = "Создать пользователя с именем '{name}'?"
"""A message that asks to confirm a user name.

    :meta hide-value:
"""

msg_select_booking = "Ваши брони:"
"""A message that displays to the user their bookings.

    :meta hide-value:
"""

msg_cancel_booking_succ = "Бронь успешно отменена."
"""
    A message that confirms the successful cancellation of a booking.

    :meta hide-value:    
"""

msg_cancel_booking_fail = "Не удалось отменить бронь."
"""
    A message that reports the failed cancellation of a booking.
    
    :meta hide-value:    
"""

msg_check_query_fail = "Произошла ошибка. Пожалуйста, введите /start для перезапуска."
"""A message that informs the user that an error has occurred and prompts them to reload the bot.

    :meta hide-value:
"""

msg_choose_action = "Выберите действие:"
"""A message that prompts the user to choose an action to perform.

    :meta hide-value:
"""

msg_share_contact = "Пожалуйста, поделитесь контактом, который будет добавлен в качестве администратора:"
"""A message that prompts the user to share a contact.

    :meta hide-value:  
"""

msg_shared_contact_already_admin = "Данный пользователь уже является администратором. Процесс прерван."
"""A message that informs the user that a shared contact is already an admin.

    :meta hide-value:  
"""

msg_shared_contact_exists = "Пользователь найден. Вы можете продолжать."
"""A message that informs the user that a shared contact is found in the db.

    :meta hide-value:  
"""

msg_shared_contact_not_found = "Пользователь не найден. Попросите его зарегистрироваться в данном боте."
"""A message that informs the user that a shared contact is not found in the db.

    :meta hide-value:  
"""

msg_add_admin_confirm = "Пользователь с логином: '{login}' будет повышен до администратора. Продолжить?"
"""A message that asks to confirm a admin promotion.

    :meta hide-value:
"""

msg_add_admin_succ = "Администратор был успешно добавлен."
"""A message that confirms the successful addition of an admin.

    :meta hide-value:
"""

msg_add_admin_fail = "Произошла ошибка. Администратор не был добавлен. Попробуйте повторить позже."
"""A message that reports the failed addition of an admin.

    :meta hide-value:
"""

msg_add_admin_cancel = "Действие было отменено. Администратор не был добавлен."
"""A message that reports the cancelled addition of an admin.

    :meta hide-value:
"""

msg_notification_text_start = "🔔 #Уведомление:\nВы забронировали комнату '{room}' на {time}⏳.\nНе забудьте явиться в указанное время! 👍"
"""A notification message that the booking is about to start.

    :meta hide-value:
"""

msg_notification_text_end = "🔔 #Уведомление:\nБронь комнаты '{room}' истекает в {time}⌛.\nПожалуйста, не забудьте убрать за собой и покинуть комнату вовремя! 🧹🚪"
"""A notification message that the booking is about to end.

    :meta hide-value:
"""

btn_yes = "Да"
"""A button that confirms an action.

    :meta hide-value:
"""

btn_no = "Нет"
"""A button that cancels an action.

    :meta hide-value:   
"""

btn_cancel_booking = "Отменить бронирование"
"""A button that cancels a booking.

    :meta hide-value:
"""

btn_menu = "🏠 Главное меню"
"""A button that takes the user to the main menu.

    :meta hide-value:
"""

btn_back = "🔙 Назад"
"""A button that takes the user to the previous menu.

    :meta hide-value:
"""


def format_string(input_string, line_length=MAX_LINE_WIDTH):
    """A function that formats a string to fit a given line width and adds a special character at the end.

    :param str input_string: The string to format.
    :param int line_length: (optional) The maximum line width. Defaults to MAX_LINE_WIDTH.

    :returns:
        str: The formatted string with the special character at the end.
    """
    return f"{input_string:<{line_length}}"+SPEC_MSG_END


def _apply_formatting():
    """A function that applies the formatting function to all the global variables that start with 'msg_'."""
    globals_to_format = {k: v for k,
                         v in globals().items() if isinstance(v, str) and k.startswith('msg_') and k != __name__}
    for name, value in globals_to_format.items():
        formatted_value = format_string(value)
        globals()[name] = formatted_value


_apply_formatting()
