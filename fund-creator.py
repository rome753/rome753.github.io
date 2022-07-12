import os

# 生成html网页，把sel里的图片放到网页列表里
list = []
for f in os.listdir('sel'):
    list.append(f)
list.sort()

str = ''
for f in list:
    if f.endswith('.png'):
        s = '''<h4 align="center">%s</h4>
        <a>
            <img src="sel/%s"/>
        </a>
        ''' % (f,f)
        str += s

html = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>fund</title>
    <script src="fund.js" defer></script>
  </head>
  <body>
    <ul>
      <li>
        %s
      </li>
    </ul>
  </body>
</html>
''' % str

print(html)

f = open('fund.html', 'w')
f.write(html)
f.close()