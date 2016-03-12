from datetime import datetime

def log(*message, **kwargs):
    '''
    Logs to stdout
    
    Pass in parameters as you would the python3 print function.
    Includes the optional 'level' keyword argument, defaults to 0.
    '''
    level = kwargs['level'] if 'level' in kwargs else 0
    levels = ['INFO:','WARNING:','ERROR:']
    
    message_str = reduce(lambda a,b: a+b, map(str,message))
    time = str(datetime.now()).replace('-','/')[:-7]
    
    print time,levels[level],message_str


def score(article_words, user_words):
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

    log("Total: ",total,". Total count: ",total_count)
    if total_count != 0:
        return total/float(total_count)
    else:
        return 0
