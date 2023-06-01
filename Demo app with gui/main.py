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
#classFrame = ttk.Frame(resultFrame)
#confidenceFrame = ttk.Frame(resultFrame)
#timeFrame = ttk.Frame(resultFrame)
resultTableFrame = ttk.Frame(resultFrame)

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
subjectClassOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectClass, borderwidth=2, relief='solid', width=11)
subjectConfidenceOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectConfidence, borderwidth=2, relief='solid', width=11)
subjectTimeOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectTime, borderwidth=2, relief='solid', width=11)
SentimentClassOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentClass, borderwidth=2, relief='solid', width=11)
SentimentConfidenceOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentConfidence, borderwidth=2, relief='solid', width=11)
SentimentTimeOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentTime, borderwidth=2, relief='solid', width=11)
errorOutput = ttk.Label(resultFrame, textvariable=error)

inputFrame.grid(column=0,row=0)

resultFrame.grid(column=0,row=1)
resultTableFrame.grid(column=0,row=1)
#classFrame.grid(column=0,row=1)
#confidenceFrame.grid(column=1,row=1)
#timeFrame.grid(column=2,row=1)

urlLabel.grid(column=0,row=0)
urlEntry.grid(column=1,row=0)
authenticationLabel.grid(column=0,row=1)
authenticationEntry.grid(column=1,row=1)
inputLabel.grid(column=0,row=2)
inputField.grid(column=1,row=2)
retrieveResultsButton.grid(column=0,row=3,columnspan=2)


ttk.Label(resultFrame, text='Tijd Data voorbereiden: ').grid(column=0,row=0)
PreProcessTimeOutput.grid(column=1,row=0)
ttk.Label(resultTableFrame, text='Onderwerp', borderwidth=2, relief='solid', width=11).grid(column=0,row=1)
ttk.Label(resultTableFrame, text='Sentiment', borderwidth=2, relief='solid', width=11).grid(column=0,row=2)
ttk.Label(resultTableFrame, text='Categorie', borderwidth=2, relief='solid', width=11).grid(column=1,row=0)
subjectClassOutput.grid(column=1,row=1)
SentimentClassOutput.grid(column=1,row=2)
ttk.Label(resultTableFrame, text='Zekerheid (%)', borderwidth=2, relief='solid', width=11).grid(column=2,row=0)
subjectConfidenceOutput.grid(column=2,row=1)
SentimentConfidenceOutput.grid(column=2,row=2)
ttk.Label(resultTableFrame, text='Tijd (s)', borderwidth=2, relief='solid', width=11).grid(column=3,row=0)
subjectTimeOutput.grid(column=3,row=1)
SentimentTimeOutput.grid(column=3,row=2)
errorOutput.grid(column=0,row=2,columnspan=2)

root.mainloop()