from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectMultipleField
from wtforms.validators import InputRequired

class CourseForm(FlaskForm):
    course_title = StringField('Course Title', validators=[InputRequired()])
    course_code = StringField('Course Code', validators=[InputRequired()])
    lecturer = StringField('Lecturer', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    courses_file = FileField('Courses File Upload', validators=[FileRequired(), FileAllowed(['csv', 'xlsx'], 'CSV or Excel Files Only!')])
    time_preferences = SelectMultipleField('Time Preferences', choices=[('01:00', '01:00'),('02:00', '02:00'),('03:00', '03:00'),('04:00', '04:00'),('05:00', '05:00'),('06:00', '06:00'),('07:00', '07:00'),('08:00', '08:00'),('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00'), ('22:00', '22:00'), ('23:00', '23:00'), ('24:00', '24:00')], validators=[InputRequired()])
    
