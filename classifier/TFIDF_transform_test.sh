time ~/Hadoop/spark-1.6.1-bin-hadoop2.6/bin/spark-submit \
	--name "TFIDF Transform Test"\
	--master "local[*]"\
	--conf "spark.driver.maxResultSize=2g"\
	TFIDF_transform_test.py 2>/dev/null | less