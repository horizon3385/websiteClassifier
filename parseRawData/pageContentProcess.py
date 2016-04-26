#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class PageContentProcessor(object):
    """
    GET url content and extract text from content.
    process `<p>` text with natural language process technology
    """

    tags_extract = ['p', 'a', 'article']
    tags_count = ['pre', 'form', 'img']
    #tags_remove = ['script', 'link', 'style']
    def __init__(self, timeout=3):
        self.timeout = timeout

    def process_url_content(self, url):
        """
        GET Response from url and process HTML content
        """
        response = requests.get(url, timeout=self.timeout)
        body = BeautifulSoup(response.content).find('body')

        results = dict()
        for tag in self.tags_extract:
            results[tag] = ' '.join([x.get_text() for x in body.findAll(tag)])

        for tag in self.tags_count:
            results[tag] = len(body.findAll(tag))

        response.close()
        return results

    @staticmethod
    def word_count(words):
        results = dict()
        for w in words:
            results.setdefault(w, 1)
            results[w] += 1
        return results

    def __call__(self, url):
        return self.process_url_content(url)



if __name__ == "__main__":
    page_content = PageContentProcessor()
    import json
    print json.dumps(page_content('http://www.abcya.com/animate.htm'))
