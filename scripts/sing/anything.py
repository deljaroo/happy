import random
def call(**kwargs):
    args = kwargs['args']
    if len(args)==0:
        args = ["abcdefghijklmnopqrstuvwxyz", "aeiou", "aeiou"]
    song = ""
    last_space = 0
    words = 0
    while words<5:
        if random.randint(0,1000) < last_space:
            words += 1
            song += " "
            last_space = 0
        else:
            song += random.choice(random.choice(args))
            last_space += 1
            last_space *= 2
    print("*Happily sings " + song[:-1] + "*")