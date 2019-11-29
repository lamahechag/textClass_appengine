# textClass_appengine
This a project to train a short text classifier and deploy it to App Engine

## Train and save model
In the short_text_class notebook the model is fit using the data in the `.xlsx` file. 
The last cell has the code to save the model and encoders vectorizers to `.joblib`, which
can be deploy in AI platform and call via REST API.

## Deploy to AI Platform

To deploy the model and encoders:

[https://cloud.google.com/ml-engine/docs/deploying-models]()


## Create Flak App in App Engine

The folder `appengine` has the code to easily create a webapp in Flask workframe.
This allows to test the classifier via web, as also delivere a REST API.

[https://cloud.google.com/appengine/docs/standard/python3/quickstart]()