from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/")
def home():
    return "Line Bot is running."

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
    i = event.message.text.strip()

    if len(i) != 10:
        reply = "請輸入剛好10個字元的字串。"
    else:
        try:
            a = int(int(i[0:4]) * 7 / 2 + 94 / 3)  # 4位亂數
            b = int(int(i[4:8]) * 9 / 6 + 83 / 1.5)  # 4位亂數
            c = chr(int(ord(i[8]) * 4 / 6 + 25))  # 65~90
            d = chr(int(ord(i[9]) * 1.5 / 1.3 - 17))  # 100~120
            message = str(a) + str(b) + c + d
            reply = f"{message}"
        except Exception as e:
            reply = f"輸入格式錯誤或無法計算：{e}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
