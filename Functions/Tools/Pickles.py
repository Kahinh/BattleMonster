import lib

def LoadPickle(FileName, mode="Liste"):
    try:
        with open(FileName, 'rb') as picklefile:
            data = lib.pickle.load(picklefile)
            picklefile.close()
    except:
        if mode == "Liste":
            data = []
        elif mode =="Dict":
            data = {}
        elif mode == "Str":
            data = ""

    return data

def DumpPickle(FileName, data):
    with open(FileName, 'wb') as picklefile:
        lib.pickle.dump(data, picklefile)
        picklefile.close()