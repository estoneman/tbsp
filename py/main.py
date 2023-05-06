"""Runner module for sliding windows implementation"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.sparse import lil_matrix

import win_proc
from win_util import fetch_lines
from win_stat import StatType

def main():
    """Sample run of processing sliding windows of domains"""
    n = 1744 # total length of input file
    THRESHOLD = 0.500

    domain_list = fetch_lines("../data/domains.in")
    FLAGS = StatType.MAX.value     \
            | StatType.MIN.value   \
            | StatType.TOP_K.value \
            | StatType.MEAN.value  \
            | StatType.STD_DEV.value

    sim_mat = win_proc.process_windows(domain_list, n, THRESHOLD, FLAGS)
    sim_mat_dense = sim_mat.toarray()
    sim_mat_filtered = gaussian_filter(sim_mat_dense, sigma=5, mode="constant",
                                       cval=0.0)
    sim_mat = lil_matrix(sim_mat_filtered)

    PLOT=True
    if PLOT:
        # plot the matrix as a heatmap
        fig, ax = plt.subplots()
        im = ax.imshow(sim_mat.toarray(), cmap='hot')
        
        # add a colorbar legend
        cbar = ax.figure.colorbar(im, ax=ax)
        
        # set the axis labels
        ax.set_xticks(np.arange(n, 1000))
        ax.set_yticks(np.arange(n, 1000))
        ax.set_title("Similarity Matrix Viz")
        
        # show the plot
        print("Plot is shown")
        plt.show()
    
if __name__ == "__main__":
    main()
