import os
import pickle
import requests
import time
import re

from k import kwords
from c import cwords

## Load or open files for saving data
# Load from file if possible
fname = './words_to_search.pkl'
if os.path.isfile(fname):
    print('Loaded from file', fname)
    pkl_file = open(fname, 'rb')
    words_to_search = pickle.load(pkl_file)
    pkl_file.close()
else:
    words_to_search = []
    for word in cwords:
        word = word.replace('c', 'k', 1)
        if word not in kwords:
            words_to_search.append(word)

    pkl_file = open(fname, 'wb')
    pickle.dump(words_to_search, pkl_file)
    pkl_file.close()
    print('Saved to file', fname)
print(len(words_to_search), 'words_to_search')

# Load from file if possible
fname = './bad_k_names.pkl'
if os.path.isfile(fname):
    print('Loaded from file', fname)
    pkl_file = open(fname, 'rb')
    bad_k_names = pickle.load(pkl_file)
    pkl_file.close()
else:
    bad_k_names = []
print(len(bad_k_names), 'bad_k_names')

# Load from file if possible
fname = './visited.pkl'
if os.path.isfile(fname):
    print('Loaded from file', fname)
    pkl_file = open(fname, 'rb')
    visited = pickle.load(pkl_file)
    pkl_file.close()
else:
    visited = []
print(len(visited), 'visited')

# define function for searching the current word list
def search_list():
    for word in all_k_words:
        if word not in visited:
            # search only the words that haven't been visited

            urlstring = 'https://api.opencorporates.com/v0.4/companies/search?jurisdiction_code=us_sc&q='+word
            print(urlstring)
            r = requests.get(urlstring)

            if r.status_code == 200:

                visited.append(word)
                fname = './visited.pkl'
                pkl_file = open(fname, 'wb')
                pickle.dump(visited, pkl_file)
                pkl_file.close()
                print('Saved to file', fname)

                json = r.json()
                temp = json['results']['companies']
                for company in temp:
                    name = company['company']['name']
                    name = name.lower()

                    if name not in bad_k_names:
                        print(name)
                        bad_k_names.append(name)
                        fname = './bad_k_names.pkl'
                        pkl_file = open(fname, 'wb')
                        pickle.dump(bad_k_names, pkl_file)
                        pkl_file.close()
                        print('Saved to file', fname)

            time.sleep(2)


# Search these initial words to build a list of business names
all_k_words = ['kabinet', 'kabinets', 'kamp', 'kamps', 'kampground', 'kampgrounds', 'kap', 'kaps', 'kapstone', 'kapstones', 'kar', 'kars', 'kare', 'kares', 'kat', 'kats', 'klan', 'kleen', 'kleeners', 'klub', 'klubs', 'klunker', 'klunkers', 'kolor', 'koncept', 'koncepts', 'konnection', 'konnections', 'korn', 'korner', 'korral', 'kosy', 'kount', 'kountry', 'kover', 'kovers', 'krab', 'kraft', 'kraftsmen', 'kraftsman', 'krazy', 'kreations', 'kreation', 'kreative', 'kunnection', 'kuntry', 'kupboard', 'kustom', 'kute', 'kuts', 'kut', 'kutts', 'kutt', 'kwik']
search_list()

# For each word in each business name, find all the k words
for business in bad_k_names:
    for word in business.split():
        word = re.sub('[,]', '', word)
        word = word.lower()
        if word.startswith('k') and word not in kwords and word not in visited and word not in all_k_words:
            cword = word.replace('k', 'c', 1)
            if cword in cwords:
                if word not in words_to_search:
                    words_to_search.append(word)

                all_k_words.append(word)
                print('added', word, 'to all_k_words')

search_list()

f = open("bad_company_names.txt","wt")
print(bad_k_names, file=f)
f.close()
