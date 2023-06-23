import requests
import time
import json

# "https://form-recognizer-stage-test.cognitiveservices.azure.com/formrecognizer/documentModels/prebuilt-invoice:analyze?api-version=2022-08-31 -H Content-Type: application/json -H Ocp-Apim-Subscription-Key: 33146113e46645c484b64657d4609320 --data-ascii {'urlSource': 'https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf'}"
tempValue = "https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf"
inputValue = ""
timeOut = 0
recognizerURL = 'https://form-recognizer-stage-test.cognitiveservices.azure.com//formrecognizer/documentModels/prebuilt-invoice:analyze?api-version=2022-08-31'

while(inputValue != "0"):
    inputValue = input("Enter URL of document or enter 'exit' to quit the application: ")
    timeOut = 0

    if inputValue != "0":
        postResult = requests.post(recognizerURL, data='{"urlSource": "' + tempValue + '"}', headers={'Content-Type' : 'application/json', 'Ocp-Apim-Subscription-Key' : '33146113e46645c484b64657d4609320'})
        getResult = requests.get(postResult.headers.get('Operation-Location'),headers={'Ocp-Apim-Subscription-Key' : '33146113e46645c484b64657d4609320'})
        actualResponse = getResult.json()

        while actualResponse['status'] == 'running' and timeOut != 5:
            time.sleep(1)
            getResult = requests.get(postResult.headers.get('Operation-Location'),headers={'Ocp-Apim-Subscription-Key' : '33146113e46645c484b64657d4609320'})
            actualResponse = getResult.json()
            timeOut = timeOut + 1

        if actualResponse['status'] == 'succeeded':
            print(actualResponse['VendorTaxId'])

        

