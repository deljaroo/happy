def call(**kwargs):
    args = kwargs['args']
    if len(args)==0:
        print("What do you want Happy to sing like?")
    else:
        work = ""
        for i in args:
            work += i + " "
        print("*Happily sings like " +work[:-1]+ "*")