"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from .forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

#Property-related routes

@app.route('/properties/create', methods=['POST', 'GET'])
def createProperty():
    form = PropertyForm()
    if request.method == 'POST':
        print (form.data)
        # Get property data and save to database and file repository
        if form.validate_on_submit():
            #first, save the property image added
            property_image = form.photo.data
            property_filename = secure_filename(property_image.filename)
            property_image.save(
                os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], property_filename)
            )
            #next, create the property object and save it to the database
            property = Property(form.title.data, form.num_bedrooms.data,
                                form.num_bathrooms.data, form.description.data,
                                form.location.data, form.property_type.data,
                                form.price.data, property_filename)
            db.session.add(property)
            db.session.commit()
            flash('File Saved', 'success')
            return redirect(url_for('home'))
        else:
            print (form.errors)
            print ("Invalid Form Submission")

    return render_template('propertyForm.html', form=form)

@app.route('/properties', methods=['GET'])
def getProperties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<propertyid>', methods=['GET'])
def getProperty(propertyid):
    property = Property.query.filter_by(id=propertyid).first()
    return render_template('propertyDetail.html', property=property)

@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), 
    app.config['UPLOAD_FOLDER']), filename)

def get_uploaded_images():
    upload_dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    file_list = []
    for  subdir, dirs, files in os.walk(upload_dir):
        for file in files:
            if file.endswith(".jpeg") or file.endswith('.png') or file.endswith('.jpg'):
             file_list.append(file)
    print (file_list)
    return file_list

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
