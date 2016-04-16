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


def build_arbitrary_dict(indent):
    print 'Enter dictionary as key: value with a blank line to quit:'
    print ' '*indent + '{'

    ret_dict = {}
    inp = raw_input(' '*(indent+4))
    while inp:
        eval('ret_dict += {{}}'.format(inp))
        inp = raw_input(' '*(indent+4))
    print ' '*indent + '}'

    return ret_dict


def buid_request(req_dict, indent=4):
    request = {}
    for key in req_dict:
        if type(req_dict[key]) == dict:
            print ' '*indent + key + ':'
            request[key] = buid_request(req_dict[key], indent+4)
            continue

        if req_dict[key] == dict:
            print ' '*indent + key + ':'
            request[key] = build_arbitrary_dict(indent+4)
            continue

        right_type = False
        while not right_type:
            inp = raw_input(' '*indent + key + ': ')
            try:
                request[key] = req_dict[key](inp)
                right_type = True
            except:
                print 'Error:', key, 'must be of type', req_dict[key]

    return request


def main():
    print 'Welcome to the Feedlark CLI!'
    print '============================'

    # Make list of all the objects in the workers module that end with 'Worker'
    w_list = [eval('workers.'+x) for x in dir(workers) if x.endswith('Worker')]

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

        print ''
        print 'Building request:'
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

        print ''
        print 'Response:'
        worker.print_response(response)

if __name__ == '__main__':
    main()
