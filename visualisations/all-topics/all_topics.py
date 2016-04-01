import sys

def mean(arr):
    if arr is None or len(arr) is 0:
        return None
    return sum(arr) / len(arr)
