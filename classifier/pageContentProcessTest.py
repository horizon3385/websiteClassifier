# -*- coding: utf-8 -*-
"""
pageContentProcessor Class test
"""
import sys
import json
from pageContentProcess import PageContentProcessor

pcp = PageContentProcessor()

with sys.stdin as f:
    for line in f:
        row = json.loads(line)
        #content = row['content']
        print(row.keys())

sys.exit()
#import sys
#import json
#from bs4 import BeautifulSoup
#from pageContentProcess import PageContentProcessor
#pcp = PageContentProcessor()
#
#with sys.stdin as f:
    #for line in f:
        #row = json.loads(line)
        #soup = BeautifulSoup(row['content'])
        ##print pcp.count_html_element(soup)
        #print pcp.text_extract(soup)
        #sys.exit(1)

import requests
from bs4 import BeautifulSoup
from pageContentProcess import PageContentProcessor

response = requests.get("http://www.cbsnews.com/news/paul-manafort-donald-trump-is-working-to-unify-the-party/")
soup = BeautifulSoup(response.content.decode(response.encoding))
pcp = PageContentProcessor()
text = pcp.text_extract(soup.body)

#line = '''Leicester City moved one step closer to the Premier League title with a 1-1 tie on Sunday against financial soccer giant Manchester United. The Foxes will clinch the title with one more point. A title would represents one of the biggest upsets in the history of sports. At the start of the season, bookmakers had the odds of Leicester winning the Premier League crown at 5,000 to 1 (on par with an Elvis sighting) after the squad almost faced relegation a year ago. Assuming City clinches, the dream season will result in at least $100 million in additional revenue in the short-term for Leicester, according to a study by sports research firm Repucom.'''
#pcp = PageContentProcessor()
#text = pcp.clean_paragraph(line)
print text

sys.exit(0)
import nltk
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
wnl = nltk.WordNetLemmatizer()


print [porter.stem(w) for w in text]
print [lancaster.stem(w) for w in text]
print [wnl.lemmatize(w) for w in text]




