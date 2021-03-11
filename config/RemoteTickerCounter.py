from config.ReqDescription import RD
from config.MsgScanner import MS

from datetime import datetime

import requests
import json
import html2text
import time
import math

class RemoteTickerCounter:
    def __init__(self):
        self.MsgScanner = MS
        self.ReqDescription = RD

        self.thread_ctr = dict()
        self.ticker_ctr = dict()

        self.freq = dict()
        self.g = dict()

        self.new_thread = 0
        self.new_reply = 0

        self.total_thread = 0
        self.total_reply = 0
        self.total_characters = 0

    def Query(self, page = 1, num_thread = 60, num_reply = 60):

        page = page
        thread_cnt = 0
        thread_queue = []

        while thread_cnt < num_thread:
            if thread_queue:
                self._read(thread_queue.pop(), num_reply)
                thread_cnt += 1
                continue

            url, headers = self.ReqDescription.generate(type = "category", page = page)

            page += 1

            data = json.loads(requests.get(url, headers = headers).content)
            threads = data["response"]["items"]

            thread_queue = threads[::-1]
        
        return

    def _read(self, thread, num_reply = 60):
        thread_id = int(thread["thread_id"])
        no_of_reply = int(thread["no_of_reply"])
        total_page = int(thread["total_page"])

        if thread_id in self.thread_ctr:
            #thread_ctr tracks the last comment read previously
            num_reply = no_of_reply - self.thread_ctr[thread_id]
        else:
            self.new_thread += 1

        self.thread_ctr[thread_id] = no_of_reply

        page = total_page
        reply_cnt = 0
        reply_queue = []

        while reply_cnt < num_reply and 1 <= page:
            if reply_queue:
                self._scan(reply_queue.pop(), thread_id)
                reply_cnt += 1

                self.new_reply += 1
                continue

            url, headers = self.ReqDescription.generate(
                type = "thread",
                page = page,
                thread_id = thread_id)

            data = json.loads(requests.get(url, headers = headers).content)["response"]["item_data"]

            reply_queue = data
            page -= 1

        return

    def _scan(self, reply, thread_id):
        msg = html2text.html2text(reply["msg"])
        
        ticker_detected = self.MsgScanner.query(msg = msg)
        self.total_characters += len(msg)

        for ticker in ticker_detected:
            ticker = ticker.upper()
            self.ticker_ctr[ticker] = self.ticker_ctr.get(ticker,0) + 1
            
            if thread_id not in self.freq:
                self.freq[thread_id] = dict()
            
            self.freq[thread_id][ticker] = self.freq[thread_id].get(ticker,0) + 1
            self.g[ticker] = self.g.get(ticker, set()) | {thread_id}

        return

    def TFIDF(self, ticker):
        s = 0
        idf = 0.5 * math.log(len(self.freq) / len(self.g[ticker]))
        top5 = []
        for thread_id in self.g[ticker]:
            tf = self.freq[thread_id][ticker] / sum(self.freq[thread_id][t] for t in self.freq[thread_id])
            top5.append(tf)

        top5.sort()

        remaining = 5
        while top5 and remaining > 0:
            s += top5.pop()
            remaining -= 1
        s /= (5 - remaining)

        return s * idf
            

    def display(self, num_ticker, to_print = False):
        ans0 = [(ticker, self.TFIDF(ticker)) for ticker in self.ticker_ctr]
        ans1 = [(ticker, self.ticker_ctr[ticker]) for ticker in self.ticker_ctr]

        #threshold for determining quality tickers
        threshold = 0 #math.log(len(self.freq)) / 10

        ans0.sort(key = lambda item: item[1])
        ans1.sort(key = lambda item: item[1])

        self.total_thread += self.new_thread
        self.total_reply += self.new_reply

        if to_print:
            print(f"Total {self.total_thread} threads, {self.total_reply} replies, {self.total_characters} characters scanned ...")
            print(f"{self.new_thread} new threads, {self.new_reply} new replies detected ...")        

        self.new_thread, self.new_reply = 0,0

        if to_print:
            print(
                "Ticker".rjust(10) + 
                "TFIDF".rjust(10) + 
                "Count".rjust(10) + 
                "doc cnt".rjust(10) + 
                "".rjust(10) +
                "Ticker".rjust(10) + 
                "Count".rjust(10) + 
                "TFIDF".rjust(10) +
                "doc cnt".rjust(10)
                )
        
        temp = {
            "name": "",
            "value": "```",
            "inline": True
        }

        col1 = temp.copy()
        col2 = temp.copy()

        col1["name"] = "tf-idf"
        col2["name"] = "Count"

        col1["value"] += "Ticker  TFIDF   Count   Doc\n"
        col2["value"] += "Ticker  Count   TFIDF   Doc\n"

        N = num_ticker

        while num_ticker > 0 and ans0:
            num_ticker -= 1

            t1, s1 = ans0.pop()
            while ans0 and self.ticker_ctr[t1] == 1 and len(self.g[t1]) == 1:
                t1, s1 = ans0.pop()
            t2, s2 = ans1.pop()

            if s1 <= threshold:
                t1 = None

            if t1 != None:
                D1, D2, D3, D4 = str(t1), format(s1, '.4f'), str(self.ticker_ctr[t1]), str(len(self.g[t1]))
            else:
                D1, D2, D3, D4 = "----", "----", "----", "----"

            to_display1 = D1.rjust(10) + D2.rjust(10) + D3.rjust(10) + D4.rjust(10)

            D5, D6, D7, D8 = str(t2), str(s2), format(self.TFIDF(t2), '.4f'), str(len(self.g[t2]))

            to_display2 = D5.rjust(10) + D6.rjust(10) + D7.rjust(10) + D8.rjust(10)

            col1["value"] += D1 + " "*(8 - len(D1)) + D2 + " "*2 + D3 + " "*(8 - len(D3)) + D4 + "\n"
            col2["value"] += D5 + " "*(8 - len(D5)) + D6 + " "*(8 - len(D6)) + D7 + " "*2 + D8 + "\n" 

            if to_print:
                print(
                    to_display1 +
                    "".rjust(10) +
                    to_display2
                    )

        col1["value"] += "```"
        col2["value"] += "```"

        response = {
            "time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "col": [col1, col2],
            "counter": [self.total_thread, self.total_reply, self.total_characters]
        }

        with open("./bot/response.json", "w") as f:
            json.dump(response, f)