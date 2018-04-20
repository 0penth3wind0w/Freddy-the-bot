# encoding: utf-8
import os
import requests
from flask import Flask, request, abort
from response import response

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage, FollowEvent,
)

ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
SECRET = os.environ.get('CHANNEL_SECRET')

app = Flask(__name__)

handler = WebhookHandler(SECRET) 
line_bot_api = LineBotApi(ACCESS_TOKEN) 

@app.route('/')
def index():
	return "<p>Hello World!</p>"

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'

# ================= Bot Start =================
@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
	msg = event.message.text #message from user
	reply_msg = response(msg)
	# 針對使用者各種訊息的回覆 Start =========
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=reply_msg))
	# 針對使用者各種訊息的回覆 End =========

@handler.add(FollowEvent)
def handle_follow(event):
	profile = line_bot_api.get_profile(event.source.user_id)
	greeting_msg = profile.display_name+"你好～我是彥霖的自我介紹機器人，很高興認識你(blush)\n請問你想之知道什麼呢？"
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=greeting_msg))
# ================= BOT End =================

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=os.environ['PORT'])
