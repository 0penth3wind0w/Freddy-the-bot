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
from linebot.models import *

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

# ============ Bot Related Handler Start ============
# Reply to text message
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
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

@handler.add(JoinEvent)
def handle_join(event):
	profile = line_bot_api.get_profile(event.source.group_id)
	greeting_msg = profile.display_name+"大家好～我是自我介紹機器人Freddy請大家趕快加我好友吧"
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=greeting_msg))
# ============ BOT Related Handler End ===============
#Button Template
button = TemplateSendMessage(
	alt_text='目錄 template',
	template=ButtonsTemplate(
		title='選擇服務',
		text='請選擇',
		thumbnail_image_url='https://i.imgur.com/kzi5kKy.jpg',
		actions=[
			MessageTemplateAction(
				label='開始玩',
				text='開始玩'),
			URITemplateAction(
				label='影片介紹 阿肥bot',
				uri='https://youtu.be/1IxtWgWxtlE'),
			URITemplateAction(
				label='如何建立自己的 Line Bot',
				uri='https://github.com/twtrubiks/line-bot-tutorial'),
			URITemplateAction(
				label='聯絡作者',
				uri='https://www.facebook.com/TWTRubiks?ref=bookmarks')])
)
# Rich Menu
'''rich_menu_to_create = RichMenu(
	size=RichMenuBound(
		width=2500,
		height=1686),
	selected= False,
	name="nice richmenu",
	chatBarText="touch me",
	areas=[
		RichMenuArea(
			RichMenuBound(
				x=0,y=0,
				width=2500,
				height=1686),
			URITemplateAction(
				uri='line://nv/location'))]
)
rich_menu_id = line_bot_api.create_rich_menu(data=rich_menu_to_create)
'''
# Use to reply users
class Reply(Event):
	def __init__(self, event=None):
		self.event = event
		self.profile = line_bot_api.get_profile(event.source.user_id)
	def reply_to_usr(self):
		replied = False
		msg = self.event.message.text #message from user
		if ("Hi" in msg) or ("Hello" in msg) or ("你好" in msg) or ("嗨" in msg) or ("哈囉" in msg):
			msgs = ["hi", "Hello", "你好", "嗨", "哈囉"]
			reply_msg = random.choice(msgs) + "～"
			msgObj = TextSendMessage(text=reply_msg)
			self.reply(msgObj)
			replied = True
		if ("Hi" in msg) or ("學歷" in msg) or ("學校" in msg) or ("就讀" in msg) or ("大學" in msg) or ("研究所" in msg):
			reply_msg = "我目前就讀於北科大的資訊工程系研究所\n大學則是就讀國立臺北大學，主修資訊工程，並雙主修金融與合作經營。"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("工作" in msg) or ("實習" in msg):
			reply_msg = "大學的寒暑假時，我曾經去巨司文化（數位時代、經理人）實習。實習的時候主要負責網站的維護"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if (("程式" in msg) or ("用" in msg)) and ("語言" in msg):
			reply_msg = "我會的程式語言有C/C++,Python\n也曾經接觸過一點點的Ruby on Rails和JavaScript喔"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("履歷" in msg) or ("簡歷" in msg) or ("自傳" in msg):
			reply_msg = "等我一下喔～我把我的自傳傳給你，裡面有更多詳細的資料唷"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			reply_msg = "https://goo.gl/nDL4eQ"
			msgObj = TextSendMessage(text=reply_msg)
			self.push(msgObj)
			replied = True
		if ("使用說明" in msg) or ("如何使用" in msg):
			msgObj = button
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

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=os.environ['PORT'])