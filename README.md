# Description
This is a Discord bot which reports which tickers that are frequently discussed on https://lihkg.com/category/15. This bot keeps track of the frequencies of NASDAQ/NYSE stock tickers among the latest replies of recent threads. This bot resets its counter every one hour.

Use the invitation link: https://discord.com/api/oauth2/authorize?client_id=818816710621528064&permissions=93184&scope=bot

Example:

```
>>> $hot
```
Response: 
```
Ticker  Count   TFIDF   Doc
HSBC    31      0.4244  9
GME     30      0.5711  12
ETH     28      0.4718  9
COIN    28      0.3566  17
VOO     27      0.3104  6
TSM     20      0.4321  6
TSLA    16      0.3679  11
LOAN    13      1.3015  2
TT      12      0.4436  4
EA      12      0.3306  2
PLTR    12      0.3211  6
TG      12      0.2735  9
FUND    11      0.1657  5
TD      9       0.2403  4
GE      9       0.2220  7
ACC     8       0.4612  5
NM      8       0.3771  1
ID      7       0.2779  4
YETI    7       0.7754  1
RC      7       0.3207  4
```
