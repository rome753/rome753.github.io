from hashlib import new
from matplotlib import fontconfig_pattern
import requests
import json
import os
from PIL import Image, ImageFont, ImageDraw

jsonPath = 'blogJson.txt'
maxFontSize = 30
createCount = 0

def requestSaveFile():
    f = open(jsonPath, 'w')
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"    
    }
    hasClose = False
    for i in range(1, 20):
        url = 'https://www.jianshu.com/asimov/users/slug/6740854c6174/public_notes?shared_at=top&page=%d' % i
        r = requests.get(url, headers=headers)
        jo = json.loads(r.content)
        f.write(r.text)
        f.write('\n')
        print("write page: %d" % i)
        if (len(jo) == 0):
            print("close file")
            f.close()
            hasClose = True
            break
        # print(jo[0]['object']['data'])
        # print(i)
    if hasClose == False:
        f.close()


def parseFile():
    if os.path.exists('images') == False:
        os.mkdir('images')
    f = open(jsonPath, 'r')
    info = []
    for line in f:
        jo = json.loads(line)
        if (len(jo) == 0):
            break
        for obj in jo:
            data = obj['object']['data']
            id = data['id']
            slug = data['slug']
            title = data['title']
            print(data['title'])

            fpath = 'images/%s.png' % id
            if os.path.exists(fpath):
                os.remove(fpath)
            createImage(fpath, title)

            d = {
                'id': id,
                'path': fpath,
                'link': 'https://www.jianshu.com/p/%s' % slug
            }
            info.append(d)

        # print(jo[0]['object']['data'])
    f.close()


    d = {
        'id': 753,
        'path': 'images/753.png',
        'link': 'https://github.com/rome753'
    }
    info.append(d)
    # info['753'] = {'url': 'https://github.com/rome753'}
    f = open('images/json.txt', 'w')
    f.write(json.dumps(info))
    f.close()

# url = 'https://www.jianshu.com/asimov/users/slug/6740854c6174/public_notes?order_by=shared_at&page=10'
# r = requests.get(url, headers=headers)
# jo = json.loads(r.content)
# print(jo)
# print(jo[0]['object']['data'])


def previewImage(text):
    fontSize = 30
    fontPath = '/Library/Fonts/Arial Unicode.ttf'
    font = ImageFont.truetype(fontPath, fontSize)
    textSize = font.getsize(text)
    
    pd = 10
    w = textSize[0] + pd + pd
    h = textSize[1] + pd + pd

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

    dr.rounded_rectangle(xy=[0,0,w,h], radius=8, fill='#cccccc')
    dr.text((pd, pd), text, font=font, fill=fontColor)
    im.show()


def createImage(fpath, text):
    global createCount
    fontSize = maxFontSize - int(createCount / 10)
    if (fontSize < 25):
        fontSize = 25
    createCount += 1
    fontPath = '/Library/Fonts/Arial Unicode.ttf'
    font = ImageFont.truetype(fontPath, fontSize)
    textSize = font.getsize(text)
    
    pd = 10
    w = textSize[0] + pd + pd
    h = textSize[1] + pd + pd

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

    dr.rounded_rectangle(xy=[0,0,w,h], radius=8, fill='#ffffff', outline='#dddddd', width=2)
    dr.text((pd, pd), text, font=font, fill=fontColor)
    im.save(fpath)



if os.path.exists(jsonPath) == False:
    requestSaveFile()
parseFile()
