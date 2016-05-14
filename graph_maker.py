import json
import codecs
from scipy import spatial
import math

translit = {u'а':u'a', u'б':u'b', u'в':u'v', u'г':u'g', u'д':u'd',
             u'е':u'e', u'ж':u'z', u'з':u'z', u'и':u'i', u'й':u'j',
             u'к':u'k', u'л':u'l', u'м':u'm', u'н':u'n', u'о':u'o',
             u'п':u'p', u'р':u'r', u'с':u's', u'т':u't', u'у':u'u',
             u'ф':u'f', u'х':u'h', u'ц':u'c', u'ч':u'c', u'ш':u's',
             u'щ':u's', u'ь':u'', u'ы':u'y', u'ъ':u'', u'э':u'e',
             u'ю':u'u', u'я':u'a', u'ё': u'e'}

def vectores_union(dictionaries):
    '''получает словарь частотных словарей для лексем и составляет
    для каждой вектор. возвращает словарь, где ключ -- лексема, а значение -- вектор'''
    collocates = set([col.split()[1] for d in dictionaries for col in dictionaries[d]])
    print(u'length of all collocates: ' + str(len(collocates))) 
    vects = {}
    for d in dictionaries:
        if len(dictionaries[d]) > 0:
            vect = []
            for el in collocates:
                isthere = False
                for key in dictionaries[d]:
                    if el == key.split()[1]:
                        isthere = True
                        vect.append(dictionaries[d][key])
                if not isthere:
                    vect.append(0)

            vects[d] = vect
            print(u'dict ' + d + ': ' + str(len(dictionaries[d])))
    return vects

def vectores_intersection(dictionaries, root):
    '''получает словарь частотных словарей для лексем и составляет
    для каждой вектор. возвращает словарь, где ключ -- лексема, а значение -- вектор'''
    coll_root = dictionaries[root].keys()
    for lexeme in dictionaries:
        rootvec = []
        currvec = []
        for collr in coll_root:
##            print(collr)
            for collc in dictionaries[lexeme]:
                if collr.split()[1] == collc.split()[1]:
##                    print(collc.split()[1])
                    rootvec.append(dictionaries[root][collr])
                    currvec.append(dictionaries[lexeme][collc])
##        print(str(rootvec))
##        print(str(currvec))
        print(lexeme + ': ' + str(1 - spatial.distance.cosine(rootvec, currvec)))

def normalizing_dict(d, method = 'freq'):
    if method == 'freq':
        total_utterances = sum([d[key]for key in d])
        d = {bigram:(d[bigram]/float(total_utterances)) for bigram in d}
    elif method == 'log':
        d = {bigram:(math.log(d[bigram])) for bigram in d}
    return d

def dictionaries_collector(method):
    with codecs.open('lexems.txt', u'r', u'utf-8') as f:
        words = [line.strip() for line in f.readlines() if line != '\r\n' and '@' not in line and '#' not in line]
    lexemes = [u''.join([translit[l] for l in word]) for word in words]
    dicts = {}
    for lex in lexemes:
        with codecs.open('C:\\google ngramms\\russian\\dictionaries\\' + lex + '-final.json', 'r', 'utf-8') as f:
            d = json.load(f)
            d = normalizing_dict(d, method = method)
            dicts[lex] = d
    return dicts

def distance_counter(vects, root):
    '''печатает расстояние между нобором готовых векторов'''
    print(root)
    result = {}
    for vec in vects:
        if vec != root:
            try:
                distance = 1 - spatial.distance.cosine(vects[root], vects[vec]) # euclidean
                print(vec + ': ' + str(distance))
                result[vec] = distance
            except:
                'something gone wrong ' + vec
    return result

def method_applier(word):
    print('\nunion log')
    l = distance_counter(vectores_union(dictionaries_collector('log')), word)
    print('\nunion freq')
    f = distance_counter(vectores_union(dictionaries_collector('freq')), word)
    print('\nsum union')
    for key in l:
        print(key + ': ' + str((l[key] + f[key])/2))
    print('\nintersection freq')
    vectores_intersection(dictionaries_collector('freq'), word)
    print('\nintersection log')
    vectores_intersection(dictionaries_collector('log'), word)

method_applier('serohovatyj')
