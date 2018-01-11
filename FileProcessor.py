from werkzeug.utils import secure_filename
import re
from models import LineError

valid_file_regex = r"^([\w_\.]+)(\.)([\w]*)$"


def process_input_file(input_file):
    file_name = input_file.filename.strip()
    file_name = secure_filename(file_name)

    error_list = []

    re_obj = re.compile(valid_file_regex)

    line_count = 0
    with input_file.stream as infile:
        for line in infile:
            line = line.rstrip()
            line_count += 1
            m = re_obj.match(line)
            if m is not None:
                # line matches the valid pattern
                # do something
                print line + " matches"
            else:
                # line doesn't match the valid pattern
                le = LineError(line_count, line)
                error_list.append(le)

    return file_name
