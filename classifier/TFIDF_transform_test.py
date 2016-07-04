# -*-coding: utf-8 -*-
import json
from pprint import pprint
from operator import add
from bs4 import BeautifulSoup


from pageContentProcess import PageContentProcessor
from TFIDFTransform import TFIDF



pcp = PageContentProcessor()

def process_document(line):
    try:
        data = json.loads(line)
        content = BeautifulSoup(data['content']).body
        return pcp.text_extract(content)
    except TypeError:
        return {}
    else:
        raise


def main(sc, fname):
    rdd = sc.textFile(fname)\
        .map(lambda line: process_document(line))\
        .cache()

    word_count = rdd.flatMap(lambda x: x.items())\
        .reduceByKey(add)\
        .map(lambda (term, count): (count, term))\
        .sortByKey(False)\
        .take(100)
    pprint(word_count)

    """
    tfidf = TFIDF(rdd)
    print(tfidf.total_documents)
    print(tfidf.select_terms(head=100))
    terms, tfidf_score = tfidf.tf_idf_score(head=100)

    import pandas as pd
    df = pd.DataFrame(tfidf_score, columns=terms, index=range(len(tfidf_score)))
    print(df)"""


if __name__ == "__main__":
    
    from pyspark import SparkContext
    sc = SparkContext()
    fname = '/home/minghao/webCategorization/websiteClassifier/parseRawData/raw_data_head.json'
    
    main(sc, fname)
    """
    import sys
    with sys.stdin as f:
        for line in f:
            data = json.loads(line)
            content = data['content']
            webpagecontent = BeautifulSoup(content).body
            print(pcp.text_extract(webpagecontent))
    """
