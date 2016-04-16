import gearman
import workers
from bson import BSON


def get_server():
    print ''
    serv = raw_input('Please enter Gearman server (or blank for localhost): ')
    serv = serv if serv else 'localhost'

    port = raw_input('Please enter Gearman port (or blank for 4730): ')
    port = port if port else '4730'

    return server + ':' + port


def buid_request(work_class):
    pass


def main():
    print 'Welcome to the Feedlark CLI!'
    print '============================'

    # Get a list of all the objects in workers that end in 'Worker'
    w_list = [eval('workers.'+x) for x in dir(workers) if x.endswith('Worker')]
#    # Turn that list into a dict with the worker names as keys
#    w_dict = {x.NAME: x for x in w_list}

    server = get_server()
    try:
        gm_client = gearman.GearmanClient([server])
    except:
        print "Error connecting to gearman server."
        print "Is {} a valid server?".format(server)
        return

    while True:
        print ''
        print "Commands available:"

        for i, worker in enumerate(w_list):
            print '    ({}) {}'.format(i, worker.NICENAME)
        print '    ({}) Exit'.format(i + 1)

        print ''
        c = raw_input("Select a command: ")

        try:
            c = int(c)
            assert 0 <= c <= len(w_list)
        except:
            print 'Please provide an int between 0 and {}'.format(len(w_list))
            continue

        if c == len(w_list):
            print "See ya later, alligator"
            return
        else:
            worker = w_list[c]

        request = buid_request(worker.REQUEST)
        bson_req = str(BSON.encode(request))

        print ''
        print "Submitting request to '{}'".format(worker.NAME)
        bsond_response = gm_client.submit_job(worker.NAME, bson_req)
        response = BSON(bsond_response).decode()

        if worker.is_error(response):
            print "There was an error with the request:"
            print worker.get_error(response)
            continue

        worker.print_response(response)

if __name__ == '__main__':
    main()
