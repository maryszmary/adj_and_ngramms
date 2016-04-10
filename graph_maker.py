import json
import codecs
from scipy import spatial

def vectors(lexemes):
    vecs = {}
    for lex in lexemes:
        with codecs.open('C:\\Users\\mary_szmary\\Dropbox\\' +
                        'course_work\\vectors\\' + lex + '.json', 'r', 'utf-8') as f:
            vec = json.load(f)
            vecs[lex] = vec
    return vecs

def distance_counter(vects, root):
    for vec in vects:
        if vec != root:
            distance = spatial.distance.cosine(vects[root], vects[vec])
            print(vec + ': ' + str(distance))

distance_counter(vectors(['umnyj', 'mudryj', 'hitryj', 'sposobnyj', 'muskulistyj', 'nacitannyj', 'ostroumnyj']), 'umnyj')
