import urllib.request, re, time, os
time.sleep(2)

def html(w):
    req = urllib.request.Request(w)
    with urllib.request.urlopen(req) as a:
        html = a.read().decode('utf-8')
    return html

def download(url):
    try:
        pages = urllib.request.urlopen(url)
        page = pages.read().decode('utf-8')
    except:
        print('Error at', url)
    return page

def clear(text):
    import html
    a = text.find('class="full-img" /><p><strong>')
    b = text.find('Рубрики:')
    text = text[a+19:b]
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = str(clean_t)
    clean = html.unescape(clean_t)
    return clean

def plain_dirs(year, mon, a):
    plain_dir = '.\za_urozaj\\plain\\' + str(year) + '\\' + str(mon)
    if not os.path.exists(plain_dir):
        os.makedirs(plain_dir)
    plain_f = plain_dir + '\\' + str(a) + '.txt'
    return plain_f

def myplain_dirs(year, mon, a):
    myplain_dir = '.\za_urozaj\\mystem-plain\\' + str(year) + '\\' + str(mon)
    if not os.path.exists(myplain_dir):
        os.makedirs(myplain_dir)
    myplain_f = myplain_dir + '\\' + str(a) + '.txt'
    return myplain_f

def xmlplain_dirs(year, mon, a):
    xmlplain_dir = '.\za_urozaj\\mystem-xml\\' + str(year) + '\\' + str(mon)
    if not os.path.exists(xmlplain_dir):
        os.makedirs(xmlplain_dir)
    xmlplain_f = xmlplain_dir + '\\' + str(a) + '.xml'
    return xmlplain_f

def csvtable():
    path = '.\za_urozaj'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, 'metadata.csv'), 'a', encoding='utf-8') as t:
        t = t.write('path' + ';' + 'author' + ';' + 'sex' + ';' + 'birthday' + ';' + 'header' + ';' + 'created' + ';' + 'sphere' + ';' + 'genre_fi' + ';' + 'type' + ';' + 'topic' + ';' + 'chronotop' + ';' + 'style' + ';' + 'audience_age' + ';' + 'audience_level' + ';' + 'audience_size' + ';' + 'source' + ';' + 'publication' + ';' + 'publisher' + ';' + 'publ_year' + ';' + 'medium' + ';' + 'country' + ';' + 'region' + ';' + 'language')

def texts(text, a):
    urls = re.findall('class="autor"></div><p><a href="(.*?)" title="', text, flags = re.DOTALL)
    for i in urls:
        page = 'http://urogay-smol.ru/' + str(i)
        text = download(page)
        #au = re.findall("<p align=\"right\"><strong>(.*?)(.|,)</strong>", text, flags = re.DOTALL)#автор никак особо не выделен в разметке
        author = 'Noname'
        title = re.findall("<title>(.*?) / газета За урожай, Смоленск", text, flags = re.DOTALL)
        date = re.findall("<span class=\"date\">(.*?)</span>", text, flags = re.DOTALL)
        date= date[0]
        day, mon, year = date[8:10], date[5:7], date[:4]
        date = day + '.' + mon + '.' + year
        clean = clear(text)
        words = clean.split()
        path = '.\za_urozaj\\plain\\' + str(year) + '\\' + str(mon)
        plain_f = plain_dirs(year, mon, a)
        myplain_f = myplain_dirs(year, mon, a)
        xmlplain_f = xmlplain_dirs(year, mon, a)
        with open(os.path.join(path, str(a) + '.txt'), 'w', encoding='utf-8') as k:
            k = k.write("@au Noname\n@ti %s\n@da %s\n@url %s\n\n%s\n" % (title[0], date, page, clean))

        os.system('.\mystem.exe -di ' + plain_f + ' ' +  myplain_f)
        os.system('.\mystem.exe -di ' + plain_f + ' ' +  xmlplain_f)

        row = '%s;%s;;;%s;%s;публицистика;;;;;нейтральный;н-возраст;н-уровень;районная;%s;За урожай;;%s;газета;Россия;какой-то регион;Смоленск, п.Шумячи;ru'
        put = '.\za_urozaj'
        with open(os.path.join(put, 'metadata.csv'), 'a', encoding='utf-8') as t:
            t = t.write('\n' + row % (plain_f, author, *title, date, page, year))
        a += 1
    return a

def main():
    a = 1
    url_common = 'http://urogay-smol.ru/?module=articles&action=list&issues='
    csvtable()
    for i in range(42, 253):
        page_url = url_common + str(i)
        text = download(page_url)
        a = texts(text, a)
    return a

end = main()
