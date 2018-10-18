import flask
from .utils import device_info
from flask import render_template, request
import json

blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route('/', methods=['GET'])
def home():
    cpu = device_info.getCpuInfo()
    mem = device_info.getMemoryInfo()
    disk = device_info.getDiskInfo()
    test = {
        'label': ['2010', '2011', '2012', '2013', '2014', '2015', '2016'],
        'values': {
            'Gpu0': ['0', '4', '2', '3', '6', '9', '6'],
            'Gpu1': ['4', '1', '7', '2', '8', '2', '6']
        }
    }

    return render_template('index.html', cpu=cpu, mem=mem, disk=disk, ads=test)
