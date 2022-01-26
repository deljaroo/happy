import subprocess, os

def yesNo(ink, good=('yes', 'y', 'no', 'n')):
    """
    A little tool for checking if user-input is yes or no (or y/n)
    The purpose of this is hard to explain, see doThis() for an example
    you can override what is considered a valid answer by using the good keyword
    """
    return ink.lower() not in good
    
def doThis(prompt="Continue?"):
    """
    Prompts the user (in the terminal) a yes or no question.
    Will loop until they say either yes or no (y/n is also fine)
    prompt:  what to say in the prompt
    returns True if they said yes, False if they said no
    """
    ink = ""
    while yesNo(ink):
        ink = input(prompt + " ").lower()
    return ink=='yes' or ink=='y'

def attempt(command):
    completed_process = subprocess.run(command, shell=True, capture_output=True)
    ret = str(completed_process.stdout)[2:-1]
    return ret

def call(**kwargs):
    """
    One argument:  the version name of the deploy you want to make
    Handles all the steps for getting cds deployed on a new tag
    """
    commands = kwargs['args'] # list of things typed up after the command that called this script; seperated by unquoted spaces
    path = kwargs['path'].replace('/','\\')
    print("*happily starts this process, but may need your help along the way*") # initial output has a short version of what it does
    REPO_NAME = "cabells-design-system"
    RNL = len(REPO_NAME)
    if path[-RNL:] != REPO_NAME:
        print("This is not the design system.  Please navigate to the design system before you run this.")
        return
    DEPLOY_PATH = path + "\\..\\cabells-design-system-deploy"
    if not os.path.isdir(DEPLOY_PATH):
        print("The deploy directory is missing.  Please clone the cabells-desing-system-deploy as a sibling to this directory.")
        return
    print("Pulling current cdsd...")
    print(attempt('git -C "'+ DEPLOY_PATH +'" pull master'))
    if not doThis("Keep going?"):
        return
    