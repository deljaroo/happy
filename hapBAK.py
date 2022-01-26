import sys
import os
import subprocess

if len(sys.argv)<3 or sys.argv[2] !='RanThruBat':
    raise SystemError("You must run happy through the batch script!")

args = sys.argv[3:]
evil_path = sys.argv[1]
good_path = evil_path.replace("\\", "/")

def showHelp():
    global outer_OU
    outer_OU.showHelp()
    return True

def fileExists(name):
    return os.path.isfile(good_path + "/" + name)

def runCommand(what, customize=False):
    """
    customize lets you overwrite the output
    the first output is merely dropped, and you can send a print before you send
    runCommand, the error message is replace with the string you put for 
    customize.  putting "|err" in the customize string will be replaced with
    the error number
    if you set customize to True, it will never report when there is an error
    code
    """
    if not customize:
        print("*happily runs the <" + what + "> command for you*")
    error_code = os.system(what)
    if error_code != 0 and customize is not True:
        if customize:
            print(str(customize.replace("|err", str(error_code))))
        else:
            print("*happily reports error number " + str(error_code) + "*")
        return False
    return True

def evilize(what):
    return what.replace("/", "\\")

class EU:
    def __init__(self, function, description):
        self.function = function
        self.description = description
    def isEU(self):
        return True
    def activate(self, commands):
        return self.function(commands)
    def showHelp(self, indent, last=False, _=None):
        for i in self.description:
            print(indent + "    " + i)

class OU:
    def __init__(self, fm, tli, subs):
        self.failure_message = fm
        self.too_little_information = tli
        self.subs = {}
        self.subs['help'] = EU(self.startShowHelp, ("Shows help for this category",))
        self.subs['help+'] = EU(self.showRecursiveHelp, (
            "Shows help for this category and recursivly below it",
            "Warning: it can be large sometimes"))
        for i in subs:
            self.subs[i.lower()] = subs[i]
    def isEU(self):
        return False
    def activate(self, commands):
        if len(commands)==0:
            print(self.too_little_information)
            return False
        if commands[0].lower() not in self.subs:
            print(self.failure_message)
            return False
        return self.subs[commands[0].lower()].activate(commands[1:])
    def showHelp(self, indent="", last=False, recursive=False):
        sub_keys = list(self.subs.keys())
        if 'sing' in sub_keys:
            sub_keys.pop(sub_keys.index('sing'))
        this_indent = "├── "
        next_indent = "│ "
        for i in range(len(sub_keys)):
            if i==len(sub_keys)-1:
                this_indent = "└── "
                next_indent = "  "
            tag = sub_keys[i]
            unit = self.subs[tag]
            if recursive and (i=='help' or i=='help+'):
                continue
            print(indent + this_indent + tag)
            if recursive or unit.isEU():
                unit.showHelp(indent + next_indent, False, recursive)
        return
        for i in sub_keys[:-1]:
            if i=='sing' or recursive and (i=='help' or i=='help+'):
                continue
            print(indent + "├── " + i)
            if recursive or self.subs[i].isEU():
                self.subs[i].showHelp(indent+"│ ", False, recursive)
        for i in sub_keys[-1:]:
            if i=="sing" or recursive and (i=='help' or i=='help+'):
                continue
            print(indent + "└── " + i)
            if recursive or self.subs[i].isEU():
                self.subs[i].showHelp(indent+ "  ", True, recursive)
    def startShowHelp(self, _):
        print("*happily offers help*")
        self.showHelp()
        print("(Items with descriptions are commands; those without are ")
        print("categories, and you can use 'happy <category/categories> help'")
        print("to see what the bottom category mentioned can do.")
        print("Make sure you separate each category or command with a space.")
    def showRecursiveHelp(self):
        self.showHelp(recursive=True)
        
def createNuxtTemplate(commands):
    bad = False
    if len(commands)<1:
        print("Happy needs a name for the template you want created.")
        bad = True
    if len(commands)>1:
        print("Happy does not like file names with spaces in them; try underscores or camel case?")
        bad = True
    if not fileExists('pageparts'):
        print("Happy was expecting a subdirectory named 'pageparts' to make the template in.")
        bad = True
    if not fileExists('pages'):
        print("Happy was expecting a subdirectory named 'pages'; are you sure you're in a Nuxt directory?")
        bad = True
    name = str(command[0])
    if fileExists('pages/' + name + ".vue"):
        print("Happy does not want to do this because it sees that you have a file named 'pages/" + name + ".vue'.")
        bad = True
    suffixes = ('.html', '.js', '.css')
    path = 'pageparts/' + name
    for i in suffixes:
        if fileExists(path + i):
            print("Happy does not want to overwrite files and '" + path + i + "' already exists.")
            bad = True
    if bad:
        return False
    for i in suffixes:
        with open(path + i, "w") as opened:
            opened.write("\n")
            print("*happily created '" + path + i + "'*")
    return True

def createGlobalShortcut():
    raise NotImplementedError

def dockerInject(commands):
    bad = False
    if len(commands)<1:
        print("Happy needs to know the docker image name you wish to give the file to")
        bad = True
    if len(commands)>1:
        print("Happy doesn't know what to do with all that you've provided; only include a single docker image name")
        bad = True
    if not fileExists('copyfile'):
        print("Happy expects there to be a file named 'copyfile' nearby for it to move")
        bad = True
    if bad:
        return False
    image = commands[0]
    ret = runCommand("docker cp " + good_path + "/copyfile " + image + ":/home/copyfile")
    return ret
    
def dockerBash(commands):
    if len(commands)<1:
        print("Happy needs to know the docker image name you wish to give the file to")
        return False
    if len(commands)>1:
        print("Happy doesn't know what to do with all that you've provided; only include a single docker image name")
        return False
    image = commands[0]
    ret = runCommand("docker exec -it " + image + " /bin/bash")
    return ret
    
def dockerPush(commands):
    print("*happily reminds you how to do this*")
    print('"')
    print("To see your image names and tags:")
    print("    docker images")
    print()
    print("To edit an image:")
    print("    docker run -d <image-name>:<tag>")
    print("-d is detached mode, and is optional")
    print("the :<tag> is also optional")
    print("and then use happy docker bash to manually edit and happy docker inject to give it a file")
    print("finally, commit it:")
    print("    docker commit <container ID> <new name>")
    print("you can use this to get the container ID (it's the gibbrish with the running one:)")
    print("    docker ps -a")
    print()
    print("YOU SHOULD ADD MORE AND LET THE USER WEED REMINDERS VIA COMMANDS")
    return True
    
def exploreHere(commands):
    if len(commands)>0:
        print("Happy doesn't know what you mean to explore; don't include any arguments")
        return False
    c = 'explorer.exe "' + evilize(good_path) + '"'
    print("*happily runs the <" + c + "> command for you*")
    ret = runCommand(c, customize=True)
    return ret

def makeBeep(commands):
    bad = False
    if len(commands)>2:
        print("Happy doesn't know what you want to do with all that information; maximum 2 arguments allowed")
        bad = True
    freq = 2000
    if len(commands)>0:
        try:
            freq = int(commands[0])
            if freq < 37:
                print("Happy cannot make sounds that low (37 minimum)")
                bad = True
            if freq > 32767:
                print("Happy cannot make sounds that high (32767 maximum)")
                bad = True
        except ValueError:
            print("Happy does not know how to make that in to a frequency")
            bad = True
    dur = 1000
    if len(commands)>1:
        try:
            dur = int(commands[1])
            if dur < 21:
                print("Happy cannot make sounds that short (21 minimum)")
                bad = True
            if dur > 3000:
                print("Happy refuses to make sounds for that long (3000 maximum)")
                bad = True
        except ValueError:
            print("Happy does not know how to make that in to a frequency")
            bad = True
    if bad:
        return False
    from winsound import Beep as beep
    print("*happily makes that beep*")
    beep(freq, dur)

def searchIt(commands): # doesn't work
    s = commands[0]
    work = "findstr /s /i /m " + s + " *"
    runCommand(work)

def cleanUpdates(commands):
    if len(commands)>0:
        print("Happy doesn't know what to do with arguments there.")
        return
    runCommand("net stop wuauserv & net stop bits & ren C:\\Windows\\SoftwareDistribution C:\\Windows\\SoftwareDistributionBAK & net start bits & net start wuauserv")

sing_fail = "Happy doesn't know what you are trying to have it sing like."
sing_pass = "*happily does its best to sing whatever that is*"
welcome = "*happy says 'hello' and is ready for your requests* (maybe try 'happy help'?)"


outer_OU = OU("Happy does not know what that first word is; run happy help to see what can be said.", welcome, {
    'create': OU("Happy does not know how to create that.", "Happy needs to know what you want to create", {
        'nuxttemplate': EU(createNuxtTemplate, (
            "Creates an html, ts and css file in a Nuxt subdirectory called pageparts to be used with vuebuild.py", 
            "Requires exactly one argument: the name of the file that vuebuild.py will eventually create sans .vue") ),
        'shortcut': EU(createGlobalShortcut, (
            "Creates a link to a command in System32 with an alias so it can be used often",
            "Requires exactly two arguments:  the alias wanted; the command",
            "REQUIRES ADMIN ACCESS"))
        }),
    'docker': OU("Happy doesn't know how to do that with docker", "Happy needs to know what you want to do with docker", {
        'inject': EU(dockerInject, (
            "Moves the 'copyfile' into a docker image and places it in /home",
            "Requires exactly one argument: the docker image name"
            )),
        'bash': EU(dockerBash, (
            "Opens up the bash internally inside a docker image",
            "Requires exactly one argument:  the docker image name"
            )),
        'remind': EU(dockerPush, (
            "Reminds you how to do it",
            ""
            ))
        }),
    'e': EU(exploreHere, (
        "Opens up Windows Explorer file manager at your current location",
        "No arguments"
        )),
    'beep': EU(makeBeep, (
        "Makes a simple beep noise",
        "Optional arguments to set the frequency (Hz) and duration (ms)"
        )),
    'cleanupdates': EU(makeBeep, (
        "Resets the current windows updates cache so that you can re-download the updates",
        "No arguments allowed."
        ))
    }
)
outer_OU.activate(args)