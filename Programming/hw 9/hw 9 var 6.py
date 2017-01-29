import re

arr = []
with open('zagr.txt', 'r', encoding='utf-8') as f:
    text = f.read().replace('\n', ' ').lower()
    words = text.split()

    con = 'загру(з|ж)(и(шь|в(ш(и(й|е|х|м(и)?)|е(го|е|й|м(у)?)|ая|ую))?|м|л(а|о|и)?|(т(е|ь)?)?)|у|ят|ен(а|о|ы|н(ы(м(и)?|е|х)|ая|о(е|й|го|м(у)?)))?)(с(я|ь))?'
    for word in words:
        m = re.search(con, word)
        if m != None:
            if word not in arr:
                print(word)
                arr.append(word)
