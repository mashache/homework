from flask import Flask
from flask import render_template
from flask import request
import urllib.request
import json

def vkinfo(ids):
    d = {}
    req = urllib.request.Request('https://api.vk.com/method/users.get?&v=5.74&&access_token=e6a80850e6a80850e6a80850dde6ca4553ee6a8e6a80850bc6311beb1ac9078899a1afb&fields=first_name,last_name,bdate,about,career,city,contacts,education,interests,occupation,personal&user_ids=' + str(ids))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    infa = json.loads(result)
    inf = infa['response'][0]
    if 'first_name' in inf:
        fname = inf['first_name']
        d['fname'] = fname
    if 'last_name' in inf:
        surname = inf['last_name']
        d['surname'] = surname
    if 'bdate' in inf:
        bdate = inf['bdate']
        d['bdate'] = bdate
    if 'university_name' in inf:
        university_name = inf['university_name']
        d['university_name'] = university_name
    if 'faculty_name' in inf:
        faculty_name = inf['faculty_name']
        d['faculty_name'] = faculty_name
    if 'city' in inf:
        city = inf['city']['title']
        d['city'] = city
    if 'about' in inf:
        about = inf['about']
        d['about'] = about
    return d

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('Getid.html')
    elif request.method == 'POST':
        ids = request.form['word']
        d = vkinfo(ids)
        if 'fname' in d:
            fname = d['fname']
        else:
            fname = 'нет'
        if 'surname' in d:
            surname = d['surname']
        else:
            surname = 'нет'
        if 'bdate' in d:
            bdate = d['bdate']
        else:
            bdate = 'нет'
        if 'university_name' in d:
            university_name = d['university_name']
        else:
            university_name = 'нет'
        if 'faculty_name' in d:
            faculty_name = d['faculty_name']
        else:
            faculty_name = 'нет'
        if 'city' in d:
            city = d['city']
        else:
            city = 'нет'
        if 'about' in d:
            about = d['about']
        else:
            about = 'нет'
        return render_template('Resume.html', fname = fname, surname = surname, bdate = bdate, city = city, university_name = university_name, faculty_name = faculty_name, about = about)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
