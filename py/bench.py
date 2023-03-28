import math
import time

import numpy as np
import matplotlib.pyplot as plt

import window
from util import fetch_lines

if __name__ == "__main__":
    n = 1000
    threshold = 0.70
    start = 10
    end = 101
    step = 10

    xs = np.arange(start, end, step)
    ys = np.empty(*xs.shape)

    for i in range(xs.shape[0]):
        domain_list = fetch_lines("../data/domains.in")
        window_len = int(n * (xs[i]/100))

        k = math.ceil(0.5*window_len)

        t1 = time.clock_gettime_ns(time.CLOCK_REALTIME)

        print(f"run: {int(xs[i] / step)}")
        top_k = window.top_k(domain_list, n, window_len, k, threshold)

        t2 = time.clock_gettime_ns(time.CLOCK_REALTIME)

        ys[i] = round((t2 - t1) / 10e9, 3)
        # with open(f"../data/topk/top-{window_len}.txt", 'a') as fp:
        #     for pair in top_k:
        #         fp.write(f"{pair[0]},{pair[1]}\n")

    plt.figure(1)

    plt.xlabel("window size (% domain size)")
    plt.ylabel("time (s)")

    plt.xticks(xs)

    plt.plot(xs, ys)

    print("Plot is shown")
    plt.show()
