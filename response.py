from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage,
    FileMessage, FollowEvent,
)

def replyText(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    msg = event.message.text #message from user
    
    if ("學歷" or "學校" or "就讀") in msg:
        reply_msg = "我目前就讀於北科大的資訊工程系研究所\n大學則是就讀國立臺北大學，主修資訊工程，並雙主修金融與合作經營。"
        line_bot_api.push_message(
            profile.user_id,
            TextSendMessage(text=reply_msg))
    if ("工作" or "實習") in msg:
        reply_msg = "大學的寒暑假時，我曾經去巨司文化（數位時代、經理人）實習。實習的時候主要負責網站的維護"()
        line_bot_api.push_message(
            profile.user_id,
            TextSendMessage(text=reply_msg)
        )
    if (("程式" and "語言") or ("用" and "語言")) in msg:
        reply_msg = "我會的程式語言有C/C++,Python\n也曾經接觸過一點點的Ruby on Rails和JavaScript喔"
        line_bot_api.push_message(
            profile.user_id,
            TextSendMessage(text=reply_msg)
        )
    if ("履歷" or "簡歷" or "自傳") in msg:
        reply_msg = "等我一下喔～我把我的自傳傳給你，裡面有更多詳細的資料唷"
        line_bot_api.push_message(
            profile.user_id,
            TextSendMessage(text=reply_msg)
        )
    else:
        reply_msg = "Sorry"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))