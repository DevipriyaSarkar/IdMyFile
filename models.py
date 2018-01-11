class LineError:

    def __init__(self, line_num=-1, line_content=None):
        self.line_num = line_num
        self.line_content = line_content

    def __str__(self):
        return "{0} : {1}".format(self.line_num, self.line_content)


class FileDetails:

    def __init__(self, file_name=None, file_ext=None):
        self.file_name = file_name
        self.file_ext = file_ext
        self.desc = None
        self.category = None
        self.lang = None
        self.paradigm = []
        self.associated_apps = []

    def __str__(self):
        return "[FileName:{0}, FileExt:{1}, Desc:{2}, Category:{3}, Lang:{4}]".format(self.file_name, self.file_ext,
                                                                                      self.desc, self.category,
                                                                                      self.lang)


class SingleFileLine:

    def __init__(self, line_num=-1, my_file=None):
        self.line_num = line_num
        self.my_file = my_file

    def __str__(self):
        return "[LINE_NUM:{0}, FILE:{1}]".format(self.line_num, self.my_file)


class CustomExt:

    def __init__(self, line_num=-1, ext=None):
        self.line_num = line_num
        self.ext = ext


class CustomLang:

    def __init__(self, line_num=-1, lang=None):
        self.line_num = line_num
        self.lang = lang
