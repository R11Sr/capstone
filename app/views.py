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

@app.route('/download')
def download_timetable():
    
    
    
    
    timeTable = [
            [M],[T],[W],[Th],[F],
            [1],[2],[3],[4],[5],
            [6],[7],[8],[9],[10],
            [11],[12],[13],[14],[15],
            [16],[17],[18],[19],[20],
            [21],[22],[23],[24],[25],
            [26],[27],[28],[29],[30],
            [31],[32],[33],[34],[35],
            [36],[37],[38],[39],[40],
            [41],[42],[43],[44],[45],
            [46],[47],[48],[49],[50],
            [51],[52],[53],[54],[55],
            [56],[57],[58],[59],[60],
            [61],[62],[63],[64],[65],
        ]
    
    return render_template('timetable.html')

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
