import tkinter
import requests
import json

from tkinter import *
from tkinter import ttk

def RetrieveResults(*args):
    
    print('function started')
    if(text != '' and url != ''):
        if(authenticationToken != ''):
            result = requests.post(url.get(), data=text.get(), auth=authenticationToken.get())
        else:
            result = requests.post(url.get(), data=text.get())

        if(result.status_code == 200):
            try:
                result = result.json()     
            except:
                print('json error: ' + result)
                error.set('Json error: ' + result)

            resultPreProcessTime.set(result['cleaning_time'])
            resultSubjectClass.set(subjectClasses[int(result['predicted_subject_class'])])
            resultSubjectConfidence.set(result['confidence_subject'])
            resultSubjectTime.set(result['prediction_subject_time'])
            resultSentimentClass.set(SentimentClasses[int(result['predicted_sentiment_class'])])
            resultSentimentConfidence.set(result['confidence_sentiment'])
            resultSentimentTime.set(result['prediction_sentiment_time'])
        else:
            error.set('Error: HTTP code ' + str(result.status_code))

# url = 'http://localhost:80/predictBody'
# authenticationToken = ''
subjectClasses = ['andere','factuur','herhaling']
SentimentClasses = ['negatief','neutraal','positief']

root = Tk()
root.title("Demo classificeerder")
inputFrame = ttk.Frame(root).grid(column=0,row=0)
resultFrame = ttk.Frame(root).grid(column=0,row=1)

url = StringVar()
authenticationToken = StringVar()
text = StringVar()
resultPreProcessTime = StringVar()
resultSubjectClass = StringVar()
resultSubjectConfidence = StringVar()
resultSubjectTime = StringVar()
resultSentimentClass = StringVar()
resultSentimentConfidence = StringVar()
resultSentimentTime = StringVar()
error = StringVar()     

urlLabel = ttk.Label(inputFrame, text='URL:').grid(column=0,row=0)
urlEntry = ttk.Entry(inputFrame, textvariable=url).grid(column=1,row=0)
authenticationLabel = ttk.Label(inputFrame, text='Authenticatie token:').grid(column=0,row=1)
authenticationEntry = ttk.Entry(inputFrame, textvariable=authenticationToken).grid(column=1,row=1)
inputLabel = ttk.Label(inputFrame, text='Voeg e-mail tekst hier in:').grid(column=0,row=2)
inputField = ttk.Entry(inputFrame, textvariable=text).grid(column=1,row=2)
retrieveResultsButton = ttk.Button(inputFrame,text='classificeer',command=RetrieveResults).grid(column=0,row=3,columnspan=2)

PreProcessTimeOutput = ttk.Label(resultFrame, textvariable=resultPreProcessTime).grid(column=0,row=0,columnspan=3)
subjectClassOutput = ttk.Label(resultFrame, textvariable=resultSubjectClass).grid(column=0,row=1)
subjectConfidenceOutput = ttk.Label(resultFrame, textvariable=resultSubjectConfidence).grid(column=1,row=1)
subjectTimeOutput = ttk.Label(resultFrame, textvariable=resultSubjectTime).grid(column=2,row=1)
SentimentClassOutput = ttk.Label(resultFrame, textvariable=resultSentimentClass).grid(column=0,row=2)
SentimentConfidenceOutput = ttk.Label(resultFrame, textvariable=resultSentimentConfidence).grid(column=1,row=1)
SentimentTimeOutput = ttk.Label(resultFrame, textvariable=resultSentimentTime).grid(column=2,row=2)
errorOutput = ttk.Label(resultFrame, textvariable=error).grid(column=0,row=3,columnspan=3)

root.mainloop()