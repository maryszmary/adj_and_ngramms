# -*- codecs:utf-8 -*-

import codecs
import os
import lxml.html

PATH = '/home/mary-szmary/Documents/ruscorpora/texts/source/post1950'

stop_words_a = [',', '.', '!', ')', '«', '*', '"', ':', '-', '--', ';',
                '...', '?', '»', '(', 'п', 'на', 'у', 'не', 'да',
                'и', 'с', 'по', 'ни', 'или', 'же', 'из', 'во',
                'быть', 'нас', 'в', 'от', 'будет', '..', 'за', 'к',
                'для', 'до', 'н', '\'', '/', 'ли', 'до', 'был', 'как',
                '1', 'бы', 'со', 'нет', 'о', 'буду', 'идет', 'мой',
                'ь', 'уже', 'даже']
adj_fl_np = ['ый', 'ое', 'ая', 'ые', 'ого', 'ой', 'ых', 'ому',
             'ым', 'ую', 'ою', 'ыми', 'ом']
adj_fl_p = ['ий', 'ее', 'яя', 'ие', 'его', 'ей', 'их', 'ему',
            'им', 'юю', 'ею', 'ими', 'ем']

def corpus(fname):
    '''получает на вход путь к файлу, открывает файл с xml, возвращает строку с текстом файла без тегов'''
    f = codecs.open(fname, 'r', 'utf-8')
    myfile = f.read().split('\n', 1)[1]
    tree = lxml.html.fromstring(myfile)
    content = tree.xpath('.//p')
    text = ''
    for el in content:
    	if el.text != None:
    		text += '\n' + el.text
    f.close()
    return text

def get_bigrams(text):
    words = [el.strip('(),.!?:;"-*«»') for el in text.split()]
    words = [w for w in words if w != '' and w != '—']
    bigrams = []
    for i in range(len(words) - 1):
        if bigram_is_ok(words[i], words[i + 1]):
            the_n_gramm = ' '.join(words[i:i + 2])
            bigrams.append(the_n_gramm.lower())
    return bigrams

def bigram_is_ok(word1, word2, flections = adj_fl_np + adj_fl_p, trash = stop_words_a):
    if word1[-2:] in flections\
    and word2 not in trash\
    and word2[0] not in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЮЯ':
        return True
    return False

def extractor():
    f = codecs.open('/home/mary-szmary/Documents/ruscorpora/bigrams_from_ruscorpora', 'w', 'utf-8')
    for d, dirs, files in os.walk(PATH):
        for file in files:
            bigrams = get_bigrams(corpus(os.path.join(d, file)))
            for i in range(len(bigrams)):
                f.write(bigrams[i] + '\t1950\t1\t\n')
                # print(bigrams[i])
    f.close()

extractor()