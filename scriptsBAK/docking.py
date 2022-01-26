def inject(commands):
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
    
def bash(commands):
    if len(commands)<1:
        print("Happy needs to know the docker image name you wish to give the file to")
        return False
    if len(commands)>1:
        print("Happy doesn't know what to do with all that you've provided; only include a single docker image name")
        return False
    image = commands[0]
    ret = runCommand("docker exec -it " + image + " /bin/bash")
    return ret
    
def remind(commands):
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

if __name__=="__main__":
    print('this is a script file used by Happy Shortcuts and does nothing when run directly')