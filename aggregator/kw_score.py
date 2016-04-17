from datetime import datetime
from spacy.en import English
from bson import BSON
from os import getenv
import gearman

# This is outside a function so it runs only once, on import.
nlp = English()


def log(*message, **kwargs):
    '''
    Logs to stdout

    Pass in parameters as you would the python3 print function.
    Includes the optional 'level' keyword argument, defaults to 0.
    '''
    level = kwargs['level'] if 'level' in kwargs else 0
    levels = ['INFO:', 'WARNING:', 'ERROR:']

    message_str = ''.join(map(str, message))
    time = str(datetime.now()).replace('-', '/')[:-7]

    print time, levels[level], message_str


def score(article_words, user_words):
    '''
    Scores articles based on the keywords in the article and the ones the user
    likes.

    This function is O(N*M) where N and M are the lengths of article_words and
    user_words
    '''
    if not (article_words and user_words):
        # If either are empty then score is 0
        return 0

    log("Tokenising article_words and user_words")
    a_tokens = nlp(u' '.join(article_words.keys()))
    u_tokens = nlp(u' '.join(user_words.keys()))

    log("Normalising article_words scores")
    word_sum = sum(article_words.values())
    a_words_norm = {x[0]: (x[1]/word_sum) for x in article_words.items()}

    log("Normalising user_words scores")
    word_sum = sum(user_words.values())
    u_words_norm = {x[0]: (x[1]/word_sum) for x in user_words.items()}

    total = 0.0
    words_used = 0
    for a in a_tokens:
        best_sim = 0
        best_word = ''
        for u in u_tokens:
            u_a_sim = a.similarity(u)
            if u_a_sim > best_sim:
                best_sim = u_a_sim
                best_word = str(u).strip()

        a_word = str(a).strip()
        if a != '' and best_word != '' and best_sim > 0.6:
            words_used += 1
            log("Best match for '", a_word,
                "' is '", best_word,
                "', similarity: ", best_sim)
            total += a_words_norm[a_word] * u_words_norm[best_word] * best_sim

    log("Total: ", total, ", words used: ", words_used)
    if words_used:
        return total/words_used
    else:
        return 0


def fast_score(article_words, user_words):
    '''
    Scores articles based on the keywords in the article and the ones the user
    likes.

    This function is O(N) where N is the size of article_words
    '''
    if not (article_words and user_words):
        # If either are empty then score is 0
        return 0

    log("Normalising article_words scores")
    word_sum = sum(article_words.values())
    a_words_norm = {x[0]: (x[1]/word_sum) for x in article_words.items()}

    log("Normalising user_words scores")
    word_sum = sum(user_words.values())
    u_words_norm = {x[0]: (x[1]/word_sum) for x in user_words.items()}

    total = 0
    total_count = 0
    for a in a_words_norm:
        if a in user_words:
            log("Word ", a, " is common")
            total += a_words_norm[a] * user_words[a]
            total_count += 1

    log("Total: ", total, ", total count: ", total_count)
    if total_count != 0:
        return total/float(total_count)
    else:
        return 0


def score_gm(worker, job):
    word_data = BSON(job.data).decode()

    key = getenv('SECRETKEY')
    if key is not None:
        log("Checking secret key")
        if 'key' not in word_data or word_data['key'] != key:
            log("Secret key mismatch")
            return str(BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch',
                }))

    try:
        a_words = word_data['article_words']
        u_words = word_data['user_words']
    except:
        log("Problem with data provided", level=2)
        return str(BSON.encode(
            {
                "status": "error",
                "description": "Problem with data provided",
            }))

    try:
        a_score = score(a_words, u_words)
    except Exception as e:
        log("Problem when scoring, is the data in the right format?", level=2)
        log(e, level=2)
        return str(BSON.encode(
            {
                "status": "error",
                "description":
                    "Problem when scoring, is the data in the right format?",
            }))

    return str(BSON.encode(
        {
            "status": "ok",
            "score": a_score,
        }))


def fast_score_gm(worker, job):
    word_data = BSON(job.data).decode()

    key = getenv('SECRETKEY')
    if key is not None:
        log("Checking secret key")
        if 'key' not in word_data or word_data['key'] != key:
            log("Secret key mismatch")
            return str(BSON.encode({
                'status': 'error',
                'description': 'Secret key mismatch',
                }))

    try:
        a_words = word_data['article_words']
        u_words = word_data['user_words']
    except:
        log("Problem with data provided", level=2)
        return str(BSON.encode(
            {
                "status": "error",
                "description": "Problem with data provided",
            }))

    try:
        a_score = fast_score(a_words, u_words)
    except Exception as e:
        log("Problem when scoring, is the data in the right format?", level=2)
        log(e, level=2)
        return str(BSON.encode(
            {
                "status": "error",
                "description":
                    "Problem when scoring, is the data in the right format?",
            }))

    return str(BSON.encode(
        {
            "status": "ok",
            "score": a_score,
        }))


if __name__ == '__main__':
    log("Starting Gearman worker")
    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    gm_worker.set_client_id('kw-scoring')

    log("Registering tasks")
    gm_worker.register_task('fast_score', fast_score_gm)
    gm_worker.register_task('score', score_gm)

    gm_worker.work()
