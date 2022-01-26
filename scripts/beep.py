def call(**kwargs):
    """
    This tool makes a beeping noise.
    By default, it makes a one second long beep at a fequency of 2000.
    You may provide up to two arguments.
    The first will overwrite the fequency.  It must be a number between 37 and 32767.  These are Hertz.
    The second will overwrite the duration.  It must be a number between 21 and 3000.  These are milliseconds.
    If you only include one argument, it will overwrite the frequency so if you want to change the duration but not the
    frequency, use 'happy beep 2000 ' followed by your intended duration.
    """
    commands = kwargs['args']
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
            print("Happy does not know how to make that in to a duration")
            bad = True
    if bad:
        return False
    from winsound import Beep as beep
    print("*happily makes that beep*")
    beep(freq, dur)