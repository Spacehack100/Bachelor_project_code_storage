import tkinter
import requests
import json

from tkinter import *
from tkinter import ttk

def RetrieveResults(*args):
    
    print('function started')
    if(text.get() != '' and url.get() != ''):
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
    else:
        print('No text or URL given')
        error.set('Geen text of URL gegeven!')

# url = 'http://localhost:80/predictBody'
# authenticationToken = ''
subjectClasses = ['andere','factuur','herhaling']
SentimentClasses = ['negatief','neutraal','positief']

root = Tk()
root.title("Demo classificeerder")
inputFrame = ttk.Frame(root, width=200, height=100, borderwidth=2, relief='raised')
resultFrame = ttk.Frame(root, width=200, height=100, borderwidth=2, relief='sunken')

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

urlLabel = ttk.Label(inputFrame, text='URL:')
urlEntry = ttk.Entry(inputFrame, textvariable=url)
authenticationLabel = ttk.Label(inputFrame, text='Authenticatie token:')
authenticationEntry = ttk.Entry(inputFrame, textvariable=authenticationToken)
inputLabel = ttk.Label(inputFrame, text='Voeg e-mail tekst hier in:')
inputField = ttk.Entry(inputFrame, textvariable=text)
retrieveResultsButton = ttk.Button(inputFrame,text='classificeer',command=RetrieveResults)

PreProcessTimeOutput = ttk.Label(resultFrame, textvariable=resultPreProcessTime)
subjectClassOutput = ttk.Label(resultFrame, textvariable=resultSubjectClass)
subjectConfidenceOutput = ttk.Label(resultFrame, textvariable=resultSubjectConfidence)
subjectTimeOutput = ttk.Label(resultFrame, textvariable=resultSubjectTime)
SentimentClassOutput = ttk.Label(resultFrame, textvariable=resultSentimentClass)
SentimentConfidenceOutput = ttk.Label(resultFrame, textvariable=resultSentimentConfidence)
SentimentTimeOutput = ttk.Label(resultFrame, textvariable=resultSentimentTime)
errorOutput = ttk.Label(resultFrame, textvariable=error)

inputFrame.grid(column=0,row=0)
resultFrame.grid(column=0,row=1)

urlLabel.grid(column=0,row=0)
urlEntry.grid(column=1,row=0)
authenticationLabel.grid(column=0,row=1)
authenticationEntry.grid(column=1,row=1)
inputLabel.grid(column=0,row=2)
inputField.grid(column=1,row=2)
retrieveResultsButton.grid(column=0,row=3,columnspan=2)

PreProcessTimeOutput.grid(column=0,row=0,columnspan=3)
subjectClassOutput.grid(column=0,row=1)
subjectConfidenceOutput.grid(column=1,row=1)
subjectTimeOutput.grid(column=2,row=1)
SentimentClassOutput.grid(column=0,row=2)
SentimentConfidenceOutput.grid(column=1,row=1)
SentimentTimeOutput.grid(column=2,row=2)
errorOutput.grid(column=0,row=3,columnspan=3)

root.mainloop()