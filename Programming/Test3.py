import re, os

def len_files(root):
    reg = 'lex='
    dic = {}
    for root, dirs, files in os.walk(root):
        for f in files:
            name = f
            with open(os.path.join(root, f), 'r', encoding='Windows-1251') as text:
                t = text.read()
                words = re.findall(reg, t)
                l = len(words)
                dic[name] = l
    return dic

def dict_to_txt(dict):
    with open('files_names.txt', 'w', encoding='utf-8') as f:
        for key, value in sorted(dict.items()):
            f.write(str(key) + '\t' + str(value) + '\n')


def info(root):
    arr = []
    author = 'content="(.*?)" name="author"'
    date = 'content="(.*?)" name="created"'
    for root, dirs, files in os.walk(root):
        for f in files:
            name = f
            with open(os.path.join(root, f), 'r', encoding='Windows-1251') as text:
                t = text.read()
                aut = re.findall(author, t)
                dat = re.findall(date, t)
                arr.append([name, aut[0], dat[0]])
    return arr
                
def info_to_csv(a):
    with open('info.csv', 'w', encoding='utf-8') as f:
        for i in range(len(a)):
            f.write(str(a[i][0]) + '\t' + str(a[i]) +'\t' + str(a[i][2])+ '\n')

def text(root):
    bi = []
    reg = 'ana>(.*?)</w>'
    bigr = 'S.*?gen.*?</ana>(.*?)</w>.*?A.*?gen.*?</ana>(.*?)</w>'
    for root, dirs, files in os.walk(root):
        for f in files:
            with open(os.path.join(root, f), 'r', encoding='Windows-1251') as text:
                t = text.read()
                lines = t.split('<se>')
                for line in lines:
                    words = re.findall(reg, line)
                    bi = re.findall(bigr, line, re.DOTALL)
                    if len(bi) > 0:                     
                        bi.append([bi, words])
    return bi

def bigr_to_csv(b):
    with open('bigr.csv', 'w', encoding='utf-8') as f:
        for i in range(len(b)):
            f.write(str(b[i][0]) + '\t' + str(b[i][1]) + '\n')
                    
def main():
    texts = len_files('.\\news')
    dict_to_txt(texts)
    i = info('.\\news')
    info_to_csv(i)
    t = text('.\\news')
    bigr_to_csv(t)


main()

