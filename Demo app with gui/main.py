import requests
import pickle
import os

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
        if(authenticationToken.get() != ''):
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
        error.set('Error: Geen tekst of URL gegeven!')

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
inputFrame = ttk.Frame(mainFrame, borderwidth=2, relief='raised')
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
resultTableFrame.grid(column=0,row=1)

urlLabel.grid(column=0,row=0, sticky='e')
urlEntry.grid(column=1,row=0, sticky='we')
authenticationLabel.grid(column=0,row=1, sticky='e')
authenticationEntry.grid(column=1,row=1, sticky='we')
inputLabel.grid(column=0,row=2, sticky='e')
inputField.grid(column=1,row=2, sticky='we')
retrieveResultsButton.grid(column=0,row=3,columnspan=2)


ttk.Label(resultFrame, text='Tijd Data voorbereiden: ').grid(column=0,row=0)
PreProcessTimeOutput.grid(column=1,row=0)
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
#inputFrame.grid_propagate(False)
#inputFrame.after(500, lambda: inputFrame.configure(width=resultFrame.winfo_width()))

Load()
root.mainloop()

