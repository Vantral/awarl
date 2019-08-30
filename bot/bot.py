import telebot, treetaggerwrapper, re, time

bot = telebot.TeleBot('703199230:AAGltbsQp2v_TS4esf4AF_e2C653ZiGiugQ')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')

def open_file(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    return text

def tagging(text):
    text = re.sub('\s\s', ' ', text)
    lines = re.sub('\.\s', '.\n', text)
    lines = re.sub('\?\s', '?\n', lines)
    lines = re.sub('!\s', '!\n', lines)
    sentences = lines.split('\n')
    text = ''
    for sentence in sentences:
        if sentence != '':
            l1 = sentence + '\n'
            tags = tagger.tag_text(sentence)

            sp = []
            for tag in tags:
                word, tag, lemma = tag.split(
                    '\t')
                nl = '<' + word + ' ' + tag + '>'
                sp.append(nl)
            spstr = ''.join(sp)
            l2 = spstr + '@' +'\n'
            text += l1
            text += l2
        #print(text)
    return text

def nounp():
    base = '(?:(?:(?:<[^>]+?\sAV0>)?(?:<[^>]+?\s(?:[DA][TP].|POS)>)?(?:<[^>]+?\sAV0>)?' +\
           '(?:<[^>]+?\s[DA]T.>)?(?:<[^>]+?\s.RD>)?(?:<[^>]+?\sAJ.>)?)*'
    #facultative attributes of NOUN
    dnoun = '(?:<[^>]+?\sN..>' + base + '<[^>]+?\sN..>))'
    # such as "college student"
    noun_phrase1 = base + '(?:<[^>]+?\s(?:N..|PN.)>))'
    #such as "actually the best extremely poor student"
    noun_phrase2 = base + dnoun + ')'
    #base and "college student"
    noun_phrase3 = base + '(?:' + dnoun + '|' + '(?:<[^>]+?\s(?:N..|PN.)>))' + '<[^>]+\sPRF>' +\
                   '(?:' + dnoun + '|' + '(?:<[^>]+?\s(?:N..|PN.)>)))'
    #constructions with "of" such as "a perfect piece of cake"
    noun_phrase10 = '(?:<[^>]+?>){0,4}(?:<[^>]+?\s(?:N..|PN.)>)'
    noun_phrase =  '(?:' + noun_phrase2 + '|' + noun_phrase1 + '|' + noun_phrase3 + ')'
    #print(noun_phrase)
    return noun_phrase

def patinv():
    #context Verb/aux + ,(?) + wh-word(+ whether + if) + aux + NP + VP
    start = '(?:<[^>]+?\sV..>)(?:,\sPUN)?(?:<[^>]+?\s(?:AVQ|PNQ|DTQ)>|<[whether|if]\s.+?>)(?:<[^>]+?\sV[B|D|H|M].>)'
    #1: all verbs, 2: comma, 3: wh-words + whether&if, 4: auxiliaries (be, do, have, modal)
    noun_phrase = nounp()
    verb = '(?:<[^>]+?\sV..>)'
    pattern = start + noun_phrase + verb
    return pattern

def inversion(text, id):
    errors = []
    new_errors = []
    sentences = text.split('@')
    for sent in sentences:
        if re.search(patinv(), sent, flags=re.IGNORECASE):
            errors.append(sent)
            for error in errors:
                error = re.search('.[^<]*', error).group()
                new_errors.append(error)
    if len(new_errors) != 0:
        #bot.send_message(id, 'Ошибки на инверсию в этих предложениях/There are mistakes on inversion in these sentences:\n\n' + '\n'.join(new_errors))
        return new_errors
    else:
        return False

def patprep():
    ##Prep + for example/for instance/maybe/however/possibly/probably +
    ##(Det (+ Adj)) N (in (,)for example (,)the course of syntax)

    start = '(?:<[^>]+\s(?:PR.|AVP)>)'
    verbs = open_file('trans.txt').split(', ')
    an_start = '(?:<' + '|'.join(verbs) + '>)'
    f_e = '(?:<for\s...><(?:example\s...>))'
    f_i = '(?:<for\s...><(?:instance\s...>))'
    mb = '(?:<maybe\s...>)'
    pr = '(?:<perhaps\s...>)'
    hw = '(?:<however\s...>)'
    psb = '(?:<possibly\s...>)'
    prb = '(?:<probably\s...>)'
    var = '|'.join([f_e, f_i, mb, pr, hw, psb, prb])
    p = '(?:' + start + '|' + an_start + ')' + '(?:' + nounp() + '?)' +  '(?:<,\sPUN>)?' + '(?:' + var + ')' + '(?:<,\sPUN>)?' + nounp()
    return p

def suchlike(errors):
    new_errors = []
    f_e = '(?:<for\s...><(?:example\s...>))'
    f_i = '(?:<for\s...><(?:instance\s...>))'
    mb = '(?:<maybe\s...>)'
    hw = '(?:<however\s...>)'
    psb = '(?:<possibly\s...>)'
    prb = '(?:<probably\s...>)'
    var = '|'.join([f_e, f_i, mb, hw, psb, prb])
    pattern = '(?:<such\s...><as\s...>|<like\s...>|<sum\s...><up\s...>)' + '(?:<,\sPUN>)?' + '(?:' + var + ')'
    for sent in errors:
        if not re.search(pattern, sent[0]):
            new_errors.append(sent)
        else:
            #print(sent)
            pass
    return new_errors

def prep(text, id):
    errors = []
    new_errors = []
    sentences = text.split('@')
    for sent in sentences:
        for clause in sent.split(';'):
            a = re.search(patprep(), clause, flags=re.IGNORECASE)
            if a:
                print(a.group())
                if 'DTQ>' not in a.group(0):
                    errors.append(sent)
    errors = suchlike(errors)
    for error in errors:
        error = re.search('.[^<]*', error).group()
        new_errors.append(error)
    if len(new_errors) != 0:
        #bot.send_message(id, 'Ошибки на вводные конструкции в этих предложениях/There are mistakes on parenthetical units in these sentences:\n\n' + '\n'.join(new_errors))
        return new_errors
    else:
        return False

def main_menu():
    mark_up = telebot.types.InlineKeyboardMarkup()
    item = telebot.types.InlineKeyboardButton(text='REALEC', url='realec.org')
    mark_up.add(item)
    item = telebot.types.InlineKeyboardButton(text='Проверить эссе/Check the essay', callback_data='2')
    mark_up.add(item)
    return mark_up

@bot.message_handler(commands=['start'])
def start_message(message):
    id = message.chat.id
    mark_up = main_menu()
    bot.send_message(id, 'Привет, я ADWISER!\nЯ создан, чтобы помочь тебе в написании эссе на английском языке.\nЧто ты хочешь сделать? Можешь посетить сайт REALEC или проверить своё эссе'
                         '\nHello, I\'m your ADWISER! I\'m ready to help you.\nYou can look at texts in REALEC or check your essay', reply_markup=mark_up)

@bot.callback_query_handler(func=None)
def gotit(message):
    id = message.from_user.id
    if message.data == '1':
        mark_up = telebot.types.InlineKeyboardMarkup()
        item1 = telebot.types.InlineKeyboardButton('Да/Yes', url='realec.org')
        item2 = telebot.types.InlineKeyboardButton('Нет/No', callback_data='3')
        mark_up.add(item1, item2)
        bot.send_message(id, 'А оно тебе надо?/Do you really need it?', reply_markup=mark_up)
    if message.data == '2':
        mark_up = telebot.types.ReplyKeyboardMarkup()
        item1 = telebot.types.KeyboardButton(text='I don\'t know what can I say now')
        item2 = telebot.types.KeyboardButton(text='I will go to, for example, America')
        mark_up.add(item1)
        mark_up.add(item2)
        bot.send_message(id, 'Вводи и отправляй! Я приготовился. (Можешь использовать готовые предложения)'
                             '\nSend it! I\'m ready. (You can use given sentences)', reply_markup=mark_up)
        @bot.message_handler()
        def errors(message):
            id = message.chat.id
            text = message.text
            ttext = tagging(text)
            a = inversion(ttext, id)
            b = prep(ttext, id)
            if not a:
                a = []
            if not b:
                b = []
            if len(a) == 0 and len(b) == 0:
                bot.send_message(message.chat.id, 'Я не нашёл ошибок. Ты молодец!'
                                            '\nThere is no mistakes. You are brilliant!')
            else:
                a.extend(b)
                bot.send_message(message.chat.id, 'В этих предложениях могут быть ошибки на порядок слов/\n'
                                 'There could be word order mistakes:\n\n' + ' '.join(a))
    if message.data == '3':
            bot.send_message(id, 'А что ты хочешь?/What do you want?', reply_markup=main_menu())

@bot.message_handler(commands=['sites'])
def sites(message):
    mark_up = telebot.types.InlineKeyboardMarkup()
    realec = telebot.types.InlineKeyboardButton('REALEC', url='realec.org')
    hse = telebot.types.InlineKeyboardButton('HSE', url='hse.ru')
    mark_up.add(realec, hse)
    bot.send_message(message.chat.id, 'Можешь перейти на сайт Высшей школы экономики и REALEC'
                                      '\nYou can visit the site of Higher School of Economics or REALEC', reply_markup=mark_up)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print('Error')
        time.sleep(3)