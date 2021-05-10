"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from dingding_robot import app,config,execjar
from flask import request
import requests
import json
import time
import hmac
import hashlib
import base64
from multiprocessing import Process,Manager

fields = ["password","key","secret","token"]


def sign_verfiy(timestamp,dingding_sign):
    """签名验证"""
    sys_timestamp = int(time.time())
    app_secret = config.AppSecret
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    print("my_sign: ",sign)
    print("dingding_sign: ",dingding_sign)
    if sign == dingding_sign:
        return True
    else:
        return False
    


def parse_data(data):
    data = json.loads(data)
    sessionWebhook = data.get("sessionWebhook")
    senderNick = data.get("senderNick")
    send_dingding(senderNick,sessionWebhook)

def send_dingding(msg, sessionWebhook):    
    webhook = sessionWebhook   

    headers = {'Content-Type': 'application/json',
               }
    data={ "msgtype": "text", "text": { "content": "hello," + msg } }
    
    r = requests.post(url=webhook,data=json.dumps(data),headers=headers)
    print("-------------------------------")
    if r.json().get("errcode") == 0:        
        print("dingding通知发送成功:",r.text)
    else:        
        print("dingding通知发送失败:",r.text)


@app.route('/',methods=['GET','POST'])
@app.route('/dingding_robot',methods=['GET','POST'])
def dingding_robot():
    
    timestamp = request.headers.get('timestamp')
    dingding_sign = request.headers.get('sign')
    
    if sign_verfiy(timestamp,dingding_sign):
        data = request.get_data()
        parse_data(data)
    else:
        return '{"status":"403"}',403


@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/encrypt')
def encrypt():
    """Renders the encrypt page."""
    data = 1
    return render_template(
        'encryptYaml.html',
        year=datetime.now().year,
        fields = ",".join(fields)

    )

@app.route('/e',methods=['POST'])
def e():
    #print("api start time:",time.asctime( time.localtime(time.time()) ))
    
    manager = Manager()
    return_dict = manager.dict()
    
    env = request.form.get("env")
    encrypt_data = request.form.get("encrypt_data")
    print("------------env is:",env)
    encrypt_data = encrypt_data.split("\n")
    num = 0
    jobs = []
    encrypt_field = ""

    for data in encrypt_data:        
        for field in fields:            
            if field in data:                
                try:
                    encrypt_field = data.split(":")[1].strip()
                    #edata = "ENC(" + execjar.encrypt("rc",encrypt_field) + ")"
                    process = Process(target=execjar.encrypt,args=(env,encrypt_field,return_dict,num))
                    jobs.append(process)
                    process.start()
                    #print(edata)
                except Exception as e :
                    print("field parse ERROR:",data,e)
                break
        num += 1

    for proc in jobs:        
        proc.join()
    if return_dict:
        for k,v in return_dict.items():
            print(encrypt_data[k])
            encrypt_data[k] = encrypt_data[k].replace(v[0],"ENC(" + v[1] + ")")
        print(return_dict)
        print(encrypt_data)
        encrypt_data = "\n".join(encrypt_data)
        return encrypt_data,200
    else:
        encrypt_data = "\n".join(encrypt_data)
        return "没有需要加密的字段\n\n" + encrypt_data ,200

    

@app.route('/d',methods=['POST'])
def d():
    """Renders the decrypt page."""
    return "未完成。"

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )



