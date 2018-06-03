import sys
import gensim, logging
import re
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
model.init_sims(replace=True)

words = ['студент_NOUN', 'студентка_NOUN', 'учиться_VERB', 'экзамен_NOUN', 'школьник_NOUN', 'преподаватель_NOUN', 'учитель_NOUN', 'учебник_NOUN', 'книга_NOUN', 'заочник_NOUN', 'первокурсник_NOUN', 'преподавать_VERB', 'экзаменационный_ADJ', 'пересдавать_VERB', 'урок_NOUN', 'конспект_NOUN']

G = nx.Graph()
for word in words:
    G.add_node(word)

for i in range(len(words)):
    for k in range(len(words)):
        if words[i] in model and words[k] in model and i < k:
            cos = model.similarity(words[i], words[k])
            if cos > 0.5:
                G.add_edge(words[i], words[k])

deg = nx.degree_centrality(G)
d = sorted(deg, key=deg.get, reverse=True)
print('Пять самых центральных слова графа: %s' % ', '.join(d[:5]))
print('Радиус графа: ', nx.radius(G))
print('Коэффициент кластеризации: ', nx.average_clustering(G))
nx.write_gexf(G, 'graph.gexf')

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='red', node_size=30)
nx.draw_networkx_edges(G, pos, edge_color='blue')
nx.draw_networkx_labels(G, pos, font_size=12, font_family='Arial')
plt.axis('off')
plt.show()
