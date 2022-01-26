import os
def call(**kwargs):
    """
    Requires one argument:  the string to find
    A second argument is optional: searches in the given subdirectory instead
    
    This tool looks in all the files, and recursively in folders, for the given
    string and lists out all the files that have that string in them.
    """
    args = kwargs['args']
    path = kwargs['path'].replace('/','\\')
    subdirectory = "*"
    if len(args)<1:
        print("Happy needs to know what you are searching for")
        return
    if len(args)>2:
        print("Happy only wants two arguments so the extras will be ignored")
    if len(args)>1:
        if os.path.isdir(path + "\\" + args[1]):
            subdirectory = args[1] + "\\*"
        else:
            print("Happy cannot find that subdirectory.")
            return
    print("*happily searches for that text*")
    to_execute = 'cd ' + path + ' & findstr /simc:"'+ args[0] + '" ' + subdirectory
    # print(to_execute)
    error_code = os.system(to_execute)
    if error_code==1:
        print("Happy couldn't find anything.")
        return
    if error_code!=0:
        print("Happy reports an error of " + str(error_code))
        print("Happy isn't sure what that means")