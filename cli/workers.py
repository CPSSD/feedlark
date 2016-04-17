from decorators import standard_error, standard_response


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
class dbupdateWorker:
    NAME = 'db-update'
    NICENAME = 'Database Update'
    REQUEST = {
        'key': str,
        'database': str,
        'collection': str,
        'data': {
            'updates': dict,
            'selector': dict,
        },
    }


@standard_response
@standard_error
class dbupsertWorker:
    NAME = 'db-upsert'
    NICENAME = 'Database Upsert'
    REQUEST = {
        'key': str,
        'database': str,
        'collection': str,
        'data': {
            'updates': dict,
            'selector': dict,
        },
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
class TextGetterWorker:
    NAME = 'article-text-getter'
    NICENAME = 'Article Text Getter'
    REQUEST = {
        'key': str,
        'url': str,
    }

    @staticmethod
    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    @staticmethod
    def get_error(response):
        return response['error-description']


@standard_response
@standard_error
class UpdateAllFeedsWorker:
    NAME = 'update-all-feeds'
    NICENAME = 'Update All Feeds'
    REQUEST = {
        'key': str,
        'url': str,
    }


@standard_response
@standard_error
class UpdateSingleFeedWorker:
    NAME = 'update-single-feed'
    NICENAME = 'Update Single Feed'
    REQUEST = {
        'key': str,
        'url': str,
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
