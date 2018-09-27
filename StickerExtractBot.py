from telegram import ChatAction
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from PIL import Image
from io import BytesIO
import requests
import logging

from config import token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

updater = Updater(token=token)
dispatcher = updater.dispatcher

@run_async
def sticker(bot, update):
    res = requests.get(bot.get_file(file_id=update.message.sticker.file_id).file_path)
    img = Image.open(BytesIO(res.content))
    compressed_image = BytesIO()
    img.convert('RGBA').save(compressed_image, 'PNG')
    compressed_image.seek(0)

    update.message.chat.send_action(ChatAction.UPLOAD_DOCUMENT)
    bot.send_document(chat_id=update.message.chat_id,
                      document=compressed_image,
                      filename=update.message.sticker.file_id + '.png',
                      reply_to_message_id=update.message.message_id,
                      disable_notification=True,
                      timeout=60)

    compressed_image.seek(0)

    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=compressed_image,
                   reply_to_message_id=update.message.message_id,
                   disable_notification=True)


sticker_handler = MessageHandler(Filters.sticker, sticker)
dispatcher.add_handler(sticker_handler)

updater.start_polling()
updater.idle()
