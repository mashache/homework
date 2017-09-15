import urllib.request
import re

def html(w):
    req = urllib.request.Request(w)
    with urllib.request.urlopen(req) as a:
        html = a.read().decode('utf-8')
    return html

def titles(html):
    t = re.compile('name\'><span class=\'name\'>(.*?)</span></a>', flags = re.DOTALL)
    titles = t.findall(html)
    return titles

def titles_file(titles):
    with open('titles.txt', 'w', encoding='utf-8') as k:
        k = k.write('\n'.join(titles))

def main():
    h = html('http://urogay-smol.ru/')
    ti = titles(h)
    titles_file(ti)

main()
