import os
def call(**kwargs):
    """
    This tool ignores all arguments given to it.
    It opens File Explorer already showing the same location you are in the command line
    """
    args = kwargs['args']
    path = kwargs['path'].replace('/','\\')
    print("*happily opens File Explorer for you at your current location*")
    error_code = os.system("explorer.exe "+path)
    if error_code!=1:
        print("Happy reports an error of " + str(error_code))
        print("Happy isn't sure what that means")