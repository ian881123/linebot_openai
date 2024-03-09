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

# 使用 curl 下載 rocma_qa.json 文件
os.system('curl -o 7.5.json -L https://raw.githubusercontent.com/ian881123/linebot_openai/master/7.5.json')


# 定義客戶端
client = OpenAI() 


# 創建 fine-tune 文件
client.files.create(
  file=open("7.5.json", "rb"),
  purpose='fine-tune'
)

# 定義函數 GPT_response，接收文字並使用 fine-tuned 模型生成回應
def GPT_response(text):
    GPT_response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::8zch08k3",
        messages=[
            {"role": "system", "content": "你扮演一名陸軍軍官學校的客服"},
            {"role": "user", "content": text}
        ],
        temperature=0.5,
        max_tokens=500,
    )

    answer = GPT_response.choices[0].message.content

  
    # 去除回复文本中的標點符號
    answer = answer.translate(str.maketrans('', '', string.punctuation))

    return answer
