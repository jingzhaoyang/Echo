#! /Users/Cai/.virtualenvs/ENV/bin/python
#encoding:utf-8
import pyaudio
import wave
import base64
import requests
import json
import sys
import os
import time
import re
import auto_record
#import vlc
from urllib import quote
from config import *
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Token(object):
    """docstring for Token"""
    def __init__(self):
        super(Token, self).__init__()

    def read_token(self):
        token_file=""
        try:
            token_file = open(".token","r")
        except Exception,e:
            self.update_token()
            token_file = open(".token","r")
        token=token_file.readlines()
        if len(token)==0 :
            self.update_token()
            return
        token_file.close()
        return token

    def update_token(self):
        token_file = open("./.token","w")
        token_file.write(self.get_token())
        token_file.close()

    def get_token(self):
        s = requests.session()
        url='https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_KEY+'&client_secret='+SECRET_KEY
        r=s.post(url)
        return json.loads(r.text).get('access_token')

TOKEN = Token().read_token()[0]


def baiduASR():
    vf = open(WAVE_OUTPUT_FILENAME,'rb')
    voice=vf.read()
    length = len(voice)
    speech = base64.b64encode(voice)
    vf.close()

    data ={
        "format":"pcm",
        "rate":8000,
        "channel":1,
        "token": TOKEN,
        "cuid":"aaaaaaaaaaaaa",
        "len":length,
        "speech": speech
    }
    #print data
    requrl = "http://vop.baidu.com/server_api"
    # header={"Content-Type":"application/json"}

    s = requests.session()
    s.headers['Content-Type']="application/json"
    r=s.post(requrl,data=json.dumps(data))

    result=json.loads(r.text)
    if result.get("err_msg") ==  "success." :
        return result.get("result")[0]
    elif "authentication failed." == result.get("err_msg"):
        Token().update_token()
        return  "ERROR:",result.get("err_msg")
    elif result.get("err_msg") == "recognition error." :
        return result.get("err_msg")
    else:
        Token().update_token()
        return None

def baiduTTS(content):
    url = "http://tsn.baidu.com/text2audio"
    data = {
            "tex": quote(content.encode('utf8')),
            "lan": "zh",
            "tok": TOKEN,
            "ctp": "1",
            "cuid": "aaaaaaaaaaaaa",
            "per":"4"
        }
    r = requests.post(url = url, data=data, stream=True)
    if r.headers['Content-type'] == "audio/mp3":
        with open(BAIDU_TTS_MP3, "wb") as answerFile:
            answerFile.write(r.content)
        return True
    else:
        result=json.loads(r.text)
        if "502" == result.get("err_no"):
            Token().update_token()
        return False

def AskTuling(tuling_api, tuling_key, content):
    if content:
        try:
            data = {
                "key":tuling_key,
                "info":content,
                "userid":"12345678"
            }

            result = requests.post(url = tuling_api, data=data)
            result = json.loads(result.text)
            if result["code"] == 100000:
                reply_text = result["text"]
            elif result["code"] == 200000:
                reply_text = '''%s''' % (result["text"])
            elif result["code"] == 302000:
                reply_text = "%s:" % result["text"]
                for i in result["list"]:
                    reply_text = reply_text + '''%s''' % (i["article"])
            else:
                reply_text = "这个问题太复杂了，我也不知道啊"
        except:
            reply_text = "我累了，要罢工！"
    else:
        print "识别错误"
        reply_text = '对不起我没有听清，请再说一遍'
    reply_text = re.sub("<br>", " ", reply_text)
    print "回答：%s" % reply_text
    return reply_text

def play_mp3(filename):
    p = vlc.MediaPlayer(filename)
    p.play()
    while True:
        time.sleep(1)
        if p.is_playing() == 0:
            break



if __name__ == '__main__':
    while True:
        auto_record.record_to_file(WAVE_OUTPUT_FILENAME)
        voice_text = baiduASR()
        print 'voice_text:', voice_text
        answer_text = AskTuling(TULING_API, TULING_KEY, voice_text)
        if baiduTTS(answer_text):
            os.system("cvlc --play-and-exit %s" % BAIDU_TTS_MP3)
