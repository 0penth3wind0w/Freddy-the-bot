import os
import random

from linebot import LineBotApi
from linebot.models import Event, TextSendMessage, StickerSendMessage, ImageSendMessage

from bing.downloader import download_wallpaper, wallpaper_exist, local_wallpaper
from message_template import button_info

ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(ACCESS_TOKEN)

class Reply(Event):
    def __init__(self, event):
        self.event = event
        self.profile = line_bot_api.get_profile(event.source.user_id)

    def reply_text(self):
        replied = False
        message = self.event.message.text #message from user
        if any(keyword in message for keyword in ['wallpaper']):
            if not wallpaper_exist():
                download_wallpaper()
            msgObj = ImageSendMessage(local_wallpaper())
            self.reply(msgObj)
            replied = True
        
        if not replied:
            msgObj = TextSendMessage(text="Invalid command")
            self.reply(msgObj)
            stkObj = StickerSendMessage(package_id=2,sticker_id=153)
            self.push(stkObj)

    def reply_sticker(self):
        stkObj = StickerSendMessage(package_id=2,sticker_id=144)
        line_bot_api.reply_message(self.event.reply_token,stkObj)

    def reply_join(self):
        group_id = self.event.source.group_id
        line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(text="Bot not available for group"))
        reply_msg = "If you would like to use the bot, add the bot to friend with QR code first" + os.environ.get('LINE')
        line_bot_api.push_message(group_id, TextSendMessage(text=reply_msg))
        url_code = os.environ.get('QRCODE')
        line_bot_api.push_message(group_id, ImageSendMessage(url_code, url_code))
        line_bot_api.leave_group(group_id)

    def reply_follow(self):
        profile = line_bot_api.get_profile(self.event.source.user_id)
        greeting_msg = "Hi {0}, I can send you the bing wallpaper today".format(profile.display_name)
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage(text=greeting_msg))
        # line_bot_api.push_message(profile.user_id, button_info)

    def push(self, msg):
        line_bot_api.push_message(self.profile.user_id, msg)

    
    def reply(self, msg):
        line_bot_api.reply_message(self.event.reply_token, msg)