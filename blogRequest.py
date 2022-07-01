import requests
import json
import os

fpath = 'blogJsonFile.txt'

def requestSaveFile():
    f = open(fpath, 'w')
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"    
    }
    hasClose = False
    for i in range(0, 20):
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
    f = open(fpath, 'r')
    for line in f:
        jo = json.loads(line)
        if (len(jo) == 0):
            break
        for obj in jo:
            data = obj['object']['data']
            print(data['title'])
        # print(jo[0]['object']['data'])

# url = 'https://www.jianshu.com/asimov/users/slug/6740854c6174/public_notes?order_by=shared_at&page=10'
# r = requests.get(url, headers=headers)
# jo = json.loads(r.content)
# print(jo)
# print(jo[0]['object']['data'])

if os.path.exists(fpath):
    parseFile()
else:
    requestSaveFile()
