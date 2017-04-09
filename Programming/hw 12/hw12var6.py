import re
def read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def text_to_sent(text):
    text_to = re.split('[.!?]', text)
    return text_to

def punct(text):
    te = [re.sub('[^\w\s]','', sent) for sent in text]
    return te

def len_aver(sent):
    for se in sent:
        words = se.split()
        if len(words) > 10:
            num = 0
            len_se = 0
            for word in words:
                num +=1
                len_se += len(word)
            if num != 0:
                len_aver = len_se/num
            print(se, ' - Это предложение со словами длины {:.2}'.format(len_aver))

def result(file_name):
    t = read(file_name)
    k = text_to_sent(t)
    p = punct(k)
    len_aver(p)

result('karenina.txt')
