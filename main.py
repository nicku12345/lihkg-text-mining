from config.RemoteTickerCounter import RemoteTickerCounter
from misc.ordinal import ordinal
import time

while True:
    print("\n" + "Initializing ...")
    RTC = RemoteTickerCounter()
    for m in range(60):
        t = time.time()

        print("-------------------------------------")
        print("scanning...", end = "\r", flush = True)
        RTC.Query(num_thread = 60, num_reply = 60)

        dt = round(time.time() - t, 4)
        print("\n" + f"{ordinal(m+1)} scanned finished. {dt} seconds elapsed ...")

        print("\n" + f"Top {20} discussed tickers:")
        RTC.display(20)

        for sec in range(60):
            time.sleep(1)
            print(f"Time for next scan: {60 - sec} seconds...", end = "\r", flush = True)