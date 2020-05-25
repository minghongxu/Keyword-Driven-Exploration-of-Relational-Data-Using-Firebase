#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests
import pandas as pd
import re


# In[ ]:





# In[2]:


url = 'https://inf551-world.firebaseio.com/index.json'
response = requests.get(url)
responsepy = json.loads(response.content)


# In[ ]:





key_dict = {'country': 'Code', 'city': 'ID', 'countrylanguage': 'Language'}


# In[22]:


def search(search_words):
    search_list = search_words.split(' ')
    result = {'country': [], 'city': [], 'countrylanguage': []}
    result_dict = {}
    for i in range(len(search_list)):
        search_list[i] = search_list[i].lower()
        search_list[i] = search_list[i].strip("[, \-!?:#$\./'\@&\()\,=\+\n]+")
        try:
            for t in responsepy[search_list[i]]:
                if len(t) == 15:
                    if t['Code'] in result_dict:
                        result_dict[t['Code']] = (result_dict[t['Code']][0] + 1,'country')
                    else:
                        result_dict[t['Code']] = (1, 'country')
                elif len(t) == 5:
                    if t['ID'] in result_dict:
                        result_dict[t['ID']] = (result_dict[t['ID']][0] + 1,'city')
                    else:
                        result_dict[t['ID']] = (1, 'city')
                elif len(t) == 4:
                    if t['Language'] in result_dict:
                        result_dict[(t['CountryCode'],t['Language'])] = (result_dict[(t['CountryCode'],t['Language'])][0] + 1,'countrylanguage')
                    else:
                        result_dict[(t['CountryCode'],t['Language'])] = (1, 'countrylanguage')
        except:
            pass
    sorted_list = sorted(result_dict.items(), key = lambda x: x[1][0], reverse=True)
    
    for i in sorted_list:
        value = i[0]
        table = i[1][1]
        ur = ''
        if table == 'countrylanguage':
            countrycode = value[0]
            language = value[1]
            ur1 = 'https://inf551-world.firebaseio.com/' + table + '.json?orderBy="CountryCode"&equalTo="'             + countrycode +'"&print=pretty'
            ur1 = re.sub(r" ", '%20',ur1)
            res1 = requests.get(ur1)
            respy = json.loads(res1.content)
            for key in respy:
                if respy[key]['Language'] == language:
                    result[table].append({key:respy[key]})

        elif type(value) is not str:
            value = str(int(value))
            ur = 'https://inf551-world.firebaseio.com/' + table + '.json?orderBy="' +             key_dict[table] + '"&equalTo=' + value +'&print=pretty'
            ur = re.sub(r" ", '%20',ur)
            res = requests.get(ur)
            respy = json.loads(res.content)
            result[table].append(respy)        
        else:
            ur = 'https://inf551-world.firebaseio.com/' + table + '.json?orderBy="' +             key_dict[table] + '"&equalTo="' + value +'"&print=pretty'
            ur = re.sub(r" ", '%20',ur)
            res = requests.get(ur)
            respy = json.loads(res.content)
            result[table].append(respy)
    return result




# In[12]:


def table_search(table, key, value):
    ur = ''
    if type(value) is not str:
        value = str(int(value))
        ur = 'https://inf551-world.firebaseio.com/' + table + '.json?orderBy="' + key + '"&equalTo=' + value
    else:
        ur = 'https://inf551-world.firebaseio.com/' + table + '.json?orderBy="' + key + '"&equalTo="' + value +'"'
    ur = re.sub(r" ", '%20',ur)
    res = requests.get(ur)
    respy = json.loads(res.content)
    return respy



# In[ ]:




