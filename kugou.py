​
import requests
import re
import time
from bs4 import BeautifulSoup
import gradio as gr
import numpy as np
cookie = {}
with open("cookie.txt", "r") as f: # 请先创建包含有cookie的文本文档(直接复制hearder的内容)
    c = f.read().split("; ")
    for i in c:
        d = i.split("=")
        cookie[d[0]] = i.replace(d[0],'')[1:]
def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.kugou.com/',
    }
    response = requests.get(url=url,headers=headers,cookies=cookie) # 如果不使用vip的cookie，部分音乐只能爬取1分钟
    return response
def get_music_list(url):
    try:
        response = get_response(url)
        h = BeautifulSoup(response.text, 'html.parser') # 网页源代码解析
        h = h.find('div', id="songs",class_="list1").find_all('li')
        name = []
        for i in h:
            name.append(i.find('a').get('title'))
        Hash_list = re.findall('"hash":"(.*?)"',response.text)
        album_id_list = re.findall('"album_id":(\d+)', response.text)
        return name, Hash_list, album_id_list
    except:
        pass

def g(pwd,url):
    a = get_music_list(url)
    if pwd == '密码':
        if a:
            b = ''
            for i in range(len(a[0])):
                link_list = f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={a[1][i]}&dfid=3ex60E2pQb582fRAwB1wYhA1&appid=1014&mid=94c23e6bf948c957d06d24c4dec18b1e&platid=4&album_id={a[2][i]}&_=1695860308340' # 通过api接口获取音乐链接
                play_url = get_response(url=link_list).json()['data']['play_url']
                b = b+a[0][i]+'\n'+play_url+'\n\n'
            return b
        else:
            return '链接错误，请输入专辑链接，例如https://www.kugou.com/album/info/kl1rb2/'
    else:
        return '密码错误'
input1 = gr.Text(label="为防止不法分子通过此网页获利，请输入密码", placeholder="请输入密码")
input2 = gr.Text(label="输入专辑链接(通过专辑爬取可以绕开酷狗的防火墙)   按下Submit提交", placeholder="类似于https://www.kugou.com/album/info/kl1rb2/")
output = gr.Text(label="输出内容（将输出链接复制到浏览器下载播放）可以上下滑动")
demo = gr.Interface(fn=g, inputs=[input1,input2], outputs=output,title="酷狗音乐下载器",description="此网页非盈利，仅用于学习交流，请勿用于非法用途，如侵权，即删")
demo.launch()
