class WorkerSkeleton:
    @staticmethod
    def is_error(response):
        return False

    @staticmethod
    def get_error(response):
        return 'No description provided'

    @classmethod
    def print_dict(cls, response, indent=0):
        for key in response:
            if type(response[key]) == dict:
                print ' '*indent + str(key) + ': '
                cls.print_dict(response[key], 4)
                continue

            print ' '*indent + str(key) + ': ' + str(response[key])


class dbgetWorker(WorkerSkeleton):
    NAME = 'db-get'
    NICENAME = 'Database Get'
    REQUEST = {
        'key': str,
        'database': str,
        'collection': str,
        'query': dict,
        'projection': dict,
    }

    @staticmethod
    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    @staticmethod
    def get_error(response):
        return response['description']


class AggregatorWorker(WorkerSkeleton):
    NAME = 'aggregate'
    NICENAME = 'Aggregate'
    REQUEST = {
        'key': str,
    }

    @staticmethod
    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    @staticmethod
    def get_error(response):
        return response['description']
