"""Statistic types for a SlidingWindow object"""

from enum import Enum

class StatType(Enum):
    """Set of supported statistics"""
    TOP_K = 1
    MEAN = 2
    MAX = 4
    MIN = 8
    STD_DEV = 16
