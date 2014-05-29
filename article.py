import os
import re


def parse_article(filepath, filename, dictionary, stop_words=None):
    # load the file
    with open(os.path.join(filepath, filename), "r") as in_file:
        input_str = in_file.read()
        input_str = re.sub(r'\W+', ' ', input_str)
       
        for word in str.split(input_str):
            if word not in stop_words:
                word = word.lower()
                dictionary[word] = dictionary.setdefault(word, {"multinomial": 0, "bernoulli": {}})
                dictionary[word]["multinomial"] += 1

                bernoulli = dictionary[word]["bernoulli"]
                bernoulli[filename] = bernoulli.setdefault(filename, {filename: 1})
