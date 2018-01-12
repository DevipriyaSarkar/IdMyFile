# -*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup

'''
Source 2: https://en.wikipedia.org/wiki/List_of_filename_extensions
Given an extension, returns its short description and applications that use this extension file,
else returns "Not Known"
'''


def get_data_from_source2(file_ext):
    # determine source 2 URL as source url has categorised the file ext based on first character of ext
    # go to https://en.wikipedia.org/wiki/List_of_filename_extensions to understand
    source_url = "https://en.wikipedia.org/wiki/List_of_filename_extensions"
    first_char_ext = file_ext[0]
    desc = "Not Known"
    associated_apps = "Not Known"

    if not first_char_ext.isalnum():
        source_url = source_url + "#!$@"
    elif first_char_ext.isdigit():
        source_url = source_url + "#0%E2%80%939"
    elif first_char_ext.isalpha():
        if ord('A') <= ord(first_char_ext) <= ord('E'):
            source_url = source_url + "_(A–E)#" + first_char_ext
        elif ord('F') <= ord(first_char_ext) <= ord('L'):
            source_url = source_url + "_(F–L)#" + first_char_ext
        elif ord('M') <= ord(first_char_ext) <= ord('R'):
            source_url = source_url + "_(M–R)#" + first_char_ext
        elif ord('S') <= ord(first_char_ext) <= ord('Z'):
            source_url = source_url + "_(S–Z)#" + first_char_ext
    else:
        # not known
        return desc, associated_apps

    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(source_url, headers=headers)

    # scrape the web page using BeautifulSoup
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    pattern = re.compile(file_ext, re.IGNORECASE)
    tags = soup.find('td', text=pattern).find_next_siblings('td')

    if tags is not None:
        desc = tags[0].get_text()
        associated_apps = tags[1].get_text()

    return desc, associated_apps


def get_desc_apps(file_ext):
    file_ext = file_ext.upper()
    return get_data_from_source2(file_ext)