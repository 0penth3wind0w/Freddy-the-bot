import os

from linebot import WebhookHandler
from linebot.models import (MessageEvent, FollowEvent, JoinEvent,
                            TextMessage, StickerMessage,)

from reply_handler import Reply

SECRET = os.environ.get('CHANNEL_SECRET')

handler = WebhookHandler(SECRET)

# Reply to message
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    Reply(event).reply_text()

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    Reply(event).reply_sticker()

# Greeting messages
@handler.add(FollowEvent)
def handle_follow(event):
    Reply(event).reply_follow()

@handler.add(JoinEvent)
def handle_join(event):
    Reply(event).reply_join()