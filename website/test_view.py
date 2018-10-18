import flask
from flask import render_template, request
import json

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route('/A')
def A():
    return render_template('index.html')


@blueprint.route('/B')
def chart():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('test.html', values=values, labels=labels)
