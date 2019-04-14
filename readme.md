# Google scrape and LDA for SEO
This project will scrape google results for a particular keyword and analyse the top pages to give an understanding of the distribution of keywords on the pages.

There are 2 parts to this project:

1. Scraping google for a particular keyword / set of keywords
2. Analysing the returning urls for patterns in keyword usage (LDA approach and simple tuples)


## 1. Scraping Google

The first jupter notebook `Scraping Google for SEO.ipynb` (converted to `google_seo.py`): 

- inputs a keyword and the number of results to fetch 
- outputs array with dictionaries with each result and the respective html tags

## 2. NLP

Uses a little bit of spacy, sklearn and nltk to analyse the combination of keywords.

1. LDA
2. tuples 
3. n-tuples



---
### Todo
- Multiple keywords at the same time.
- Clean the html further
- Complete the LDA to include graphs