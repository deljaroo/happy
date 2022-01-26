import sys
import os
import re
from glob import glob

# reserved words
RESERVED = {"False","break","for","not","None","class","from","or","True","continue","global","pass","__peg_parser__","def","if","raise","and","del","import","return","as","elif","in","try","assert","else","is","while","async","except","lambda","with","await","finally","nonlocal","yield"}

# build all the regex we need
valid_shortcut_list = re.compile('^([a-zA-Z,_-]|,\s)+$')
valid_shortcut_answer = re.compile('^[a-zA-Z_-]+$')

# check if this is run through the batch script
# (you can bypass this by putting 'RanThruBat' as the thrid thing (second argument) when running
# but then the path being ran will not be pulled and will use the second thing (first argument)
# as the path
if len(sys.argv)<3 or sys.argv[2] !='RanThruBat':
    raise SystemError("You must run happy through the batch script!")

home_dir = sys.argv[0][:-6].replace("\\", "/") # the location of this script
args = sys.argv[3:] # arguments not including the dir, path and batch-check
evil_path = sys.argv[1] # the path given by the batch script, contains backslashes
good_path = evil_path.replace("\\", "/") # to not include backslashes

######### here are all the functions we might need #########

def fileExists(name):
    return os.path.isfile(good_path + "/" + name)

def isScript(path):
    return os.path.isfile(path)

def isScriptDirectory(path):
    return os.path.isdir(path)

def evilize(what):
    return what.replace("/", "\\")

def printPlainHelp():
    raise NotImplementedError # TODO

def printDirectoryHelp(directory):
        
    in_current_dir = os.listdir(directory)
    print("Happy doesn't have detailed help about that topic, but try one of these arguments:")
    if isScript(directory + "/default.py"):
        in_current_dir.remove("default.py")
    for i in in_current_dir:
        if '__' in i:
            continue
        if os.path.isdir(directory + "/" + i):
            print("   ", i)
        if i[-3:]=='.py':
            print("   ",i[:-3])

def printSpecificHelp(func):
    if func.__doc__:
        print("*Happily gets you the help information for that tool*")
        print(func.__doc__)
    else:
        print("Happy doesn't know how to help with that.  Please contact the develop of that script to have them add that.")


def callTool(directory, args):
    if len(args)==0:
        if isScript(directory + "/default.py"):
            callTool(directory, ['default'])
        else:
            print("Happy needs you to be more specific")
    else:
        next = args[0]
        if next in RESERVED:
            sys.exit("Happy cannot run commands with the word '" + next + "' in them.  If that is really needed, please contact the developer of that script to have them fix the error.")
        if isScript(directory + "/" + next + ".py"):
            exec("import " + directory.replace("/", ".") + "." + next + " as our_tool")
            try:
                if len(args)==2 and args[1]=='help':
                    exec("printSpecificHelp(our_tool.call)")
                else:
                    exec("our_tool.call(args=args[1:], path=good_path)")
            except AttributeError:
                sys.exit("Happy reports an error with that tool.  Please contact the developer of that script to have them fix the error.")
        elif isScriptDirectory(directory + "/" + next):
            callTool(directory + "/" + next, args[1:])
        else:
            if next=='help':
                printDirectoryHelp(directory)
            elif isScript(directory + "/default.py"):
                new_args = ['default'] + args
                callTool(directory, new_args)
            else:
                print("Happy doesn't know how to '" +next+ ".'  Check your spelling perhaps? Or try using 'happy help'.")

######### function section end #########

# check if the user didn't tell happy what to do
if len(args)==0:
    sys.exit("Happy would be happy to help.  Try 'happy help' if you are not sure what to do.")
# check if the user is requesting help
if args[0]=='help':
    if len(args)==1:
        printPlainHelp() # when 'happy help' is typed
    else:
        args = args[1:] + [args[0]] # makes 'happy help <stuff>' be the same as 'happy <stuff> help'

# check if the user ever used double underscores (which is not allowed)
for i in args:
    if '__' in i:
        sys.exit("Happy hates double-underscores.  DON'T")

# check for the required file structure
if not os.path.isdir('scripts'):
    sys.exit("Scripts directory is missing")

# make our shortcuts
shortcuts = {}
if os.path.isfile('scripts/shortcuts.config'):
    with open('scripts/shortcuts.config', 'r') as opened:
        for index, line in enumerate(opened):
            line_array = line.split(':')
            if len(line_array) != 2:
                sys.exit("error in shortcuts config file\non line " +str(index)+ "\neach line should contains exactly one colon")
            if valid_shortcut_list.match(line_array[0])==None:
                sys.exit("error in shortcuts config file\non line " +str(index)+ "\ncontent before colon invalid")
            if line_array[0] in RESERVED:
                sys.exit("error in shortcuts config file\non line "+str(index)+"\ncontent before colon contains reserved word")
            if valid_shortcut_answer.match(line_array[1])==None:
                sys.exit("error in shortcuts config file\non line " +str(index)+ "\ncontent after colon invalid")
            shortcut_list = line_array[0].split(',')
            for i in shortcut_list:
                stripped = i.strip()
                if stripped in RESERVED:
                    sys.exit("error in shortcuts config file\non line " +str(index)+ "\ncontent after colon invalid contains a reserved word")
                if stripped in shortcuts:
                    print("warning in shortcuts config file\non line " +str(index))
                    print("duplicate shortcut: " + stripped)
                    print("using first instance: " + shortcuts[stripped])
                else:
                    shortcuts[stripped] = line_array[1].strip()

# replace all the args that are shortcuts with their full version of the arg
for i in range(len(args)):
    if args[i] in shortcuts:
        args[i] = shortcuts[args[i]]

# start it
callTool('scripts', args)