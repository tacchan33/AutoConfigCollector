from Main import *
import time

if __name__ == "__main__":
    start = time.time()
    mainclass = Main()
    mainclass.run()
    del mainclass
    elapsed_time = time.time() - start
    print("かかった時間は"+format(elapsed_time)+"[sec]")
