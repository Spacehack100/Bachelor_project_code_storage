from simpletransformers.classification import ClassificationModel
from bs4 import BeautifulSoup
import re
import time
import json
import numpy as np
from scipy.special import softmax
from flask import Flask
from flask import render_template
app = Flask(__name__, template_folder="template")

class Main(object):
    def __init__(self):
        self.model = ClassificationModel("bert","model")

    def predict(self, X):
        X = json.loads(X)
        X = self.preprocess(X)
        prediction, raw_output = self.model.predict(list(X))
        return str(prediction)
    
def RemoveNonAlphanumeric(contentInput, removePunctuation = False):
        # with punctuation
        if removePunctuation == True:
            contentOutput = re.sub(r'[^A-Za-z0-9 ]+', '',contentInput)
        
        # without punctuation
        else:
            contentOutput = re.sub(r'[^A-Za-z0-9 ,?.:;!]+', '',contentInput)
            contentOutput = re.sub(r'(, ){2,}','',contentOutput)
        
        return contentOutput
    
@app.route('/')
def hello(): 
    return 'input string after /predict/'

@app.route('/predict/<text>')
def predict(text):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    response = ''
    model = ClassificationModel("bert","model", use_cuda=False)

    timePreProcessBefore = time.perf_counter()
    text = BeautifulSoup(text, features="html.parser").get_text()
    text = re.sub(r'[' + escapes + r']',' ', text)
    text = re.sub(r'http\S+', '', text)
    text = RemoveNonAlphanumeric(text, removePunctuation = False)
    text = re.sub(r'(BIC:) [A-Z]*','',text)
    text = re.sub(r'\w*\d\w*', '', text).strip()
    text = re.sub(' +', ' ', text)
    timePreProcessAfter = time.perf_counter()
    timePreProcess = timePreProcessAfter - timePreProcessBefore

    inputList = []
    inputList.append(text)
    timePredBefore = time.perf_counter()
    prediction, raw_output = model.predict(inputList)
    probabilities = softmax(raw_output[0]).tolist()
    timePredAfter = time.perf_counter()
    timePred = timePredAfter - timePredBefore
    #response = 'Predicted class = ' + str(prediction[0]) + ' Cleaning time = ' + str(timePreProcess) + ' Prediction time = ' + str(timePred)
    response = json.dumps({"predicted_class" : str(prediction[0]), "confidence" : probabilities[prediction[0]], 'cleaning_time' : timePreProcess, 'prediction_time' : timePred})

    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)