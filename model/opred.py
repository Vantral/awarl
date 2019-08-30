import inversion, os, pprint, xlsxwriter, re


def search(pattern, directory = 'C:/Users/Prestigio/Desktop/awarl/new/'):
    errors = []
    folders = os.listdir(directory)
    for folder in folders:
        print(folder)
        files = os.listdir(directory + folder)
        for file in files:
            text = inversion.open_file(directory + folder + '/' + file)
            sentences = text.split('@')
            for sent in sentences:
                errexp = re.search(pattern, sent, flags=re.IGNORECASE)#!
                if errexp:#re.search(pattern, sent, flags=re.IGNORECASE)
                    errors.append([re.sub('^\n', '', sent), file, folder, errexp.group()])#!
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
        worksheet.write(row, col + 3, error[3])#!
        row += 1
    workbook.close()

def patt():

    addExp = '(?:<[^>]+\s(?<!ing )(?<!<due )(?:AJ0)>)'
    
    
    aux = '(?<!VBB>)(?<!VBZ>)(?<!VBD>)(?<!VBG>)(?<!VBI>)(?<!VBN>)(?<!VDB>)(?<!VDD>)(?<!VDG>)(?<!VDI>)(?<!VDN>)(?<!VDZ>)(?<!VHB>)(?<!VHD>)(?<!VHG>)(?<!VHI>)(?<!VHN>)(?<!VHZ>)(?<!VM0>)'

    
    exp0 = '(?:<[^>]+\s(?:AT0|DPS)>)?'+ aux + '(?:' + addExp + '|(?:<[^>]+\s(?:AJC|AJS|VBN|VDN|VHN|VVN)>))(?:(?:<[^>]+\s(?:PRF|PRP)>)|(?:<than+\s...>))' # without ing
    exp1 = '(?:<[^>]+\s(?:DPS)>)?'+ aux + '(?:' + addExp + '|(?:<[^>]+\s(?:AJC|AJS|VBN|VDN|VHN|VVN|VBG|VDG|VHG|VVG)>))(?:(?:<[^>]+\s(?:PRF|PRP)>)|(?:<than+\s...>))' # without articles
    exp2 = '(?:<[^>]+\s(?:AT0|DPS)>)?'+ aux + '(?:' + addExp + '|(?:<[^>]+\s(?:AJC|AJS|VBN|VDN|VHN|VVN|VBG|VDG|VHG|VVG)>))(?:(?:<[^>]+\s(?:PRP)>)|(?:<than+\s...>))' #without of
    final_exp = '(?:'+ exp0 +'|'+ exp1 +'|'+ exp2 +')'
    res = final_exp + inversion.nounp() + inversion.nounp()
    return res

def sssort(getf):
    for spisok in getf:
        list_of_words = re.findall('<[^>]*>', spisok[0], flags=re.IGNORECASE)
        err = re.search(patt(), spisok[0], flags=re.IGNORECASE).group()
        list_of_words_in_err = re.findall('<[^>]*>', err, flags=re.IGNORECASE)
        for i in range(len(list_of_words)):
            if list_of_words[i] == list_of_words_in_err[0] and list_of_words[i+1] == list_of_words_in_err[1] and i >= 2 :
                # print('last word in err', list_of_words_in_err[-1])
                if list_of_words_in_err[-1].endswith('PNQ>'):
                    # print('ENDS WITH PNQ')
                    getf.remove(spisok)
                    # break
                elif list_of_words[i-1].endswith('AV0>'):
                    regexp = '(?:VBB|VBZ|VBD|VBG|VBI|VBN|VDB|VDD|VDG|VDI|VDN|VDZ|VHB|VHD|VHG|VHI|VHN|VHZ|VM0)'
                    if re.search(regexp, list_of_words[i-2], flags=re.IGNORECASE):
                        getf.remove(spisok)
                break
    



def main():
    getf = search(patt(), 'C:/Users/Asus/Desktop/OI/new/')
    #print(len(getf))
    sssort(getf)           
    writeln(getf, 'table.xlsx')
    #pprint.pprint(getf)
    print(len(getf))


if __name__ == '__main__':
    main()
