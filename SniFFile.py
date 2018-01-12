from flask import Flask, request, render_template, abort
from FileProcessor import process_input_file
import urllib2


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt'}       # input file containing the list of file names and file types can only be text file


# check if the passed file type is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# check for internet connectivity
def is_connected():
    try:
        url = "https://www.google.com"
        urllib2.urlopen(url)
        return True
    except:
        return False


# test URL
@app.route('/test')
def test():
    return 'SniFFile is working!'


# URL to get the input file list and post the results
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method != "POST":
        # show the form to submit input file
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

        # check for internet connectivity
        if not is_connected():
            abort(400, "No internet connection. Please connect to the internet and try again.")

        # file exists and allowed
        if input_file and allowed_file(file_name):
            file_name, error_list, res_data = process_input_file(input_file)
            return render_template('sample.html', file_name=file_name, error_list=error_list, res_data=res_data)
        else:
            abort(400, "Invalid file format. Please pass only plain text file input")


# show sample input
@app.route('/sample_input')
def show_sample_input_file():
    return render_template("sample_input.html")


if __name__ == '__main__':
    app.run()
