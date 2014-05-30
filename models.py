from category import Category
import math


def bernoulli(category, article_words):
    probability = category.prior_probability

    for word in article_words:
        if word in category.word_counts:
            word_probability = category.word_counts[word]["b"]
        else:
            word_probability = 1 - 1/len(article_words)

        probability += math.log(word_probability)

    return probability


def multinomial(category, article_words):
    probability = category.prior_probability

    for word in article_words:
        if word in category.word_counts:
            word_probability = category.word_counts[word]["m"]
        else:
            word_probability = 1 - 1/len(article_words)

        probability += math.log(word_probability)

    return probability


def baseline(category, article_words):
    return category.prior_probability
