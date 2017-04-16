import os
import re
punct = '[.!&_+;=,-]'

def num_files(search):
    files = [f for f in os.listdir('.') if os.path.isfile(f) and len(re.findall(search, f))>1] 
    return files

def files_only(files):
    names = [i.rsplit('.', 1)[0] for i in files]
    return names

def result(search):
    f = num_files(search)
    n = files_only(f)
    print(len(f), ', '.join(f))
    print(', '.join(set(n)))

result(punct)
