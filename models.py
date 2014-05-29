from category import Category
import math


def bernoulli(category, article_words):
    print "bernoulli"
    probability = category.prior_probability
	
    for word in article_words:
        if word in category.word_counts:
            word_probability = category.word_counts[word]["b"] 
        else:
            word_probability = 1
		
        probability += math.log(word_probability)
	
    return probability


def multinomial(category, article_words):
    return 0


def baseline(category, article_words):
    return category.prior_probability
