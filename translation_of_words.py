#!/usr/bin/env python3
import os
import re
import random
import shutil
WORD_TRANSLATE_SEPARATOR = ' -- '
TRANSLATE_SEPARATOR      = ','
DICTIONARY_PATH          = os.path.basename(__file__).replace('.py', '.dictionary')
COPY_DICTIONARY_PATH     = DICTIONARY_PATH + '.copy'
words                    = {}



def open_file (path, write = False):
    result = {'file': None, 'message': ''}
    try:
        if write:
            result['file'] = open(path, 'w+')
        else:
            result['file'] = open(path)
    except FileNotFoundError:
        result['file']    = False
        result['message'] = 'Файла словаря не существует!'
    except IOError:
        result['file']    = False
        result['message'] = 'Файл словаря не доступен'
    return result



def hendle_translate (translate):
    result = translate.strip(TRANSLATE_SEPARATOR)
    comma  = translate.find(TRANSLATE_SEPARATOR)
    if comma >= 0:
        result    = []
        translate = translate.split(TRANSLATE_SEPARATOR)
        for t in translate:
            result.append(t.strip(' \t'))
    return result



def read_words ():
    result = False
    file = open_file(DICTIONARY_PATH)
    if (file['file']):
        row = file['file'].readline()
        while row:
            word, translate = row.split(WORD_TRANSLATE_SEPARATOR)
            word        = word.strip(' \t')
            translate   = hendle_translate(translate.strip(' \t\n'))
            words[word] = translate
            row = file['file'].readline()
        result = True
    else:
        if file['message']:
            print(file['message'])
        else:
            print('Не удалось открыть файл ' + DICTIONARY_PATH)
    file['file'].close()
    return result



def write_words ():
    shutil.copyfile(DICTIONARY_PATH, COPY_DICTIONARY_PATH)
    file = open_file(DICTIONARY_PATH, write = True)
    if (file['file']):
        file['file'].seek(0)
        for w in words:
            row = ''
            if isinstance(words[w], str):
                row = w + WORD_TRANSLATE_SEPARATOR + words[w] + '\n'
            else:
                row = w + WORD_TRANSLATE_SEPARATOR + (TRANSLATE_SEPARATOR + ' ').join(words[w]) + '\n'
            file['file'].write(row)
    else:
        if file['message']:
            print(file['message'])
        else:
            print('Не удалось открыть файл ' + DICTIONARY_PATH)



def print_words ():
    print('\nСловарь\n' + ('-' * 15))
    for w in words:
        if isinstance(words[w], str):
            print(w + WORD_TRANSLATE_SEPARATOR + words[w])
        else:
            print(w + WORD_TRANSLATE_SEPARATOR + (TRANSLATE_SEPARATOR + ' ').join(words[w]))
    print(('-' * 15) + '\n\n')



def add_word ():
    msg  = 'Введите слово (или 0 для возврата к предыдущему меню): '
    word = (input(msg)).lower()
    while word in words and word != '0':
        word = (input('Слово "' + word + '" уже присутствует. ' + msg)).lower()
    if word != '0':
        translate = (input('Введите перевод для слова "' + word + '" (можно ввести несколько слов через запятую): ')).lower()
        words[word] = hendle_translate(translate)
        write_words()



def delete_word ():
    msg  = 'Введите слово из словаря ДЛЯ ЕГО УДАЛЕНИЯ (или 0 для возврата к предыдущему меню): '
    word = (input(msg)).lower()
    while word not in words and word != '0':
        word = (input('Слова "' + word + '" не существует в словаре. ' + msg)).lower()
    if word != '0':
        del words[word]
        write_words()



def change_word ():
    msg  = 'Введите слово, которое предполагается изменить (или 0 для возврата к предыдущему меню): '
    word = (input(msg)).lower()
    while word not in words and word != '0':
        word = (input('Слова "' + word + '" не существует в словаре. ' + msg)).lower()
    if word != '0':
        rewrite  = False
        new_word = ''
        while re.match('^[a-zA-Z]+(-[a-zA-Z]+)*$', new_word) is None:
            new_word = ((input('Введите слово вместо "' + word + '", если хотите его изменить (если не хотите его менять просто нажмите Enter): ')).strip()).lower()
            if new_word == '':
                break
        if new_word and new_word != word:
            rewrite         = True
            words[new_word] = words[word]
            del words[word]
            word = new_word
        translate = (input('Введите перевод для слова "' + word + '" (можно ввести несколько слов через запятую или можно просто нажать Enter, если не хотите менять перевод): ')).lower()
        if translate:
            rewrite     = True
            words[word] = hendle_translate(translate)
        if rewrite:
            write_words()



def test_knowledge ():
    print('=' * 80)
    words_len = len(words)
    if words_len:
        num       = 0
        size_msg  = 'Введите количество проверяемых слов (не менее 1 и не более ' + str(words_len) + '): '
        while num <= 0 or num > words_len:
            num = int(input(size_msg))
        words_keys = list(words.keys())
        test_keys  = []
        i          = 0
        while i < num:
            i_key = int(random.random() * (len(words_keys) - 1))
            test_keys.append(words_keys[i_key])
            del words_keys[i_key]
            i += 1
        
        test_dictionary = {}
        num_words       = int(random.random() * num)
        if num_words:
            i = 0
            while i < num_words:
                i_key = int(random.random() * len(test_keys))
                key   = test_keys[i_key]
                test_dictionary[key] = words[key]
                del test_keys[i_key]
                i += 1
        for key in test_keys:
            if isinstance(words[key], str):
                test_dictionary[key] = words[key]
            else:
                last_translates = len(words[key]) - 1
                translate_r = int(random.random() * last_translates)
                translate = words[key][translate_r]
                if translate_r == 0:
                    translate += ' (' + ', '.join(words[key][1:]) + ')'
                elif translate_r == last_translates:
                    translate += ' (' + ', '.join(words[key][:last_translates]) + ')'
                else:
                    translate += ' (' + ', '.join(words[key][:last_translates] + words[key][last_translates + 1:]) + ')'
                test_dictionary[translate] = key
        
        print('Вам по очереди будут выведены слова для перевода. В ответ вы должны будете указать одно слово перевода (или нажать Enter если не знаете перевода).\n')
        test_keys   = test_dictionary.keys()
        points      = {'success': 0, 'error': 0, 'empty': 0}
        msg_success = 'Все верно.'
        msg_error   = 'Вы ошиблись.'
        indent      = 1
        i = 1
        for key in test_keys:
            if isinstance(test_dictionary[key], str) and (test_dictionary[key] in words):
                if isinstance(words[test_dictionary[key]], str):
                    hint = test_dictionary[key] + ' -- ' + words[test_dictionary[key]]
                else:
                    hint = test_dictionary[key] + ' -- ' + (TRANSLATE_SEPARATOR + ' ').join(words[test_dictionary[key]])
            else:
                if isinstance(test_dictionary[key], str):
                    hint = key + ' -- ' + test_dictionary[key]
                else:
                    hint = key + ' -- ' + (TRANSLATE_SEPARATOR + ' ').join(test_dictionary[key])
            
            answer_num = str(i) + ') '
            answer     = (input(answer_num + key + ': ')).lower()
            answer_e   = answer.replace('ё', 'е')
            if answer:
                indent = len(answer_num)
                if isinstance(test_dictionary[key], str):
                    if (answer == test_dictionary[key]) or (answer_e == test_dictionary[key]):
                        print((' ' * indent) + '\033[1;32m' +  msg_success + ' (' + hint + ')\033[0m\n')
                        points['success'] += 1
                    else:
                        print((' ' * indent) + '\033[1;31m' +  msg_error + ' (' + hint + ')\033[0m\n')
                        points['error'] += 1
                else:
                    if (answer in test_dictionary[key]) or (answer_e in test_dictionary[key]):
                        print((' ' * indent) + '\033[1;32m' +  msg_success + ' (' + hint + ')\033[0m\n')
                        points['success'] += 1
                    else:
                        print((' ' * indent) + '\033[1;31m' +  msg_error + ' (' + hint + ')\033[0m\n')
                        points['error'] += 1
            else:
                print((' ' * indent) + '\033[3m' + '(' + hint + ')\033[0m\n')
                points['empty'] += 1
            i += 1
        
        separator = '\n' + (' ' * indent)
        print('Результат:' + separator + separator.join(['Правильных ответов: ' + str(points['success']), 'Ошибок: ' + str(points['error']), 'Пропущенных ответов: ' + str(points['empty'])]) + '\n')
    else:
        print('Нечего проверять. Словарь пуст.')
    print('=' * 80)



def main ():
    if read_words():
        if len(words) and os.path.exists(COPY_DICTIONARY_PATH):
            os.remove(COPY_DICTIONARY_PATH)
        
        item_separator = '\n  * '
        c_m1 = '-1 -- вывести словарь'
        c_0  = '0 -- выход из программы'
        c_1  = '1 -- удалить слово из словаря'
        c_2  = '2 -- добавить новое слово'
        c_3  = '3 -- изменить уже добавленное слово'
        c_4  = '4 -- проверить свои знания'
        action_msg = 'Введите номер команды:' + item_separator + (item_separator.join([c_m1, c_0, c_1, c_2, c_3, c_4])) + '\n  > '
        action = int(input(action_msg))
        while action:
            if action is -1:
                print_words()
            elif action is 1:
                delete_word()
            elif action is 2:
                add_word()
            elif action is 3:
                change_word()
            elif action is 4:
                test_knowledge()
            action = int(input(action_msg))

main()
exit()