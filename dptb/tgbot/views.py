import json
from typing import Any, Dict

from django.http import HttpRequest, JsonResponse
from django.views import View
from telegram import Update

from dptb.celery import app

from .cleaner import clear_commands
from .dispatcher import dispatcher
from .loader import bot


@app.task(ignore_result=True)
def process_telegram_event(update_json: Dict[str, Any]) -> None:
    """Обработка json и распределение запроса."""
    update = Update.de_json(update_json, bot)
    if update.message:
        clear_commands(update_json)
    dispatcher.process_update(update)


class TelegramBotWebhookView(View):
    """Получение запроса от Телеграмм."""
    def post(self, request: HttpRequest, *args, **kwargs) -> Dict[str, Any]:
        process_telegram_event.delay(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request: HttpRequest, *args, **kwargs) -> Dict[str, Any]:
        return JsonResponse({"ok": "Get request received! But nothing done"})
