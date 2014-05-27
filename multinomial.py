import math

class Multinomial:

    def __init__(self, categories):
        self.data = {}
        self.categories = categories
        
    def classify(self, data):
        probabilities = [0]*20
        i = 0
        for category in self.categories:
            for word in data:
                
