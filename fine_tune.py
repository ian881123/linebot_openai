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
os.system('curl -o 6.5.json -L https://raw.githubusercontent.com/ian881123/linebot_openai/master/6.5.json')

# 定義客戶端
client = OpenAI() 

# 列出文件
client.files.list()

# 創建 fine-tuning 作業
client.fine_tuning.jobs.create(
  training_file="file-7n5Ofb1gV90R76SqVLthdsVs", 
  model="ft:gpt-3.5-turbo-0125:personal::8zQwGxZk", 
  hyperparameters={
    "n_epochs":7
  }
)

# 列出 fine-tuning 作業
client.fine_tuning.jobs.list(limit=10)

# 檢索 fine-tuning 作業事件
client.fine_tuning.jobs.retrieve("ftjob-65nHjhG639C3sChSephm8MXv")

# 列出 fine-tuning 作業事件
client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-65nHjhG639C3sChSephm8MXv", limit=10)

# 創建帶有 fine-tuned 模型的聊天完成
completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::8zQwGxZk",
  messages=[
    {"role": "system", "content": "你扮演一名陸軍軍官學校的客服"},
    {"role": "user", "content": "留讀的標準有哪些?"}
  ]
)

print(completion.choices[0].message.content)

# 定義函數 GPT_response，接收文字並使用 fine-tuned 模型生成回應
def GPT_response(text):
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::8zQwGxZk",
        messages=[
            {"role": "system", "content": "你扮演一名陸軍軍官學校的客服"},
            {"role": "user", "content": text}
        ]
    )

    answer = response.choices[0].message.content

    # 去除回复文本中的標點符號
    answer = answer.translate(str.maketrans('', '', string.punctuation))

    return answer
