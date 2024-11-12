from flask import Flask
from flask_restful import Api
from app_resources import Property


app = Flask(__name__)
api = Api(app)

api.add_resource(Property, "/api/properties", "/api/properties/<int:property_id>")


if __name__ == '__main__':
    app.run(debug=True)
