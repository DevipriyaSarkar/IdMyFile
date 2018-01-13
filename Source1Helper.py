import yaml
import urllib2
import json
import os
import traceback

'''
Source 1: https://github.com/github/linguist/blob/master/lib/linguist/languages.yml
Given an extension, returns its language family and category that use this extension file,
else returns "Not Known"
'''


# performed only once when first line is processed
# otherwise info taken from scraped data file
def get_data_from_source1(file_ext):
    # source 1 yaml file
    source_url = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(source_url, headers=headers)
    page = urllib2.urlopen(req)

    lang = "Not Known"
    category = "Not Known"

    try:
        data_dict = yaml.load(page)

        # remove all languages that do not have extension information
        data_dict = {k: v for k, v in data_dict.iteritems() if "extensions" in v}

        # make all extensions lower case
        for language, info in data_dict.iteritems():
            info["extensions"] = [x.lower() for x in info["extensions"]]

        # return current extension's language and category details in a dict
        # eg. {"Java": {"codemirror_mime_type": "text/x-java", "extensions": [".java"],
        #               "type": "programming", "language_id": 181}}

        # checks if language's extension list contains given file extension
        cur_lang_dict = {k: v for k, v in data_dict.iteritems() if file_ext in v.get("extensions", [])}

        for language, info in cur_lang_dict.iteritems():
            lang = language
            category = info.get("type", "Not Known")
            break  # just in case extension is used in multiple languages, retrieve the first one and return

        try:
            # save the dict to file "media/lang_info.json"
            directory = os.path.join(os.path.dirname(__file__), "media")
            if not os.path.exists(directory):
                os.makedirs(directory)
            lang_info_file = os.path.join(directory, "lang_info.json")
            with open(lang_info_file, 'w+') as outfile:
                json.dump(data_dict, outfile)
        except Exception as e:
            print e
            traceback.print_exc()
        finally:
            return lang, category

    except yaml.YAMLError as exc:
        print exc
        return lang, category


def get_lang_cat(file_ext):
    file_ext = "." + file_ext.lower()

    directory = os.path.join(os.path.dirname(__file__), "media")
    lang_info_file = os.path.join(directory, "lang_info.json")
    exists = os.path.exists(lang_info_file)

    # if file exists, return data from file
    # else fetch from source url after processing

    if exists:
        with open(lang_info_file) as json_data:
            data_dict = json.load(json_data)
            cur_lang_dict = {k: v for k, v in data_dict.iteritems() if file_ext in v.get("extensions", [])}

            lang = "Not Known"
            category = "Not Known"

            for language, info in cur_lang_dict.iteritems():
                lang = language
                category = info.get("type", "Not Known")
                break  # just in case extension is used in multiple languages, retrieve the first one and return

            return lang, category
    else:
        return get_data_from_source1(file_ext)
