import codecs

with open('quotes.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.split()
        for words in line:
            words = words.split(' ')
        if len(line) < 10:
            line = ' '.join(line)
            print(line)



