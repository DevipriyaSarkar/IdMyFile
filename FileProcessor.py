from werkzeug.utils import secure_filename
from models import LineError, MyFile, MyLine, CustomExt, CustomLang
import re
import Queue
import threading

valid_file_regex = r"^([\w_\.]+)(\.)([\w]*)$"
ext_queue1 = Queue.Queue()   # extensions
ext_queue2 = Queue.Queue()   # extensions
lang_queue = Queue.Queue()  # language.yml
res_line_data_list = []         # final result


class Thread1(threading.Thread):        # find data from language.yml

    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            # grabs file extension from queue
            custom_file_ext = self.queue.get()
            file_ext = custom_file_ext.ext
            cur_line_num = custom_file_ext.line_num

            # gets language and other data of the host
            # lang_data = getData(file_ext)
            lang_data = "sample language 1"
            category_data = "sample category 1"

            # place language data into out lang_queue
            custom_lang = CustomLang(cur_line_num, lang_data)
            self.out_queue.put(custom_lang)

            cur_file_data = res_line_data_list[cur_line_num].my_file
            # change cur_file_data
            cur_file_data.lang = lang_data
            cur_file_data.category = category_data
            res_line_data_list[cur_line_num].my_file = cur_file_data

            # signals to ext_queue job is done
            self.queue.task_done()


class Thread2(threading.Thread):            # find data from file-extension website

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # grabs file extension from queue
            custom_file_ext = self.queue.get()
            file_ext = custom_file_ext.ext
            cur_line_num = custom_file_ext.line_num

            # gets other data of the host
            # data = getData(file_ext)
            desc_data = "sample description 2"
            app_data = ["sample app 21", "sample app 22"]

            cur_file_data = res_line_data_list[cur_line_num].my_file
            # change cur_file_data
            cur_file_data.desc = desc_data
            cur_file_data.associated_apps = app_data
            res_line_data_list[cur_line_num].my_file = cur_file_data

            # signals to queue job is done
            self.queue.task_done()


class Thread3(threading.Thread):            # find paradigm from scrapper

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # grabs language from queue
            custom_file_lang = self.queue.get()
            lang = custom_file_lang.lang
            cur_line_num = custom_file_lang.line_num

            # gets paradigm and other data of the host
            # data = getData(lang)
            paradigm = ["sample paradigm 31", "sample paradigm 32"]

            cur_file_data = res_line_data_list[cur_line_num].my_file
            # change cur_file_data
            cur_file_data.paradigm = paradigm
            res_line_data_list[cur_line_num].my_file = cur_file_data

            # signals to queue job is done
            self.queue.task_done()


def process_input_file(input_file):
    file_name = input_file.filename.strip()
    file_name = secure_filename(file_name)

    error_list = []

    re_obj = re.compile(valid_file_regex)
    line_count = 0
    dummy_line = MyLine(line_count)
    res_line_data_list.append(dummy_line)

    # spawn a pool of threads, and pass them queue instance
    for i in range(10):
        t = Thread1(ext_queue1, lang_queue)
        t.setDaemon(True)
        t.start()

    for i in range(10):
        dt = Thread2(ext_queue2)
        dt.setDaemon(True)
        dt.start()

    for i in range(10):
        dt = Thread3(lang_queue)
        dt.setDaemon(True)
        dt.start()

    # process input file lines one by one
    with input_file.stream as infile:
        for line in infile:
            line = line.rstrip()
            line_count += 1
            m = re_obj.match(line)
            if m is not None:
                # line matches the valid pattern
                # do something
                cur_file_name = m.group(1)
                cur_ext = m.group(3)
                print cur_file_name + cur_ext

                my_file = MyFile(cur_file_name, cur_ext)
                my_line = MyLine(line_count, my_file)
                res_line_data_list.append(my_line)

                custom_ext = CustomExt(line_count, cur_ext)

                # populate queue with data
                ext_queue1.put(custom_ext)
                ext_queue2.put(custom_ext)

            else:
                # line doesn't match the valid pattern
                le = LineError(line_count, line)
                error_list.append(le)

    # wait on the queue until everything has been processed
    ext_queue1.join()
    ext_queue2.join()
    lang_queue.join()

    for d in res_line_data_list:
        print d

    return file_name, error_list, res_line_data_list
