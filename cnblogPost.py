from config import *
from datetime import datetime
import xmlrpc.client
import time
import os
import requests
import json

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
    r = client.metaWeblog.getRecentPosts(BLOG_USERNAME,BLOG_USERNAME,BLOG_TOKEN,100)
    print('读取博客，篇数：%d' % len(r))
    for j in r:
        xmlrpcTime = j['dateCreated']
        j['dateCreated'] = xmlrpcTime.value # string
    f = open('cnblog.txt','w')
    f.write(json.dumps(r))
    f.close()



# readMyBlog()
# new_post('33测试标题','33这是测试内容',None)
# getRecentPost()


# j = {
#     'a':123,
#     'b':datetime.now()
# }

# json.dumps(j)
