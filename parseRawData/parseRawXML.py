#!/usr/bin/python

import sys
import json

from bs4 import BeautifulSoup

import logging
logging.basicConfig(format='%(asctime)s - %(name)s -  %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



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
                logger.info("processed\t%d\t%s" % (cnt, result['url']))
                print >> sys.stdout, json.dumps(result)
                xml = ''

            if trigger:
                xml += line.rstrip('\n').replace('d:', '')


if __name__ == "__main__":
    main(sys.argv[1:])

