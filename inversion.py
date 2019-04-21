import re, os, pprint, xlsxwriter

def open_file(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    return text

def nounp():
    base = '(?:(?:(?:<[^>]+?\sAV0>)?(?:<[^>]+?\s(?:[DA][TP].|POS)>)?(?:<[^>]+?\sAV0>)?' +\
           '(?:<[^>]+?\s[DA]T.>)?(?:<[^>]+?\sAJ.>)?)*'
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
    ##print(noun_phrase)
    return noun_phrase

def patt():
    #context Verb/aux + ,(?) + wh-word(+ whether + if) + aux + NP + VP
    start = '(?:<[^>]+?\sV..>)(?:,\sPUN)?(?:<[^>]+?\s(?:AVQ|PNQ|DTQ)>|<[whether|if]\s.+?>)(?:<[^>]+?\sV[B|D|H|M].>)'
    #1: all verbs, 2: comma, 3: wh-words + whether&if, 4: auxiliaries (be, do, have, modal)
    nounp = noun_phrase()
    verb = '(?:<[^>]+?\sV..>)'
    pattern = start + noun_phrase + verb
    return pattern

def search(pattern):
    errors = []
    directory = 'C:/Users/Prestigio/Desktop/awarl/new/'
    folders = os.listdir(directory)
    directory += '/'
    for folder in folders:
        print(folder)
        files = os.listdir(directory + folder)
        for file in files:
            text = open_file(directory + folder + '/' + file)
            sentences = text.split('@')
            for sent in sentences:
                if re.search(pattern, sent):
                    errors.append([re.sub('^\n', '', sent), file, folder])
    return errors

def writeln(errors):
    workbook = xlsxwriter.Workbook('inversion.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for error in errors:
        worksheet.write(row, col, error[0])
        worksheet.write(row, col + 1, error[1])
        worksheet.write(row, col + 2, error[2])
        row += 1
    workbook.close()

def main():
    nounp()

if __name__ == '__main__':
    main()
