
class Bernoulli:

    def __init__(self, categories):
        self.data = {}
        self.categories = categories
    
    def classify(self, data):
        probabilities = [1]*20
        i = 0
        
        for category in self.categories:
            for word in data:
                probabilities[i] *= category[word]
            i++
        
        best = 0
        i = 0
        
        for prob in probabilities:
            if prob > probabilities[best]:
                best = i
            i++
            
        return best
