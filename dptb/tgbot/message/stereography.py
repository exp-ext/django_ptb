import asyncio
import json
import os
from datetime import datetime, timedelta, timezone

import requests
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from ..checking import check_registration
from ..models import HistoryWhisper

load_dotenv()

User = get_user_model()
ADMIN_ID = os.getenv('ADMIN_ID')


class AudioTranscription():
    """
    Отправляет в чат ответом на сообщение транскрибацию речи,
    порученную от АПИ openai-whisper-asr-webservice.

    Для работы в режиме DEBAG необходимо запустить АПИ в контейнере:

    docker run -d -p 9000:9000 -e ASR_MODEL=small \
        onerahmet/openai-whisper-asr-webservice:latest
    """
    ERROR_TEXT = 'Что-то пошло не так 🤷🏼'
    STORY_WINDOWS_TIME = 11
    MAX_TYPING_TIME = 10

    def __init__(self,
                 update: Update,
                 context: CallbackContext) -> None:
        self.update = update
        self.context = context
        self.file_id = update.message.voice.file_id
        self.user = None
        self.current_time = None
        self.time_start = None
        self.transcription_text = None
        self.event = asyncio.Event()
        self.set_user()
        self.set_windows_time()

    def get_audio_transcription(self) -> dict:
        """Основная логика."""
        if self.check_in_works():
            return {'code': 423}

        try:
            asyncio.run(self.get_transcription())

            HistoryWhisper.objects.update(
                user=self.user,
                file_id=self.file_id,
                transcription=self.transcription_text
            )
        except Exception as err:
            self.context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f'Ошибка в Whisper: {err.args[0]}',
            )
            self.transcription_text = AudioTranscription.ERROR_TEXT
        finally:
            self.context.bot.send_message(
                chat_id=self.update.effective_chat.id,
                text=self.transcription_text,
                reply_to_message_id=self.update.message.message_id
            )

    async def get_transcription(self) -> None:
        """
        Асинхронно запускает 2 функции.
        """
        asyncio.create_task(self.send_typing_periodically())
        await sync_to_async(self.request_to_whisper)()

    async def send_typing_periodically(self) -> None:
        """"
        Передаёт TYPING в чат Телеграм откуда пришёл запрос.
        """
        time_stop = (
            datetime.now()
            + timedelta(minutes=AudioTranscription.MAX_TYPING_TIME)
        )
        while not self.event.is_set():
            self.context.bot.send_chat_action(
                chat_id=self.update.effective_chat.id,
                action=ChatAction.TYPING
            )
            await asyncio.sleep(3)
            if datetime.now() > time_stop:
                break

    def request_to_whisper(self) -> None:
        """
        Делает запрос в whisper и выключает typing.
        """
        audio = self.context.bot.get_file(self.file_id)
        response = requests.get(audio.file_path)

        if response.status_code != 200:
            raise HttpResponseBadRequest("Bad Request")
        files = [
            ('audio_file', ('audio.ogg', response.content, 'audio/ogg'))
        ]
        url = (
            'http://localhost:9000/asr'
            if settings.DEBUG else 'http://todo_whisper:9000/asr'
        )
        params = {
            'task': 'transcribe',
            'language': 'ru',
            'output': 'json',
        }
        headers = {
            'accept': 'application/json',
        }
        response = requests.post(
            url=url,
            headers=headers,
            params=params,
            files=files
        )
        self.transcription_text = json.loads(response.content)['text']
        self.event.set()

    def check_in_works(self) -> bool:
        """Проверяет нет ли уже в работе этого запроса."""
        if (self.user.history_whisper.filter(
                created_at__range=[self.time_start, self.current_time],
                file_id=self.file_id).exists()):
            return True
        HistoryWhisper.objects.create(
            user=self.user,
            file_id=self.file_id,
            transcription=AudioTranscription.ERROR_TEXT
        )
        return False

    def set_user(self) -> None:
        """Определяем и назначаем  атрибут user."""
        self.user = get_object_or_404(
            User,
            username=self.update.effective_user.id
        )

    def set_windows_time(self) -> None:
        """Определяем и назначаем атрибуты current_time и time_start."""
        self.current_time = datetime.now(timezone.utc)
        self.time_start = (
            self.current_time
            - timedelta(minutes=AudioTranscription.STORY_WINDOWS_TIME)
        )


def send_audio_transcription(update: Update, context: CallbackContext):
    answers_for_check = {
        '':
        f'Сделаю транскрибацию, если [зарегистрируетесь]({context.bot.link}).'
    }
    if check_registration(update, context, answers_for_check) is False:
        return {'code': 401}
    AudioTranscription(update, context).get_audio_transcription()
