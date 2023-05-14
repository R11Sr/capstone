from app import app
from flask import render_template, flash, request
from werkzeug.utils import secure_filename
from app.forms import CourseForm


###
# Routing for UWI Time and Place application.
###

@app.route('/', methods=['GET', 'POST'])
def form():
    form = CourseForm()

    if form.validate_on_submit():
        courses_file = request.files['fileUpload']
        course_title = request.form['courseTitle']
        course_code =  request.form['courseCode']
        lecturer = request.form['lecturer']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        time_preferences = request.form.getlist('timePreferences')
        
        filename = secure_filename(courses_file.filename)
        
        
        
        flash('Property Information Successfully Added!', 'success')

        # Return a response or redirect to another page
        return 'Form submitted successfully!'

    return render_template('upload.html', form=form)

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
