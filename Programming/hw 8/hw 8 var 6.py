import random

dic = dict()
f = open('zag.csv')
f = f.readlines()
for line in f:
    a = line.strip('\n')
    a = a.split(';')
    dic[a[0]] = a[1]

word = random.choice(list(dic.keys()))
print(dic.get(word))
left = 3

for i in range(3):
    ans = input('Ваш ответ: ')
    if ans == word:
        print('Молодец! Это правильный ответ!')
        break
    else:
        left -= 1
        print('Неправильно:( Количество оставшихся попыток: ' + str(left) + '.')
