import urllib2
from bs4 import BeautifulSoup


def get_data_from_source3(lang):

    source_url = "https://medium.com/web-development-zone/a-complete-list-of-computer-programming-languages-1d8bc5a891f"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(source_url, headers=headers)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    lang_dict = {}
    tag = soup.find('h3')
    cur_paradigm = str(tag.get_text())

    while tag.find_next_sibling('h3') is not None:
        while tag.next_sibling.name != "h3":
            tag = tag.next_sibling
            if tag.name == "h4":
                cur_lang = tag.get_text()
                if cur_lang in lang_dict:
                    lang_dict[cur_lang].append(cur_paradigm)
                else:
                    lang_dict[cur_lang] = [cur_paradigm]
        tag = tag.next_sibling
        cur_paradigm = str(tag.get_text())

    lang_list = tag.find_next_siblings("h4")
    for l in lang_list:
        cur_lang = l.get_text()
        if cur_lang in lang_dict:
            lang_dict[cur_lang].append(cur_paradigm)
        else:
            lang_dict[cur_lang] = [cur_paradigm]


