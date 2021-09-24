import os

from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent, FollowEvent, JoinEvent,
                            TextMessage, StickerMessage,)

ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(ACCESS_TOKEN)

from .reply import Reply
from .push import Push
from bing.wploader import get_wp_url

SECRET = os.environ.get('CHANNEL_SECRET')
handler = WebhookHandler(SECRET)

# Reply to message
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    reply_instance = Reply(event.reply_token)
    push_instance = Push(event.source.user_id)
    replied = False
    message = event.message.text.lower() #message from user
    if 'wallpaper' in message:
        wallpaper_url = get_wp_url()
        reply_instance.reply_image(wallpaper_url)
        push_instance.push_text(wallpaper_url)
        replied = True
    if not replied:
        reply_instance.reply_text("Invalid command")
        push_instance.push_sticker(sticker_package=2, sticker_id=149)
    
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    Reply(event.reply_token).reply_sticker(sticker_package=2, sticker_id=144)

# Greeting messages
@handler.add(FollowEvent)
def handle_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    greeting_msg = "Hi {0}, I can send you the bing wallpaper today".format(profile.display_name)
    Reply(event.reply_token).reply_text(greeting_msg)

@handler.add(JoinEvent)
def handle_join(event):
    group_id = event.source.group_id
    Reply(event.reply_token).reply_text("Bot not available for group")
    push_msg = "If you would like to use the bot, add the bot to friend with QR code first" + os.environ.get('LINE')
    push_instance = Push(group_id)
    push_instance.push_text(push_msg)
    url_code = os.environ.get('QRCODE')
    push_instance.push_image(url_code)
    line_bot_api.leave_group(group_id)
