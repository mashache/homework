def punct_zero():
    punct = ',".?1234567890[]'
    a = []
    with open('omnibus.txt', 'r', encoding='utf-8') as f:
        words = f.read().split()

    for word in words:
        word = word.strip(punct)
        word = word.lower()
        a.append(word)
    return a

def omni():
    omni = []
    for word in punct_zero():
        if word.startswith('omni'):
            if word not in omni:
                omni.append(word)
    return omni

def count_omni():
    c_omni = []
    for word in omni():
        c = punct_zero().count(word)
        c_omni.append(c)
    return c_omni

def osnovy_ne_omni():
    ne_omni = []
    for word in omni():
        new = word[4:]
        ne_omni.append(new)
    return ne_omni

def count_ne_omni():
    c_ne_omni = []
    b = osnovy_ne_omni()
    for word in b:
        c = punct_zero().count(word)
        c_ne_omni.append(c)
    return c_ne_omni

def result():
    om = omni()
    c_omni = count_omni()
    ne_omni = osnovy_ne_omni()
    c_ne_omni = count_ne_omni()
    res_omni = []
    res_ne_omni = []
    for i in range(len(om)):
        res_omni.append('Слово ' + om[i] + ' (с приставкой omni-) встречается в тексте ' + str(c_omni[i]) + ' раз.')
        res_ne_omni.append('Слово ' + ne_omni[i] + ' (слово без приставки omni-) встречается в тексте ' + str(c_ne_omni[i]) + ' раз.')
    for i in range(len(om)):
        print(res_omni[i], res_ne_omni[i])

result()
