# General Info

### Tech Stack

Python, Flask, AWS Elastic Beanstalk, Tensorflow

### Data Sources

- Labs 22 used _______ Kaggle dataset. Can be found here ________________
- Contact ____ for credentials to the drive that contains the photos Labs 24 used to train.
- Go into file structure of drive here

# Model

Getting Started:
(THIS IS A ROUGH DRAFT)

Initially the idea was to build an all purpose generalized model that could handle any signs thrown at it. Upon further research and investigation, we found just how hard it would be to achieve that. To get up to spead on the differences between sign language recognition, continuous sign language recognition, and sign language translation we recommend the following research ________________________. With this in mind and the goal of building a DuoLingo app for signing, we decided that the best course of action was to treat this as an object detection problem. At the current stage of the project, each lesson focuses on a small subset of signs. By having a model for each individual lesson we can increase accuracy. The idea is to train on labelled (letter of sign) images along with bounding boxes (coordinates) of where the sign is located in the image.

### Predictions

- Describe your models here

# Flask App

Getting started:

- Git clone the repo
- cd into the FlaskApp subdirectory
- pipenv shell to create a virtual environment
- Ensure your virtual environment is active, if not shell into it
- pipenv install flask
- code . to open up files in your text editor
- export FLASK_APP=SignLingoAPI.py (set if using anaconda)
- flask run

File Structure:

- How the files are related here

# AWS Elastic BeanStalk API

### How to connect to the web API

- API endpoints, what they expect, and what they return

### How to connect to the data API

Getting Started:

- Contact ____ for the login credentials
- navigate to ________________
