import window 
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    domain_list = window.fetch_lines("../data/domains.in")
    n = 1000 
    
    xs = np.arange(0.1, 1.1, 0.1)

    ys = np.empty(10)

    for i in range(len(xs)):
        window_len = int(xs[i]*n)
        k = int(0.5*window_len)
        top, y = window.top_k(domain_list, n, window_len, k, 0.50)
        ys[i] = y

    plt.figure(1)
    plt.plot(xs, ys)

    plt.title(f"Sliding Windows @ {n} domains")

    plt.xlabel("Window Size (% of Input Size)")
    plt.ylabel("Time (s)")

    plt.xticks(xs)

    plt.show()
