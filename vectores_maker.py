# -*- coding: utf-8 -*-

import codecs
import os
from pymystem3 import Mystem
import time
import json
import file_cleaner
import math

PATH = u'C:\\google ngramms\\russian\\'

FLECTIONS = [u'ый', u'ое', u'ая', u'ые', u'ого', u'ой', u'ых', u'ому',
             u'ым', u'ую', u'ою', u'ыми', u'ом',
             u'ий', u'ее', u'яя', u'ие', u'его', u'ей', u'их', u'ему',
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
             u'ю':u'u', u'я':u'a', u'ё': u'e'}

m = Mystem()

def cleaner(filename, base, flections = FLECTIONS, trash = stop_words_a):
    '''получает на вход название файла, содержащего биграммы, основу
    прилагательного и массив окончаний, возвращает словарь с биграммами, очищенными от мусора'''
    forms = [base + aff for aff in flections] + [base[0].upper() + base[1:] + aff for aff in flections]
##    for form in forms:
##        print(form)
    with codecs.open(filename,'r', u'utf-8') as f:

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
##    what_i_need = {bigram:(what_i_need[bigram]/float(total_utterances)) for bigram in what_i_need} # здесь абсолютное кол-во вхождений превращается в частотность
##    what_i_need = {bigram:(math.log(what_i_need[bigram])) for bigram in what_i_need}
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
    try:
        if 'qual' in [key for an in sec_word[u'analysis'] for key in an]\
           and sec_word[u'text'][-2:] == u'ию':
            sec_word[u'analysis'] = [{u'lex': u'учтивость', u'gr': u'S,жен,неод=твор,ед'}]
    except Exception as e:
        print(e)
##        exit()
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
    if not a:
##        print 'noooooooooo: ' + bigram[0][u'text'] + u' ' + bigram[2][u'text'] + u'\n'
    return True

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
    print 'agreement: ' + bigram[0][u'text'] + u' ' + bigram[1][u'text'] + u'\n'
    return False


def hypothesis_collector(bigram):
    '''получает биграмму с анализом, собирает грамматическую информацию в одно место, делает её сопоставимой для 1 и 2 слов,
    возвращает два списка множеств. вызывается в agreement_checker'''
    hyp_a = [hyp.split(u',') for hyp in bigram[0][u'analysis'][0][u'gr'][2:].strip(u'()').split(u'|')]
    hyp_a_cleaned = [set([el for el in hyp if el not in (u'полн', u'устар')]) for hyp in hyp_a]

    try:
        info_s = bigram[1][u'analysis'][0][u'gr'].split(u'=')
        hyp_s = [u','.join([info_s[0], hyp]).replace(u'местн', u'пр').split(u',')[1:] for hyp in info_s[1].strip(u'()').split(u'|')]
        hyp_s_cleaned = [set([el for el in hyp if not (el in (u'жен', u'муж', u'сред') and u'мн' in hyp)
                              and el not in (u'фам', u'имя', u'полн', u'устар', u'обсц')]) for hyp in hyp_s]
        return hyp_a_cleaned, hyp_s_cleaned
    except Exception as e:
        print(e)
        return [], []


def input_checker(word, translit = translit):
    '''получает слово, возвращает название файла и основу, если это похоже на русское прилагательное.
    вызывается в file_walker'''
    if u'#' not in word:
        if word[-2:] not in [u'ый', u'ий', u'ой']:
            print word + u' : there is some mistake'
            return None
        else:
            transliterated = u''.join([translit[l] for l in word])
            # flections = [adj_fl_p if fl == u'ий' else adj_fl_np for fl in [word[-2:]]][0] # хорош баловаться с генераторами, сделай нормально
########            if word[-2:] == u'ий':
########                flections = adj_fl_p
########            elif word[-2:] == u'ый' or [word[-2:]] == u'ой':
########                flections = adj_fl_np
########            else:
########                print([word[-2:]][0])
########                flections = ['aaaaaaa']
            return word[:-2], transliterated


def file_walker(words):
    '''получает на вход массив слов, для каждого слова запускает другие функции,
    которые обрабатывают файлы, возвращает массив частотных словарей'''
    dictionaries = []
    for word in words:
        if input_checker(word) is not None:
            base, transliterated = input_checker(word)
            
            print transliterated + u'\nstart: ' + str(time.clock())

            a = fastener(transliterated, base, PATH)

            with codecs.open(PATH + u'cleaned\\' + transliterated + u'.txt', u'w', u'utf-8') as quick:
                for el in a:
                    quick.write(el)
            analyzed = grammar_analyzer(year_merger(a))
            with codecs.open(PATH + u'\\analyzed\\' + transliterated + u'-an.json', u'w', u'utf-8')as f:
                json.dump(analyzed, f, ensure_ascii=False, indent=2)
            d = final_dictionary(analyzed)
            dictionaries.append(d)
            with codecs.open(PATH + u'\\dictionaries\\' + transliterated + u'-final.json', u'w', u'utf-8')as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            print transliterated + u'\nfinish: ' + str(time.clock())
    return dictionaries

def fastener(transliterated, base, path):
    try:
        do_not
        a = cleaner(path + u'cleaned/' + transliterated + u'.txt', base)
    except Exception as e:
        print(e)
        try:
            a = cleaner(path + 'bigrams_opencorpora', base)
        except Exception as e:
            print(e)



        
            try:
                a = cleaner(path + u'for_adjectives/' + transliterated[:2], base)
            except Exception as e:
                print(e)
                try:
                    file_cleaner.cleaner(path, transliterated[:2])
                    a = cleaner(path + transliterated[:2], base)
                except Exception as e:
                    a = []
                    print transliterated + str(e)
    return a


def main():
    with codecs.open('lexems.txt', u'r', u'utf-8') as f:
        words = [line.strip() for line in f.readlines()]
    dictionaries = file_walker(words)

main()


##########
##to do:
##    -- написать bastard dealer (qual имплицирует bastard): spell-checker (Алёна)
##    -- подумать, что делать с образовательницней (ничего?)
##    -- субстантивированные прилагательные (как-нибудь надёжно пополнить их количество)
##    -- сделать что-то с умной животиной и "хитрых лис", "хитрого лиса"
##########
