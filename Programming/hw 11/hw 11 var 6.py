import re

with open('Fin.html', 'r', encoding='utf-8') as f:
    f = f.read()
    f = re.sub('Финлянди', 'Малайзи', f, flags=re.I | re.DOTALL)

with open('results.txt', 'w', encoding='utf-8') as k:
    k = k.write(f)
