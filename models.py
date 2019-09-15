from Flsk import db
import datetime


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class Customer(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    about = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(12))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    anketa = db.relationship('Anketa', backref='customer', lazy=True)
    tariff = db.relationship('Tariff', backref='customer', lazy=True)



class Anketa(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(64), nullable=False, default='Online')
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    phonenumber = db.Column(db.String(20))
    categories_sex = db.relationship('Categories_sex', backref='anketa', lazy=True)
    rating = db.Column(db.Float(), nullable=False)
    otzyvy = db.relationship('Otzyvy', backref='anketa', lazy=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'),
                          nullable=False)
    na_vyezd = db.relationship('Na_vyezd', backref='anketa', lazy=True)
    calls = db.relationship('Calls', backref='anketa', lazy=True)
    texts = db.relationship('Texts', backref='anketa', lazy=True)
    views = db.relationship('Views', backref='anketa', lazy=True)
    photos = db.relationship('Photos', backref='anketa', lazy=True)

class Tariff(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_tariff = db.Column(db.String(), nullable=False, default='Стандарт')
    tariff_price = db.Column(db.Float(), nullable=False, default=10000)
    tariff_base = db.Column(db.Float(), nullable=False, default=30)
    tariff_status = db.Column(db.String(), nullable=False, default='Not_Active')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'),
                          nullable=False)

class Categories_sex(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_category = db.Column(db.String(), nullable=False, default='Классика')
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                            nullable=False)

class Otzyvy(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otzyv = db.Column(db.Text(), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    seen = db.Column(db.Boolean, nullable=False, default=True)
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                          nullable=False)

class Na_vyezd(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False, default='У себя')
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                          nullable=False)
class Calls(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                          nullable=False)

class Texts(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                          nullable=False)

class Views(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                          nullable=False)

class Photos(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    anketa_id = db.Column(db.Integer, db.ForeignKey('anketa.id'),
                          nullable=False)
    info = db.Column(db.String(), nullable=True)
    image = db.Column(db.String(), nullable=False)


    # def __init__(self, name, author, published):
    #     self.name = name
    #     self.author = author
    #     self.published = published
    #
    # def __repr__(self):
    #     return '<id {}>'.format(self.id)
    #
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'author': self.author,
    #         'published': self.published
    #     }