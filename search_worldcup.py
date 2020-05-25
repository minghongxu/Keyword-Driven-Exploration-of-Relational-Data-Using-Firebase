#!/usr/bin/env python
# coding: utf-8

# In[33]:


import json
import requests
import pandas as pd
import re


# In[ ]:





url = 'https://inf551-worldcup.firebaseio.com/index.json'
response = requests.get(url)
responsepy = json.loads(response.content)


# In[ ]:







# In[3]:


key_dict = {'WorldCupMatches': 'MatchID', 'WorldCupPlayers': 'Player Name',            'WorldCups': 'Year'}


# In[49]:


def search(search_words):
    search_list = search_words.split(' ')
    result = {'WorldCupMatches': [], 'WorldCupPlayers': [], 'WorldCups': []}
    result_dict = {}
    for i in range(len(search_list)):
        search_list[i] = search_list[i].lower()
        search_list[i] = search_list[i].strip("[, \-!?:#$\./'\@&\()\,=\+\n]+")
        try:
            for t in responsepy[search_list[i]]:
                if len(t) == 20:
                    if t['MatchID'] in result_dict:
                        result_dict[t['MatchID']] = (result_dict[t['MatchID']][0] + 1,'WorldCupMatches')
                    else:
                        result_dict[t['MatchID']] = (1, 'WorldCupMatches')
                elif len(t) == 9:
                    if t['Player Name'] in result_dict:
                        result_dict[t['Player Name']] = (result_dict[t['Player Name']][0] + 1,'WorldCupPlayers')
                    else:
                        result_dict[t['Player Name']] = (1, 'WorldCupPlayers')
                elif len(t) == 10:
                    if t['Year'] in result_dict:
                        result_dict[t['Year']] = (result_dict[t['Year']][0] + 1,'WorldCups')
                    else:
                        result_dict[t['Year']] = (1, 'WorldCups')
        except:
            pass
    sorted_list = sorted(result_dict.items(), key = lambda x: x[1][0], reverse=True)
    
    for i in sorted_list:
        value = i[0]
        table = i[1][1]
        ur = ''
        if type(value) is not str:
            value = str(int(value))
            ur = 'https://inf551-worldcup.firebaseio.com/' + table + '.json?orderBy="' +             key_dict[table] + '"&equalTo=' + value
        else:
            ur = 'https://inf551-worldcup.firebaseio.com/' + table + '.json?orderBy="' +             key_dict[table] + '"&equalTo="' + value +'"'
        ur = re.sub(r" ", '%20',ur)
        res = requests.get(ur)
        respy = json.loads(res.content)
        result[table].append(respy)
    return result






# In[52]:


def table_search(table, key, value):
    ur = ''
    if type(value) is not str:
        value = str(int(value))
        ur = 'https://inf551-worldcup.firebaseio.com/' + table + '.json?orderBy="' + key + '"&equalTo=' + value
    else:
        ur = 'https://inf551-worldcup.firebaseio.com/' + table + '.json?orderBy="' + key + '"&equalTo="' + value +'"'
    ur = re.sub(r" ", '%20',ur)
    res = requests.get(ur)
    respy = json.loads(res.content)
    return respy



# In[ ]:




