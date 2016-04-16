class WorkerSkeleton:
    def is_error(response):
        return False

    def get_error(response):
        return 'No description provided'


class dbgetWorker(WorkerSkeleton):
    NAME = 'db-get'
    REQUEST = {
        'key': str,
        'database': str,
        'collection': str,
        'query': dict,
        'projection': dict,
    }

    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    def get_error(response):
        return response['description']


class AggregatorWorker(WorkerSkeleton):
    NAME = 'aggregate'
    REQUEST = {
        'key': str,
    }

    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    def get_error(response):
        return response['description']
