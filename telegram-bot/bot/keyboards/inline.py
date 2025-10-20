from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Role data can be stored here or fetched from somewhere else if it becomes dynamic
ROLES = ["admin", "projectOwner", "boardUser"]


def get_main_keyboard():
    """Creates the main menu keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="Create Detailed", callback_data="full_create_user"
            )
        ],
        [
            InlineKeyboardButton(
                text="Quick Generation", callback_data="quick_create_user"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_role_keyboard():
    """Creates the role selection keyboard."""
    keyboard = [
        [InlineKeyboardButton(text=role, callback_data=f"set_role_{role}")]
        for role in ROLES
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
