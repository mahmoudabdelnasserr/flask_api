from flask_restful import Resource


class contact_us(Resource):
    def get(self):
        name = 'Islam'
        Email = 'eslam.com'
        return {
            'name': name,
            'email': Email
        }