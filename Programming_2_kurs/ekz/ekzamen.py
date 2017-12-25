import re
import os
import json
from flask import Flask
from flask import render_template
from flask import request

def main():
    th = re.compile('href=\'/id/[0-9]+\'>(.*?)<(.*?)class=[a-z]+?>[a-z]+?</td><td>(.*?)</td></tr>', re.DOTALL)
    thai_eng = {}
    eng_thai = {}
    for root, dirs, files in os.walk('.'):
        for f in files:
            with open(os.path.join(root, f), 'r', encoding='utf-8') as text:
                t = text.read()
                thai = re.findall(th, t)
                for i in range(len(thai)):
                    thai_eng[thai[i][0]] = thai[i][2]
                    eng_thai[thai[i][2]] = thai[i][0]
    k = open('thai_eng.json', 'w', encoding='utf-8')
    json.dump(thai_eng, k, ensure_ascii = False, indent = 4)
    k.close()
    m = open('eng_thai.json', 'w', encoding='utf-8')
    json.dump(eng_thai, m, ensure_ascii = False, indent = 4)
    m.close()

main()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('TypeWord.html')
    elif request.method == 'POST':
        word = request.form['word']
        with open('eng_thai.json', 'r', encoding='utf-8') as f:
            d = f.read()
        data = json.loads(d)
        word_tr = data.get(word)
        return render_template('AnswerWord.html', word = word_tr)

if __name__ == '__main__':
    app.run(debug=True)
