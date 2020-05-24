'''
gutils.py
'''

import time

class TicToc:

    def __init__(self):
        self.tic = time.time()
        self.toc = 0
    def __getattr__(self, now):
        if self.tic > 0:
            self.toc = time.time()
            return "{:.4f}".format(self.toc - self.tic)
        else:
            self.tic = time.time()


if __name__ == "__main__":
    timer = TicToc()

    print(timer.now)
    print(timer.now)