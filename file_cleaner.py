# -*- coding: utf-8 -*-

import codecs
import os


adj_fl_np = [u'ый', u'ое', u'ая', u'ые', u'ого', u'ой', u'ых', u'ому',
             u'ым', u'ую', u'ою', u'ыми', u'ом']
adj_fl_p = [u'ий', u'ее', u'яя', u'ие', u'его', u'ей', u'их', u'ему',
            u'им', u'юю', u'ею', u'ими', u'ем']
stop_words_a = [u',', u'.', u'!', u')', u'«', u'*', u'"', u':', u'-', '--', u';',
                u'...', u'?', u'»', u'(', u'п', u'на', u'у', u'не', u'да',
                u'и', u'с', u'по', u'ни', u'или', u'же', u'из', u'во',
                u'быть', u'нас', u'в', u'от', u'будет', u'..', u'за', u'к',
                u'для', u'до', u'н', u'\'', u'/', u'ли', u'до', u'был', u'как',
                u'1', u'бы', u'со', u'нет', u'о', u'буду', u'идет', u'мой',
                u'ь', u'уже', u'даже']


def cleaner(filename, flections = adj_fl_np, trash = stop_words_a):
    '''получает на вход название файла, содержащего биграммы, основу
    прилагательного и массив окончаний, возвращает словарь с биграммами, очищенными от мусора'''
    with codecs.open(u'C:\\google ngramms\\russian\\' + filename,'r', u'utf-8') as f:

        ## здесь отбрасываются все разобранные биграммы, биграммы, которые
        ## содержат стоп-слова, биграммы, зафиксированные раньше 1930 года
        ## и биграммы, в которых второе слово начинается с апперкейса.
        lines = {line.lower(): 1 for line in f
                 if u'_' not in line
                 and int(line.split(u'\t')[1]) > 1929
                 and line.split(u'\t')[0].split()[0][-2:] in flections
                 and line.split(u'\t')[0].split()[1] not in trash
                 and line.split(u'\t')[0].split()[1][0] not in u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЮЯ'}
    with codecs.open('C:\\google ngramms\\russian\\for_adjectives\\' + filename, u'w', u'utf-8') as f1:
    	for line in lines:
    		f1.write(line)
    return f1

def mem_safe_cleaner(filename, flections = adj_fl_np, trash = stop_words_a):
    '''the same function but for really big files in order to avoid Memory error'''
    f_new = codecs.open('C:\\google ngramms\\russian\\for_adjectives\\' + filename, u'w', u'utf-8')
    with codecs.open(u'C:\\google ngramms\\russian\\' + filename,'r', u'utf-8') as f:
         for line in f:
             if u'_' not in line\
             and int(line.split(u'\t')[1]) > 1929\
             and line.split(u'\t')[0].split()[0][-2:] in flections\
             and line.split(u'\t')[0].split()[1] not in trash\
             and line.split(u'\t')[0].split()[1][0] not in u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЮЯ':            
                f_new.write(line)
    f_new.close()

mem_safe_cleaner('pr', adj_fl_np + adj_fl_p)
