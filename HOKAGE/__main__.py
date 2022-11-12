import html
import importlib
import json
import re
import time
import traceback
from sys import version_info
from typing import Optional
from pyrogram import Client, idle, filters
from pyrogram.types import Message

from pyrogram import __version__ as pver
from pyrogram import idle
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as lver
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import CallbackContext, CallbackQueryHandler, Filters, MessageHandler
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tver

import HOKAGE.modules.sql.users_sql as sql
from HOKAGE import (
    BOT_USERNAME,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    OWNER_USERNAME,
    PORT,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    UPDATES_CHANNEL,
    URL,
    WEBHOOK,
    StartTime,
    dispatcher,
    pgram,
    telethn,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from HOKAGE.modules import ALL_MODULES
from HOKAGE.modules.disable import DisableAbleCommandHandler
from HOKAGE.modules.helper_funcs.alternate import typing_action
from HOKAGE.modules.helper_funcs.chat_status import is_user_admin
from HOKAGE.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


HELP_MSG = "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴍᴇɴᴜ ~"
START_MSG = "* ɪ ᴀᴍ ᴡᴇʟʟ ᴀɴᴅ ᴀʟɪᴠᴇ ;)"


PM_START_TEX = """
ʜᴇʟʟᴏ `{}`, ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ sᴡᴇᴇᴛʜᴇᴀʀᴛ\nɪ ᴀᴍ ᴡᴏʀᴋɪɴɢ ᴡɪᴛʜ ᴀᴡᴇsᴏᴍᴇ sᴘᴇᴇᴅ
"""

PM_START_TEXT = """
*ʜᴇʟʟᴏ {} !*
ɪ ᴀᴍ  ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ \nᴡɪᴛʜ ᴜsᴇғᴜʟʟ ғᴇᴀᴛᴜʀᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛʜᴇɴ sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀs ʙᴜᴅᴅʏ
∘──────◈───────∘
 ➻ *ᴜᴘᴛɪᴍᴇ:* `{}`
 ➻ *ᴜsᴇʀs:* `{}`
 ➻ *chats:* `{}`
∘──────◈───────∘
⊚ ɪ ᴄᴀɴ ᴅᴏ ᴀ ᴠᴀʀɪᴇᴛʏ ᴏꜰ ᴛʜɪɴɢꜱ, ᴍᴏꜱᴛ ᴄᴏᴍᴍᴏɴ ᴏꜰ ᴇᴍ ᴀʀᴇ:
⊚ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ʙᴀɴ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ.
⊚ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴍᴇᴅɪᴀ + ᴛᴇxᴛ ᴀɴᴅ ʙᴜᴛᴛᴏɴꜱ, ᴡɪᴛʜ ᴘʀᴏᴘᴇʀ ꜰᴏʀᴍᴀᴛᴛɪɴɢ.
⊚ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ ᴡʜᴏ ꜰʟᴏᴏᴅ ʏᴏᴜʀ ᴄʜᴀᴛ ᴜꜱɪɴɢ ᴍʏ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ᴍᴏᴅᴜʟᴇ.
⊚ ᴡᴀʀɴ ᴜꜱᴇʀꜱ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴛʜᴇ ᴏᴘᴛɪᴏɴꜱ ꜱᴇᴛ ᴀɴᴅ ʀᴇꜱᴛʀɪᴄᴛ ᴇᴍ ᴀᴄᴄᴏʀᴅɪɴɢʟʏ.
⊚ ꜱᴀᴠᴇ ɴᴏᴛᴇꜱ ᴀɴᴅ ꜰɪʟᴛᴇʀꜱ ᴡɪᴛʜ ᴘʀᴏᴘᴇʀ ꜰᴏʀᴍᴀᴛᴛɪɴɢ ᴀɴᴅ ʀᴇᴘʟʏ ᴍᴀʀᴋᴜᴘ.
⊚ ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ ᴛᴏᴏ ɪɴ ᴜʀ ɢʀᴏᴜᴘꜱ
⊚ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ꜰᴇᴀᴛᴜʀᴇꜱ ᴡʜɪᴄʜ ᴜ ʟɪᴋᴇ ᴛʜᴀᴛꜱ
ᴛʜᴇʀᴇꜱ ᴇᴠᴇɴ ᴍᴏʀᴇ! ᴛʜɪꜱ ɪꜱ ᴊᴜꜱᴛ ᴛʜᴇ ᴛɪᴘ ᴏꜰ ᴛʜᴇ ɪᴄᴇʙᴇʀɢ. ᴅᴏ ɴᴏᴛᴇ ɪ ɴᴇᴇᴅ
ᴛᴏ ʙᴇ ᴘʀᴏᴍᴏᴛᴇᴅ ᴡɪᴛʜ ᴘʀᴏᴘᴇʀ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ᴛᴏ ꜰᴜɴᴄᴛɪᴏɴ ᴘʀᴏᴘᴇʀʟʏ. 
ᴇʟꜱᴇ ɪ ᴡᴏɴ'ᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ꜰᴜɴᴄᴛɪᴏɴ ᴀꜱ ꜱᴀɪᴅ.
━━━━━━━━━━━━━━━━━━━━━━━
ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ!
"""


GROUP_START_TEXT = """
ɪ'ᴀᴍ  ᴀʟɪᴠᴇ  ʙᴀʙʏ !

ʜᴀᴠᴇɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ: {} 
"""

buttons = [
    [
        InlineKeyboardButton(
            text="➕ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ➕ ", url=f"t.me/{BOT_USERNAME}?startgroup=true"
        )
    ],
    [
        InlineKeyboardButton(text="🧰️ ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_back"),
        InlineKeyboardButton(
            text="🎓 ɪɴғᴏʀᴍᴀᴛɪᴏɴ", callback_data="Hokage_"
        ),
    ],
    [
        InlineKeyboardButton(text="⛽ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(
            text="📣 ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{UPDATES_CHANNEL}"
        ),
    ],
]

buttons2 = [
           [
        InlineKeyboardButton(text="💢 ᴍᴀɪɴᴛᴀɪɴᴇʀ", url="https://t.me/ItsProf"),
        InlineKeyboardButton(
            text="🎓 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/xelyourslurred"),
        ),
    ],
    [
        InlineKeyboardButton(text="⛽ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(
            text="📣 ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{UPDATES_CHANNEL}"
        ),
    ],
           ]


HELP_STRINGS = """
ʜᴇʏ ᴛʜᴇʀᴇ! ᴍʏ ɴᴀᴍᴇ ɪs ʜᴏᴋᴀɢᴇ.
ʜᴀᴠᴇ ᴀ ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ғᴏʀ ᴀɴ ɪᴅᴇᴀ ᴏғ sᴏᴍᴇ ᴏғ ᴛʜᴇ ᴛʜɪɴɢs ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴡɪᴛʜ
━━━━━━━━━━━━━━━━━━━━━━━
*ᴍᴀɪɴ* ᴄᴏᴍᴍᴀɴᴅs ᴀᴠᴀɪʟᴀʙʟᴇ:
❏ /help: PM's ʏᴏᴜ ᴛʜɪs ᴍᴇssᴀɢᴇ.
❏ /donate: ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏɴ ʜᴏᴡ ᴛᴏ ᴅᴏɴᴀᴛᴇ!
❏ /settings:
   ↣ ɪɴ ᴘᴍ: ᴡɪʟʟ sᴇɴᴅ ʏᴏᴜ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ғᴏʀ ᴀʟʟ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs.
   ↣ ɪɴ ᴀ ɢʀᴏᴜᴘ: ᴡɪʟʟ ʀᴇᴅɪʀᴇᴄᴛ ʏᴏᴜ ᴛᴏ ᴘᴍ, ᴡɪᴛʜ ᴀʟʟ ᴛʜᴀᴛ ᴄʜᴀᴛ  sᴇᴛᴛɪɴɢs.
━━━━━━━━━━━━━━━━━━━━━━━
"""

INFO_ABOUT = """
━━━━━━━━━━━━━━━━━━━━━━━
ɪ'ᴍ ᴀ ᴘᴀʀᴛ ᴏғ ᴛᴇᴄʜ ǫᴜᴀʀᴅ
ʜᴀᴠᴇ ᴀ ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ғᴏʀ ᴀɴ ɪᴅᴇᴀ ᴏғ sᴏᴍᴇ ᴏғ ᴛʜᴇ ᴛʜɪɴɢs ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴡɪᴛʜ
━━━━━━━━━━━━━━━━━━━━━━━
ʜᴇʀᴇ ɪs ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏғ ʜᴏᴋᴀɢᴇ ʀᴏʙᴏᴛ
ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴛᴇᴄʜǫᴜᴀʀᴅ
"""
buttons3 = [
            [
                InlineKeyboardButton("🍂 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/xelyourslurred"),
                InlineKeyboardButton("🍄 ᴍᴀɪɴᴛᴀɪɴᴇʀ", url=f"https://t.me/ItsProf"),
            ],
            [
                InlineKeyboardButton("🫖 ʀᴇᴘᴏsɪᴛᴏʀʏ", url=f"https://xnxx.com"),
                
            ],
            [
                InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="Hokage_back"),
            ]
            ]


DONATE_STRING = """➢ ᴊᴜsᴛ sᴜᴘᴘᴏʀᴛ ᴜs, ᴡᴇ ᴡɪʟʟ ʙᴇ ᴍᴏʀᴇ ᴛʜᴀɴ ʜᴀᴘᴘʏ"""


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"HOKAGE.modules.{module_name}")
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("ᴄᴀɴ'ᴛ ʜᴀᴠᴇ ᴛᴡᴏ ᴍᴏᴅᴜʟᴇs ᴡɪᴛʜ ᴛʜᴇ sᴀᴍᴇ ɴᴀᴍᴇ! ᴘʟᴇᴀsᴇ ᴄʜᴀɴɢᴇ ᴏɴᴇ")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("ᴛʜɪs ᴘᴇʀsᴏɴ ᴇᴅɪᴛᴇᴅ ᴀ ᴍᴇssᴀɢᴇ")
    print(update.effective_message)


def start(update: Update, context: CallbackContext):
    args = context.args
    usr = update.effective_user
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if mod == "Admins":
                    mod = "Admins"
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="⟲ ʙᴀᴄᴋ ⟳", callback_data="help_back"
                                )
                            ]
                        ]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match[1])

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match[1], update.effective_user.id, False)
                else:
                    send_settings(match[1], update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("🎊")
            time.sleep(0.5)
            lol.edit_text("⚡")
            time.sleep(0.3)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ... ")
            time.sleep(0.4)
            lol.delete()
            update.effective_message.reply_text(
                    PM_START_TEXT.format(
                    escape_markdown(first_name),
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats(),
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ʜᴇʏ `{}`,\n\nɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !\n➺ᴜᴘᴛɪᴍᴇ: `{}` \n➺ᴜsᴇʀs: `{}` \n➺ᴄʜᴀᴛs: `{}` ".format(
                usr.first_name,
                uptime,
                sql.num_users(),
                sql.num_chats(),
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons2))
                

   


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="ᴇxᴄᴇᴘᴛɪᴏɴ ᴡʜɪʟᴇ ʜᴀɴᴅʟɪɴɢ ᴀɴ ᴜᴘᴅᴀᴛᴇ:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = f"An ᴇxᴄᴇᴘᴛɪᴏɴ ᴡᴀs ʀᴀɪsᴇᴅ ᴡʜɪʟᴇ ʜᴀɴᴅʟɪɴɢ ᴀɴ ᴜᴘᴅᴀᴛᴇ\n<pre>ᴜᴘᴅᴀᴛᴇ = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}</pre>\n\n<pre>{html.escape(tb)}</pre>"

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update, context):
    """#TODO
    Params:
        update  -
        context -
    """

    try:
        raise context.error
    except (Unauthorized, BadRequest):
        pass
        # remove update.message.chat_id from conversation list
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match[1]
            text = (
                f"╒═══「 *{HELPABLE[module].__mod_name__}* module: 」\n"
                + HELPABLE[module].__help__
            )

            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="⟲ ʙᴀᴄᴋ ⟳", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match[1])
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match[1])
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass



def hokage_callback_data(update, context):
    query = update.callback_query
    first_name = update.effective_user.first_name
    uptime = get_readable_time((time.time() - StartTime))
    if query.data == "Hokage_":
        query.message.edit_text(
            text=INFO_ABOUT,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons3))
                
    elif query.data == "Hokage_back":
        first_name = update.effective_user.first_name
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(uptime),
                sql.num_users(),
                sql.num_chats(),
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )



@typing_action
def get_help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏғ {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=" ʜᴇʟᴘ ​",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=" ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ ",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=" ᴏᴩᴇɴ ʜᴇʀᴇ ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = f" 〔 *{HELPABLE[module].__mod_name__}* 〕\n" + HELPABLE[module].__help__

        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⟲ ʙᴀᴄᴋ ⟳", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                f"*{mod.__mod_name__}*:\n{mod.__user_settings__(user_id)}"
                for mod in USER_SETTINGS.values()
            )

            dispatcher.bot.send_message(
                user_id,
                "ᴛʜᴇsᴇ ᴀʀᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴜsᴇʀ sᴘᴇᴄɪғɪᴄ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    elif CHAT_SETTINGS:
        chat_name = dispatcher.bot.getChat(chat_id).title
        dispatcher.bot.send_message(
            user_id,
            text=f"ᴡʜɪᴄʜ ᴍᴏᴅᴜʟᴇ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ {chat_name}'s sᴇᴛᴛɪɴɢs ғᴏʀ?",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
            ),
        )

    else:
        dispatcher.bot.send_message(
            user_id,
            "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ any chat settings available :'(\nsᴇɴᴅ ᴛʜɪs "
            "in ᴀ ɢʀᴏᴜᴘ chat ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ɪɴ ᴛᴏ ғɪɴᴅ ɪᴛs ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs!",
            parse_mode=ParseMode.MARKDOWN,
        )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match[1]
            module = mod_match[2]
            chat = bot.get_chat(chat_id)
            text = f"*{escape_markdown(chat.title)}* ʜᴀs ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴇᴛᴛɪɴɢs ғᴏʀ ᴛʜᴇ *{CHAT_SETTINGS[module].__mod_name__}* ᴍᴏᴅᴜʟᴇ:\n\n" + CHAT_SETTINGS[
                module
            ].__chat_settings__(
                chat_id, user.id
            )

            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⟲ ʙᴀᴄᴋ ⟳",
                                callback_data=f"stngs_back({chat_id})",
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match[1]
            curr_page = int(prev_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {chat.title} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ in.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match[1]
            next_page = int(next_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {chat.title} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ in.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match[1]
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text=f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {escape_markdown(chat.title)} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "ᴍᴇssᴀɢᴇ ɪs ɴᴏᴛ ᴍᴏᴅɪғɪᴇᴅ",
            "Query_id_invalid",
            "ᴍᴇssᴀɢᴇ ᴄᴀɴ'ᴛ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ",
        ]:
            LOGGER.exception("ᴇxᴄᴇᴘᴛɪᴏɴ ɪɴ sᴇᴛᴛɪɴɢs ʙᴜᴛᴛᴏɴs. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type == chat.PRIVATE:
        send_settings(chat.id, user.id, True)

    elif is_user_admin(chat, user.id):
        text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ  sᴇᴛᴛɪɴɢs, as ᴡᴇʟʟ ᴀs ʏᴏᴜʀs."
        msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴇᴛᴛɪɴɢs",
                            url=f"t.me/{context.bot.username}?start=stngs_{chat.id}",
                        )
                    ]
                ]
            ),
        )

    else:
        text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs."


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 5513481385 and DONATION_LINK:
            update.effective_message.reply_text(
                f"ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ the ᴘᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ [ʜᴇʀᴇ]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ PM ғɪʀsᴛ to ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("ᴍɪɢʀᴀᴛɪɴɢ ғʀᴏᴍ %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("sᴜᴄᴄᴇssғᴜʟʟʏ ᴍɪɢʀᴀᴛᴇᴅ!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendAnimation(
                f"@{SUPPORT_CHAT}",
                animation="https://telegra.ph/file/c16b730bfdf7c7f0625fa.jpg",
                caption=f"""
ㅤ◨ {dispatcher.bot.first_name} ɪs ᴀʟɪᴠᴇ.

━━━━━━━━━━━━━
≕ **ᴍʏ ᴏᴡɴᴇʀ :** [ᴍɪᴛʜʟᴏʀᴀᴀ](https://t.me/{OWNER_USERNAME})
≕ **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
≕ **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
≕ **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
≕ **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
≕ **ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `2.0`
━━━━━━━━━━━━━
""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                "ʙᴏᴛ ɪsɴᴛ ᴀʙʟᴇ ᴛᴏ sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴛᴏ support_chat, ɢᴏ ᴀɴᴅ ᴄʜᴇᴄᴋ !"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = DisableAbleCommandHandler("start", start, run_async=True)

    help_handler = DisableAbleCommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = DisableAbleCommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    hokage_callback_handler = CallbackQueryHandler(
        hokage_callback_data, pattern=r"Hokage_", run_async=True
    )
    donate_handler = DisableAbleCommandHandler("donate", donate, run_async=True)
    migrate_handler = MessageHandler(
        Filters.status_update.migrate, migrate_chats, run_async=True
    )

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(hokage_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("ᴜsɪɴɢ webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info(f"◆ ʜᴏᴋᴀɢᴇ sᴛᴀʀᴛᴇᴅ, ᴜsɪɴɢ ʟᴏɴɢ ᴘᴏʟʟɪɴɢ. | sᴜᴘᴘᴏʀᴛ: [@{SUPPORT_CHAT}]")
        updater.start_polling(
            timeout=15,
            read_latency=4,
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES,
        )


if __name__ == "__main__":
    LOGGER.info(
        f"◆ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴏᴀᴅᴇᴅ ᴍᴏᴅᴜʟᴇs. : {str(ALL_MODULES)}"
    )
    telethn.start(bot_token=TOKEN)
    pgram.start()
    main()
    idle()


