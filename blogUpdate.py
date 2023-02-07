from matplotlib import fontconfig_pattern
import requests
import json
import os
from PIL import Image, ImageFont, ImageDraw
from config import *
from datetime import datetime
import xmlrpc.client
import time



postCount = 0

def readMyBlog():
    postCount = 0
    path = LOCAL_DIR # 本地目录，我这是两层目录
    dir = os.listdir(path)
    for d in dir:
        pp = os.path.join(path, d)
        if os.path.isdir(pp) == False:
            continue
        dd = os.listdir(pp)
        for ff in dd:
            if ff.endswith('.md') == False:
                continue
            p = os.path.join(pp, ff)
            f = open(p, 'r+', encoding="utf-8")
            title = ff[:len(ff)-3]
            print(title)
            content = f.read()
            category = None
            if (title.startswith('Android')):
                category = 'Android'
            if (title.startswith('iOS')):
                category = 'iOS'
            if (title.startswith('FFmpeg')):
                category = 'FFmpeg'
            if (title.startswith('OpenCV')):
                category = 'OpenCV'
            f.close()

            if postCount < 0: # 从上次报错的位置继续
                postCount += 1
                continue
            print(postCount)
            new_post(title, content, category)
            postCount += 1
            time.sleep(30)


def new_post(title, content, category):
    # 构建发布内容
    struct = {
        'title': title,
        'dateCreated': 0,
        'description': content,
    }
    if category is not None:
        struct['categories'] = ['[Markdown]', category]
    else:
        struct['categories'] = ['[Markdown]']

    client = xmlrpc.client.ServerProxy(METAWEBLOG_API)
    postid = client.metaWeblog.newPost('',BLOG_USERNAME, BLOG_TOKEN, struct, True)
    print('发布成功' + postid)


def getRecentPost():
    client = xmlrpc.client.ServerProxy(METAWEBLOG_API)
    r = client.metaWeblog.getRecentPosts(BLOG_USERNAME,BLOG_USERNAME,BLOG_TOKEN,200)
    print('读取博客，篇数：%d' % len(r))

    info = []

    for j in r:
        xmlrpcTime = j['dateCreated']
        j['dateCreated'] = xmlrpcTime.value # string
        
        info.append(blogInfo(j['postid'], j['title']))

    info.append(titleInfo())
    info.append(githubInfo())

    f = open('images/json.txt', 'w')
    f.write(json.dumps(info))
    f.close()



def blogInfo(id, title):
    print(title)
    fpath = 'images/%s.png' % id
    if os.path.exists(fpath):
        os.remove(fpath)
    im = createImage(False, title)
    im.save(fpath)

    return {
        'id': id,
        'title': title,
        'path': fpath,
        'link': 'https://www.cnblogs.com/rome753/p/%d.html' % id
    }
    

def titleInfo():
    # 添加标题图片
    fpath = 'images/1.png'
    if os.path.exists(fpath):
        os.remove(fpath)
    im = createTitle(False, "Rome753's Blog")
    im.save(fpath)

    return {
        'id': 1,
        'path': fpath,
        'link': 'https://rome753.github.io'
    }


def githubInfo():
    # 添加Github图片
    return {
        'id': 753,
        'path': 'images/753.png',
        'link': 'https://github.com/rome753'
    }



# readMyBlog()
# new_post('33测试标题','33这是测试内容',None)




fontSize = 25
fontPath = '/Library/Fonts/Arial Unicode.ttf'
font = ImageFont.truetype(fontPath, fontSize)

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"    
}

def findHalfWidth(text):
    w = font.getsize(text)[0]
    for i in range(0, 1000):
        t = text[:i]
        if font.getsize(t)[0] > w / 2:
            return i
    return 0

def createTitle(isShow, text):
    font = ImageFont.truetype(fontPath, 30)
    textSize = font.getsize(text)
    
    pd = 10
    w = textSize[0]
    h = textSize[1]
    w = pd + w + pd
    h = pd + h + pd

    fontColor = '#000000'

    im = Image.new("RGBA", [w, h], (255,255,255,0))
    dr = ImageDraw.Draw(im)

    dr.rounded_rectangle(xy=[0,0,w,h], radius=0, fill='#ffffff')
    dr.text((pd, pd), text, font=font, fill=fontColor)
    if isShow:
        im.show()
    return im


def createImage(isShow, text):
    half = findHalfWidth(text)
    text1 = text[:half]
    text2 = text[half:]

    textSize1 = font.getsize(text1)
    textSize2 = font.getsize(text2)
    
    pd = 10
    w1 = textSize1[0]
    h1 = textSize1[1]
    w2 = textSize2[0]
    h2 = textSize2[1]

    w = pd + max(w1, w2) + pd
    h = pd + h1 + h2 + pd

    fontColor = '#000000'
    if (text.startswith('Android')):
        fontColor = '#009933'
    if (text.startswith('iOS')):
        fontColor = '#996633'
    if (text.startswith('FFmpeg')):
        fontColor = '#6600cc'
    if (text.startswith('OpenCV')):
        fontColor = '#993399'

    im = Image.new("RGBA", [w, h], (255,255,255,0))
    dr = ImageDraw.Draw(im)

    # dr.rounded_rectangle(xy=[0,0,w,h], radius=0, fill='#ffffff', outline='#dddddd', width=2)
    dr.rounded_rectangle(xy=[0,0,w,h], radius=0, fill='#ffffff')
    dr.text((pd, pd), text1, font=font, fill=fontColor)
    dr.text((pd, pd + h1), text2, font=font, fill=fontColor)
    if isShow:
        im.show()
    return im


getRecentPost()


# createImage(True, 'Android ios这是测试134加肥加大')
# createTitle(True)




def downloadImage(url, name):
    path = 'cdn/%s' % name
    r = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(r.content)

