import os
import json
from article import parse_article

JSON_EXT = ".json"
WORDS_KEY = "words"
ARTICLES_KEY = "articles"


class Category:
    def __init__(self, database_path, category_name, stop_words):
        self.database_path = database_path
        self.category_name = category_name
        self.stop_words = stop_words
        self.article_count = 0
        self.word_counts = {}
        self.total_words = 0
        self.prior_probability = 0

    def load(self):
        try:
            # open the data file
            with open(os.path.join(self.database_path, self.category_name + JSON_EXT), "r") as in_file:
                print "Loading category %s from %s" % (self.category_name, in_file.name)
                # read the data file into a json dictionary
                
                data = json.load(in_file)
                          
                # make sure the ARTICLES_KEY and the WORDS_KEY are in the dictionary
                if not ARTICLES_KEY in data or not WORDS_KEY in data:
                    return False

                # save the article count and the word count
                self.article_count = data[ARTICLES_KEY]
                self.word_counts = data[WORDS_KEY]

            # sum up all of the word counts
            #self.total_words = sum(self.word_counts.itervalues())
            for counts in self.word_counts.itervalues():
                self.total_words += counts["m"]
        except Exception, e:
            # if there was a problem, then the category did not load successfully
            print e
            return False

        # there were no problems loading the data file
        return True

    def save(self):
        # prepare the output dictionary with the article count and the word count
        output = {ARTICLES_KEY: self.article_count, WORDS_KEY: self.word_counts}

        # open the output .json file for writing
        with open(os.path.join(self.database_path, self.category_name + JSON_EXT), "w") as out_file:
            print "Writing results of categorizing %s to %s" % (self.category_name, out_file.name)

            # dump the output dictionary to the .json file
            json.dump(output, out_file)

        # the file was saved successfully
        return True

    def categorize(self, path):
        for article in os.listdir(path):
            self.article_count += 1

            # TODO add exception handling
            parse_article(path, article, self.word_counts, self.stop_words)
