import html
import json
import re
from time import sleep
import requests
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import InsaneRobot.modules.sql.chatbot_sql as sql
from InsaneRobot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from InsaneRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from InsaneRobot.modules.log_channel import gloggable
from MukeshAPI import api

@user_admin_no_reply
@gloggable
def Insanerm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_Insane = sql.set_Insane(chat.id)
        if is_Insane:
            is_Insane = sql.set_Insane(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"ᴀɪ ᴅɪꜱᴀʙʟᴇᴅ\n"
                f"<b>ᴀᴅᴍɪɴ :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin_no_reply
@gloggable
def Insaneadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_Insane = sql.rem_Insane(chat.id)
        if is_Insane:
            is_Insane = sql.rem_Insane(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"ᴀɪ ᴇɴᴀʙʟᴇ\n"
                f"<b>ᴀᴅᴍɪɴ :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin
@gloggable
def Insane(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "• ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="add_chat({})"),
                InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="rm_chat({})"),
            ],
        ]
    )
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def Insane_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "Insane":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message:
        if reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_Insane = sql.is_Insane(chat_id)
    if is_Insane:
        return

    if message.text and not message.document:
        if not Insane_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        url=api.chatgpt(message.text,mode="gf")["results"]
        message.reply_text(url)


CHATBOTK_HANDLER = CommandHandler("chatbot", Insane, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(Insaneadd, pattern=r"add_chat", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(Insanerm, pattern=r"rm_chat", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]
