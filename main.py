from config.RemoteTickerCounter import RTC
import time

while True:
    print("-------------------------------------")
    print("scanning...", end = "\r", flush = True)
    RTC.Query(num_thread = 60, num_reply = 60)
    print("\n" + f"Top {20} discussed tickers:")
    RTC.display(20)

    for _ in range(60):
        time.sleep(1)
        print(f"Time for next scan: {60 - _} seconds...", end = "\r", flush = True)