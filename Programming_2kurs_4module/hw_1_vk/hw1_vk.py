import urllib.request
import json
import datetime

def num_posts():
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-28460520&v=5.74&&access_token=e6a80850e6a80850e6a80850dde6ca4553ee6a8e6a80850bc6311beb1ac9078899a1afb')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    posts = json.loads(result)
    num = posts['response']['count']
    return num


def jsonfile(n):
    k = (n//100)+1
    di = {}
    post_info = []
    com_info = []
    for off in range(k):
        req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-28460520&v=5.74&&access_token=e6a80850e6a80850e6a80850dde6ca4553ee6a8e6a80850bc6311beb1ac9078899a1afb&offset=' + str(off*100))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        posts = json.loads(result)
        for i in range(100):
            comen = []
            try:
                post = posts['response']['items'][i]['text']
                post_id = posts['response']['items'][i]['id']
                post_au = posts['response']['items'][i]['signer_id']#id автора поста
                req3 = urllib.request.Request('https://api.vk.com/method/users.get?&v=5.74&&access_token=e6a80850e6a80850e6a80850dde6ca4553ee6a8e6a80850bc6311beb1ac9078899a1afb&fields=city,bdate&user_ids=' + str(post_au))
                response3 = urllib.request.urlopen(req3)
                result3 = response3.read().decode('utf-8')
                infa3 = json.loads(result3)
                inf = infa3['response'][0]
                bday_post = inf['bdate']#bday автора поста
                ci = inf['city']
                city_post = ci['title']#город автора поста
                i1 = [post, bday_post, city_post]
                post_info.append(i1)
                
                num = posts['response']['items'][i]['comments']
                num_com = num['count']
                h = (num_com//100)+1
                for ofs in range(h):
                    req2 = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-28460520&v=5.74&&access_token=e6a80850e6a80850e6a80850dde6ca4553ee6a8e6a80850bc6311beb1ac9078899a1afb&post_id=' + str(post_id) + '&offset=' + str(ofs*100))
                    response2 = urllib.request.urlopen(req2)
                    result2 = response2.read().decode('utf-8')
                    coms = json.loads(result2)
                    for j in range(100):
                        comment = coms['response']['items'][j]['text']
                        comen.append(comment)
                        com_au = coms['response']['items'][j]['from_id']#id автора коммента
                        req4 = urllib.request.Request('https://api.vk.com/method/users.get?&v=5.74&&access_token=e6a80850e6a80850e6a80850dde6ca4553ee6a8e6a80850bc6311beb1ac9078899a1afb&fields=city,bdate&user_ids=' + str(com_au))
                        response4 = urllib.request.urlopen(req4)
                        result4 = response4.read().decode('utf-8')
                        infa4 = json.loads(result4)
                        inf2 = infa4['response'][0]
                        bday_com = inf2['bdate']#bday комм
                        ci2 = inf2['city']
                        city_com = ci2['title']#город комм
                        i2 = [comment, bday_com, city_com]
                        com_info.append(i2)
            except:
                pass
            di[post] = comen
            
    f = open('scandinavia.json', 'w', encoding='utf-8')
    json.dump(di, f, ensure_ascii = False, indent = 4)
    f.close()
    f2 = open('post_info.json', 'w', encoding='utf-8')
    json.dump(post_info, f2, ensure_ascii = False, indent = 4)
    f2.close()
    f3 = open('comm_info.json', 'w', encoding='utf-8')
    json.dump(com_info, f3, ensure_ascii = False, indent = 4)
    f3.close()


def plot_from_arr(arr):#из массива вида [len_post, [sum_len, num_com]] делает массив из пар значений len_post к sum_len/num_com с учетом того, что len_post могут быть одинаковыми
    x = []
    y = []
    dic = {}
    for k in range(len(arr)):
        t = arr[k]
        if t[0] not in x:#решает проблему постов с одинаковой длиной
            x.append(t[0])
            y.append(t[1])
        else:
            ind = int(x.index(t[0]))
            a = y[ind]
            a[0] += t[1][0]
            a[1] += t[1][1]

    for v in range(len(y)):
        if y[v][1] == 0:
            y[v] = 0
        else:
            y[v] = y[v][0]/y[v][1]
        dic[x[v]] = y[v]

    m = []
    n = []
    for r in sorted(dic.keys()):
        m.append(r)
        n.append(dic[r])
    mn = [m, n]
    return mn


def len_plot():
    with open('scandinavia.json', 'r', encoding='utf-8') as f:
        d = f.read()
        data = json.loads(d)
    total = []
    len_p = []
    for key in data:
        sum_len = 0#сумма длин всех комм
        p = str(key).split()
        len_post = len(p)
        len_p.append(len_post)
        comm = data[key]#массив комментов
        num_com = len(comm)#скока комм
        for i in comm:
            c = str(i).split()
            sum_len += len(c)
        para = [len_post, [sum_len, num_com]]
        total.append(para)

    a = plot_from_arr(total)
    m, n = a[0], a[1]
    import matplotlib.pyplot as plt
    plt.plot(m, n)
    plt.title('Соотношение длины поста со средней длиной его комментариев')
    plt.xlabel('Длина поста')
    plt.ylabel('Средняя длина комментариев')
    plt.show()

        
def goroda_plot():
    a = []
    with open('post_info.json', 'r', encoding='utf-8') as f:
        d = f.read()
        data = json.loads(d)
    for i in range(len(data)):
        len_posta = len(str(data[i][0]).split())
        a.append([data[i][2], [len_posta, 1]])
    a2 = plot_from_arr(a)
    m, n = a2[0], a2[1]
    import matplotlib.pyplot as plt
    plt.plot(m, n)
    plt.title('Соотношение города со средней длиной постов')
    plt.xlabel('Город')
    plt.ylabel('Средняя длина поста')
    plt.xticks(range(len(m)), m, rotation = 90)
    plt.show()

    b = []
    with open('comm_info.json', 'r', encoding='utf-8') as f2:
        d2 = f2.read()
        data2 = json.loads(d2)
    for i in range(len(data2)):
        len_com = len(str(data2[i][0]).split())
        b.append([data2[i][2], [len_com, 1]])
    b2 = plot_from_arr(b)
    m, n = b2[0], b2[1]
    import matplotlib.pyplot as plt
    plt.plot(m, n)
    plt.title('Соотношение города со средней длиной комментариев')
    plt.xlabel('Город')
    plt.ylabel('Средняя длина комментариев')
    plt.xticks(range(len(m)), m, rotation = 90)
    plt.show()

def vozrast(date):#возраст по году рождения и текущей дате для 1 человека
    res = 0
    now = str(datetime.datetime.now())
    year, month, day = int(now[:4]), int(now[5:7]), int(now[8:10])
    try:
        year_b, month_b, day_b = int(date.split('.')[2]), int(date.split('.')[1]), int(date.split('.')[0])
        if month > month_b:
            res = year - year_b
        elif month == month_b and day >= day_b:
            res = year - year_b       
        else:
            res = year - year_b - 1
    except:
        pass
    return res
        
   
def vozrast_plot():
    a = []
    with open('post_info.json', 'r', encoding='utf-8') as f:
        d = f.read()
        data = json.loads(d)
    for i in range(len(data)):
        len_posta = len(str(data[i][0]).split())
        vozr = vozrast(data[i][1])
        a.append([vozr, [len_posta, 1]])
    a2 = plot_from_arr(a)
    m, n = a2[0], a2[1]
    import matplotlib.pyplot as plt
    plt.plot(m, n)
    plt.title('Соотношение возраста со средней длиной постов')
    plt.xlabel('Возраст')
    plt.ylabel('Средняя длина поста')
    plt.show()

    b = []
    with open('comm_info.json', 'r', encoding='utf-8') as f2:
        d2 = f2.read()
        data2 = json.loads(d2)
    for i in range(len(data2)):
        len_com = len(str(data2[i][0]).split())
        vozr = vozrast(data[i][1])
        b.append([vozr, [len_com, 1]])
    b2 = plot_from_arr(b)
    m, n = b2[0], b2[1]
    import matplotlib.pyplot as plt
    plt.plot(m, n)
    plt.title('Соотношение возраста со средней длиной комментариев')
    plt.xlabel('Возраст')
    plt.ylabel('Средняя длина комментариев')
    plt.show()
        
    
def main():
    n = num_posts()
    jsonfile(n)
    len_plot()
    goroda_plot()
    vozrast_plot()
    

main()
