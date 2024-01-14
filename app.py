#載入LineBot所需要的模組 
from flask import Flask, request, abort  
from linebot import (
    LineBotApi, WebhookHandler
 ) 
from linebot.exceptions import (
    InvalidSignatureError
 ) 
from linebot.models import *

app = Flask(__name__)  
# 必須放上自己的Channel Access Token 
line_bot_api = LineBotApi('你自己的token')  
# 必須放上自己的Channel Secret
handler = WebhookHandler('你自己的secret')
