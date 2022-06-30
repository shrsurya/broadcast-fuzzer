import atheris
import sys

with atheris.instrument_imports():
    import idna



def TestOneInput(data):
    global counter
    global filetype
    path = "./FuzzedData/" + filetype + "/" + str(counter) + "." + filetype
    file = open(path, "w")
    file.write("fuzzeddata next line: \n")
    file.close()
    file2 = open(path, "ab")
    file2.write(data)
    file2.close();
    counter += 1
    try:
        idna.decode(data)
    except idna.IDNAError:
        pass

if __name__ == '__main__':
    #global counter
    #global filetype
    counter = int(sys.argv[2])
    filetype = sys.argv[3]
    argv = sys.argv[0:2]
    atheris.Setup(argv, TestOneInput)
    atheris.Fuzz()
