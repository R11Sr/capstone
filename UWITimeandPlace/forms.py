from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired

class CourseForm(FlaskForm):
    course_title = StringField('Course Title', validators=[InputRequired()])
    course_code = StringField('Course Code', validators=[InputRequired()])
    lecturer = StringField('Lecturer', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    time_preferences = SelectField('Time Preferences', choices=[('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00')], validators=[InputRequired()])
    courses_file = FileField('Courses File Upload', validators=[FileRequired(), FileAllowed(['csv', 'xlsx'], 'CSV or Excel Files Only!')])
