"""Runner module for sliding windows implementation"""
import win_proc
from win_util import fetch_lines
from win_stat import StatType

def main():
    """Sample run of processing sliding windows of domains"""
    n = 1744 # total length of input file
    THRESHOLD = 0.600

    domain_list = fetch_lines("../data/domains.in")
    FLAGS = StatType.MAX.value | \
            StatType.MIN.value | \
            StatType.TOP_K.value | \
            StatType.MEAN.value | \
            StatType.STD_DEV.value

    win_proc.process_windows(domain_list, n, THRESHOLD, FLAGS)

if __name__ == "__main__":
    main()
