from config.RemoteTickerCounter import RTC
import time

while True:
    t = time.time()

    print("-------------------------------------")
    print("scanning...", end = "\r", flush = True)
    RTC.Query(num_thread = 60, num_reply = 60)

    dt = round(time.time() - t, 4)
    print("\n" + f"{dt} seconds used...")

    print("\n" + f"Top {20} discussed tickers:")
    RTC.display(20)

    for _ in range(60):
        time.sleep(1)
        print(f"Time for next scan: {60 - _} seconds...", end = "\r", flush = True)