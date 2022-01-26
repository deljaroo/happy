import os
def call(**kwargs):
    """
    Takes one argument, a keyword that matches a directory "bookmark"
    This will change the active directory to the requested bookmark
    If the argument is "list", instead of cding it will list out all the current bookmarks
    """
    commands = kwargs['args'] # list of things typed up after the command that called this script; seperated by unquoted spaces
    if len(commands) < 1:
        print("Where would you like happy to take you?")
    elif len(commands) > 1:
        print("Too many arguments were given; Happy Hop needs exactly one argument.")
    else:
        bookmarks = {
            'cds': 'C:\\Users\\Joel\\Documents\\gitrepos\\cabells-design-system',
            'cmm': 'C:\\Users\\Joel\\Documents\\gitrepos\\cabells-marketing-medicine',
            'csc': 'C:\\Users\\Joel\\Documents\\gitrepos\\cabells-strapi-cms'
            }
        hop_to = commands[0]
        if hop_to=='list':
            print("*happily lists out Hop bookmarks*")
            for i in bookmarks:
                print(str(i) + "\t" + str(bookmarks[i]))
        elif hop_to not in bookmarks:
            print("Happy does not know that bookmark.  Try 'happy hop list' to see the list of options.")
        else:
            print("*happily hops you to that location*")
            path = kwargs['path'].replace('/','\\')
            os.system(path + "\\test.bat")