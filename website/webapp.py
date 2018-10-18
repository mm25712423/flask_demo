from flask import Flask

app = Flask(__name__)

from . import index_view
app.register_blueprint(index_view.blueprint)

from . import test_view
app.register_blueprint(test_view.blueprint)

from .model.facial_recognition import classification
app.register_blueprint(classification.blueprint, url_prefix="/")