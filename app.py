from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

# 從環境變數讀取
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/")
def home():
    return "Line Bot on Render!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 你原本的運算
    i = "95864152Uu"
    a = int(int(i[0:4]) * 7 / 2 + 94 / 3)  # 4位亂數
    b = int(int(i[4:8]) * 9 / 6 + 83 / 1.5)  # 4位亂數
    c = chr(int(ord(i[8]) * 4 / 6 + 25))  # 65~90
    d = chr(int(ord(i[9]) * 1.5 / 1.3 - 17))  # 100~120
    message = str(a) + str(b) + c + d

    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你的結果是：{message}")
    )

if __name__ == "__main__":
    app.run()
