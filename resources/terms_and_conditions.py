from flask_restful import Resource


class terms_and_conditions(Resource):
    def get(self):
        return {'message': 'terms and conditions'}
