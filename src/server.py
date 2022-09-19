from flasgger import Swagger
from flask import Flask, Blueprint
from flask.blueprints import Blueprint
from flask_migrate import Migrate
from flask_restful import Api

import config
import routes
from models import db
from utils import errors

# config your API specs
# you can define multiple specs in the case your api has multiple versions
# ommit configs to get the default (all views exposed in /spec url)
# rule_filter is a callable that receives "Rule" object and
#   returns a boolean to filter in only desired views
api_bp = Blueprint('api', __name__)
api = Api(api_bp, errors=errors)
server = Flask(__name__)

server.config["SWAGGER"] = {
    "swagger_version": "2.0",
    "title": "Gomerce API",
    'uiversion': 3,
    "static_url_path": "/apidocs",
}
Swagger(server)

server.debug = config.DEBUG
server.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS  # noqa
db.init_app(server)
db.app = server
migrate = Migrate(server, db)

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.APPLICATION_ROOT)
server.register_blueprint(api_bp)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT)
