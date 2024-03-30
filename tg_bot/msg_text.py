MAX_LINE_WIDTH = 200
"""A constant that defines the maximum line width for the messages.

    :meta hide-value:
"""

SPEC_MSG_END = '&#x200D;'
"""A constant that defines the special character to mark the end of a message.

    :meta hide-value:
"""

msg_welcome_new = "Welcome! Please, register to start using."
"""A message that welcomes a new user and prompts them to create a user.

    :meta hide-value:
"""

msg_welcome = "Welcome, {name}!"
"""A message that welcomes an existing user by their name.

    :meta hide-value:
"""

msg_enter_name = "Enter your login:"
"""A message that asks the user to enter their login.

    :meta hide-value:
"""

msg_register_succ = "Registered successfully."
"""A message that confirms the successful creation of a user.

    :meta hide-value:
"""

msg_register_fail = "Registration failed."
"""A message that reports the failed creation of a user.

    :meta hide-value:
"""

msg_register_confirm = "Create a user with '{name}' name?"
"""A message that asks to confirm a user name.

    :meta hide-value:
"""

msg_select_booking = "Your bookings"
"""A message that displays to the user their bookings.

    :meta hide-value:
"""

msg_cancel_booking_succ = "Booking canceled successfully."
"""
    A message that confirms the successful cancellation of a booking.

    :meta hide-value:    
"""

msg_cancel_booking_fail = "Booking cancellation failed."
"""
    A message that reports the failed cancellation of a booking.
    
    :meta hide-value:    
"""

msg_check_query_fail = "An error occured. Please, use /start to reload."
"""A message that informs the user that an error has occurred and prompts them to reload the bot.

    :meta hide-value:
"""

msg_choose_action = "Choose an action:"
"""A message that prompts the user to choose an action to perform.

    :meta hide-value:
"""

msg_share_contact = "Please share a contact to add as admin:"
"""A message that prompts the user to share a contact.

    :meta hide-value:  
"""

msg_shared_contact_already_admin = "This user is already an admin. Aborted."
"""A message that informs the user that a shared contact is already an admin.

    :meta hide-value:  
"""

msg_shared_contact_exists = "User found, you can proceed."
"""A message that informs the user that a shared contact is found in the db.

    :meta hide-value:  
"""

msg_shared_contact_not_found = "User not found, ask them to register in this bot."
"""A message that informs the user that a shared contact is not found in the db.

    :meta hide-value:  
"""

msg_add_admin_confirm = "User with login: '{login}' will be promoted to admin. Proceed?"
"""A message that asks to confirm a admin promotion.

    :meta hide-value:
"""

msg_add_admin_succ = "Admin added successfully."
"""A message that confirms the successful addition of an admin.

    :meta hide-value:
"""

msg_add_admin_fail = "An error occured. Admin was not added. Please, try again later"
"""A message that reports the failed addition of an admin.

    :meta hide-value:
"""

msg_add_admin_cancel = "Cancelled. Admin was not added."
"""A message that reports the cancelled addition of an admin.

    :meta hide-value:
"""

btn_yes = "Yes"
"""A button that confirms an action.

    :meta hide-value:
"""

btn_no = "No"
"""A button that cancels an action.

    :meta hide-value:   
"""

btn_cancel_booking = "Cancel booking"
"""A button that cancels a booking.

    :meta hide-value:
"""

btn_menu = "🏠 Main Menu"
"""A button that takes the user to the main menu.

    :meta hide-value:
"""

btn_back = "🔙 Back"
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
