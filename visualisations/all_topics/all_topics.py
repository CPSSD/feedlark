import sys
import gearman
import bson

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
        if arr[i] != curr_val: # we've reached a new number
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

def add_user_data(all_topics, user_topics):
    for topic in user_topics:
        if topic in all_topics:
            all_topics[topic].append(float(user_topics[topic]))
        else:
            all_topics[topic] = [float(user_topics[topic])]

def get_all_topic_data(users):
    topic_data = {}
    for user in users:
        add_user_data(topic_data, user['words'])
    return topic_data

def main():
    if len(sys.argv) != 2:
        print 'This tool takes 1 command line argument; the number of topics to output data on. See README.md'
        return
    num_requested_topics = int(sys.argv[1])
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    result = bson.BSON.decode(bson.BSON(gearman_client.submit_job('db-get', str(bson.BSON.encode({'database':'feedlark', 'collection':'user', 'query':{}, 'projection':{'words':1}}))).result))
    
    if result[u'status'] == u'ok':
        users = result['docs']
        print len(users)
        topic_data = get_all_topic_data(users)
        num_output_topics = min(num_requested_topics, len(topic_data))
        print len(topic_data), num_output_topics
        sorted_topics = sorted(topic_data, key=lambda x:len(topic_data[x]), reverse=True)
        for i in xrange(num_output_topics):
            sorted_values = sorted(topic_data[sorted_topics[i]])
            mean_val = mean(sorted_values)
            mode_val = mode(sorted_values)
            median_val = median(sorted_values)

            if mode_val is None:
                mode_val = 'X'
            print sorted_topics[i], len(sorted_values), mean_val, mode_val, median_val
    else:
        print('Error getting user data from database')
        print(result['description'])
        return

if __name__ == '__main__':
    main()
