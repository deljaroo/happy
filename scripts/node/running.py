import os
def call(**kwargs):
    """
    No arguments.
    Lists out if any node processes are currently running
    """
    commands = kwargs['args'] # list of things typed up after the command that called this script; seperated by unquoted spaces
    path = kwargs['path'].replace('/','\\')
    print("*happily lists what node is running*") # initial output has a short version of what it does
    to_execute = "tasklist | find /i \"node\""
    error_code = os.system(to_execute)