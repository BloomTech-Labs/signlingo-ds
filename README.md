# Repo layout

- The labs 22 DS team's work can be found in the *archived* folder
- *app* contains our flaskapp along with the folders and files necessary to deploy to AWS.
  - *.ebextensions* to increase max_file_body_size when deploying our model to Elastic Beanstalk. Without this increase the endpoint won't work with video.
  - *model* contains the files necessary to build the model with the correct architecture, weights, and labels.
  - *remote-docker* is for AWS deployment. The dockerfile we use that compiles ffmpeg from source takes to long to deploy normally.
  - *templates* contains our index route for API testing purposes.
  - *testing_video.mp4* for quick API testing
  - *app.py* contains the Flask class used to run the app and the API POST endpoint
  - *Dockerfile* - necessary to get opencv and ffmpeg to work on AWS EB.
  - *HelperFunctions* - Helper functions that get called in the /api route.
  - *model_test.py* - Run this file to test current model real time via webcam.
  - *ModelFunctions* - Functions to build the model, feed an image, and return a predicted letter.  
  - *Procfile* - Necessary for the Gunicorn engine & deployment
  - *Requirements.txt* - The libraries used for our model & API endpoint.
  - *unit_tests* - Testing suite. Run from the command line.
- *Notebooks* contains the notebook used to build our Yolo models.
  - Weight and cfg files get saved to the drive
  - Our most upto date model weights and cfg files for the individual lessons can be found in FlaskApp/model

# Steps to run locally

Create and navigate to a working directory and run the following.  
`git clone https://github.com/Lambda-School-Labs/signlingo-ds.git`  
`cd signlingo-ds/FlaskApp`  
Create a virtual environment.  
`pipenv shell --python 3.7`  
If the pip files are incorrectly installing the libraries into the environment, delete them and run the following  
`pipenv install -r requirements.txt`
Run the following to initialize the TEMPVID and TEMPPICS folders  
`python app.py`  
Launching the flask app (NOTE: depending on the terminal, export can be substituted for set)  
`export FLASK_APP=app.py`  
`flask run`  
<br/>
(Documentation on how to run using Docker can be found in the Dockerfile)


# YoloV3 Alphabet Model

- Further documentation can be found in the google drive but maybe a breif overview of why we chose to use object detection, maybe go into drive layout breifly, talk about data and higher level model processes we followed.


# AWS Elastic BeanStalk API

- https://ds.thesignlingo.com/api
- Expects three inputs with the following names
  - 'video' of type file
  - 'expected' of type string
  - 'right-handed' of type number (1 for right hand)

