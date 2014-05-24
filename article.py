import os


def parse_article(filepath, filename, dictionary, stop_words=None):
    # load the file
    file = open(filepath + os.sep + filename, 'r')

    # read the words
    for line in file:
        print line

    pass