import os
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from bot import Bot
from botTito import BotTito
parser = reqparse.RequestParser()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello',methods=('GET',"POST"))
    def hello():
        if request.method == "GET":
            return 'Hello, World!'
        else:
            return str(request)
    api.add_resource(BotTito,'/tito')

    return app
