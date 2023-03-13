from simpletransformers.classification import ClassificationModel
from bs4 import BeautifulSoup
import re

class Main(object):
    def __init__(self):
        self.model = ClassificationModel("bert","model")

    def predict(self, X):
        X = str(X)
        X = self.preprocess(X)
        prediction, raw_output = self.model.predict(list(X))
        return str(prediction)

    def preprocess(self, text):
        
        escapes = ''.join([chr(char) for char in range(1, 32)])

        text = BeautifulSoup(text).get_text()
        text = re.sub(r'[' + escapes + r']',' ', text)
        text = re.sub(r'http\S+', '', text)
        text = self.RemoveNonAlphanumeric(text, removePunctuation = True)
        text = re.sub(r'(BIC:) [A-Z]*','',text)
        text = re.sub(r'\w*\d\w*', '', text).strip()
        text = re.sub(' +', ' ', text)

        return text

    def RemoveNonAlphanumeric(contentInput, removePunctuation = False):
        # with punctuation
        if removePunctuation == True:
            contentOutput = re.sub(r'[^A-Za-z0-9 ]+', '',contentInput)
        
        # without punctuation
        else:
            contentOutput = re.sub(r'[^A-Za-z0-9 ,?.:;!]+', '',contentInput)
            contentOutput = re.sub(r'(, ){2,}','',contentOutput)
        
        return contentOutput

    