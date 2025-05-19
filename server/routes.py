from flask import Blueprint
from flask_restful import Api

main = Blueprint('main', __name__)
api = Api(main)

# API Version 1 Prefix
API_PREFIX = '/api/v1'

@main.route('/')
def home():
    return 'Welcome To Ja Gedo API!'