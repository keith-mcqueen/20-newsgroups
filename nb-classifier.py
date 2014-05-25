import argparse
import os
import errno
import json
from category import categorize


class Classifier:
    def __init__(self):
        self.docroot = ""
        self.database = ""
        self.is_training = False
        self.stop_list = frozenset()

        # parse the arguments
        self.parse_args()

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
        for category in os.listdir(self.docroot):
            # if the category is a file (not a directory), then skip it
            if os.path.isfile(category):
                continue

            # call the function to handle the directory/category
            word_count, article_count = categorize(self.docroot, category, self.stop_list)

            output = {}
            output["articles"] = article_count
            output["words"] = word_count

            # write the returned dictionary out to the category/directory name in the database
            with open(os.path.join(self.database, category + ".json"), "w") as out_file:
                print "Writing results of categorizing %s to %s" % (category, out_file.name)
                json.dump(output, out_file)

    def classify(self):
        pass


if __name__ == '__main__':
    c = Classifier()

    try:
        if c.is_training:
            c.learn()
        else:
            c.classify()
    except Exception, e:
        print e