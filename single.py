def new_search(pattern, directory = 'C:/Users/Prestigio/Desktop/awarl/new/'):
    errors = []
    folders = os.listdir(directory)
    for folder in folders:
        print(folder)
        files = os.listdir(directory + folder)
        for file in files:
            text = open_file(directory + folder + '/' + file)
            sentences = text.split('@')
            for sent in sentences:
                if '?' in sent:
                    a = re.search(pattern, sent, flags=re.IGNORECASE)       
                    if a:
                        if len(a.groups()[0].split('><')) > 1:
                            errors.append([re.sub('^\n', '', sent), file, folder])
    return errors
