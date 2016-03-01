import re
from spacy.en import English

nlp = English()

def remove_stop_words(doc):
    new_doc = []
    for index in range(len(doc)-1, -1, -1):
        if (not (doc[index]).is_stop) and (len(re.sub("\s+", "", doc[index].text)) > 0):
            new_doc.append(doc[index])
    return new_doc

def count_words(word_list):
    words = {}
    print("Word list: " + str(word_list))
    for orig_word in word_list:
        word = orig_word.text.strip()
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
    return words

def get_topics(article):
    doc = nlp(article)
    print("orig: " + str(doc))
    doc = remove_stop_words(doc)
    print("sans stop words: " + str(doc))
    word_counts = count_words(doc)
    print(word_counts)
    return word_counts
