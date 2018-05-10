import telebot
import conf
import flask
from pymystem3 import Mystem
import pymorphy2
import json
import random
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

def wordforms():
    di = {}
    with open('1grams-3.txt', 'r', encoding='utf-8') as f:
        f = f.read().split('\n')
    for line in f:
        word = line.split('\t')[1]
        ana = morph.parse(word)[0]
        gram = ana.tag
        di[word] = str(gram)
    
    k = open('gr.json', 'w', encoding='utf-8')
    json.dump(di, k, ensure_ascii = False, indent = 4)
    k.close()

#wordforms()

def changeword(word, gram):
    newdi = {}
    with open('gr.json', 'r', encoding='utf-8') as f:
        d = f.read()
        data = json.loads(d)
    for key in data:
        if data[key] == gram:
            newdi[key] = gram
        else:
            pass
    w, g = random.choice(list(newdi.items()))
    return w

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.chat.id
    bot.send_message(user, "Здравствуйте! Это бот, который возвращает похожее, но совсем другое предложение.")

@bot.message_handler(func=lambda m:True)
def changesentence(message):
    new = []
    text = str(message.text)
    t = text.split()
    for word in t:
        ana = morph.parse(word)[0]
        gram = str(ana.tag)
        newword = changeword(word, gram)
        new.append(newword)
    bot.send_message(message.chat.id, ' '.join(new))	

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)
