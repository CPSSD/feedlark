import re
import gearman, bson
from spacy.en import English

nlp = English()
gearman_client = None

def remove_stop_words(doc):
    new_doc = []
    for index in range(len(doc)-1, -1, -1):
        if (not (doc[index]).is_stop) and (len(re.sub("\s+", "", doc[index].text)) > 0):
            new_doc.append(doc[index])
    return new_doc

def count_words(word_list):
    words = {}
    total = 0
    print("Word list: " + str(word_list))
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
    print("orig: " + str(doc))
    doc = remove_stop_words(doc)
    print("sans stop words: " + str(doc))
    word_counts, total = count_words(doc)
    print(word_counts)
    normalised_counts = {k:(v/float(total)) for k,v in word_counts.items()}
    return normalised_counts

def get_topics_gearman(worker, job):
    print("Get topics: " + job.data)
    bson_obj = bson.BSON(job.data)
    data = bson_obj.decode() 
    if "article" not in data:
        return str(bson.BSON.encode({"status":"error", "description":"No article supplied"}))
    print("Article: " + data["article"])

    article = data["article"]
    topics = get_topics(article)
    if(len(topics) > 10):
        try:
            print("More than 10 topics")
            sorted_topics = sorted(topics.items(), key=lambda x : x[1], reverse=True)
            print(sorted_topics)
            new_topics = {}
            for i in xrange(10):
                new_topics[sorted_topics[i][0]] = sorted_topics[i][1]
            topics = new_topics
        except Exception as e:

            print(e)

    print(topics)

    response = {"status":"ok", "topics":topics}
    bson_response = bson.BSON.encode(response)
    return str(bson_response)

if __name__ == '__main__':
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('topic-modeller')
    print("Registering gearman worker 'get-topics'")
    gearman_worker.register_task('get-topics', get_topics_gearman)
    gearman_worker.work()
