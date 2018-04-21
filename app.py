# encoding: utf-8
import os
import requests
from flask import Flask, request, abort
import random
import re
import regex as r

# LINE
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	Event, MessageEvent,
	TextMessage, TextSendMessage,
	StickerMessage, StickerSendMessage,
	FileMessage, FollowEvent,
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
# Reply to text message
@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
	Reply(event).reply_to_usr()

# Greeting messages when user add this bot
@handler.add(FollowEvent)
def handle_follow(event):
	profile = line_bot_api.get_profile(event.source.user_id)
	greeting_msg = profile.display_name+"你好～我是自我介紹機器人Freddy，很高興認識你\n請問你想之知道什麼呢？"
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=greeting_msg))
	#line_bot_api.push_message(profile.user_id,)
# ================= BOT End =================

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=os.environ['PORT'])

class Reply(Event):
	def __init__(self, event=None):
		self.event = event
		self.profile = line_bot_api.get_profile(event.source.user_id)
	def reply_to_usr(self):
		replied = False
		msg = self.event.message.text #message from user
		if bool(re.match("[(hi)|(Hello)|(你好)|(嗨)|(哈囉)]", msg)):
			msgs = ['hi', 'Hello', "你好", "嗨", "哈囉"]
			reply_msg = random.choice(msgs) + "～"
			msgObj = TextSendMessage(text=reply_msg)
			self.reply(msgObj)
			replied = True
		if bool(re.search("[學歷|學校|就讀|大學|研究所]", msg)):
			reply_msg = "我目前就讀於北科大的資訊工程系研究所\n大學則是就讀國立臺北大學，主修資訊工程，並雙主修金融與合作經營。"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if bool(re.search("[工作|實習]", msg)):
			reply_msg = "大學的寒暑假時，我曾經去巨司文化（數位時代、經理人）實習。實習的時候主要負責網站的維護"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if bool(re.search("[程式.語言|語言.程式|用.語言]", msg)):
			reply_msg = "我會的程式語言有C/C++,Python\n也曾經接觸過一點點的Ruby on Rails和JavaScript喔"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if bool(re.search("[履歷|簡歷|自傳]", msg)):
			reply_msg = "等我一下喔～我把我的自傳傳給你，裡面有更多詳細的資料唷"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if not replied:
			reply_msg = "對不起，我現在還不會回答這個問題\nQ_Q"
			msgObj = TextSendMessage(text=reply_msg)
			self.reply(msgObj)
			stkObj = StickerSendMessage(package_id=2,sticker_id=153)
			self.push(stkObj)
	def push(self, msg):
		line_bot_api.push_message(
				self.profile.user_id,
				msg)
	def reply(self, msg):
		line_bot_api.reply_message(
				self.event.reply_token,
				msg)