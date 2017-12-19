from flask import Flask
from flask import render_template
from flask import request
import urllib.request
import re
import json
from pymystem3 import Mystem

def pogoda():
    req = urllib.request.Request('https://yandex.ru/pogoda/10463')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    p = re.search('Сейчас.*?temp__value">(.*?)</span>', html)
    pogoda = p.group(1)
    return pogoda


def dorev_dict():
    pages = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9',
             'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3',
             'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'dd', 'de', 'df']
    p = 'http://www.dorev.ru/ru-index.html?l='
    dict_dorev = {}
    for i in pages:
        url = p + i
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('windows-1251')
        regwords = re.compile('<td class="uu">([А-Яа-я]*?)</td><td></td><td class="uu">(.*?)</td>', re.DOTALL)
        di = re.findall(regwords, html)
        regTag = re.compile('<.*?>', re.DOTALL)
        regComment = re.compile('<!--.*?-->', re.DOTALL)
        for i in range(len(di)):
            import html
            t = di[i][1]
            clean = regComment.sub("", t)
            clean = regTag.sub("", clean)
            clean_t = str(clean)
            clean = html.unescape(clean_t)
            word = clean.split()[0]
            dict_dorev[di[i][0]] = word
    k = open('dorev.json', 'w', encoding='utf-8')
    json.dump(dict_dorev, k, ensure_ascii = False, indent = 4)
    k.close()


d = dorev_dict()

app = Flask(__name__)

#server/
@app.route('/', methods=['GET', 'POST'])
def main_page():
    po = pogoda()
    if request.method == 'GET':
        return render_template('TypeWord.html', pogoda = po)
    elif request.method == 'POST':
        word = request.form['word']
        with open('dorev.json', 'r', encoding='utf-8') as f:
            d = f.read()
        data = json.loads(d)
        word_tr = data.get(word)
        return render_template('AnswerWord.html', word = word_tr)


@app.route('/test', methods=['GET', 'POST'])
def test():
    c = 0
    if request.method == 'GET':
        return render_template('Test.html')
    elif request.method == 'POST':
        one = request.form['1']
        if one == "ѣ":
            c += 1
        two = request.form['2']
        if two == "е":
            c += 1
        three = request.form['3']
        if three == "ѣ":
            c += 1
        four = request.form['4']
        if four == "ѣ":
            c += 1
        five = request.form['5']
        if five == "е":
            c += 1
        six = request.form['6']
        if six == "ѣ":
            c += 1
        seven = request.form['7']
        if seven == "е":
            c += 1
        eight = request.form['8']
        if eight == "е":
            c += 1
        nine = request.form['9']
        if nine == "ѣ":
            c += 1
        ten = request.form['10']
        if ten == "е":
            c += 1
        return render_template('Answers.html', c = c, one = one, two = two,
                three = three, four = four, five = five, six = six,
                seven = seven, eight = eight, nine = nine, ten = ten)


@app.route('/lenta')
def lenta():
    import html
    res = []
    with open('dorev.json', 'r', encoding='utf-8') as f:
        d = f.read()
    data = json.loads(d)
    r = urllib.request.Request('https://lenta.ru/')
    with urllib.request.urlopen(r) as response:
        page = response.read().decode('utf-8')
    page = page.split("query-input")[0]
    page = page.split("88Q');")[1]
    regTag = re.compile('<.*?>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    regCom = re.compile('{.*?}', re.DOTALL)
    clean = regComment.sub(" ", page)
    clean = regTag.sub(" ", clean)
    clean = regCom.sub(" ", clean)
    clean_t = str(clean)
    text = html.unescape(clean_t)
    text = re.sub('[^\w\s\n]','', text)
    text = re.sub('\s+', ' ', text)

    m = Mystem()
    lemmas = m.lemmatize(text)
    for i in lemmas:
        word_tr = data.get(i)
        if word_tr != None:
            res.append(word_tr)
        else:
            res.append(i)
    freq = {}
    for word in res:
        if freq.get(word) == None:
            freq[word] = 1
        else:
            freq[word] += 1
    fr = sorted(freq, key=freq.get, reverse=True)
    f = fr[1:11]
    return render_template ('Lenta.html', content = ''.join(res), f = f)


if __name__ == '__main__':
    app.run(debug=True)
