from app import app
from flask import render_template, flash
from werkzeug.utils import secure_filename
from app.forms import CourseForm


###
# Routing for UWI Time and Place application.
###

@app.route('/', methods=['GET', 'POST'])
def form():
    form = CourseForm()

    if form.validate_on_submit():
        courses_file = form.file_upload.data
        course_title = form.course_title.data
        course_code = form.course_code.data
        lecturer = form.lecturer.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        time_preferences = form.time_preferences.data

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
