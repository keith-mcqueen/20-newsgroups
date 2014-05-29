import os
import re


def parse_article(filepath, filename, dictionary, stop_words=None):
    # load the file
    with open(os.path.join(filepath, filename), "r") as in_file:
        input_str = in_file.read()
        input_str = re.sub(r'\W+', ' ', input_str)

        found_words = set()
        for word in str.split(input_str):
            if word not in stop_words:
                word = word.lower()
                dictionary[word] = dictionary.setdefault(word, {"m": 0, "b": 0})
                dictionary[word]["m"] += 1

                if word not in found_words:
                    dictionary[word]["b"] += 1
                    found_words.add(word)
