# encoding: utf-8
import os
import requests
from flask import Flask, request, abort, send_file
import random

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

@app.route('/image')
def get_image():
	filename = 'image/carousel.jpg'
	return send_file(filename, mimetype='image/jpg')

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

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
	stkObj = StickerSendMessage(package_id=2,sticker_id=144)
	decide = [True, False]
	if decide:
		line_bot_api.reply_message(
		event.reply_token,
		stkObj)

# Greeting messages when user add this bot
@handler.add(FollowEvent)
def handle_follow(event):
	profile = line_bot_api.get_profile(event.source.user_id)
	greeting_msg = profile.display_name+"你好～我是自我介紹機器人Freddy，很高興認識你\n請先試試看各項功能吧"
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
# Template Message
button_info = TemplateSendMessage(
	alt_text="使用說明",
	template=ButtonsTemplate(
		title="使用說明",
		text="請參考以下說明：",
		thumbnail_image_url='https://self-promote-linebot.herokuapp.com/image',
		actions=[
			MessageTemplateAction(
				label="使用範例",
				text="使用範例"),
			URITemplateAction(
				label='功能介紹',
				uri='https://github.com/0penth3wind0w'),
			MessageTemplateAction(
				label="聯絡方式",
				text="聯絡方式")])
)

carousel_example = TemplateSendMessage(
	alt_text="範例問題",
	template=CarouselTemplate(
		columns=[
			CarouselColumn(
				thumbnail_image_url='https://self-promote-linebot.herokuapp.com/image',
				title="功能介紹 - 實習相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你有實習的經驗嗎？",
						text="你有實習的經驗嗎？"),
					MessageTemplateAction(
						label="說說你的實習經驗吧",
						text="說說你的實習經驗吧"),
					MessageTemplateAction(
						label="你有相關的工作經驗嗎？",
						text="你有相關的工作經驗嗎？"),]),
			CarouselColumn(
				thumbnail_image_url='https://self-promote-linebot.herokuapp.com/image',
				title="功能介紹 - 學歷相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你目前就讀那間學校呢？",
						text="你目前就讀那間學校呢？"),
					MessageTemplateAction(
						label="說說你的學歷吧",
						text="說說你的學歷吧"),
					MessageTemplateAction(
						label="你畢業於哪一所學校呢？",
						text="你畢業於哪一所學校呢？"),]),
			CarouselColumn(
				thumbnail_image_url='https://self-promote-linebot.herokuapp.com/image',
				title="功能介紹 - 程式語言相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你會使用哪些程式語言呢？",
						text="你會使用哪些程式語言呢？"),
					MessageTemplateAction(
						label="說說你會用的語言吧",
						text="說說你會用的語言吧"),
					MessageTemplateAction(
						label="你都用什麼語言寫程式？",
						text="你都用什麼語言寫程式？"),]),
			CarouselColumn(
				thumbnail_image_url='https://self-promote-linebot.herokuapp.com/image',
				title="功能介紹 - 履歷相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="可以看看你的履歷嗎？",
						text="可以看看你的履歷嗎？"),
					MessageTemplateAction(
						label="可以提供自傳相關資料嗎？",
						text="可以提供自傳相關資料嗎？"),
					MessageTemplateAction(
						label="有沒有提供簡歷呢？",
						text="有沒有提供簡歷呢？"),])])
)

# Use to reply users
class Reply(Event):
	def __init__(self, event=None):
		self.event = event
		self.profile = line_bot_api.get_profile(event.source.user_id)
	def reply_to_usr(self):
		replied = False
		msg = self.event.message.text #message from user
		if ("Hi" in msg) or ("Hello" in msg) or ("你好" in msg) or ("嗨" in msg) or ("哈囉" in msg):
			msgs = ["Hi", "Hello", "你好", "嗨", "哈囉"]
			reply_msg = random.choice(msgs) + "～"
			msgObj = TextSendMessage(text=reply_msg)
			self.reply(msgObj)
			replied = True
		if ("Bye" in msg) or ("掰掰" in msg) or ("再見" in msg):
			msgs = ["Bye", "掰掰", "再見"]
			reply_msg = random.choice(msgs) + "～"
			msgObj = TextSendMessage(text=reply_msg)
			self.reply(msgObj)
			replied = True
		if ("學歷" in msg) or ("學校" in msg) or ("就讀" in msg) or ("大學" in msg) or ("研究所" in msg):
			msgObj = TextSendMessage(text="我目前就讀於北科大的資訊工程系研究所\n大學則是就讀國立臺北大學，主修資訊工程，並雙主修金融與合作經營。")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("工作" in msg) or ("實習" in msg):
			msgObj = TextSendMessage(text="大學的寒暑假時，我曾經去巨司文化（數位時代、經理人）實習。實習的時候主要負責網站的維護")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if (("程式" in msg) or ("用" in msg)) and ("語言" in msg):
			msgObj = TextSendMessage(text="我最近常用的語言是Python\n其他會使用的語言有C/C++，也接觸過一點點的Ruby on Rails和JavaScript喔")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("履歷" in msg) or ("簡歷" in msg) or ("自傳" in msg):
			msgObj = TextSendMessage(text="等我一下喔～我把我的自傳傳給你，裡面有更多詳細的資料唷")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			reply_msg = os.environ.get('RESUME')
			msgObj = TextSendMessage(text=reply_msg)
			self.push(msgObj)
			replied = True
		if ("使用"in msg) and (("說明"in msg) or ("方式"in msg)):
			if replied:
				self.push(button_info)
			else:
				self.reply(button_info)
			replied = True
		if ("範例" in msg):
			if replied:
				self.push(carousel_example)
			else:
				self.reply(carousel_example)
			replied = True
		if ("聯絡" in msg):
			msgObj = TextSendMessage(text="你可以透過這個email聯絡我喔")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			reply_msg = os.environ.get('CONTACT_INFO')
			msgObj = TextSendMessage(text=reply_msg)
			self.push(msgObj)
			replied = True
		if not replied:
			msgObj = TextSendMessage(text="對不起，我現在還不會回答這個問題...\nQ_Q")
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

# Rich Menu
'''rich_menu = RichMenu(
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
rich_menu_id = line_bot_api.create_rich_menu(data=rich_menu)
'''
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=os.environ['PORT'])