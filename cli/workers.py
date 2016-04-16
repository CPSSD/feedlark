def standard_error(in_class):
    @staticmethod
    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    @staticmethod
    def get_error(response):
        return response['description']

    in_class.is_error = is_error
    in_class.get_error = get_error
    return in_class


def standard_response(in_class):
    @classmethod
    def print_response(cls, response, indent=4):
        for key in response:
            if type(response[key]) == dict:
                print ' '*indent + str(key) + ': '
                cls.print_dict(response[key], indent + 4)
                continue

            print ' '*indent + str(key) + ': ' + str(response[key])

    in_class.print_response = print_response
    return in_class


@standard_response
@standard_error
class dbaddWorker:
    NAME = 'dd-add'
    NICENAME = 'Database Add'
    REQUEST = {
        'key': str,
        'database': str,
        'collection': str,
        'data': dict,
    }


@standard_response
@standard_error
class dbgetWorker:
    NAME = 'db-get'
    NICENAME = 'Database Get'
    REQUEST = {
        'key': str,
        'database': str,
        'collection': str,
        'query': dict,
        'projection': dict,
    }


@standard_response
@standard_error
class AggregatorWorker:
    NAME = 'aggregate'
    NICENAME = 'Aggregate'
    REQUEST = {
        'key': str,
    }


@standard_response
@standard_error
class ScoreWorker:
    NAME = 'score'
    NICENAME = 'Word crossover score'
    REQUEST = {
        'key': str,
        'article_words': dict,
        'user_words': dict,
    }


@standard_response
@standard_error
class FastScoreWorker:
    NAME = 'fast_score'
    NICENAME = 'Word crossover score (simple)'
    REQUEST = {
        'key': str,
        'article_words': dict,
        'user_words': dict,
    }
