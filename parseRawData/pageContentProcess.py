#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class PageContentProcess(object):
    """
    GET url content and extract text from content.
    process `<p>` text with natural language process technology
    """

    tags_extract = ['a', 'p']
    tags_count = ['pre', 'form', 'img', 'audio', 'video']
    tags_remove = ['script', 'link', 'style']
    def __init__(self, timeout=3):
        self.timeout = timeout

    def process_html_content(self, url):
        """
        GET Response and process HTML content
        """
        response = requests.get(url, timeout=self.timeout)
        response.close()
        return response

    def process_content(self, response):
        body = BeautifulSoup(response.content).find('body')

        # extract text from `tags_extract`
        

        # count HTML elements exist and remove
        results = dict()
        for tag in self.tags_remove_count:
            results[tag] = len([x.extract() for x in body.findAll(tag)])

        text = body.get_text().replace(u'\n', '')

        results.update({"text": text})
        return results

    @staticmethod
    def word_count(words):
        results = dict()
        for w in words:
            results.setdefault(w, 1)
            results[w] += 1
        return results

    def __call__(self, url):
        response, headers = self.fetch_content(url)
        results = self.process_content(response)
        results.update(headers)
        return results
