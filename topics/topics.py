import re
from datetime import datetime
import gearman, bson
from spacy.en import English

nlp = English()
gearman_client = None

def log(level, message):
    time = datetime.now().strftime('%H:%M %d/%m/%Y')
    levels = ['INFO', 'WARNING', 'ERROR']
    print(str(time) + " " + levels[level] + ": " + str(message))

def limit_dict(d, num):
    # returns a dict of max length num, with the elements of d that had the highest values
    if len(d) <= num:
        return d
    sorted_d = sorted(d.items(), key=lambda x : x[1], reverse=True)
    log(0, sorted_d)
    e = {}
    for i in xrange(num):
        e[sorted_d[i][0]] = sorted_d[i][1]
    return e


def remove_stop_words(doc):
    new_doc = []
    for index in range(len(doc)-1, -1, -1):
        if (not (doc[index]).is_stop) and (len(re.sub("[^\w]+", "", doc[index].text)) > 0):
            new_doc.append(doc[index])
    return new_doc

def count_words(word_list):
    words = {}
    total = 0
    log(0, "Word list: " + str(word_list))
    for orig_word in word_list:
        word = orig_word.text.lower().strip()
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
        total += 1
    return words, total

def get_topics(article):
    doc = nlp(article)
    log(0, "orig: " + str(doc))
    doc = remove_stop_words(doc)
    log(0, "sans stop words: " + str(doc))
    word_counts, total = count_words(doc)
    log(0, word_counts)
    normalised_counts = {k:(v/float(total)) for k,v in word_counts.items()}
    return normalised_counts

def get_topics_gearman(worker, job):
    log(0, "Get topics: " + job.data)
    bson_obj = bson.BSON(job.data)
    data = bson_obj.decode() 
    if "article" not in data:
        return str(bson.BSON.encode({"status":"error", "description":"No article supplied"}))
    log(0, "Article: " + data["article"])

    article = data["article"]
    topics = get_topics(article)
    if(len(topics) > 10):
        log(0, "More than 10 topic words, returning only most frequent 110")
        topics = limit_dict(topics, 10)
    response = {"status":"ok", "topics":topics}
    bson_response = bson.BSON.encode(response)
    return str(bson_response)

if __name__ == '__main__':
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('topic-modeller')
    log(0, "Registering gearman worker 'get-topics'")
    gearman_worker.register_task('get-topics', get_topics_gearman)
    gearman_worker.work()
