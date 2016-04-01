import sys

def mean(arr):
    if arr is None or len(arr) is 0:
        return None
    return sum(arr) / (len(arr) + 0.0)

def mode(arr):
    #for performance reasons, this requires the input to be sorted in ascending order (which is required for median calculation anyway)
    if arr is None or len(arr) == 0:
        return None
    curr_val = None
    curr_count = 0
    curr_mode = curr_val
    mode_count = 0

    for i in xrange(0, len(arr)):
        if arr[i] < curr_val:
            raise ValueError('Input is not sorted: ' + str(arr[i]) + ' < ' + str(curr_val))
        if arr[i] is not curr_val: # we've reached a new number
            if curr_count > mode_count:
                 mode_count = curr_count
                 curr_mode = curr_val
            elif curr_count == mode_count:
                 curr_mode = None
            curr_count = 0
            curr_val = arr[i]
        curr_count += 1

    if curr_count > mode_count:
        curr_mode = curr_val
    elif curr_count == mode_count:
        curr_mode = None
    return curr_mode

def median(arr):
    # requires input to be sorted, raises ValueError if it isn't.
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            raise ValueError('Input is not sorted: ' + str(arr[i]) + ' < ' + str(arr[i-1]))
    if arr is None or len(arr) == 0:
        return None
    if len(arr) % 2 == 0:
        return mean(arr[len(arr)/2-1:len(arr)/2+1])
    else:
        return arr[len(arr)/2]
