import os, sys
###### Ten kawałek zmieniany jest przy kopiowaniu poprzez skrypt deploy.py #######
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
PRZERZUCONE=False
##################################################################################
sys.path.append(KATALOG_SKRYPTOW)
import time, datetime
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000
        print("Function ", func.__name__, " took ",int(elapsed_time_ms)," milliseconds")
        #print(f"Function '{func.__name__}' took {elapsed_time_ms:.2f} milliseconds")
        return result
    return wrapper
    
logplik = open(os.path.join(KATALOG_ORYGINALNY, 'log.txt'),'w', encoding='utf-8')
#Zamienić tryb na 'a', jesli się chce mieć wiecznie puchnące logi, o których się zapomni...
def log(*args, **kwargs):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"|", file=logplik, end="")
    print(*args, **kwargs, file=logplik)
    print(*args, **kwargs)
    logplik.flush()