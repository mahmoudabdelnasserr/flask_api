from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.String(20), unique=True)
    profile_image_url = db.Column(db.String(255))

    def __init__(self, username, password,
                 phone, email, profile_image_url):
        # self.baseuser_id = baseuser_id
        self.username = username
        self.password = password
        self.email = email
        self.profile_image_url = profile_image_url
        self.phone = phone

    def json(self):
        return {'user_id': self.id,
                'username': self.username,
                'phone': self.phone, 'email': self.email,
                'profile_image_url': self.profile_image_url,
                'password': self.password}

    @classmethod
    def find_by_userid(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_image(cls, image):
        return cls.query.filter_by(profile_image_url=image).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()