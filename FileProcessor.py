from werkzeug.utils import secure_filename
from models import LineError, FileDetails, SingleFileLine, CustomExt, CustomLang
from Source1Helper import get_lang_cat
from Source2Helper import get_desc_apps
from Source3Helper import get_paradigm

import re
import Queue
import threading

'''
The multi-threading pattern used in the following logic is as follows:
1. Create an instance of Queue.Queue() and then populate it with data.
2. Pass that instance of populated data into the threading class that you created from inheriting from threading.Thread.
Spawn a pool of daemon threads.
3. Pull one item out of the queue at a time, and use that data inside of the thread, the run method, to do the work.
4. After the work is done, send a signal to the queue with queue.task_done() that the task has been completed.
5. Join on the queue, which really means to wait until the queue is empty, and then exit the main program. 
'''

valid_file_regex = r"^([\w_\.]+)(\.)([\w]*)$"
ext_queue1 = Queue.Queue()   # queue to hold extensions as they are waiting to be processed by source 1
ext_queue2 = Queue.Queue()   # queue to hold extensions as they are waiting to be processed by source 2
lang_queue = Queue.Queue()      # queue to hold languages as they are waiting to be processed by source 3
res_line_data_list = []         # final result list containing file details indexed by their line number


class Thread1(threading.Thread):        # thread class to fetch details (language, category) from source 1

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

            # gets language and category of the file extension
            lang_data, category_data = get_lang_cat(file_ext)

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


class Thread2(threading.Thread):            # thread class to fetch details (description, associated apps) from source 2

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # grabs file extension from queue
            custom_file_ext = self.queue.get()
            file_ext = custom_file_ext.ext
            cur_line_num = custom_file_ext.line_num

            # gets description and associated apps of the file extension
            desc_data, app_data = get_desc_apps(file_ext)

            cur_file_data = res_line_data_list[cur_line_num].my_file
            # change cur_file_data
            cur_file_data.desc = desc_data
            cur_file_data.associated_apps = app_data
            res_line_data_list[cur_line_num].my_file = cur_file_data

            # signals to queue job is done
            self.queue.task_done()


class Thread3(threading.Thread):            # thread class to fetch details (paradigm) from source 3

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # grabs language from queue
            custom_file_lang = self.queue.get()
            lang = custom_file_lang.lang
            cur_line_num = custom_file_lang.line_num

            # gets paradigm of the language
            paradigm = get_paradigm(lang)

            cur_file_data = res_line_data_list[cur_line_num].my_file
            # change cur_file_data
            cur_file_data.paradigm = paradigm
            res_line_data_list[cur_line_num].my_file = cur_file_data

            # signals to queue job is done
            self.queue.task_done()


# method to process input file line by line
def process_input_file(input_file):
    file_name = input_file.filename.strip()
    file_name = secure_filename(file_name)

    error_list = []     # list to hold the lines that don't match the pattern "<file_name>.<file_ext>"

    re_obj = re.compile(valid_file_regex)   # regex object for valid file pattern
    line_count = 0      # count to hold the line number being processed

    # adding details for a dummy line 0
    # for easy processing
    # later removed
    dummy_line = SingleFileLine(line_count)
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

    # process lines one by one in the input file
    with input_file.stream as infile:
        for line in infile:
            line = line.rstrip()
            line_count += 1
            m = re_obj.match(line)
            if m is not None:
                # line matches the valid pattern
                cur_file_name = m.group(1)
                cur_ext = m.group(3)

                # add the file information available now (file name and file extension) to result list
                # later each thread adds the respective details that they fetch
                my_file = FileDetails(cur_file_name, cur_ext)
                my_line = SingleFileLine(line_count, my_file)
                res_line_data_list.append(my_line)

                # add current extension to the queue to fetch it's corresponding details
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

    del res_line_data_list[0]       # deleting the dummy line added before

    return file_name, error_list, res_line_data_list
