import urllib2
import json
import os
from bs4 import BeautifulSoup

'''
Source 3: https://medium.com/web-development-zone/a-complete-list-of-computer-programming-languages-1d8bc5a891f
Given a language, returns its paradigm if known, else returns "Not Known"
'''


# performed only once when first line is processed
# otherwise info taken from scraped data file
def get_data_from_source3(lang):
    # source 3 url
    source_url = "https://medium.com/web-development-zone/a-complete-list-of-computer-programming-languages-1d8bc5a891f"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(source_url, headers=headers)

    # scrape the web page using BeautifulSoup
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")

    lang_dict = {}
    tag = soup.find('h3')
    cur_paradigm = str(tag.get_text())

    while tag.find_next_sibling('h3') is not None:
        while tag.next_sibling.name != "h3":
            tag = tag.next_sibling
            if tag.name == "h4":
                cur_lang = tag.get_text().encode('utf-8').lower()       # unicode to string
                cur_lang = cur_lang.replace("\xc2\xa0", " ")    # data source web page contains non-breaking space
                lang_dict[cur_lang] = cur_paradigm
        tag = tag.next_sibling
        cur_paradigm = str(tag.get_text())

    lang_list = tag.find_next_siblings("h4")
    for l in lang_list:
        cur_lang = l.get_text().encode('utf-8').lower()
        cur_lang = cur_lang.replace("\xc2\xa0", " ")
        lang_dict[cur_lang] = cur_paradigm

    # save the scraped dict to file "media/paradigm.json"
    directory = os.path.join(os.path.dirname(__file__), "media")
    paradigm_file = os.path.join(directory, "paradigm.json")
    with open(paradigm_file, 'w+') as outfile:
        json.dump(lang_dict, outfile)

    return lang_dict.get(lang, "Not Known")      # return the required language paradigm if it exists


def get_paradigm(lang):
    lang = lang.lower()
    directory = os.path.join(os.path.dirname(__file__), "media")
    paradigm_file = os.path.join(directory, "paradigm.json")
    exists = os.path.exists(paradigm_file)

    # if file exists, return data from file
    # else fetch from source url after scraping

    if exists:
        with open(paradigm_file) as json_data:
            lang_dict = json.load(json_data)
            return lang_dict.get(lang, "Not Known")
    else:
        return get_data_from_source3(lang)

