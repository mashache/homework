import codecs
big = 'ЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ'
score = 0

f = codecs.open('anna.txt', 'r', 'utf-8')
with open('anna.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    words = text.split()
    words_num = len(words)

for words in text:
    for letter in big:
        if words.startswith(letter):
            score += 1
res = (score/words_num)*100
print(res)
