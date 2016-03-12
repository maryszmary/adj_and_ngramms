# -*- coding: utf-8 -*-

import codecs
import os
from pymystem3 import Mystem
import time
import json

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
subst_adj = [u'малый', u'ученый', u'рабочий', u'пожарный', u'полицейский', u'дежурный',
             u'военный']
for_bastards = {u'учтивостию':u'учтивостью', u'человькъ': u'человек',
                u'человвкъ': u'человек', u'бояры':u'бояре', u'человвк': u'человек',
                u'человвка': u'человека'}
translit = {u'а':u'a', u'б':u'b', u'в':u'v', u'г':u'g', u'д':u'd',
             u'е':u'e', u'ж':u'z', u'з':u'z', u'и':u'i', u'й':u'j',
             u'к':u'k', u'л':u'l', u'м':u'm', u'н':u'n', u'о':u'o',
             u'п':u'p', u'р':u'r', u'с':u's', u'т':u't', u'у':u'u',
             u'ф':u'f', u'х':u'h', u'ц':u'c', u'ч':u'c', u'ш':u's',
             u'щ':u's', u'ь':u'', u'ы':u'y', u'ъ':u'', u'э':u'e',
             u'ю':u'u', u'я':u'a'}

m = Mystem()

def cleaner(filename, base, flections = adj_fl_np, trash = stop_words_a):
    '''получает на вход название файла, содержащего биграммы, основу
    прилагательного и массив окончаний, возвращает словарь с биграммами, очищенными от мусора'''
    forms = [base + aff for aff in flections] + [base[0].upper() + base[1:] + aff for aff in flections]
    with codecs.open(u'C:\\google ngramms\\russian\\' + filename,'r', u'utf-8') as f:

        ## здесь отбрасываются все разобранные биграммы, биграммы, которые
        ## содержат стоп-слова, биграммы, зафиксированные раньше 1930 года
        ## и биграммы, в которых второе слово начинается с апперкейса.
        ## отбираются те, первое слово которых -- словоформа данной лексемы
        lines = {line.lower(): 1 for line in f
                 if u'_' not in line
                 and int(line.split(u'\t')[1]) > 1929
                 and line.split(u'\t')[0].split()[0] in forms
                 and line.split(u'\t')[0].split()[1] not in trash
                 and line.split(u'\t')[0].split()[1][0] not in u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЮЯ'}
    return lines


def year_merger(lines):
    '''получает на вход словарь, где ключи -- отобранные строки google ngrams,
    возвращает словарь где ключи -- биграммы, а значения -- их частотность'''
    merged = {}
    for line in lines:
        current_bigram = line.split(u'\t')[0]
        current_freq = int(line.split(u'\t')[2])
        merged[current_bigram] = merged.get(current_bigram, 0) + current_freq
    return merged


def grammar_analyzer(merged_lines):
    '''получает на вход словарь, где ключи -- биграммы, а значения -- их
    частотность, возвращает кортеж массивов, первый элемент которых -- разбор
    биграммы, а второй -- количество вхождений'''
    bigrams = tuple()
    frequencies = tuple()
    for el in merged_lines:
        bigrams += (el,)
        frequencies += (merged_lines[el],)
    bigrams = u' ; '.join([line.split(u'\t')[0] for line in merged_lines])
    analized_bigrams = analysis_parser(m.analyze(bigrams))
    analized_bigrams = zip(analized_bigrams, frequencies)
    return analized_bigrams


def analysis_parser(analized_bigrams):
    '''получает на вход массив словарей с грамматическим разбором биграмм, возвращает
    кортеж с массивами разборов для каждой биграммы. вызывается в grammar_analyzer'''
    parsed_analysis = tuple()
    current_bigram = []
    for d in analized_bigrams:
        if d[u'text'] == u' ; ':
            parsed_analysis += (current_bigram, )
            current_bigram = []
        else:
            current_bigram.append(d)
    return parsed_analysis


def final_dictionary(for_checking):
    '''получает кортеж массивов, первый элемент которых -- разбор
    биграммы, а второй -- количество вхождений, возвращает частотный словарь'''
    what_i_need = {}
    for el in for_checking: 
        if pos_checker(el[0]):
            
            ## где-то здесь должен быть кусок кода, который отвечает за бастарды. вот он.
            not_bast = [el[0][0], bastards_and_instrumental(el[0][2])]
                        
            if not_bast is not None and agreement_checker(not_bast):
                ## тогда лемматизируем
                new_bigram = u' '.join([not_bast[0][u'analysis'][0]['lex'], not_bast[1][u'analysis'][0]['lex']])
                what_i_need[new_bigram] = what_i_need.get(new_bigram, 0) + el[1]
    total_utterances = sum([what_i_need[key]for key in what_i_need])
    print 'total: ' + str(total_utterances)
    what_i_need = {bigram:(what_i_need[bigram]/float(total_utterances)) for bigram in what_i_need}
    print u'length of dictionary: ' +  str(len(what_i_need))
    return what_i_need
    
# заменить на спеллчекер.
def those_are_not_bastards(not_analyzed_bigrams):
    '''берёт бираммы до майстема, прогоняет их через словарь исключений,
возвращает те же биграммы в чуть более адекватном виде'''
    pass

def bastards_and_instrumental(sec_word):
    '''берёт 2 слово биграммы, проверяет, не потому ли это бастард,
    что это алломорф инструменталиса, если да -- меняет лемму. вызывается в final_dictionary'''
    if 'qual' in [key for an in sec_word[u'analysis'] for key in an] and sec_word[u'text'][-2:] == u'ию':
        sec_word[u'analysis'] = [{u'lex': u'учтивость', u'gr': u'S,жен,неод=твор,ед'}]
    return sec_word

def pos_checker(bigram, substantivated = subst_adj):
    '''получает массив словарей с разбором биграммы, возвращает True, если 1-ое
    слово -- прилагательное в положительной степени, а второе -- 
    существительное, в обратном случае -- False. вызывается в final_dictionary'''    
    a = bigram[0][u'analysis'][0][u'gr'][0] == u'A'\
        and bigram[0][u'analysis'][0][u'gr'] != u'A=срав'\
        and u'analysis' in bigram[2]\
        and len(bigram[2][u'analysis']) > 0\
        and (bigram[2][u'analysis'][0][u'gr'][:2] == u'S,'
             or bigram[2][u'analysis'][0][u'lex'] in subst_adj)
    return a

def agreement_checker(bigram):
    '''получает массив словарей с разбором биграммы, возвращает True, если среди
    грамматических разборов 1 и 2 слов есть одинаковые по роду, числу и падежу,
    в обратном случае -- False. вызывается в final_dictionary'''
    first, second = hypothesis_collector(bigram)
    for hyp_a in first:
        for hyp_s in second:
            if hyp_a == hyp_s or hyp_s.difference(hyp_a).issubset(set([u'неод', u'од', u'мж']))\
               or hyp_s.difference(hyp_a) in (set([u'муж', u'мж', u'од']), set([u'жен', u'мж', u'од']))\
               or (hyp_a == set([u'муж', u'ед', u'род']) and hyp_s == set([u'муж', u'ед', u'дат', u'неод'])
                   and bigram[1][u'text'][-1] == u'у')\
               or (hyp_a == set([u'мн', u'род']) and set([u'ед', u'род']).issubset(hyp_s)):
                return True

    # print bigram[0][u'text'] + u' ' + bigram[1][u'text'] + u'\n'              
##    print 'first: '
##    for hyp in first:
##        for el in hyp:
##            print el
##        print u'---------------------'
##    print 'second: '
##    for hyp in second:
##        for el in hyp:
##            print el
##        print u'---------------------'
##    print u'\n====================\n'
    return False


def hypothesis_collector(bigram):
    '''получает биграмму с анализом, собирает грамматическую информацию в одно место, делает её сопоставимой для 1 и 2 слов,
    возвращает два списка множеств. вызывается в agreement_checker'''
    hyp_a = [hyp.split(u',') for hyp in bigram[0][u'analysis'][0][u'gr'][2:].strip(u'()').split(u'|')]
    hyp_a_cleaned = [set([el for el in hyp if el not in (u'полн', u'устар')]) for hyp in hyp_a]
    
    info_s = bigram[1][u'analysis'][0][u'gr'].split(u'=')
    hyp_s = [u','.join([info_s[0], hyp]).replace(u'местн', u'пр').split(u',')[1:] for hyp in info_s[1].strip(u'()').split(u'|')]
    hyp_s_cleaned = [set([el for el in hyp if not (el in (u'жен', u'муж', u'сред') and u'мн' in hyp)
                          and el not in (u'фам', u'имя', u'полн', u'устар', u'обсц')]) for hyp in hyp_s]
    return hyp_a_cleaned, hyp_s_cleaned


def input_checker(word, translit = translit):
    '''получает слово, возвращает название файла и основу, если это похоже на русское прилагательное.
    вызывается в file_walker'''
    if word[-2:] not in [u'ый', u'ий', u'ой']:
            print word + u' : there is some mistake'
            return None
    else:
        transliterated = u''.join([translit[l] for l in word])
        # flections = [adj_fl_p if fl == u'ий' else adj_fl_np for fl in [word[-2:]]][0] # хорош баловаться с генераторами, сделай нормально
        if [word[-2:]] == u'ий':
            flections = adj_fl_p
        else:
            flections = adj_fl_np
        return word[:-2], transliterated, flections


def file_walker(words):
    '''получает на вход массив слов, для каждого слова запускает другие функции,
    которые обрабатывают файлы, возвращает массив частотных словарей'''
    dictionaries = []
    for word in words:
        if input_checker(word) is not None:
            base, transliterated, flections = input_checker(word)
            
            print transliterated + u'\nstart: ' + str(time.clock())

            try:
                a = cleaner(u'cleaned\\' + transliterated + u'.txt', base, flections = flections)
            except:
                a = cleaner(transliterated[:2], base, flections = flections)

            with codecs.open(u'C:\\google ngramms\\russian\\cleaned\\' + transliterated + u'.txt', u'w', u'utf-8') as quick:
                for el in a:
                    quick.write(el)
            # print u'after cleaner: ' + str(time.clock())
            analyzed = grammar_analyzer(year_merger(a))
            with codecs.open(u'C:\\google ngramms\\russian\\analyzed\\' + transliterated + u'-an.json', u'w', u'utf-8')as f:
                json.dump(analyzed, f, ensure_ascii=False, indent=2)
            d = final_dictionary(analyzed)
            dictionaries.append(d)
            with codecs.open(u'C:\\google ngramms\\russian\\dictionaries\\' + transliterated + u'-final.json', u'w', u'utf-8')as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
    return dictionaries


def vectores(dictionaries):
    '''читает файл с лексемами, запускает их в file_walker и составляет
    для каждой вектор. возвращает словарь, где ключ -- лексема, а значение -- вектор.
    главная функция'''

    collocates = set([col.split()[1] for d in dictionaries for col in list(d)])
    print u'length of all collocates: ' + str(len(collocates))
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
        print u'dict: ' + str(len(d))
        print u'vect: ' + str(len(vect))
    return vects


def main():
    with codecs.open('lexems.txt', u'r', u'utf-8') as f:
        words = [line.strip() for line in f.readlines()]
    dictionaries = file_walker(words)

    vects = vectores(dictionaries)
    for vec in vects:
        with codecs.open(u'vectors\\' + u''.join([translit[l] for l in vec]) + u'.json', u'w', u'utf-8') as f:
            # for num in vects:
            json.dumps(vec, f, ensure_ascii = False)

main()


##########
##to do:
##    -- написать bastard dealer (qual имплицирует bastard): spell-checker (Алёна)
##    -- подумать, что делать с образовательницней (ничего?)
##    -- субстантивированные прилагательные (как-нибудь надёжно пополнить их количество)
##    -- сделать что-то с умной животиной и "хитрых лис", "хитрого лиса"
##########
