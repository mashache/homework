import os

def extens_dir():
    i = 0
    for root in os.walk('.'):
        files = root[2]
        a = []
        current = 0
        for f in files:
            k = f.split('.')[1]
            if k not in a:
                a.append(k)
            else:
                current += 1
        if current > 0:
            i += 1
    print('Найдено {} папок, в которых есть файлы с одинаковым расширением'.format(i))

extens_dir()
