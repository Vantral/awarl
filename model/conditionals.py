import os
import pprint
import re
import xlsxwriter

def open_file(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
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


def patt():
    # CONTEXT:
    # If/if + NP context + will OR
    # If/if + NP context + would OR
    # If/if + NP context + V1 +  {[1,5] words + } {, + } NP context + would OR
    # NP context + would +  {[1,6] words + } if + NP context + V1
    fstart = '(?:<[iI]f\s...>)' + nounp() + '(?:<[will|would]\sV..>|<[^>]+?\sV[VB][BZ]>' + '(?:<[^>]+?\s...>){1,5}' +\
        '(?:<,\s...>)?' + nounp() + '<would\s...>)'

    sstart = nounp() + '<would\s...>' + '(?:<[^>]+?\s...>){1,6}' + '(?:<[iI]f\s...>)' + nounp() + '<[^>]+?\sV[VB][BZ]>'

    pattern = '(?:' + fstart + ')|(?:' + sstart + ')'
    return pattern

def search(pattern, directory = 'C:/Users/Антон/Desktop/awarl/new/'):
    bad_words = '|'.join(open_file('verbs.txt').split('\n')).lower()
    trg = '<that\s...>(?:<even\s...>)?<if\s...>'
    trg1 = '(?:<[^>]+?\sXX0>)?<(?:' + bad_words + ')\s...>(?:<even\s...>)?<if\s...>'
    trg2 = '(<(?:that|who|which)\s...>' + nounp() + '(?:<[^>]+?\sV..>){1.3}' + '(?:<,\s...>)?)' + nounp() + '<[^>]+?\sV..>'
    # print('<[that|' + bad_words + ']\s...>(?:<[^>]+?\s>){0,1}<if\s...>')
    errors = []
    folders = os.listdir(directory)
    for folder in folders:
        print(folder)
        files = os.listdir(directory + folder)
        for file in files:
            text = open_file(directory + folder + '/' + file)
            sentences = text.split('@')
            for sent in sentences:
                a = re.search(pattern, sent, flags=re.IGNORECASE)
                if a:
                    b = re.search(trg2, a.group())
                    if b:
                        sent = sent.replace(b.group(1), '')
                        print(b.group(1))
                    if not re.search(trg, sent) and not re.search(trg1, sent):
                        errors.append([re.sub('^\n', '', sent), file, folder])
                    #else:
                     #   print(re.search(trg, sent).group())

    return errors

def writeln(errors, filename):
    workbook = xlsxwriter.Workbook(filename)
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
    a = search(patt())
    writeln(a, 'conditionals.xlsx')

if __name__ == '__main__':
    main()