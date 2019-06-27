import os
from flask import Flask, request, g
from flask_restful import Api, Resource, reqparse
from . import botTito
import datetime as dt
from collections import defaultdict
parser = reqparse.RequestParser()

cache = defaultdict(dict)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
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
    api.add_resource(botTito.BotTito,'/tito',resource_class_kwargs={'wakeUp': cache})
    app.app_context()
    from . import db
    db.init_app(app)
    return app

app = create_app()

