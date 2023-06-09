from simpletransformers.classification import ClassificationModel
from bs4 import BeautifulSoup
import re
import time
import json
import numpy as np
from scipy.special import softmax
from flask import Flask, request
from flask import render_template
app = Flask(__name__, template_folder="template")

class Main(object):
    def __init__(self):
        self.model = ClassificationModel("bert","model")

    def predict(self, X):
        #X = json.loads(X)
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

@app.route('/predict/<inputText>')
def predictURL(inputText):
    return actualPredict(inputText)

@app.route('/predictBody', methods=['POST'])
def predictBody():
    request.get_data()
    inputText = request.data
    return actualPredict(inputText)

def actualPredict(text):
    response = ''

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
    timePredSubjectBefore = time.perf_counter()
    prediction_subject, raw_output = subjectModel.predict(inputList)
    probabilities_subject = softmax(raw_output[0]).tolist()
    timePredSubjectAfter = time.perf_counter()
    timePredSubject = timePredSubjectAfter - timePredSubjectBefore
    #response = 'Predicted class = ' + str(prediction[0]) + ' Cleaning time = ' + str(timePreProcess) + ' Prediction time = ' + str(timePred)
    if(prediction_subject[0] == 0):
        response = json.dumps({"predicted_subject_class" : str(prediction_subject[0]), "confidence_subject" : probabilities_subject[prediction_subject[0]], 'cleaning_time' : timePreProcess, 'prediction_subject_time' : timePredSubject})
    else:
        timePredSentimentBefore = time.perf_counter()
        prediction_sentiment, raw_output = sentimentModel.predict(inputList)
        probabilities_sentiment = softmax(raw_output[0].tolist())
        timePredSentimentAfter = time.perf_counter()
        timePredSentiment = timePredSentimentAfter - timePredSentimentBefore
        response = json.dumps({"predicted_subject_class" : str(prediction_subject[0]), "confidence_subject" : probabilities_subject[prediction_subject[0]], "predicted_sentiment_class" : str(prediction_sentiment[0]), "confidence_sentiment" : probabilities_sentiment[prediction_sentiment[0]], 'cleaning_time' : timePreProcess, 'prediction_subject_time' : timePredSubject, 'prediction_sentiment_time' : timePredSentiment})
    return response

if __name__ == '__main__':
    escapes = ''.join([chr(char) for char in range(1, 32)])
    subjectModel = ClassificationModel("bert","subject_model", use_cuda=False)
    sentimentModel = ClassificationModel("bert","sentiment_model", use_cuda=False)
    app.run(debug=False, host='0.0.0.0', port=80)