def call(**kwargs):
    """
    What arguments does it need?
    What does it do?
    """
    commands = kwargs['args'] # list of things typed up after the command that called this script; seperated by unquoted spaces
    path = kwargs['path'].replace('/','\\')
    print("*happily ...*") # initial output has a short version of what it does
    pass # do stuff