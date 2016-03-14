from datetime import datetime

def log(*message, **kwargs):
    '''
    Logs to stdout
    
    Pass in parameters as you would the python3 print function.
    Includes the optional 'level' keyword argument, defaults to 0.
    '''
    level = kwargs['level'] if 'level' in kwargs else 0
    levels = ['INFO:','WARNING:','ERROR:']
    
    message_str = ''.join(map(str,message))
    time = str(datetime.now()).replace('-','/')[:-7]
    
    print time,levels[level],message_str


def score(article_words, user_words):
	return


def fast_score(article_words, user_words):
    '''
    Scores articles based on the keywords in the article and the ones the user likes.

    This function is O(N) where N is the size of article_words
    '''
    if not (article_words and user_words):
        #If either are empty then score is 0
        return 0
    
    log("Normalising article_words scores")
    word_sum = sum(article_words.values())
    a_words_norm = {x[0]:(x[1]/word_sum) for x in article_words.items()}

    total = 0
    total_count = 0
    for a in a_words_norm:
        if a in user_words:
            log("Word ",a," is common")
            total += a_words_norm[a] * user_words[a]
            total_count += 1

    log("Total: ",total,", total count: ",total_count)
    if total_count != 0:
        return total/float(total_count)
    else:
        return 0
