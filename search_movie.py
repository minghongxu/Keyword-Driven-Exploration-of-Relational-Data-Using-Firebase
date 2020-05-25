#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests
import pandas as pd
import re


# In[ ]:





# In[2]:


url = 'https://inf551-movie.firebaseio.com/index.json'
response = requests.get(url)
responsepy = json.loads(response.content)


# In[ ]:





key_dict = {'movies': 'movieId', 'ratings': 'Index', 'tags': 'Index'}


# In[3]:


def search(search_words):
    search_list = search_words.split(' ')
    result = {'movies': [], 'ratings': [], 'tags': []}
    result_dict = {}
    for i in range(len(search_list)):
        search_list[i] = search_list[i].lower()
        search_list[i] = search_list[i].strip("[, \-!?:#$\./'\@&\()\,=\+\n]+")
        try:
            for t in responsepy[search_list[i]]:
                if len(t) == 3:
                    if t['movieId'] in result_dict:
                        result_dict[t['movieId']] = (result_dict[t['movieId']][0] + 1,'movies')
                    else:
                        result_dict[t['movieId']] = (1, 'movies')
                elif len(t) == 5:
                    if t['Index'] in result_dict:
                        result_dict[t['Index']] = (result_dict[t['Index']][0] + 1,'ratings')
                    else:
                        result_dict[t['Index']] = (1, 'ratings')
                elif len(t) == 4:
                    if t['Index'] in result_dict:
                        result_dict[t['Index']] = (result_dict[t['Index']][0] + 1,'tags')
                    else:
                        result_dict[t['Index']] = (1, 'tags')
        except:
            pass
    sorted_list = sorted(result_dict.items(), key = lambda x: x[1][0], reverse=True)
    
    for i in sorted_list:
        value = i[0]
        table = i[1][1]
        ur = ''
        if type(value) is not str:
            value = str(int(value))
            ur = 'https://inf551-movie.firebaseio.com/' + table + '.json?orderBy="' +             key_dict[table] + '"&equalTo=' + value +'&print=pretty'
        else:
            ur = 'https://inf551-movie.firebaseio.com/' + table + '.json?orderBy="' +             key_dict[table] + '"&equalTo="' + value +'"&print=pretty'
        ur = re.sub(r" ", '%20',ur)
        res = requests.get(ur)
        respy = json.loads(res.content)
        result[table].append(respy)
    return result




# In[8]:


def table_search(table, key, value):
    ur = ''
    if type(value) is not str:
        value = str(int(value))
        ur = 'https://inf551-movie.firebaseio.com/' + table + '.json?orderBy="' + key + '"&equalTo=' + value
    else:
        ur = 'https://inf551-movie.firebaseio.com/' + table + '.json?orderBy="' + key + '"&equalTo="' + value +'"'
    ur = re.sub(r" ", '%20',ur)
    res = requests.get(ur)
    respy = json.loads(res.content)
    return respy







# In[ ]:




