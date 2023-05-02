from django.conf import settings
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Dispatcher, Filters,
                          MessageHandler)

from .external_api.chat_gpt import get_answer_davinci_person
from .external_api.image_gen import first_step_get_image, get_image_dall_e
from .geoservis.positions import my_current_geoposition
from .loader import bot
from .menus import ask_registration, main_menu, private_menu
from .message.stereography import send_audio_transcription
from .parse.jokes import show_joke
from .service_message import cancel


def setup_dispatcher(dp: Dispatcher):
    """
    Добавление обработчиков событий из Telegram
    """
    # команды
    dp.add_handler(
        CommandHandler('ask_registration', ask_registration)
    )
    # основное меню и его Handler's
    dp.add_handler(
        CommandHandler('main_menu', main_menu)
    )
    dp.add_handler(
        ConversationHandler(
            entry_points=[CallbackQueryHandler(first_step_get_image,
                                               pattern='^gen_image_first$')],
            states={
                'image_gen': [MessageHandler(Filters.text, get_image_dall_e)]
            },
            fallbacks=[MessageHandler(Filters.regex('cancel'), cancel)]
        )
    )
    dp.add_handler(
        CallbackQueryHandler(show_joke, pattern='^show_joke$')
    )
    dp.add_handler(
        MessageHandler(Filters.location, private_menu)
    )
    dp.add_handler(
        CallbackQueryHandler(my_current_geoposition, pattern='^my_position$')
    )

    dp.add_handler(
        MessageHandler(
            Filters.voice, send_audio_transcription
        )
    )
    dp.add_handler(
        MessageHandler(
            Filters.text,
            get_answer_davinci_person
        )
    )
    return dp


n_workers = 0 if settings.DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True)
)
