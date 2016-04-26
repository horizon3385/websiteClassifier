#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import requests
from bs4 import BeautifulSoup

import logging
logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(name)s -  %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_page_content(url, timeout=1):
    """
    get page `content` and `content-length` from html request
    """
    response = requests.get(url, timeout=timeout)
    content = response.content.decode(response.encoding).encode('utf-8')
    try:
        content_length = int(response.headers.get('content-length'))
    except TypeError:
        content_length = None
    response.close()
    return content, content_length


def extract_xml(markup):
    """
    Extract `url`, `title`, 'description`, and `topic` from XML 'ExternalPage' markup
    """
    soup = BeautifulSoup(markup, 'lxml')
    tag = soup.externalpage

    result = dict()
    result['url'] = tag['about']
    result['title'] = tag.title.text
    result['description'] = tag.description.text
    result['topic'] = tag.topic.text.split('/')
    try:
        content, content_length = get_page_content(result['url'])
    except requests.exceptions.Timeout:
        logger.warning('Timeout\t\t%s' % result['url'])
        return
    except UnicodeDecodeError:
        logger.warning('UnicodeEncodeError\t%s' % result['url'])
        return
    except Exception as e:
        logger.warning('%s\t%s' % (e, result['url']))
        return
    result['content'] = content
    result['content_length'] = content_length
    return result


def main(argv):

    cnt = 0
    xml = ''
    trigger = False
    with sys.stdin as f:
        for line in f:
            # set up start tag
            if '<ExternalPage' in line:
                trigger = True
            # set up close tag
            elif '</ExternalPage>' in line:
                cnt += 1
                trigger = False
                xml += line.rstrip('\n')

                # process xml block
                result = extract_xml(xml)
                if result:
                    logger.info("processed\t%d\t%s" % (cnt, result['url']))
                    print >> sys.stdout, json.dumps(result)
                xml = ''

            if trigger:
                xml += line.rstrip('\n').replace('d:', '')


if __name__ == "__main__":
    main(sys.argv[1:])

