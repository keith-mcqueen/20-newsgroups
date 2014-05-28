import os


def parse_article(filepath, filename, dictionary, stop_words=None):
    # load the file
    article_path = os.path.join(filepath, filename)
    with open(os.path.join(filepath, filename), "r") as in_file:
        for word in str.split(in_file.read()):
            word = word.lower()
            dictionary[word] = dictionary.setdefault(word, 0) + 1

    #print str(dictionary)
