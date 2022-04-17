import os

from linebot import LineBotApi
from linebot.models import TextSendMessage, StickerSendMessage, ImageSendMessage

ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(ACCESS_TOKEN)

class Reply:
    def __init__(self, reply_token):
        self.reply_token = reply_token

    def reply_text(self, message):
        text_message = TextSendMessage(text=message)
        line_bot_api.reply_message(self.reply_token, text_message)
    
    def reply_image(self, image_url):
        image_message = ImageSendMessage(image_url, image_url)
        line_bot_api.reply_message(self.reply_token, image_message)

    def reply_sticker(self, sticker_package, sticker_id):
        sticker_message = StickerSendMessage(package_id=sticker_package, sticker_id=sticker_id)
        line_bot_api.reply_message(self.reply_token, sticker_message)
        
