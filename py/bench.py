"""Visualize performance of sliding windows implementation
"""

import math
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import window
from util import fetch_lines

if __name__ == "__main__":
    n = 10
    THRESHOLD = 0.70
    START = 10
    END = 101
    STEP = 10

    xs = np.arange(START, END, STEP)
    ys = np.empty(*xs.shape)

    for i in range(xs.shape[0]):
        domain_list = fetch_lines("../data/domains.in")
        window_len = int(n * (xs[i]/100))

        k = math.ceil(0.5*window_len)

        t1 = time.clock_gettime_ns(time.CLOCK_REALTIME)

        print(f"scale: {int(xs[i] / STEP)*10}%")
        top_k = window.top_k(domain_list, n, window_len, k, THRESHOLD)

        t2 = time.clock_gettime_ns(time.CLOCK_REALTIME)

        ys[i] = round((t2 - t1) / 10e9, 3)
        # with open(f"../data/topk/top-{window_len}.txt", 'a') as fp:
        #     for pair in top_k:
        #         fp.write(f"{pair[0]},{pair[1]}\n")

    plt.figure(1)

    plt.title(f"Sliding Window @ {n=} Domains")
    plt.xlabel("window size (% domain size)")
    plt.ylabel("time (s)")

    plt.xticks(xs)

    plt.plot(xs, ys, color=mcolors.BASE_COLORS["k"])
    marker, stemlines, baseline = plt.stem(xs, ys)
    plt.setp(marker, "color", mcolors.BASE_COLORS["k"])
    plt.setp(stemlines, "color", mcolors.BASE_COLORS["k"])
    plt.setp(stemlines, "linestyle", "dotted")
    plt.setp(baseline, "color", "grey")

    print("Plot is shown")
    plt.show()
