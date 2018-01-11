from werkzeug.utils import secure_filename


def process_input_file(input_file):
    file_name = input_file.filename.strip()
    file_name = secure_filename(file_name)
    with input_file.stream as infile:
        for line in infile:
            print line
    return file_name
