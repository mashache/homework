from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import json

app = Flask(__name__)

d = {'Результаты исследования' : '2017'}
with open('results.csv', 'w', encoding='utf-8') as k:
    k.write('Здесь будут результаты гениального исследования: \n')
f = open('new.json', 'w', encoding='utf-8')
json.dump(d, f, ensure_ascii = False, indent = 4)
f.close()


def freq_dict(arr):
    freq = {}
    for word in arr:
        if freq.get(word) == None:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


def content_arr():
    c = []
    with open('results.csv', 'r', encoding='utf-8') as t:
        t = t.read()
        csv = t.split('\n')
        for i in csv:
            i = i.split('\t')
            c.append(i)
    return c


def search_count(word):
    r = 0
    c = content_arr()
    for i in c:
        if word in i:
            r += 1
    return r


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('Anketa.html')
    elif request.method == 'POST':
        five = request.form['five']
        six = request.form['six']
        seven = request.form['seven']
        eight = request.form['eight']
        nine = request.form['nine']
        sex = request.form['sex']
        age = request.form['age']
        town = request.form['town']
        ev = {'Пять': five, 'Шесть': six, 'Семь': seven, 'Восемь': eight,
              'Девять': nine, 'Пол': sex, 'Возраст': age, 'Город': town}
        with open('results.csv', 'a', encoding='utf-8') as f:
            f.write(five + '\t' + six + '\t' + seven + '\t' + eight +
                    '\t' + nine + '\t' + sex + '\t' + age + '\t' + town + '\n')
        k = open('new.json', 'a', encoding='utf-8')
        json.dump(ev, k, ensure_ascii = False, indent = 4)
        k.close()
        return render_template('Anketa.html')


@app.route('/json')
def show_json():
    with open('new.json', 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('Json.html', content = content)


@app.route('/results')
def results():
    return render_template('Found.html', number = request.args.get('number'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('Search.html')
    elif request.method == 'POST':
        num = request.form['number']
        number = search_count(num)
        return redirect(url_for('results', number = number))


@app.route('/stats')
def stats():
    c = content_arr()
    five = []
    six = []
    seven = []
    eight = []
    nine = []
    sex = []
    age = []
    town = []
    for k in c:
        if len(k) > 1:
            five.append(k[0])
            six.append(k[1])
            seven.append(k[2])
            eight.append(k[3])
            nine.append(k[4])
            sex.append(k[5])
            age.append(k[6])
            town.append(k[7])
    five = freq_dict(five)
    six = freq_dict(six)
    seven = freq_dict(seven)
    eight = freq_dict(eight)
    nine = freq_dict(nine)
    sex = freq_dict(sex)
    age = freq_dict(age)
    town = freq_dict(town)
    return render_template('Stats.html', five = five, six = six, seven = seven,
            eight = eight, nine = nine, sex = sex, age = age, town = town)

    
if __name__ == '__main__':
    app.run(debug=True)


