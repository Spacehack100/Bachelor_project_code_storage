# Bachelor_project_code_storage

Repo for storing code and data related to a bachelor project about AI email classification.
Note: models are stored sepperatly, as they are too big. All non-public data and corresponding references have been removed for privacy reasons.

### Setting up local Docker deployment
1) Install and start Docker deamon (tutorial here -> https://docs.docker.com/engine/install/).
2) Start a command line interface and navigate to the Docker deployment folder (which contains a 'docker-compose.yaml' file and         'inference container' map).
3) Here enter the command 'docker-compose up'. This will build the image and start a new instance.
4) After this the API can be reached via HTTP at 'localhost:8000/predictBody', adding the text in the body of the request.

### Setting up Docker deployment on Azure (with Azure Container Instances or ACI's)
1) Repeat steps 1 and 2 of 'Setting up local Docker deployment'.
2) This time use the command 'docker-compose build', as to only create an image and not start an instance.
3) Next the image needs to be uploaded to an online repository. Here Dockerhub is used since you can freely upload images (as long as they are public). For this you will need to create a Dockerhub account, open a new repository and push the image. The following documantion explains this (https://docs.docker.com/docker-hub/repos/create/).
4) Once the image is availible via the online repo, in can be deployed on an ACI. Here you will need to start again with creating an account.
5) Using the visual interface you can create a new ACI, give it a name, choose regions, etc.
6) Under 'Image source' select 'other registry', 'public' under 'Image type' and then enter the name you gave it in the repo (format of 'user/imagename').
7) Finnaly select the OS (prefferably Linux) and configure the amount of virtual processers (1 enough) and RAM (3Gb enough).
8) Under networking you can create the URL (DNS name) and change any ports if necassary.
9) After this you can deploy the ACI and reach it with HTTP at the URL configured earlier. Keep in mind to add /predictBody after it and put the text in the body of the request, as you do with a local deployment.

### Setting up Azure Machine Learning (AML) deployment
1) First create a new AML workspace. The visual interface walks you trough the needed configuration. Here you can also choose to use existing resouces if they are of the required type or let AML create new ones.
2) Once in the workspace start by creating a new environment. Give it a usefull and proper name/description, select 'use existing docker image with optional conda file' as source and copy the image name from the 'Classifier_env_config.txt' file.
3) In the next step add the dependencies part from the 'Classifier_env_config.txt' file to the 'conda.yaml' file and finish creating the enviroment.
4) Now you can upload the model(s). In the model section, click register and choose from local files. Then set type to unspecified and  upload the folders with the models. FInally give it a name/description and you're done.
5) Finnaly we can set up the endpoint. Give it a name/description, select the model, configure deployment options, choose the enviroment + upload the scoring file (located in same folder as 'Classifier_env_config.txt'), configure the amount of compute you need (1 standerd_DS2-v2 is enough), allocate the traffic to 100% and review and confirm everything.
6) The API can now be used via HTTP with the URL and Authentication token provided under the 'consume' tab. 