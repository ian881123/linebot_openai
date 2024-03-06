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


# 創建帶有 fine-tuned 模型的聊天完成
completion2 = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::8zch08k3",
  messages=[
    {"role": "system", "content": "你扮演一名陸軍軍官學校的客服"},
    {"role": "user", "content": "枕頭與棉被之間的間距規定為?"}
  ]
)

print(completion2.choices[0].message.content)


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
