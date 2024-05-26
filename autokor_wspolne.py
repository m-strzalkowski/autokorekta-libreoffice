import os, sys
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
sys.path.append(KATALOG_SKRYPTOW)
import datetime

logplik = open(os.path.join(KATALOG_ORYGINALNY, 'log.txt'),'a', encoding='utf-8')
def log(*args, **kwargs):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"|", file=logplik, end="")
    print(*args, **kwargs, file=logplik)
    print(*args, **kwargs)
    logplik.flush()