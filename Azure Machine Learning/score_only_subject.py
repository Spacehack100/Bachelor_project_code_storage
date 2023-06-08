from simpletransformers.classification import ClassificationModel
from bs4 import BeautifulSoup
from scipy.special import softmax
import re
import json
import numpy
import time


def init():
    global model
    model = ClassificationModel("bert","model",use_cuda=False)

def run(X):
    X = json.loads(X)
    timePreProcessBefore = time.perf_counter()
    X = preprocess(X)
    timePreProcessAfter = time.perf_counter()
    timePreProcess = timePreProcessAfter - timePreProcessBefore

    inputList = []
    inputList.append(X)
    timePredBefore = time.perf_counter()
    prediction, raw_output = model.predict(inputList)
    timePredAfter = time.perf_counter()
    timePred = timePredAfter - timePredBefore
    probabilities = softmax(raw_output[0]).tolist()
    return json.dumps({"predicted_class" : str(prediction[0]), "confidence" : probabilities[prediction[0]], 'cleaning_time' : timePreProcess, 'prediction_time' : timePred})

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
