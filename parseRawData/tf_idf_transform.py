# -*- coding: utf-8 -*-
from __future__ import division

import math
import json
from operator import add


class TFIDF:
    def __init__(self, corpus_rdd=None):
        """
        Input the pyspark.SparkContext RDD object

        Data Structure:

        >>> CORPUS = [
        ...         {"this": 1, "is": 1, "a": 2, "sample": 1},
        ...         {"this": 1, "is": 1, "another": 2, "example": 3}
        ...     ]
        >>> corpus_rdd = sc.parallelize(CORPUS)
        """
        if corpus_rdd is None:
            raise(ValueError("Corpus cannot be `None` object"))
        self.corpus_rdd = corpus_rdd

    @property
    def total_documents(self):
        """
        return: total count of all documents in corpus rdd
        """
        if hasattr(self, "_total_documents"):
            return self._total_documents
        self._total_documents = self.corpus_rdd.map(lambda x: 1).reduce(add)
        return self._total_documents

    @property
    def terms(self):
        """
        return: (`terms`, `count`) tuple list for all terms
        """
        if hasattr(self, '_terms'):
            return self._terms
        self._terms = self.corpus_rdd\
            .flatMap(lambda document: document.items())\
            .reduceByKey(add)\
            .map(lambda (term, count): (count, term))\
            .sortByKey(False)\
            .map(lambda (count, term): (term, count))\
            .collect()
        return self._terms

    def select_terms(self, head=None, threshold=None):
        """
        `head`: take the first N elements from term list
        `threshold`: take elements with count greater than threshold
            overwrite by `head` if set
        """
        if not head is None:
            return [term[0] for term in self.terms[:head]]
        elif not threshold is None:
            return [term[0] for term in self.terms if term[1] > threshold]
        else:
            raise(ValueError("Either `head` or `threshold` must be set"))

    @property
    def idf_vector(self):
        """
        return: inverse document frequency vector
            a dict of terms
        """
        if hasattr(self, "_idf_vector"):
            return self._idf_vector

        total = self.total_documents
        self._idf_vector = dict(self.corpus_rdd\
            .flatMap(lambda document: document.keys())\
            .map(lambda term: (term, 1))\
            .reduceByKey(add)\
            .map(lambda (term, count): (term, math.log10(total / count)))\
            .collect())
        return self._idf_vector

    def tf_idf_score(self, head=None, threshold=None):
        terms = self.select_terms(head, threshold)
        idf_vector = self.idf_vector
        tf_idf = self.corpus_rdd\
            .map(lambda document: [document.get(t, 0) * idf_vector[t] for t in terms])\
            .collect()
        return terms, tf_idf