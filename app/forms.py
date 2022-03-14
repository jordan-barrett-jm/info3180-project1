from typing import Text
from flask_wtf import FlaskForm
from wtforms import TextField, SelectField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed, FileRequired

class PropertyForm(FlaskForm):
    title = TextField('Title')
    num_bedrooms = TextField('Number of Bedrooms')
    num_bathrooms = TextField('Number of Bathrooms')
    description = TextField('Description', widget=TextArea())
    location = TextField('Location')
    property_type = SelectField('Property Type',
                                choices=[('House', 'House'), 
                                ('Apartment', 'Apartment')])
    price = TextField('Price')
    photo = FileField('Image', validators=[
        FileRequired(),
         FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])