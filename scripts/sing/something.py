def call(**kwargs):
    """
    This is a testing tool for hap.py
    Arguments are optional, and this will merely output some text.
    """
    args = kwargs['args']
    if len(args)==0:
        print("Happy doesn't know what to sing :(")
    else:
        song = ""
        for i in args:
            song += str(i) + " "
        print("*Happily sings '" +song[:-1]+ "' over and over*")