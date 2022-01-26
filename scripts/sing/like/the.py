def call(**kwargs):
    """
        Just a test tool
    """
    args = kwargs['args']
    if len(args)==0:
        print("Happy crys out: 'the WHAT' 'WHAT DO YOU WANT ME TO SING LIKE'")
    else:
        work = ""
        for i in args:
            work += i + " "
        print("*Happily sings like the " +work[:-1]+ "*")