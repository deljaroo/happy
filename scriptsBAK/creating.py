def nuxtTemplate(commands):
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

def shortcut():
    raise NotImplementedError


if __name__=="__main__":
    print('this is a script file used by Happy Shortcuts and does nothing when run directly')