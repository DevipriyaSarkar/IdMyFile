from flask import Flask, request, render_template, abort
from FileProcessor import process_input_file

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/test')
def test():
    return 'SniFFile is working!'


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method != "POST":
        return render_template('index.html')
    else:
        if 'input_file' not in request.files:
            abort(400, "Input file not passed")

        input_file = request.files['input_file']
        file_name = input_file.filename.strip()
        # if user does not select file, browser also
        # submit a empty part without filename
        if file_name == '':
            abort(400, "Input file not passed")

        if input_file and allowed_file(file_name):
            file_name = process_input_file(input_file)
            return render_template('result.html', file_name=file_name)
        else:
            abort(400, "Invalid file format. Please pass only plain text file input")


if __name__ == '__main__':
    app.run()
