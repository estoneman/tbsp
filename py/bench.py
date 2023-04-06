"""Visualize performance of sliding windows implementation
"""

import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import win_proc
from win_util import fetch_lines
from win_stat import StatType

def main():
    n = 1744
    THRESHOLD = 0.90
    START = 10
    END = 101
    STEP = 10

    xs = np.arange(START, END, STEP)
    ys = np.empty(*xs.shape)

    for i in range(xs.shape[0]):
        domain_list = fetch_lines("../data/domains.in")
        # domain_list = fetch_lines(
        #         "/usr/local/opt/wordlists/rockyou/rockyou.txt"
        # )
        window_len = int(n * (xs[i]/100))
        k = 5
        FLAGS = StatType.MAX.value | \
                StatType.MIN.value | \
                StatType.TOP_K.value

        t1 = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)

        print(f"scale: {int(xs[i] / STEP)*10}%")
        top = win_proc.process_windows(domains, n, window_len,
                                       THRESHOLD, FLAGS)

        t2 = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)

        ys[i] = round((t2 - t1) / 10e9, 3)
        print(f"  ttc: {ys[i]} seconds")
        print(top)

    plt.figure(1)

    plt.title(f"Sliding Window @ {n=} Domains")
    plt.xlabel("window size (% domain size)")
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
