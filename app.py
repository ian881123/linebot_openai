# 引入 Flask 框架和相關模組
from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import os
import openai
from openai import OpenAI
import tempfile
import datetime
import time
import string
from fine_tune import GPT_response # 從 fine_tune 模組中引入 GPT_response 函數


# 建立 Flask 應用程式實例
app = Flask(__name__, template_folder='templates')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


# 設定 Line Bot API 通訊金鑰
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))


# 設定 Line Bot Webhook 金鑰
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 初始化 OpenAI API 金鑰
client = OpenAI() 


# 定義應用程式首頁路由
@app.route("/")
def index():
    return render_template("./index.html")


# 定義 Line Bot 的 Webhook 路由，接收 POST 請求
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭的值
    signature = request.headers['X-Line-Signature']
    # 獲取請求正文作為文本
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 處理 Webhook 正文
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理 Line Bot 的訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    # 在這裡呼叫 GPT_response 函數處理用戶的訊息
    GPT_answer = GPT_response(msg)
    print(GPT_answer)

    # 回復用戶訊息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))


# 如果是主程序，啟動 Flask 應用程式
if __name__ == "__main__":
    # 獲取應用程式運行的端口號
    port = int(os.environ.get('PORT', 5000))
    # 在 0.0.0.0 地址上運行應用程式
    app.run(host='0.0.0.0', port=port)
