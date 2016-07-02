# -*- coding: utf -*-
"""
webpage content process class

process webpage content cleaning
html elements feature extract
natual language stemming and words count

return a dict object
"""
import re
from bs4 import BeautifulSoup
from collections import Counter

import nltk
from nltk import word_tokenize
from nltk import pos_tag

wnl = nltk.WordNetLemmatizer()
porter = nltk.PorterStemmer()

def tagger():
    # current one is nltk pos_tag tagger
    return pos_tag

def sentence_word_tagger_stemmer(paragraph, selected=None):
    if selected is None:
        selected = ('NN', 'JJ', 'PR', 'RB', 'UH', 'VB')
    tags = pos_tag(word_tokenize(paragraph))

    # filter by selected tags
    words = [tag[0] for tag in tags if tag[1][:2] in selected]

    # Lemmatization
    #words = [wnl.lemmatize(word) for word in words]

    # Stem
    words = [porter.stem(word) for word in words]

    return words


class PageContentProcessor(object):
    """
    GET url content and extract text from content.
    process `<p>` text with natural language process technology

    webpage content is body element of html page content
    """

    def __init__(self, tags_extract=None, tags_count=None):
        """
        tags_extract default ('p', 'a', 'article')
        tags_count default ('pre', 'form', 'img', 'script', 'link', 'style')
        """
        if tags_extract is None:
            tags_extract = ('p', 'a', 'article')
        if tags_count is None:
            tags_count = ('pre', 'form', 'img', 'script', 'link', 'style')

        self.tags_extract = tags_extract
        self.tags_count = tags_count
        self.tags_remove = ('script', 'link', 'style')

    def count_html_element(self, webpagecontent):
        """
        count pre-defined elements
        """
        #assert isinstance(webpagecontent, BeautifulSoup)

        counter = Counter()
        for element in self.tags_count:
            counter[element] += len(webpagecontent.findAll(element))
        return counter

    @staticmethod
    def clean_paragraph(paragraph):
        # add ntlk feature in this function
        return sentence_word_tagger_stemmer(paragraph)

    def text_extract(self, webpagecontent):
        text = []
        #for element in self.tags_extract:
        #    text += webpagecontent.findAll(element)
        #print text
        for element in self.tags_remove: 
            for s in webpagecontent(element):
                s.extract()
        text = webpagecontent.get_text()
        return Counter(self.clean_paragraph(text))

    def __call__(self, webpagecontent):
        output = dict()
        output['count_element'] = dict(self.count_html_element(webpagecontent))
        output['count_words'] = dict(self.text_extract(webpagecontent))
        return output


if __name__ == "__main__":
    import sys
    import json
    pcp = PageContentProcessor()

    with sys.stdin as f:
        for line in f:
            row = json.loads(line)
            webpagecontent = BeautifulSoup(row.pop('content')).body
            row.update(pcp(webpagecontent))
            print json.dumps(row)

