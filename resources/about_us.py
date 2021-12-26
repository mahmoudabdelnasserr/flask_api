from flask_restful import Resource


class About_us(Resource):
    def get(self):
        return {'message': 'hello this is our page hello this is our page hello this is our page hello this is our page hello this is our page'}