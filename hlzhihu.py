# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:18:09 2017

@author: 10192072

python2.7
"""

import requests
import cookielib
import time
import re
from PIL import Image


headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
}

def get_xsrf():
    url = 'http://www.zhihu.com'
    r = requests.get(url, headers=headers)
    #pattern = re.compile(r'name="_xsrf" value="(.*?)"')
    pattern = r'name="_xsrf" value="(.*?)"'
    return re.findall(pattern, r.text)[0]

def get_captcha(session):
    url = 'https://www.zhihu.com/captcha.gif?r=' + str(int(time.time()*1000+100)) + "&type=login"
    r = session.get(url, headers=headers)
    with open('captcha.jpg','wb') as f:
        f.write(r.content)
        f.close()
    im = Image.open('captcha.jpg')
    im.show()
    im.close()
    return raw_input('请输入验证码: ')

def load_cookie():
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='testcookies')
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print "没有cookier文件"
    return session
    
def is_login(session):
    url = 'https://www.zhihu.com/settings/profile'
    return session.get(url,headers=headers,allow_redirects=False).status_code == 200

def login():
    session = load_cookie()
    if not is_login(session):
        url = 'https://www.zhihu.com/login/phone_num'
        data={
            '_xsrf': get_xsrf(),
            'phone_num': '17715249146',
            'password': 'ty123456hl'
        }
        headers["X-Xsrftoken"] = data['_xsrf']
        headers["X-Requested-With"] = "XMLHttpRequest"
        r = session.post(url,data=data,headers=headers)
        if r.json()['r'] == 1:
            print '需要验证码'
            data['captcha'] = get_captcha(session)
            r = session.post(url,data=data,headers=headers)
        else:
            print '无验证码登录成功'
        print r.json()['msg']
        session.cookies.save('testcookies')
    else:
        print 'session默认登录'
        
if __name__ == '__main__':
    login()
        
    
