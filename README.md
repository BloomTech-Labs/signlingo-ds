# Repo layout

- The labs 22 DS team's work can be found in the archived folder
- FlaskApp
- Notebooks contains the notebook used to build our Yolo models.
  - Weight and cfg files get saved to the drive
  - Our most upto date model weights and cfg files for the individual lessons can be found in FlaskApp/model

# Steps to run locally

Create and navigate to a working directory and run the following.
`git clone https://github.com/Lambda-School-Labs/signlingo-ds.git`
`cd signlingo-ds/FlaskApp`
Create a virtual environment.
`pipenv shell --python 3.7`
`pipenv install -r requirements.txt`
Launching the flask app (NOTE: depending on the terminal, export can be substituted for set)
`export FLASK_APP=SignLingoAPI.py`
`flask run`

Flask App File structure:

- SignLingoAPI.py contains the routes and launches the app
- HelperFunctions contains functions to help split incoming video and manage temporary image/video storage
- ModelFunctions contains functions to make predictions using the model


# Model

Getting Started:
(THIS IS A VERY ROUGH DRAFT)

Initially the idea was to build an all purpose generalized model that could handle any signs thrown at it. Upon further research and investigation, we found just how hard it would be to achieve that. To get up to spead on the differences between sign language recognition, continuous sign language recognition, and sign language translation we recommend the following research ________________________. With this in mind and the goal of building a DuoLingo app for signing, we decided that the best course of action was to treat this as an object detection problem. At the current stage of the project, each lesson focuses on a small subset of signs. By having a model for each individual lesson we can increase accuracy. The idea is to train on labelled (letter of sign) images along with bounding boxes (coordinates) of where the sign is located in the image.

### Predictions

- Describe your models here

### Data Sources

- Labs 22 used _______ Kaggle dataset. Can be found here ________________
- Contact ____ for credentials to the drive that contains the photos Labs 24 used to train.
- Go into file structure of drive here


# AWS Elastic BeanStalk API

### How to connect to the web API

- API endpoints, what they expect, and what they return

### How to connect to the data API

Getting Started:

- Contact ____ for the login credentials
- navigate to ________________
