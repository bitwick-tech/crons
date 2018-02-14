import magic
import time

if __name__ == '__main__':
    x = 2
    while x > 0:
        x = x-1
        magic.do_magic()
        if x != 0:
            time.sleep(28)
