from flask import Blueprint
from app.controllers import *

blueprint = Blueprint('routes', __name__)


@blueprint.route('/prediction')
def predict():
    return predictions.predict()


@blueprint.route('/')
def home():
    return 'Hello World!'
