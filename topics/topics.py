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

def update_article_data(old_data, link, modifications):
    if "items" not in old_data:
        raise IndexError("No 'items' entry exists in the document")
    for item in old_data["items"]:
        if item["link"] == link:
            for k in modifications:
                item[k] = modifications[k]
            break
    return old_data
        

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
    try:
        log(0, 'got topics, sending to db')
        gclient = gearman.GearmanClient(['localhost:4730'])
        log(0, '_id:' + str(bson.ObjectId(data['_id'])))
        log(0, data)
        db_resp = bson.BSON.decode(bson.BSON(gclient.submit_job('db-get', str(bson.BSON.encode({'database':'feedlark', 'collection':'feed', 'query':{u'_id':data[u'_id']}, 'projection':{'_id':1, 'items':1}}))).result))
        if len(db_resp['docs']) == 0:
             raise Exception('No documents returned with given query.')
        old_data = db_resp['docs'][0]
        log(0, 'old_data: ' + str(old_data))
        modifications = {"topics":topics}
        link = data['link']
        new_data = update_article_data(old_data, link, modifications)
        log(0, 'new_data: ' + str(new_data))
        r = bson.BSON.decode(bson.BSON(gclient.submit_job('db-update', str(bson.BSON.encode({'database':'feedlark', 'collection': 'feed', 'data':{'selector':{'_id':data['_id']}, 'updates':new_data}}))).result))
    except Exception as e:
	log(2, str(e))
        response = {"status":"error", "description": str(e)}        

    bson_response = bson.BSON.encode(response)
    return str(bson_response)

if __name__ == '__main__':
    gearman_client = gearman.GearmanClient(['localhost:4730'])
    gearman_worker = gearman.GearmanWorker(['localhost:4730'])
    gearman_worker.set_client_id('topic-modeller')
    log(0, "Registering gearman worker 'get-topics'")
    gearman_worker.register_task('get-topics', get_topics_gearman)
    gearman_worker.work()
