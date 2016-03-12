
def log(message, level=0):
    levels = ['INFO:','WARNING:','ERROR:']
    time = str(datetime.now()).replace('-','/')[:-7]
    print time,levels[level],message

def score(article_words, user_words):
    log("Normalising article_words scores")
    word_sum = sum(article_words.values())
    a_words_norm = {x[0]:(x[1]/word_sum) for x in article_words.items()}

    
