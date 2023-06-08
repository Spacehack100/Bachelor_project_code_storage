import requests
import pickle
import os
import json

from tkinter import *
from tkinter import ttk

filename = 'Demo app with gui\data.pk'
tableWidth = 14
tableAnchor = 'center'
tableRelief = 'solid'
tableBorderWidth = 2

def RetrieveResults(*args):
    
    print('function started')
    if(text.get() != '' and url.get() != ''):
        try:
            if(authenticationToken.get() != ''):
                result = requests.post(url.get(), data=text.get(), headers = {'Authorization':('Bearer '+ authenticationToken.get())})
            else:
                result = requests.post(url.get(), data=text.get())
        except Exception as e:
            print('Connection error: ' + str(e))
            error.set('Connection error: ' + str(e))
            return

        if(result.status_code == 200):
            try:
                if(type(result) != type.__dict__):
                    result = result.json()
                if(type(result) == type.__str__):
                    result = json.loads(result)
            except:
                print('json error: ' + result)
                error.set('Json error: ' + result)
                return

            preProcessTime = round(float(result['cleaning_time']),5)
            subjectConfidence = round(float(result['confidence_subject'])*100,2)
            subjectTime = round(float(result['prediction_subject_time']),3)
            sentimentConfidence = round(float(result['confidence_sentiment'])*100,2)
            sentimentTime = round(float(result['prediction_sentiment_time']),3)

            resultPreProcessTime.set(str(preProcessTime) + ' seconden')
            resultSubjectClass.set(subjectClasses[int(result['predicted_subject_class'])])
            resultSubjectConfidence.set(subjectConfidence)
            resultSubjectTime.set(subjectTime)
            resultSentimentClass.set(SentimentClasses[int(result['predicted_sentiment_class'])])
            resultSentimentConfidence.set(sentimentConfidence)
            resultSentimentTime.set(sentimentTime)
        else:
            error.set('Error: HTTP code ' + str(result.status_code))
            return
    else:
        print('No text or URL given')
        error.set('Error: Geen tekst of URL gegeven!')
        return

def Save(*args):
    try:
        dataList = [url.get(),authenticationToken.get()]
        with open(filename, 'wb') as savePointer:
            pickle.dump(dataList,savePointer)
    except:
        print('could not save data!')
    root.destroy()

def Load(*args):
    if(os.path.isfile(filename)):
        with open(filename, 'rb') as loadPointer:
            dataList = pickle.load(loadPointer)
            url.set(dataList[0])
            authenticationToken.set(dataList[1])

subjectClasses = ['andere','factuur','herhaling']
SentimentClasses = ['negatief','neutraal','positief']

root = Tk()
root.title("Demo classificeerder")
mainFrame = ttk.Frame(root, padding=5)
inputFrame = ttk.Frame(mainFrame)
resultFrame = ttk.Frame(mainFrame, borderwidth=2, relief='sunken')
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
subjectClassOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectClass, borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor)
subjectConfidenceOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectConfidence, borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor)
subjectTimeOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectTime, borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor)
SentimentClassOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentClass, borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor)
SentimentConfidenceOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentConfidence, borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor)
SentimentTimeOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentTime, borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor)
errorOutput = ttk.Label(resultFrame, textvariable=error)

mainFrame.grid(column=0,row=0)
inputFrame.grid(column=0,row=0, sticky='we')
inputFrame.grid_columnconfigure(0, weight=1)
inputFrame.grid_columnconfigure(1, weight=1)
resultFrame.grid(column=0,row=1)
resultTableFrame.grid(column=0,row=1, columnspan=2)

urlLabel.grid(column=0,row=0, sticky='e')
urlEntry.grid(column=1,row=0, sticky='we')
authenticationLabel.grid(column=0,row=1, sticky='e')
authenticationEntry.grid(column=1,row=1, sticky='we')
inputLabel.grid(column=0,row=2, sticky='e')
inputField.grid(column=1,row=2, sticky='we')
retrieveResultsButton.grid(column=0,row=3,columnspan=2)


ttk.Label(resultFrame, text='Tijd Data voorbereiden: ').grid(column=0,row=0, sticky='e')
PreProcessTimeOutput.grid(column=1,row=0, sticky='w')
ttk.Label(resultTableFrame, text='Onderwerp', borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor).grid(column=0,row=1)
ttk.Label(resultTableFrame, text='Sentiment', borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor).grid(column=0,row=2)
ttk.Label(resultTableFrame, text='Categorie', borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor).grid(column=1,row=0)
subjectClassOutput.grid(column=1,row=1)
SentimentClassOutput.grid(column=1,row=2)
ttk.Label(resultTableFrame, text='Zekerheid (%)', borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor).grid(column=2,row=0)
subjectConfidenceOutput.grid(column=2,row=1)
SentimentConfidenceOutput.grid(column=2,row=2)
ttk.Label(resultTableFrame, text='Tijd (s)', borderwidth=tableBorderWidth, relief=tableRelief, width=tableWidth,anchor=tableAnchor).grid(column=3,row=0)
subjectTimeOutput.grid(column=3,row=1)
SentimentTimeOutput.grid(column=3,row=2)
errorOutput.grid(column=0,row=2,columnspan=2)

root.resizable(False, False)
root.protocol('WM_DELETE_WINDOW', Save)
root.bind('<Return>', RetrieveResults)

Load()
root.mainloop()

# url local: http://localhost:8000/predictBody
# url Azure Docker: http://emailclassificationwithsentiment.bbg9h8bvfqbaf8ht.westeurope.azurecontainer.io/predictBody
# url Azure ML: https://emailclassifiertest-full-v1.westeurope.inference.ml.azure.com/score
# authentication token AML: 5UVRpJNhYlVd2h2XbW0If7pOKKSSJ9yx