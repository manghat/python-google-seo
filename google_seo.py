
# coding: utf-8

# In[22]:


# importing the neccessary dependancies

import bs4 as bs #importing beautiful script => reads the HTML
from bs4.element import Comment
import urllib.request # to request a url => gets the page
import time
import requests
import pandas as pd


# # The objective is to get the SEO relevant info for the top ranking pages on google 
# 
# 

# In[6]:


# filters for visible elements dependant on from bs4.element import Comment

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = bs.BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return "\n ".join(t.strip() for t in visible_texts)


# In[7]:


def get_txt(url):
    r  = requests.get(url,headers=USER_AGENT).text
#     r = urllib.request.urlopen(i).read()
#     soup = bs.BeautifulSoup(r.text,'lxml')    
    a = text_from_html(r)
    t = a.split(' ')
    return t
#     o.append([w for w in t if len(w)>3 and w.istitle()])
#     o.append(a)    


# In[48]:


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def get_seo(url):
    html_txt  = requests.get(url,headers=USER_AGENT).text
#     txt = get_txt(html_txt)
    soup = bs.BeautifulSoup(html_txt, 'html.parser')
    txt = text_from_html(html_txt)
    out = {}
    
    out['h1'] = [a.text.strip() for a in soup.findAll('h1')]
    out['h2']= [a.text.strip() for a in soup.findAll('h2')]
    out['title']= soup.title.string
    meta = []
    for tags in soup.find_all('meta'):
        meta.append(tags.get('content'))
#     out.append({'h1': h1, 'h2' : h2, 'title' : title, 'meta' : meta, 'text' : txt})
    out['meta'] = meta
    out['text'] = txt
    return out

a =  get_seo('https://intercom.com/')


# ## Scrape function
# 
# fetch_results() - gets the urls of the search results.
# 
# i/p - keyword, no. of results. and language

# In[15]:


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# fetch google search results

def fetch_results(search_term, number_results, language_code = 'en'):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
 
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()
 
    return search_term, response.text
 


# # Parsing the results

# In[52]:


# Filter urls
def filter_result(url):
    exclude_list= ['youtube', 'dailymotion', 'facebook'] # exlude these websites
    return url.startswith('http') and url.split('.')[1] not in exclude_list

#Parsed results

def parse_results(html, keyword):
    soup = bs.BeautifulSoup(html, 'html.parser')
    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
#         title = result.find('h3', attrs={'class': 'r'})
        title = result.find('h3', attrs={'class': 'LC20lb'})
        description = result.find('span', attrs={'class': 'st'})
#         print(link['href'])
#         to add the other stuff - SEO related
        if link and title:
            link = link['href']
            print(link)
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#' and filter_result(link):
                temp = get_seo(link)
                found_results.append({
                    'keyword': keyword, 
                    'rank': rank, 
                    'title': title, 
                    'description': description, 
                    'link':link, 
                    'doc':get_txt(link), 
                    'h1':temp['h1'], 
                    'h2': temp['h2'], 
                    'title' : temp['title']})
# #                 print({'keyword': keyword, 'rank': rank, 'title': title, 'description': description})
                rank += 1
#                 links.append(link)
    return(found_results)


# In[53]:


# parse_results(fetch_results('delhi public school', 5, 'en')[1],fetch_results('delhi public school justdial', 5, 'en')[0] )


# # Main function

# In[57]:


def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


# if __name__ == '__main__':
# #     keywords = ['edmund martin', 'python', 'google scraping']

# destination = input('What is your keyword?')
# x = destination
# links =[]
# # keywords = [x+" tourism", x+" travel", x+" vaccation"]
# data = []
# # for keyword in x:

keyword = input('What is your keyword?')
results = int(input('How Many search results would you want to fetch : '))
data = []

try:
    results = scrape_google(keyword, results, "en")
    for result in results:
        data.append(result)
        print(len(results))
except Exception as e:
    print(e)
finally:
    time.sleep(1)


# In[58]:


data

