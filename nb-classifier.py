import argparse
import os
from category import categorize


class Classifier:
    def __init__(self):
        # parse the arguments
        self.parse_args()

        # print self.docroot
        # print self.databsae
        # print self.is_training

    def parse_args(self):
        # set up the arg-parser
        parser = argparse.ArgumentParser(prog='Naive-Bayes Classifier',
                                         description='blah, blah',
                                         add_help=True)

        # add the <num-threads> argument
        parser.add_argument('--docroot', type=str, action='store',
                            help='where the documents are located')

        # add the <num-threads> argument
        parser.add_argument('--database', type=str, action='store',
                            help='where the learning database is (or should be) located')

        # add the <debug> argument
        parser.add_argument('-t', '--training', type=bool, action='store',
                            help='Are we training?', default=False)

        # parse the arguments
        args = parser.parse_args()

        # set the number of threads to use
        self.docroot = args.docroot
        self.databsae = args.database
        self.is_training = args.training

    def learn(self):
        for item in os.listdir(self.docroot):
            # call the function to handle the directory/category
            word_count, article_count = categorize(self.docroot, item)

            # write the returned dictionary out to the category/directory name in the database

    def classify(self):
        pass


if __name__ == '__main__':
    c = Classifier()
    if c.is_training:
        c.learn()
    else:
        c.classify()