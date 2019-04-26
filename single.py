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
