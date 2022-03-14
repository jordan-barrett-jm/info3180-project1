from . import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    num_bedrooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    description = db.Column(db.String(255))
    location = db.Column(db.String(40))
    property_type = db.Column(db.String(20))
    price = db.Column(db.Float)
    photo = db.Column(db.String(255))

    def __init__(self, title, num_bedrooms, num_bathrooms,
    description, location, property_type, price,
    photo):
        self.title = title
        self.num_bathrooms = num_bedrooms
        self.description = description
        self.location = location
        self.property_type = property_type
        self.price = price
        self.photo = photo
