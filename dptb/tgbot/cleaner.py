import re
from typing import Any, Dict

from telegram import Update
from telegram.ext import CallbackContext

from dptb.celery import app

from .commands import COMMANDS
from .loader import bot


def clear_commands(update: Dict[str, Any]) -> None:
    """Удаление команд бота из чата."""
    try:
        message = update.get('message')
        chat_id = message['chat'].get('id')
        message_id = message.get('message_id')

        if message.get('location'):
            text = 'delete'
        else:
            text = message.get('text')
            if text:
                text = text.replace('/', '')
                command = re.findall(r'(.*?)(?=\@)', text)
                if command:
                    text = command[0]

        if text in COMMANDS['en'] or text == 'delete':
            bot.delete_message(chat_id, message_id)

    except Exception:
        text = (
            'Для корректной работы, я должен быть администратором группы! '
            'Иначе я не смогу удалять подобные технические сообщения.'
        )
        bot.send_message(chat_id, text)


def remove_keyboard(update: Update, context: CallbackContext) -> None:
    """
    Удаление клавиатуры после нажатия.
        Принимает:
    - update (:obj:`Update`)
    - context (:obj:`CallbackContext`)
    """
    chat = update.effective_chat
    del_menu_id = update.effective_message.message_id
    try:
        context.bot.delete_message(chat.id, del_menu_id)
    except Exception as error:
        raise KeyError(error)


@app.task(ignore_result=True)
def delete_messages_by_time(chat_id: int, message_id: int) -> None:
    """
    Удаление сообщения.
        Параметры:
    - chat id (:obj:`int` | :obj:`str`)
    - message id (:obj:`int` | :obj:`str`)
    """
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as error:
        raise KeyError(error)
