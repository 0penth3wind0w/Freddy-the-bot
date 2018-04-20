# encoding: utf-8
import os
import requests
from flask import Flask, request, abort

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
	profile = line_bot_api.get_profile(event.source.userID
	# 針對使用者各種訊息的回覆 Start =========
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=msg))
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=profile.displayName))
	# 針對使用者各種訊息的回覆 End =========

@handler.add(FollowEvent)
def handle_follow(event):
	#profile = line_bot_api.get_profile(event.source.userId)
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text='Got follow event'))
# ================= BOT End =================

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=os.environ['PORT'])
