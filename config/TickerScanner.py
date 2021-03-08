#initialize a data structure storing tickers
#support quick query and insert
f = open("./config/symbol/ticker.txt", "r")
TICKERS = set([word[:-1] for word in f.readlines()])
f.close()

f = open("./config/symbol/ignore.txt", "r")
IGNORE = set([word[:-1] for word in f.readlines()])
f.close()

class Trie:
    def __init__(self):
        self.children = dict()
        self.is_ended = False
        self.ticker = ""

class TickerScanner:
    def __init__(self):
        self.t = Trie()
        self.ig = Trie()

        for word in IGNORE:
            self.insert(self.ig, word)

        for word in TICKERS:
            if not self.query(word, type = "ignore"):
                self.insert(self.t, word)

    def insert(self, node, word):
        cur = node

        for i,char in enumerate(word):
            if char not in cur.children:
                cur.children[char] = Trie()
            cur = cur.children[char]
        
        cur.is_ended = True
        cur.ticker = word

        return

    def query(self, word, type = "default"):
        cur = self.t if type == "default" else self.ig

        for i,char in enumerate(word):
            if char not in cur.children:
                return False
            cur = cur.children[char]
        
        if cur.is_ended and cur.ticker == word:
            return True
        return False

TS = TickerScanner()