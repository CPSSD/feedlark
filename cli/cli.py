import gearman
import workers


def main():
    print 'Welcome to the Feedlark CLI!'
    print '============================'

    # Get a list of all the objects in workers that end in 'Worker'
    w_list = [eval('workers.'+x) for x in dir(workers) if x.endswith('Worker')]
#    # Turn that list into a dict with the worker names as keys
#    w_dict = {x.NAME: x for x in w_list}

    while True:
        print ''
        print "Commands available:"

        for i, worker in enumerate(w_list):
            print '    ({}) {}'.format(i, worker.NAME)
        print '    ({}) Exit'.format(i + 1)

        print ''
        c = raw_input("Select a command: ")

        try:
            c = int(c)
            assert c <= len(w_list)
        except:
            print 'Please provide an int between 0 and {}'.format(len(w_list))
            continue

        print w_list[c]

if __name__ == '__main__':
    main()
