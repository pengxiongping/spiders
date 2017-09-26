import hashlib
import requests
from lxml import etree

header = {
        'Host':'passport.lagou.com',
        'Origin':'https://passport.lagou.com',
        'Referer':'https://passport.lagou.com/login/login.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
        }
session = requests.session()
def encryption(data):
    h = hashlib.md5(data.encode('utf-8')).hexdigest()
    c = 'veenike'+h+'veenike'
    passwords = hashlib.md5(c.encode('utf-8')).hexdigest()
    print(passwords)
    return passwords

def gettoken():
    url = 'https://passport.lagou.com/login/login.html'
    content = session.get(url,headers=header,timeout = 30).text
    selector = etree.HTML(content)
    js = selector.xpath("//script[@type='text/javascript']/text()")[1]
    anti_token = {'X-Anit-Forge-Token' : 'None', 'X-Anit-Forge-Code' : '0'}
    anti_token['X-Anit-Forge-Token'], anti_token['X-Anit-Forge-Code'] = map(
        lambda x:
            x.split('=')[1].strip(' \';\n')
        ,
        js.split(';',1)
    )
    return anti_token
    # {'X-Anit-Forge-Token': '3f57c395-c11d-44fc-baf2-e4257cac4ccd', 'X-Anit-Forge-Code': '95844130'}

def login(account,password):
    password = encryption(password)
    anti_token = gettoken()
    login_header=header.copy()
    login_header.update(anti_token)
    post_data = {
        'isValidate':'true',
        'username':account,
        'password':password,
        'request_form_verifyCode':'',
        'submit':'',
        }
    url = 'https://passport.lagou.com/login/login.json'
    r = session.post(url,headers = login_header,data=post_data)
    print(r.text)

if __name__ == '__main__':
    account = input("请输入您的账号：")
    password = input("请输入您的密码：")
    login(account,password)