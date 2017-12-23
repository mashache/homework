import sqlite3
import matplotlib
import matplotlib.pyplot as plt

conn = sqlite3.connect('hittite.db')
co = sqlite3.connect('itog.db')
c = conn.cursor()
a = co.cursor()
a.execute("CREATE TABLE IF NOT EXISTS words (Id INTEGER PRIMARY KEY AUTOINCREMENT, Lemma text, Wordform text, Glosses text)")
c.execute("SELECT * FROM wordforms")
wordforms = c.fetchall()
for e in range(len(wordforms)):
    lemma = wordforms[e][0]
    wordform = wordforms[e][1]
    gloss = wordforms[e][2]
    a.execute("INSERT INTO words (Lemma, Wordform, Glosses) VALUES (?,?,?)", (lemma, wordform, gloss))

a.execute("CREATE TABLE IF NOT EXISTS glosses (Id INTEGER PRIMARY KEY AUTOINCREMENT, Gloss text, Meaning text)")
with open("Glossing_rules.txt", 'r', encoding="utf-8") as f:
    f = f.readlines()
for i in f:
    i = i.strip('\n')
    gloss = i.split(' — ')[0]
    meaning = i.split(' — ')[1]
    a.execute("INSERT INTO glosses (Gloss, Meaning) VALUES (?,?)", (gloss, meaning))

a.execute("SELECT Id, Glosses FROM words")
id_words = a.fetchall()
a.execute("SELECT Id, Gloss FROM glosses")
id_glosses = a.fetchall()

a.execute("CREATE TABLE IF NOT EXISTS id (Id_word text, Id_gloss text)")
for k in range(len(id_words)):
    g = id_words[k][1].split('.')
    for j in g:
        for t in range(len(id_glosses)):
            p = id_glosses[t][1]
            if j == p:
                a.execute("INSERT INTO id VALUES (?,?)", (id_words[k][0], id_glosses[t][0]))

freq = {}
a.execute("SELECT Id_gloss FROM id")
id_gl = a.fetchall()
for v in range(len(id_gl)):
    v = id_gl[v][0]
    if freq.get(v) == None:
        freq[v] = 1
    else:
        freq[v] += 1

glo = []
fr = freq.values()
num = [i for i in range(len(fr))]
for el in freq.keys():
    for kl in range(len(id_glosses)):
        if el == str(id_glosses[kl][0]):
            glo.append(id_glosses[kl][1])
            
plt.bar(num, fr)
plt.xticks(num, glo)
plt.title('Частотность глосс')
plt.show()
co.commit()
conn.commit()
co.close()
conn.close()
