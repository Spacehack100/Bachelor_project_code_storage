from simpletransformers.classification import ClassificationModel
from bs4 import BeautifulSoup
from scipy.special import softmax
import re
import json
import numpy
import time
import os


def init():
    global subjectModel
    global sentimentModel
    subjectModel_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "models/subject_model")
    sentimentModel_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "models/sentiment_model")
    subjectModel = ClassificationModel("bert",subjectModel_path,use_cuda=False)
    sentimentModel = ClassificationModel("bert",sentimentModel_path,use_cuda=False)

def run(X):
    timePreProcessBefore = time.perf_counter()
    X = preprocess(X)
    timePreProcessAfter = time.perf_counter()
    timePreProcess = timePreProcessAfter - timePreProcessBefore

    inputList = []
    inputList.append(X)
    timePredSubjectBefore = time.perf_counter()
    prediction_subject, raw_output = subjectModel.predict(inputList)
    probabilities_subject = softmax(raw_output[0]).tolist()
    timePredSubjectAfter = time.perf_counter()
    timePredSubject = timePredSubjectAfter - timePredSubjectBefore
    #response = 'Predicted class = ' + str(prediction[0]) + ' Cleaning time = ' + str(timePreProcess) + ' Prediction time = ' + str(timePred)
    if(prediction_subject[0] == 0):
        response = json.dumps({"predicted_class" : str(prediction_subject[0]), "confidence" : probabilities_subject[prediction_subject[0]], 'cleaning_time' : timePreProcess, 'prediction_time' : timePredSubject})
    else:
        timePredSentimentBefore = time.perf_counter()
        prediction_sentiment, raw_output = sentimentModel.predict(inputList)
        probabilities_sentiment = softmax(raw_output[0].tolist())
        timePredSentimentAfter = time.perf_counter()
        timePredSentiment = timePredSentimentAfter - timePredSentimentBefore
        response = json.dumps({"predicted_subject_class" : str(prediction_subject[0]), "confidence_subject" : probabilities_subject[prediction_subject[0]], "predicted_sentiment_class" : str(prediction_sentiment[0]), "confidence_sentiment" : probabilities_sentiment[prediction_sentiment[0]], 'cleaning_time' : timePreProcess, 'prediction_subject_time' : timePredSubject, 'prediction_sentiment_time' : timePredSentiment})
    return response

def preprocess(text):
        
    escapes = ''.join([chr(char) for char in range(1, 32)])

    text = BeautifulSoup(text).get_text()
    text = re.sub(r'[' + escapes + r']',' ', text)
    text = re.sub(r'http\S+', '', text)
    text = RemoveNonAlphanumeric(text, removePunctuation = True)
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
