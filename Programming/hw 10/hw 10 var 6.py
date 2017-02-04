import re

with open('hom.html', 'r', encoding='utf-8') as f:
    f = f.read()

reg = 'Отряд.*?([А-Яа-я]+)'
r = re.search(reg, f, re.DOTALL)
res = r.group(1)
k = open('homiaki.txt', 'w', encoding='utf-8')
k.write(res)
k.close()
