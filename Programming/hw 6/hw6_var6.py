import random

def noun():
    f = open('nouns.txt', encoding='utf-8')
    nouns = f.read().split()
    return random.choice(nouns)   

def adverb():
    f = open('adverbs.txt', encoding='utf-8')
    adverbs = f.read().split()
    return random.choice(adverbs)

def adjective():
    f = open('adjectives.txt', encoding='utf-8')
    adjs = f.read().split()
    return random.choice(adjs)

def verb():
    f = open('verbs.txt', encoding='utf-8')
    verbs = f.read().split()
    return random.choice(verbs)

def verb_transitive(subj, obj):
    f = open('verbs.txt', encoding='utf-8')
    verbs = f.read().split()
    return subj + ' ' + random.choice(verbs) + ' ' + obj + 'n'

def imperative(subj, obj):
    f = open('osnovy.txt', encoding='utf-8')
    verbs = f.read().split()
    return subj + ' ' + random.choice(verbs) + ' ' + obj + 'n'

def sent_positive():
    sentence = adverb() + ' ' + adjective() + ' ' + verb_transitive(noun(), noun()) + '.'
    return sentence.capitalize()

def sent_negative():
    sentence = adverb() + ' ' + adjective() + ' ' + imperative(noun() + ' ei', noun()) + '.'
    return sentence.capitalize()

def sent_imperative():
    sentence = adjective() + ' ' + imperative(noun() + ',', noun()) + ' ' + adverb() + '!'
    return sentence.capitalize()

def sent_question():
    sentence = verb() + 'ko ' + adjective() + ' ' + noun() + ' ' + noun() + 'n ' + adverb() + '?'
    return sentence.capitalize()

def sent_conditional():
    cond = ['Jos', 'Kun']
    sentence = random.choice(cond) + ' ' + adjective() + ' ' + noun() + ' ' + verb() + ' ' + noun() + 'n, ' + adjective() + ' ' + noun() + ' ' + verb() + ' ' + noun() + 'n.'
    return sentence

def sent_all():
    a = [sent_positive(), sent_negative(), sent_imperative(), sent_question(), sent_conditional()]
    random.shuffle(a)
    a = ' '.join(a)
    return a
    
print(sent_all())
