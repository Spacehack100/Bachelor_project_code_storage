import requests
import pickle
import os

from tkinter import *
from tkinter import ttk

filename = 'Demo app with gui\data.pk'

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

# url = 'http://localhost:80/predictBody'
# authenticationToken = ''
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
subjectClassOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectClass, borderwidth=2, relief='solid', width=13,anchor='center')
subjectConfidenceOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectConfidence, borderwidth=2, relief='solid', width=13,anchor='center')
subjectTimeOutput = ttk.Label(resultTableFrame, textvariable=resultSubjectTime, borderwidth=2, relief='solid', width=13,anchor='center')
SentimentClassOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentClass, borderwidth=2, relief='solid', width=13,anchor='center')
SentimentConfidenceOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentConfidence, borderwidth=2, relief='solid', width=13,anchor='center')
SentimentTimeOutput = ttk.Label(resultTableFrame, textvariable=resultSentimentTime, borderwidth=2, relief='solid', width=13,anchor='center')
errorOutput = ttk.Label(resultFrame, textvariable=error)

mainFrame.grid(column=0,row=0)
inputFrame.grid(column=0,row=0)
resultFrame.grid(column=0,row=1)
resultTableFrame.grid(column=0,row=1)

urlLabel.grid(column=0,row=0)
urlEntry.grid(column=1,row=0)
authenticationLabel.grid(column=0,row=1)
authenticationEntry.grid(column=1,row=1)
inputLabel.grid(column=0,row=2)
inputField.grid(column=1,row=2)
retrieveResultsButton.grid(column=0,row=3,columnspan=2)


ttk.Label(resultFrame, text='Tijd Data voorbereiden: ').grid(column=0,row=0)
PreProcessTimeOutput.grid(column=1,row=0)
ttk.Label(resultTableFrame, text='Onderwerp', borderwidth=2, relief='solid', width=13,anchor='center').grid(column=0,row=1)
ttk.Label(resultTableFrame, text='Sentiment', borderwidth=2, relief='solid', width=13,anchor='center').grid(column=0,row=2)
ttk.Label(resultTableFrame, text='Categorie', borderwidth=2, relief='solid', width=13,anchor='center').grid(column=1,row=0)
subjectClassOutput.grid(column=1,row=1)
SentimentClassOutput.grid(column=1,row=2)
ttk.Label(resultTableFrame, text='Zekerheid (%)', borderwidth=2, relief='solid', width=13,anchor='center').grid(column=2,row=0)
subjectConfidenceOutput.grid(column=2,row=1)
SentimentConfidenceOutput.grid(column=2,row=2)
ttk.Label(resultTableFrame, text='Tijd (s)', borderwidth=2, relief='solid', width=13,anchor='center').grid(column=3,row=0)
subjectTimeOutput.grid(column=3,row=1)
SentimentTimeOutput.grid(column=3,row=2)
errorOutput.grid(column=0,row=2,columnspan=2)

root.resizable(False, False)
root.protocol('WM_DELETE_WINDOW', Save)

Load()
root.mainloop()