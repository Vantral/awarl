import inversion, os, pprint, xlsxwriter, re
from inversion import nounp, writeln, open_file

def pattern():
    ##Prep + for example/for instance/maybe/however/possibly/probably +
    ##NP (in (,)for example (,)the course of syntax)

    start = '(?:<[^>]+\s(?:PR.|AVP)>)'
    verbs = open_file('trans.txt').split(', ')
    an_start = '(?:<(?:' + '|'.join(verbs) + ')\s[^N]..>)'
    f_e = '(?:<for\s...><(?:example\s...>))'
    f_i = '(?:<for\s...><(?:instance\s...>))'
    mb = '(?:<maybe\s...>)'
    pr = '(?:<perhaps\s...>)'
    hw = '(?:<however\s...>)'
    psb = '(?:<possibly\s...>)'
    prb = '(?:<probably\s...>)'
    var = '|'.join([f_e, f_i, mb, pr, hw, psb, prb])
    p = '(?:' + start + '|' + an_start + ')' + '(?:<,\sPUN>)?' + '(?:' + var + ')' + '(?:<,\sPUN>)?' + '(' + nounp() + ')'
    return p

def search(pattern, directory = 'C:/Users/Prestigio/Desktop/awarl/new/'):
    errors = []
    folders = os.listdir(directory)
    for folder in folders:
        print(folder)
        files = os.listdir(directory + folder)
        for file in files:
            text = open_file(directory + folder + '/' + file)
            sentences = text.split('@')
            for sent in sentences:
                for clause in sent.split(';'):
                    a = re.search(pattern, clause, flags=re.IGNORECASE) 
                    if a:
                        if 'DTQ>' not in a.groups(1)[0]:
                            errors.append([re.sub('^\n', '', sent), file, folder])
    return errors

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


def main():
    a = search(pattern())
    b = suchlike(a)
    writeln(b, 'for_example.xlsx')
    #pprint.pprint(b)
    #print(len(b))

if __name__ == '__main__':
    main()
