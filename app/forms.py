from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import InputRequired

class CourseForm(FlaskForm):
    course_title = StringField('Course Title', validators=[InputRequired()])
    course_code = StringField('Course Code', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    time_preferences = SelectMultipleField('Time Preferences', choices=[('1', '01:00'),('2', '02:00'),('3', '03:00'),('4', '04:00'),('5', '05:00'),('6', '06:00'),('7', '07:00'),('8', '08:00'),('9', '09:00'), ('10', '10:00'), ('11', '11:00'), ('12', '12:00'), ('13', '13:00'), ('14', '14:00'), ('15', '15:00'), ('16', '16:00'), ('17', '17:00'), ('18', '18:00'), ('19', '19:00'), ('20', '20:00'), ('21', '21:00'), ('22', '22:00'), ('23', '23:00'), ('24', '24:00')], validators=[InputRequired()])
    
