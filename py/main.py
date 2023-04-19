"""Runner module for sliding windows implementation"""

import time

import matplotlib.pyplot as plt
import numpy as np

import win_proc
from win_util import fetch_lines
from win_stat import StatType

def main():
    """Main method (for now) for testing sliding windows implementation"""
    n = 500
    THRESHOLD = 0.000
    START = 50

    # domain_list = fetch_lines("../data/domains.in")
    domain_list = fetch_lines("/usr/local/opt/wordlists/rockyou/rockyou.txt")
    window_len = int(n * (START/100))
    FLAGS = StatType.MAX.value | \
            StatType.MIN.value | \
            StatType.TOP_K.value | \
            StatType.MEAN.value | \
            StatType.STD_DEV.value
    
    sim_mat = win_proc.process_windows(domain_list, n, window_len,
                                       THRESHOLD, FLAGS)

    # === PLOT DATA COVERAGE ===
    plt.figure(1)
    nonzero_mask = sim_mat != 0
    rows, cols = np.nonzero(nonzero_mask)
    values = sim_mat[nonzero_mask]

    plt.scatter(rows, cols, c=values)
    plt.title("Sliding Window Data Coverage")

    print("PLOT IS SHOWN")
    plt.show()

if __name__ == "__main__":
    main()
