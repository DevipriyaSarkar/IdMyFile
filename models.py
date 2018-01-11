class LineError:

    def __init__(self, line_num=-1, line_content=""):
        self.line_num = line_num
        self.line_content = line_content

    def __str__(self):
        return "{0} : {1}".format(self.line_num, self.line_content)
