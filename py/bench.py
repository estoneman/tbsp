import window 
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    domain_list = window.fetch_lines("../data/domains.in")
    n = 400
    
    xs = np.arange(0.1, 0.5, 0.1)

    ys = np.empty(*xs.shape)

    for i in range(xs.shape[0]):
        window_len = int(xs[i]*n)
        k = int(0.5*window_len)
        top, y = window.top_k(domain_list, n, window_len, k, 0.50)
        ys[i] = y
        domain_list = window.fetch_lines("../data/domains.in")

    plt.figure(1)
    plt.plot(xs, ys)

    plt.title(f"Sliding Windows @ {n} domains")

    plt.xlabel("Window Size (% of Input Size)")
    plt.ylabel("Time (s)")

    plt.xticks(xs)

    plt.show()
