from config.TickerScanner import TS

f = open("./config/to_inspect.txt", "r")
INSPECT_LIST = set([x.strip() for x in f.readlines()])
f.close()

class Scanner:
    def __init__(self):
        self.TS = TS
    
    def query(self, msg):
        res = []
        window = []
        to_skip = False
        for i in range(len(msg)):
            if to_skip:
                if msg[i].lower() == msg[i].upper() and msg[i] not in ":./?=%&":
                    to_skip = False
                continue

            if msg[i].lower() != msg[i].upper():
                window.append(msg[i])

            if len(window) > 5 or msg[i] in ":./?=%&":
                to_skip = True
                window = []

            if i == len(msg) - 1 or msg[i].lower() == msg[i].upper():
                word = "".join(window).upper()

                if word and self.TS.query(word):
                    if word in INSPECT_LIST:
                        print(word)
                        print(msg)
                        print('------------------------------------')
                    #print(f"{word} + 1!!!!!")
                    res.append(word)
                window = []
                
        return res

MS = Scanner()