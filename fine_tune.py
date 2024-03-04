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
os.system('curl -o 1.json -L https://raw.githubusercontent.com/ian881123/linebot_openai/master/1.json')

# 定義客戶端
client = OpenAI() 

# 創建 fine-tune 文件
client.files.create(
  file=open("1.json", "rb"),
  purpose='fine-tune'
)
