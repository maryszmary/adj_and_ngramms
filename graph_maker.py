import json
import codecs
from scipy import spatial

translit = {u'а':u'a', u'б':u'b', u'в':u'v', u'г':u'g', u'д':u'd',
             u'е':u'e', u'ж':u'z', u'з':u'z', u'и':u'i', u'й':u'j',
             u'к':u'k', u'л':u'l', u'м':u'm', u'н':u'n', u'о':u'o',
             u'п':u'p', u'р':u'r', u'с':u's', u'т':u't', u'у':u'u',
             u'ф':u'f', u'х':u'h', u'ц':u'c', u'ч':u'c', u'ш':u's',
             u'щ':u's', u'ь':u'', u'ы':u'y', u'ъ':u'', u'э':u'e',
             u'ю':u'u', u'я':u'a', u'ё': u'e'}

def vectores_union(dictionaries):
    '''читает файл с лексемами, запускает их в file_walker и составляет
    для каждой вектор. возвращает словарь, где ключ -- лексема, а значение -- вектор.
    главная функция'''

    collocates = set([col.split()[1] for d in dictionaries for col in list(d)])
    #collocates = intersect(dictionaries)
    print(u'length of all collocates: ' + str(len(collocates)))
    vects = {}
    for d in dictionaries:
        if len(d) > 0:
            vect = []
            current_word = d.keys()[0].split()[0]
            for el in collocates:
                isthere = False
                for key in d:
                    if el == key.split()[1]:
                        isthere = True
                        vect.append(d[key])
                        # print current_word + u' ' + el + u' : ' + str(d[key])
                if not isthere:
                    vect.append(0)
                    # print current_word + u' ' + el + u' : ' + str(0)

            vects[current_word] = vect
            print(current_word)
            print(u'dict: ' + str(len(d)))
    return vects

def intersect(dictionaries):
    st = False
    for d in dictionaries:
        current_colls = set([key.split()[1] for key in d.keys()])
        if st:
            intersection = intersection.intersection(current_colls)
            print('\nint: ')
            for el in intersection:
                print(el, end = ',')
        else:
            intersection = current_colls
            st = True
    return intersection

def dictionaries_collector(lexemes):
    dicts = {}
    for lex in lexemes:
        with codecs.open('C:\\google ngramms\\russian\\dictionaries\\' + lex + '-final.json', 'r', 'utf-8') as f:
            d = json.load(f)
            dicts[lex] = d

    for key in dicts['ostryj']:
        print(key + ' : ' + str(dicts['ostryj'][key]))
    return dicts

def vectors_collector(lexemes):
    vecs = {}
    for lex in lexemes:
        with codecs.open('C:\\Users\\mary_szmary\\Dropbox\\' +
                        'course_work\\vectors\\' + lex + '.json', 'r', 'utf-8') as f:
            vec = json.load(f)
            vecs[lex] = vec
    return vecs

def distance_counter(vects, root):
    print(root)
    for vec in vects:
        if vec != root:
            distance = spatial.distance.cosine(vects[root], vects[vec])
            print(vec + ': ' + str(distance))

with codecs.open('lexems.txt', u'r', u'utf-8') as f:
    words = [line.strip() for line in f.readlines() if line != '\r\n' and '@' not in line and '#' not in line]
transliterated = [u''.join([translit[l] for l in word]) for word in words]
distance_counter(vectores_union(dictionaries_collector(transliterated)), 'ostryj')
