Сейчас прамма vectores_maker делает следующее:
берёт файл lexems.txt со списком лексем и (помимо промежуточных результатов) создаёт файлы с векторами для поданных лексем


file_walker:
-- обходятся файлы для поданного на вход массива лексем. функция устроена так, что, если она находит файл с уже отброшенным шумом (если лексема уже анализировалась, такой файл был создан как промежуточный результат), то берёт для анализа его, что в 500-10000 раз сокращает время обработки лексемы;

cleaner:
-- отброшены слова с морф.разбором;
-- выбраны только биграммы после 1929 года;
-- выбраны только биграммы, где первое слово -- словоформа искомого;
-- отброшены биграммы, где второе слово -- явно какой-то мусор (знаки препинания, предлоги, союзы и т.д.)
-- отброшены биграммы, где второе слово начинается с апперкейса;

year_merger:
-- биграммы смёрджены по годам;

grammar_analizer:
-- морф. анализ майстемом;

final_dictionary:

    pos_checker:
    -- отбрасываются биграммы, где второе слово -- не (существительное или субстантивированное прилагательное);

    agreement_checker:
    -- проверяется согласование, с учётом:
    	-- второго генитива
    	-- конструкций типа "четыре умных человека"
    	-- второго предложного
    	-- двуродовых слов;

    -- биграммы лемматизированы;

vectores:
-- для лексем создаются вектора

Проблемы и недоделанное:
проблема с согласованием:

-- майстем считает, что животина -- сущ. мужского рода, поэтому такие словосочетания отбрасываются; проблема в том, что я не очень понимаю, в чём дело, и есть ли ещё такие случаи;

-- в биграмме "хитрого лиса" лиса по умолчанию -- номинатив женского рода. я не знаю, насколько сильное искажение могут давать такие случаи. и нужно ли с ними бороться;

-- в биграмме "хитрых лис" такая же проблема, только с мужским родом.