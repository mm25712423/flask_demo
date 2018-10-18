import flask
from flask import render_template, request
import json

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route('/facial_recognition/classification.html')
def claddification_view():
    return render_template('Facial-recognition/classification.html')
