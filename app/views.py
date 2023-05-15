from app import app
from flask import render_template, flash, request, send_file
from werkzeug.utils import secure_filename
from app.forms import CourseForm
from flask import Flask, render_template, make_response
import pdfkit

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


days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = [
    "8:00", "9:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00", "20:00"
]

@app.route('/download')
def download_timetable():
    
    timeTable = [
        ["1"], ["2"], ["3"], ["4"], ["5"],
        ["6"], ["7"], ["8"], ["9"], ["10"],
        ["11"], ["12"], ["13"], ["14"], ["15"],
        ["16"], ["17"], ["18"], ["19"], ["20"],
        ["21"], ["22"], ["23"], ["24"], ["25"],
        ["26"], ["27"], ["28"], ["29"], ["30"],
        ["31"], ["32"], ["33"], ["34"], ["35"],
        ["36"], ["37"], ["38"], ["39"], ["40"],
        ["41"], ["42"], ["43"], ["44"], ["45"],
        ["46"], ["47"], ["48"], ["49"], ["50"],
        ["51"], ["52"], ["53"], ["54"], ["55"],
        ["56"], ["57"], ["58"], ["59"], ["60"],
        ["61"], ["62"], ["63"], ["64"], ["65"]
    ]
    

    timetable = {}
    for day in days_of_week:
        timetable[day] = {}
        for time_slot in time_slots:
            timetable[day][time_slot] = ""

    for i, day in enumerate(days_of_week):
        for j, time_slot in enumerate(time_slots):
            index = i + j * len(days_of_week)
            if index < len(timeTable):
                timetable[day][time_slot] = timeTable[index][0]

    return render_template('timetable.html', timetable=timetable, days_of_week=days_of_week, time_slots=time_slots)




@app.route('/download_pdf')
def download_pdf():
    timetable = download_timetable()  # Replace with your function that generates the timetable
    html = render_template('timetable.html', timetable=timetable, days_of_week=days_of_week, time_slots=time_slots)

    # Generate PDF from HTML
    pdf = pdfkit.from_string(html, False)

    # Create a Flask response with the PDF as the content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=timetable.pdf'
    return response


# Your existing route for rendering the timetable HTML
@app.route('/timetable')
def render_timetable():
    timetable = download_timetable()  # Replace with your function that generates the timetable
    return render_template('timetable.html', timetable=timetable, days_of_week=days_of_week, time_slots=time_slots)

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
