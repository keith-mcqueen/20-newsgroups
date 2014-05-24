import os
from article import parse_article

def categorize(dirpath, catname, stop_words=None):
    print dirpath
    print catname

    word_counts = {}

    article_count = 0
    catpath = dirpath + os.sep + catname
    for article in os.listdir(catpath):
        article_count += 1

        # TODO add exception handling
        parse_article(catpath, article, word_counts, stop_words)

    return word_counts, article_count
