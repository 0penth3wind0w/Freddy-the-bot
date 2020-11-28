import os
from linebot.models import TemplateSendMessage, ButtonsTemplate, URITemplateAction, MessageTemplateAction

CAROUSEL = os.environ.get('BASE_ROUTE') + '/image/caousel.jpg'

button_info = TemplateSendMessage(
    alt_text="使用說明",
    template=ButtonsTemplate(
        title="使用說明",
        text="請參考以下說明：",
        thumbnail_image_url=CAROUSEL,
        actions=[
            URITemplateAction(
                label='詳細功能介紹',
                uri='https://github.com/0penth3wind0w/Freddy-the-bot/blob/master/README.md'),
            MessageTemplateAction(
                label="使用範例",
                text="使用範例")])
)