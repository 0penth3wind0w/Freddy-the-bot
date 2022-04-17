import os

from linebot import LineBotApi
from linebot.models import TextSendMessage, StickerSendMessage, ImageSendMessage

ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(ACCESS_TOKEN)

class Push:
    def __init__(self, uid):
        self.uid = uid

    def push_text(self, message):
        text_message = TextSendMessage(text=message)
        line_bot_api.push_message(self.uid, text_message)
    
    def push_image(self, image_url):
        image_message = ImageSendMessage(image_url, image_url)
        line_bot_api.push_message(self.uid, image_message)

    def push_sticker(self, sticker_package, sticker_id):
        sticker_message = StickerSendMessage(package_id=sticker_package, sticker_id=sticker_id)
        line_bot_api.push_message(self.uid, sticker_message)
        
