from matplotlib import fontconfig_pattern
import requests
import json
import os
from PIL import Image, ImageFont, ImageDraw


fontSize = 25
fontPath = '/Library/Fonts/Arial Unicode.ttf'
font = ImageFont.truetype(fontPath, fontSize)

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"    
}

def parseFile():
    if os.path.exists('images') == False:
        os.mkdir('images')

    info = []
    f = open('cnblog.txt', 'r')
    jo = json.loads(f.read())
    f.close()
    for j in jo:
        title = j['title']
        id = j['postid']
        print(title)
        fpath = 'images/%s.png' % id
        if os.path.exists(fpath):
            os.remove(fpath)
        im = createImage(False, title)
        im.save(fpath)

        d = {
            'id': id,
            'path': fpath,
            'link': 'https://www.cnblogs.com/rome753/p/%d.html' % id
        }
        info.append(d)

    d = {
        'id': 753,
        'path': 'images/753.png',
        'link': 'https://github.com/rome753'
    }
    info.append(d)
    f = open('images/json.txt', 'w')
    f.write(json.dumps(info))
    f.close()


def findHalfWidth(text):
    w = font.getsize(text)[0]
    for i in range(0, 1000):
        t = text[:i]
        if font.getsize(t)[0] > w / 2:
            return i
    return 0


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


parseFile()

# createImage(True, 'Android ios这是测试134加肥加大')




def downloadImage(url, name):
    path = 'cdn/%s' % name
    r = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(r.content)

