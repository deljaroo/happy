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

def runCommand(what):
    print("*happily runs the '" + what + "' command for you*")
    error_code = os.system(what)
    if error_code != 0:
        print("*happily reports error number " + str(error_code) + "*")
        return False
    return True

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
    def __init__(self, fm, tli, dir, subs):
        self.failure_message = fm
        self.too_little_information = tli
        self.directory = dir
        self.subs = {}
        self.subs['help'] = EU(self.startShowHelp, ("Shows help for this category","Can be used on any category"))
        self.subs['help+'] = EU(self.showRecursiveHelp, (
            "Shows help for this category and recursivly below it",
            "Can be used on any category",
            "Warning: it can be large sometimes"))
        self.hidden = ['help', 'help+']
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
        for i in self.hidden:
            if i in sub_keys:
                sub_keys.pop(sub_keys.index(i))
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
    def startShowHelp(self):
        print("*happily offers help*")
        self.showHelp()
        print("(Items with descriptions are commands; those without are ")
        print("categories, and you can use 'happy <category/categories> help'")
        print("to see what the bottom category mentioned can do.")
        print("Make sure you separate each category or command with a space.")
    def showRecursiveHelp(self):
        self.showHelp(recursive=True)
        
def importAll(parent, config_file = "happy.config"):
    class DataUnit:
        def __init__(self, raw_line):
            self.parent = None
            self.raw = line.rstrip()
            self.indent = len(line.rstrip()) - len(line.strip())
            self.stripped = line.strip()
            self._swe = False
            if self.stripped[0]=='!':
                self.stripped = self.stripped[1:]
                self._swe = True
            self.unit = None
        def isEU(self):
            return self._swe
        def isOU(self):
            return not self._swe
        def hasParent(self):
            return self.parent is not None
        def isMoreIndentedThan(self, other):
            return self.indent > other.indent
        def isLessIndentedThan(self, other):
            return self.indent < other.indent
        def isNotMoreIndentedThan(self, other):
            return self.indent <= other.indent
        def isNotLessIndentedThan(self, other):
            return self.indent >= other.indent
        def hasSameIndentAs(self, other):
            return self.indent == other.indent
        def _compooseAsOU(self):
            first_space = self.stripped.find(' ')
            name = self.stripped[:first_space]
            component = self.stripped[first_space+1:]
            pipe = component.find('|')
            atter = component.find('@')
            fm = ""
            tli = ""
            dir = ""
            if pipe>=0 and atter>pipe: # has both messages and action directory
                fm = component[:pipe]
                tli = component[pipe+1:][:atter-pipe-1]
                dir = component[atter+1:]
            elif pipe>=0: # has both messages but no action directory
                fm = component[:pipe]
                tli = component[pipe+1:]
            elif atter>=0: # single message with action directory
                fm = tli = component[:atter]
                dir = component[atter+1:]
            else: # single message with no action directory
                fm = tli = component
            work = OU(fm, tli, dir, {})
            self.unit = work
        def _composeAsEU(self):
            package_name = ""
            target = self
            while target.hasParent:
                pd = target.parent.directory
                if pd != "":
                    if package_name != "":
                        package_name += "."
                    package_name += pd
                target = target.parent
            imp = 'from ' + package_name + ' import ' + self.stripped
            exec(imp)
        def createUnit(self):
            if self.isEU():
                return self._composeAsEU()
            return self._compooseAsOU()
    data = []
    # grab all data
    with open(config_file) as opened:
        for line in opened:
            if line.strip() != "":
                data.append(DataUnit(line))
    # validate indents and assign parents
    for i in range(len(data)-1):
        first = data[i]
        second = data[i+1]
        if i==0:
            first.parent = parent
        if first.isOU():
            assert first.isLessIndentedThan(second), "OU on line " + str(i) + " is not followed by child"
        if first.isEU():
            assert first.isNotLessIndentedThan(second), "EU on line " + str(i) + " is followed by a child"
        if first.isMoreIndentedThan(second):
            matched = False
            for j in range(i, -1, -1): # counts down starting at first's index ending before -1 ie the last count will be 0
                if data[j].indent==second.indent:
                    matched = True
                    second.parent = data[j].parent
                    break
            assert matched, "Dedent on line " + str(i+1) + " does not match a previous dedent."
        elif first.isLessIndentedThan(second):
            second.parent = first
        else:
            second.parent = first.parent
    # build units and put them in the appropriate subs
    for i in data:
        i.createUnit()

def importAllOLD(parent, config_file = "happy.config"):
    arch = {}
    stack = [arch]
    active = arch # points to
    expecting_indent = False
    current_info = [{'sub': parent.subs, 'indent': 0, 'dir': "scripts"}]
    with open(config_file) as opened:
        for line_number, line in enumerate(opened):
            DEBUG = line + " "
            expected_indent = current_info[-1]['indent']
            indent_size = len(line) - len(line.lstrip())
            if expecting_indent:
                assert indent_size > expected_indent, "Expected indent on line " + str(line_number)
                DEBUG += "INDENT "
            else:
                if indent_size < expected_indent:
                    DEBUG += "DEDENT "
                    who = None
                    for which, indent in enumerate(current_info):
                        if indent_size == indent:
                            who = which
                            break
                    assert who is not None, "Un-indention size does not match any previous tier"
                    expected_size = who+1
                    to_remove = len(current_info) - expected_size
                    for _ in range(to_remove):
                        current_info.pop(-1)
            line = line.strip()
            name = ""
            new = None
            if line[0]=="!":
                line = line[1:]
                name = line
                expecting_indent = False
                path = ""
                for info in current_info:
                    if info['dir'] != '':
                        if len(path)>0:
                            path += "."
                        path+=info['dir']
                imp = "from " + path + " import " + name
                DEBUG += imp#exec(imp)
                function = None#exec(name)
                new = EU(function, function.__doc__)
            else:
                first_space = line.find(' ')
                name = line[:first_space]
                component = line[first_space+1:]
                fail = ""
                tli = ""
                dir = ""
                pipe = component.find("|")
                atter = component.find("@")
                if pipe>=0 and atter>pipe: # has both messages and action directory
                    fail = component.split("|")[0]
                    tli = component.split("|")[1].split('@')[0]
                    dir = component.split("|")[1].split('@')[1]
                elif pipe>=0: # has both messages but no action directory
                    fail = component.split("|")[0]
                    tli = component.split("|")[1]
                elif atter>=0: # single message with action directory
                    fail = tli = component.split("@")[0]
                    dir = component.split("@")[1]
                else: # single message with no action directory
                    fail = tli = component
                subs = {}
                new = OU(fail, tli, subs)
                current_info.append({'sub': subs, 'indent': indent_size, 'dir': dir})
                expecting_indent = True
            
            current_info[-2 if expecting_indent else -1]['sub'][name] = new
            


if __name__=="__main__":    
    outer_OU = OU("Happy does not know what that first word is; run happy help to see what can be said.",
        "*happy says 'hello' and is ready for your requests* (maybe try 'happy help'?)", "", {})
    importAll(outer_OU)
    outer_OU.hidden = ['sing'] # hides the demo group, sing, and unhides the help groups for this outer level
    outer_OU.activate(args)