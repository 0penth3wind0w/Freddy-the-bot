# encoding: utf-8
import os

from flask import Flask, request, abort, send_file, redirect
from linebot.exceptions import InvalidSignatureError

from linewrapper.handler import handler
from linewrapper.push import Push
from bing.wploader import get_wp_url

MAGIC_MESSAGE = os.environ.get('MAGIC_MESSAGE')
MAGIC_PASSPHRASE = os.environ.get('MAGIC_PASSPHRASE')
MAGIC_UID = os.environ.get('MAGIC_UID')

app = Flask(__name__)

# Redirect to Github
@app.route('/')
def index():
    return redirect("https://www.github.com/0penth3wind0w", code=302)

# Static file
@app.route('/image/carousel')
def get_carousel_img():
    filename = 'image/carousel.jpg'
    return send_file(filename, mimetype='image/jpeg')

@app.route('/image/QRcode')
def get_qrcode_img():
    filename = 'image/QRcode.png'
    return send_file(filename, mimetype='image/png')

@app.route('/image/wallpaper/<image_name>/')
def get_wallpaper(image_name):
    filename = 'image/wallpaper/{0}.jpg'.format(image_name)
    return send_file(filename, mimetype='image/jpeg')

# Line reply
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route("/deliver", methods=['POST'])
def deliver():
    data = request.json
    if data["message"] == MAGIC_MESSAGE and data["passphrase"] == MAGIC_PASSPHRASE:
        push_instance = Push(MAGIC_UID)
        wp_url = get_wp_url()
        push_instance.push_image(wp_url)
        push_instance.push_text(wp_url)
    else:
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])