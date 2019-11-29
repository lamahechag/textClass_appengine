import logging
import re
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from flask import Flask, render_template, request, jsonify

classes = ['CROSS CATEGORY', 'EXTRA CONTENIDO', 'GRATIS CON PRODUCTO',
       'PAGUE X LLEVE Y', 'PRECIO ESPECIAL']
credentials = GoogleCredentials.get_application_default()
api = discovery.build('ml', 'v1', credentials=credentials)
PROJECT_ID = "nlsn-gcdml-glbcrm"
VERSION_NAME = "offer_class2"
MODEL_NAME = "ofert_class_1"
service = discovery.build('ml', 'v1')
name = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
name += '/versions/{}'.format(VERSION_NAME)
app = Flask(__name__)


def process_list(x):
    x = [re.sub(r'\d{6,}', '', txt) for txt in x]
    responses = service.projects().predict(name=name, body={'instances': x}).execute()
    result = [classes[i] for i in responses["predictions"]]
    return result


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():
    desc = request.form['desc']
    desc = re.sub(r'\d{6,}', '', desc)
    if ']' not in desc[-3:]:
        off_class = "REGULAR"
    else:
        responses = service.projects().predict(name=name, 
                                            body={'instances': [desc]}).execute()
        off_class = classes[responses["predictions"][0]]
    return render_template('submitted_form.html', desc=desc, off_class=off_class)


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    x = data["instances"]
    result = jsonify({'predictions': process_list(x)})
    return result


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
