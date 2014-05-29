import argparse
import os
import errno
import math
import sys
import json

import models
from category import Category
from article import parse_article


JSON_EXT = ".json"


class Classifier:
    def __init__(self):
        self.docroot = ""
        self.database = ""
        self.is_training = False
        self.stop_list = frozenset()
        self.confusion_matrix = {}
        self.model = "baseline"
        self.model = models.baseline

        # parse the arguments
        self.parse_args()

        # prepare the categories collection
        self.categories = {}
        self.total_articles = 0

    def parse_args(self):
        # set up the arg-parser
        parser = argparse.ArgumentParser(prog="Naive-Bayes Classifier",
                                         description="This a Naive-Bayes classifier that works with the "
                                                     "20-Newsgroups data set.",
                                         add_help=True)

        # add the <num-threads> argument
        parser.add_argument("--docroot",
                            action="store",
                            help="The path to the directory containing the documents to be classified.")

        # add the <num-threads> argument
        parser.add_argument("--database",
                            action="store",
                            help="The path to the directory for the database created during training.  "
                                 "If the directory does not exist, it will be created.")

        # add the <debug> argument
        parser.add_argument("-t", "--training",
                            type=bool,
                            action='store',
                            help="Indicate whether training is to be performed (default = False)",
                            default=False)

        # add the <debug> argument
        parser.add_argument("--stop-list",
                            action='store',
                            help="Path to file containing the list of stop words (words to be excluded from indexing)")

        # add the <debug> argument
        parser.add_argument("--model",
                            action='store',
                            help="bernoulli, multinomial or baseline",
                            default="baseline")

        # parse the arguments
        args = parser.parse_args()

        # save the document root
        self.docroot = args.docroot

        # make sure the document root directory exists
        if not os.path.exists(self.docroot):
            raise Exception("Document root %s does not exist" % self.docroot)

        # save the knowledge database
        self.database = args.database

        # if the database location does not exist, create it
        if not os.path.exists(self.database):
            print "Database directory %s does not exist.  Creating it." % self.database
            os.makedirs(self.database)

        self.is_training = args.training

        self.model = getattr(models, args.model)
        self.model_name = args.model

        # load the list of stop words
        try:
            self.stop_list = frozenset(open(args.stop_list).read().split())
        except IOError, exc:
            if exc.errno != errno.ENOENT:
                raise
            print exc
            print "Classification will proceed without a stop list of words."

    def learn(self):
        # for each directory in the document root...
        for category_name in os.listdir(self.docroot):
            category_path = os.path.join(self.docroot, category_name)

            # if the category is a file (not a directory), then skip it
            if os.path.isfile(category_path):
                continue

            category = Category(self.database, category_name, self.stop_list)
            self.categories[category_name] = category

            # call the function to handle the directory/category
            category.categorize(category_path)
            category.save()

    def load_categories(self):
        for filename in os.listdir(self.database):
            category_name = os.path.splitext(filename)[0]

            category = Category(self.database, category_name, self.stop_list)
            if category.load():
                self.total_articles += category.article_count
                self.categories[category_name] = category

    def classify(self):
        # load all the Category instances from the database
        self.load_categories()

        # with all categories loaded, assign each their prior probability
        # (P(C=cat)) which is the number of documents in the category divided
        # by total number of documents
        for category_name in self.categories:
            category = self.categories[category_name]
            category.prior_probability = math.log(float(category.article_count) / float(self.total_articles))
            print "Prior probability for category: %s is %s articles out of %s total articles = %s" % (
                category_name, category.article_count, self.total_articles, category.prior_probability)

        for category_name in os.listdir(self.docroot):
            category_path = os.path.join(self.docroot, category_name)

            # if the category is a file (not a directory), then skip it
            if os.path.isfile(category_path):
                continue

            self.classify_category(category_path, self.model)

        #print self.confusion_matrix
        # open the output .json file for writing
        with open(os.path.join(self.docroot, self.model_name + JSON_EXT), "w") as out_file:
            print "Writing results of classification to %s" % out_file.name

            # dump the output dictionary to the .json file
            json.dump(self.confusion_matrix, out_file)

    def classify_category(self, category_path, model_func):
        confusion_row = {}

        for article in os.listdir(category_path):
            article_words = {}
            parse_article(category_path, article, article_words, self.stop_list)

            best_probability = -sys.maxint - 1
            best_category = None

            for category_name in self.categories:
                probability = model_func(self.categories[category_name], article_words)
                if probability > best_probability:
                    best_probability = probability
                    best_category = category_name

            confusion_row[best_category] = confusion_row.setdefault(best_category, 0) + 1

        self.confusion_matrix[os.path.basename(category_path)] = confusion_row


if __name__ == '__main__':
    c = Classifier()

    # try:
    #     if c.is_training:
    #         c.learn()
    #     else:
    #         c.classify()
    # except Exception, e:
    #     print e

    if c.is_training:
        c.learn()
    else:
        c.classify()
