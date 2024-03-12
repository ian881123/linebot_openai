# 引入所需的模組
from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import os
import openai
import requests
from openai import OpenAI
import tempfile
import datetime
import time
import string

# 安裝或升級 openai 庫
os.system('pip install openai --upgrade')

# 定義客戶端
client = OpenAI() 

# 定義函數 GPT_response，接收文字並使用 fine-tuned 模型生成回應
def GPT_response(text):
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:rocmacis::91rwvDZ4",
        messages=[
            {"role": "system", "content": "你扮演一名陸軍軍官學校的客服"},
            {"role": "user", "content": text}
        ],
        temperature=0.5,
        max_tokens=256,
    )

    answer = response.choices[0].message.content

    # 去除回复文本中的標點符號
    answer = answer.translate(str.maketrans('', '', string.punctuation))

    return answer
