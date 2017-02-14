import re
with open('isl.xml', 'r', encoding='utf-8') as f:
    text = f.read()
    text = re.sub('</teiHeader>', '</teiHeader>$', text)
    a = text.split('$')
    part1 = a[0]
    part1 = part1.split('/n')
    l = len(part1)
    print(l)

with open('result_len.txt', 'w', encoding='utf-8') as f:
    f = f.write(str(l))

reg = 'lemma=".*?" type="(.*?)"'
words = re.findall(reg, text, re.DOTALL)
  
freq = {}
for word in words:
        if freq.get(word) == None:
            freq[word] = 1
        else:
            freq[word] += 1 

with open('result_freq.txt', 'w', encoding='utf-8') as k:
    k = k.write(str(freq))
        

mest = 'type="f.h.*?>(.*?)<'
mestoim = re.findall(mest, text, re.DOTALL)
print(mestoim)
