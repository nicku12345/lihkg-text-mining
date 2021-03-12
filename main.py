from src.RemoteTickerCounter import RemoteTickerCounter
from misc.ordinal import ordinal
import time

to_print = False

if to_print:
    print("\n" + "Initializing ...")
RTC = RemoteTickerCounter()

while True:
    
    RTC.reset()

    for m in range(60):
        t = time.time()
        
        print("-------------------------------------")
        print("scanning...", end = "\r", flush = True)
        RTC.Query(page = m%3 + 1, num_thread = 60, num_reply = 60)

        dt = round(time.time() - t, 4)
        print("\n" + f"{ordinal(m+1)} scanned finished. {dt} seconds elapsed ...")

        if to_print:
            print("\n" + f"Top {20} discussed tickers:")
        RTC.display(20, to_print = to_print)

        for sec in range(60):
            time.sleep(1)
            print(f"Time for next scan: {60 - sec} seconds...", end = "\r", flush = True)