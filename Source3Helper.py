import urllib2
from bs4 import BeautifulSoup


def get_data_from_source3():

    source_url = "https://medium.com/web-development-zone/a-complete-list-of-computer-programming-languages-1d8bc5a891f"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(source_url, headers=headers)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    paradigm_dict = {}
    tag = soup.find('h3')
    cur_paradigm = tag.get_text()
    cur_lang_list = []

    while tag.find_next_sibling('h3') is not None:
        while tag.next_sibling.name != "h3":
            tag = tag.next_sibling
            if tag.name == "h4":
                cur_lang_list.append(tag.get_text())
        paradigm_dict[cur_paradigm] = cur_lang_list
        tag = tag.next_sibling
        cur_paradigm = tag.get_text()
        cur_lang_list = []

    lang_list = tag.find_next_siblings("h4")
    for l in lang_list:
        cur_lang_list.append(l.get_text())
    paradigm_dict[cur_paradigm] = cur_lang_list
