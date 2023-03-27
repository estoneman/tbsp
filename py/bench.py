import window 
import numpy as np
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    n = 1000
    
    start = 0.10 
    end = 1.01 
    step = 0.1

    xs = np.arange(start, end, step)
    ys = np.empty(*xs.shape)

    for i in range(xs.shape[0]):
        domain_list = window.fetch_lines("../data/domains.in")
        window_len = int(xs[i]*n)
        k = math.ceil(0.5*window_len)
        top_k = window.top_k(domain_list, n, window_len, k, 0.50)
        with open("topk.csv", 'a') as fp:
            fp.write(f"=== WINDOW SIZE @ {window_len} ===")
            for pair in top_k:
                fp.write(f"{pair[0]},{pair[1]}\n")

