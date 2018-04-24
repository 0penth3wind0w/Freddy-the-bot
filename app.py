# encoding: utf-8
import os
import requests
import wikipedia as wiki
from flask import Flask, request, abort, send_file, redirect
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

wiki.set_lang("zh-tw")

@app.route('/')
def index():
	return redirect("https://www.github.com/0penth3wind0w", code=302)
@app.route('/image/carousel')
def get_carousel_img():
	filename = 'image/carousel.jpg'
	return send_file(filename, mimetype='image/jpeg')
@app.route('/image/QRcode')
def get_qrcode_img():
	filename = 'image/QRcode.png'
	return send_file(filename, mimetype='image/png')
@app.route('/image/amp1')
def get_amp1_img():
	filename = 'image/amp1.jpg'
	return send_file(filename, mimetype='image/jpeg')
@app.route('/image/amp2')
def get_amp2_img():
	filename = 'image/amp2.jpg'
	return send_file(filename, mimetype='image/jpeg')
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
	line_bot_api.reply_message(event.reply_token,stkObj)

# Greeting messages when user add this bot
@handler.add(FollowEvent)
def handle_follow(event):
	profile = line_bot_api.get_profile(event.source.user_id)
	greeting_msg = profile.display_name+"您好～我是Freddy，很高興認識你\n請先試試看下面的功能吧"
	line_bot_api.reply_message(
		event.reply_token, TextSendMessage(text=greeting_msg))
	line_bot_api.push_message(profile.user_id, carousel_example)
	line_bot_api.push_message(profile.user_id, TextSendMessage(text="如果想要知道更詳細的說明也可以從下方點選喔"))

@handler.add(JoinEvent)
def handle_join(event):
	gid = event.source.group_id
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="大家好～很高興認識你們～"))
	reply_msg = "請大家先透過網址或行動條碼加我好友吧："+os.environ.get('LINE')
	line_bot_api.push_message(gid,TextSendMessage(text=reply_msg))
	url_code = os.environ.get('QRCODE')
	line_bot_api.push_message(gid,ImageSendMessage(
		original_content_url=url_code,
		preview_image_url=url_code))
	line_bot_api.push_message(gid, TextSendMessage(text="希望有機會可以在一對一聊天中看到大家囉\n掰掰～"))
	line_bot_api.leave_group(gid)
# ============ BOT Related Handler End ===============
# Template Message
url_carousel = reply_msg = os.environ.get('CAROUSEL')
button_info = TemplateSendMessage(
	alt_text="使用說明",
	template=ButtonsTemplate(
		title="使用說明",
		text="請參考以下說明：",
		thumbnail_image_url=url_carousel,
		actions=[
			URITemplateAction(
				label='詳細功能介紹',
				uri='https://github.com/0penth3wind0w/Freddy-the-bot/blob/master/README.md'),
			MessageTemplateAction(
				label="使用範例",
				text="使用範例")])
)

carousel_example = TemplateSendMessage(
	alt_text="範例問題",
	template=CarouselTemplate(
		columns=[
			CarouselColumn(
				thumbnail_image_url=url_carousel,
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
				thumbnail_image_url=url_carousel,
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
				thumbnail_image_url=url_carousel,
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
				thumbnail_image_url=url_carousel,
				title="功能介紹 - 興趣相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你的興趣是什麼呢？",
						text="你的興趣是什麼呢？"),
					MessageTemplateAction(
						label="說說你的興趣吧",
						text="說說你的興趣吧"),
					MessageTemplateAction(
						label="你有什麼興趣嗎？",
						text="你有什麼興趣嗎？"),]),
			CarouselColumn(
				thumbnail_image_url=url_carousel,
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

carousel_amp = TemplateSendMessage(
	alt_text="擴大機的照片",
	template=ImageCarouselTemplate(
		columns=[
			ImageCarouselColumn(
				image_url='https://self-promote-linebot.herokuapp.com/image/amp1',
				action=URITemplateAction(
					label="擴大機的照片",
					uri='https://self-promote-linebot.herokuapp.com/image/amp1')),
			ImageCarouselColumn(
				image_url='https://self-promote-linebot.herokuapp.com/image/amp2',
				action=URITemplateAction(
					label="擴大機的照片",
					uri='https://self-promote-linebot.herokuapp.com/image/amp2'))])
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
		if ("你是誰" in msg) or ("自我介紹" in msg) or (("簡" in msg) and ("介" in msg)):
			msgObj = TextSendMessage(text="我是Freddy。是一個個性沉穩的研究生。\n你可以透過問問題來認識我喔！")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("學歷" in msg) or ("學校" in msg) or ("就讀" in msg) or ("大學" in msg) or ("研究所" in msg):
			msgObj = TextSendMessage(text="我現在就讀於北科大的資訊工程研究所，目前是碩一研究生")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			msgObj = TextSendMessage(text="大學則是就讀國立臺北大學，主修資訊工程，另外還有雙主修金融與合作經營")
			self.push(msgObj)
			replied = True
		if ("工作" in msg) or ("實習" in msg):
			msgObj = TextSendMessage(text="我在大學的寒暑假時，曾去巨思文化（數位時代、經理人）實習。實習的時候主要負責網站的維護")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			msgObj = TextSendMessage(text="另外在大學時也有在通訊工程系的語音處理實驗室打工，主要是負責資料處理程式的撰寫喔")
			self.push(msgObj)
			replied = True
		if (("程式" in msg) or ("用" in msg)) and ("語言" in msg):
			msgObj = TextSendMessage(text="我最近常用的語言是Python\n其他會使用的語言有C/C++，也接觸過一點點的JavaScript和Ruby on Rails喔")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("興趣"in msg):
			msgObj = TextSendMessage(text="我的興趣是聽音樂跟DIY做一些有趣的東西。\n像是50音記憶的網頁跟耳機用的擴大機都是利用閒暇時間做出來的喔")
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			msgObj = TextSendMessage(text='http://0penth3wind0w.github.io/gojuon_game/')
			self.push(msgObj)
			self.push(carousel_amp)
			replied = True
		if ("履歷" in msg) or ("簡歷" in msg) or ("自傳" in msg) or ("開發經驗" in msg):
			msgObj = TextSendMessage(text="等我一下喔～我把我的自傳傳給你，裡面有程式開發經驗等更多詳細的資料唷")
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
		if ("Bye" in msg) or ("掰掰" in msg) or ("再見" in msg):
			msgs = ["Bye", "掰掰", "再見"]
			reply_msg = random.choice(msgs) + "～"
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if ("維基" in msg[0:2]):
			reply_msg = getWiki(msg[2:])
			msgObj = TextSendMessage(text=reply_msg)
			if replied:
				self.push(msgObj)
			else:
				self.reply(msgObj)
			replied = True
		if not replied:
			msgObj = TextSendMessage(text="對不起，我現在還不會回答這個問題...Q_Q")
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

# Experimental Function
def getWiki(str):
	try:
		return wiki.summary(str)
	except:
		return "抱歉，我沒有找到相關訊息喔"

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=os.environ['PORT'])