import time

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

import win_proc
from win_stat import StatType
import win_util

def main() -> None:
    # xs = np.arange(500,2501,500)
    xs = np.arange(1000,1501,100)
    ys = np.empty(xs.shape[0])

    domains = win_util.fetch_lines(
            "/usr/local/opt/wordlists/rockyou/rockyou.txt") 
    threshold = 0.50
    flags = StatType.MAX.value \
            | StatType.TOP_K.value \
            | StatType.STD_DEV.value

    i = 0
    for x in xs:
        t1 = time.time()
        win_proc.process_windows(domains, x, threshold, flags, max_win=x)
        ys[i] = time.time() - t1
        i += 1

    PLOT=True
    if PLOT:
        plt.figure(1)

        plt.title("Max Window Variant Performance")
        plt.xlabel("window size")
        plt.ylabel("time (s)")

        plt.xticks(xs)

        plt.plot(xs, ys, color=mcolors.BASE_COLORS["k"])
        marker, stemlines, baseline = plt.stem(xs, ys)
        plt.setp(marker, "color", "grey")
        plt.setp(stemlines, "color", "grey")
        plt.setp(stemlines, "linestyle", "dotted")
        plt.setp(baseline, "color", "grey")

        print("Plot is shown")
        plt.show()

if __name__ == "__main__":
    main()
