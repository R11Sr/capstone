from app import app
from flask import render_template, flash, request, send_file, redirect, url_for
from app.forms import CourseForm, ParameterForm, CSVUploads
from flask import Flask, render_template, make_response, Response
from werkzeug.utils import secure_filename
from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import pdfkit
import os
import tempfile
import requests
import random
import csv
import json
from collections import OrderedDict

###
# Routing for UWI Time and Place application.
###



@app.route('/', methods=['GET', 'POST'])
def form():
    
       
    form = CourseForm()

    if form.validate_on_submit():
        course_title = form.course_title.data
        course_code =  form.course_code.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        time_preferences = form.time_preferences.data  
        full_name = first_name + last_name 

        # flash(f'Course Title: {course_title}')
        # flash(f'Course Code: {course_code}')
        # flash(f'First Name: {first_name}')
        # flash(f'Last Name: {last_name}')
        # flash(f'Time Preferences: {", ".join(time_preferences)}')
        
        
        flash('New Course Information Successfully Added!', 'success')
    
    flash_errors(form)
    
    

    first = random.randint(116, 256)
    second, third, fourth = generate_numbers(first)
    course1= "INFO"
    course2= "COMP"
    course3= "SWEN"
    
    file_exists1 = os.path.exists('form_course.csv')
    try:
        with open('form_course.csv', 'a', newline='') as csvfile:
            writer1 = csv.writer(csvfile)
            if file_exists1:
                writer1.writerow([course_code, first, course1, second, course2, third, course3, fourth])
            else:
                
                writer1.writerow([course_code, first, course1, second, course2, third, course3, fourth])
                
    except Exception as e:
        # flash('An error occurred while writing to the CSV file. Please try again.', 'error')
        error_message = f"An error occurred while writing to the CSV file: {str(e)}"
        # flash(error_message, 'error')
    
    # file_exists2 = os.path.exists('form_registration.csv')
    # values = generate_values(first)
    # try:
    #     values = generate_values(first)

    #     with open('form_registration.csv', 'a', newline='') as csvfile:
    #         writer2 = csv.writer(csvfile)
    #         if file_exists2:
    #             writer2.writerow([course_code, first, values['Lecture'], values['Tutorial'], values.get('Seminar', ''), values.get('Lab', '')])
    #         else:
    #             writer2.writerow(['Course Code', 'First', 'Lecture', 'Tutorial', 'Seminar', 'Lab'])
    #             writer2.writerow([course_code, first, values['Lecture'], values['Tutorial'], values.get('Seminar', ''), values.get('Lab', '')])
            
    # except Exception as e:
    #     error_message = f"An error occurred while writing to the CSV file: {str(e)}"
    #     flash(error_message, 'error')
    

    # try:
        
    #     course_data = generate_course_data(course_code)
                
    #     write_course_data_to_csv(course_data, 'form_registration.csv')
        
    # except Exception as e:
    #     error_message = f"An error occurred while writing to the CSV file: {str(e)}"
    #     flash(error_message, 'error')
        

    file_exists3 = os.path.exists('lecturer_pref.csv')
    try:
        with open('lecturer_pref.csv', 'a', newline='') as csvfile:
            writer3 = csv.writer(csvfile)
            if file_exists3:
                writer3.writerow([[full_name], time_preferences])
            else:
                
                writer3.writerow([[full_name], time_preferences])
                
    except Exception as e:
        # flash('An error occurred while writing to the CSV file. Please try again.', 'error')
        error_message = f"An error occurred while writing to the CSV file: {str(e)}"
        # flash(error_message, 'error')
    
    clear_form(form)

    return render_template('upload.html', form=form)


@app.route('/parameters', methods=['GET', 'POST'])
def paramsform():
    pform = ParameterForm()

    if pform.validate_on_submit():
        population_size = int(pform.population_size.data)
        p_crossover =  0.9
        p_mutation = 0.1
        max_generations = int(pform.max_generations.data)
        optimal_fitness_score = int(pform.optimal_fitness_score.data)  
        max_runtime = int(pform.max_runtime.data)

        flash('Parameters Set Successfully!', 'success')

        """ flash(f'population_size : {population_size}')
        flash(f'p_crossover: {p_crossover}')
        flash(f'p_mutation: {p_mutation}')
        flash(f'max_generations: {max_generations}')
        flash(f'optimal_fitness_score: {optimal_fitness_score}')
        flash(f'max_runtime: {max_runtime}')  """
    
    flash_errors(pform)

    file_exists11 = os.path.exists('form_parameters.csv')
    try:
        with open('form_parameters.csv', 'a', newline='') as csvfile11:
            writer11 = csv.writer(csvfile11)
            if file_exists11:
                writer11.writerow([population_size, p_crossover, p_mutation, max_generations, optimal_fitness_score, max_runtime])
            else:
                writer11.writerow([population_size, p_crossover, p_mutation, max_generations, optimal_fitness_score, max_runtime])
                
    except Exception as e:
        # flash('An error occurred while writing to the CSV file. Please try again.', 'error')
        error_message = f"An error occurred while writing to the CSV file: {str(e)}"
        # flash(error_message, 'error')
    
    
    clear_form(pform)
    

    return render_template('setParameters.html', form=pform)

@app.route('/fileuploads', methods=['GET', 'POST'])
def csvfileuploads():
    csvform = CSVUploads()
    
    if csvform.validate_on_submit():
        student_reg_file = csvform.student_reg_file.data

        student_reg_filename=secure_filename(student_reg_file.filename)
        student_reg_file.save(generate_output_csvfile_path(student_reg_filename,'Student_Registration_files'))

        lect_pref_file = csvform.lect_pref_file.data

        lect_pref_filename=secure_filename(lect_pref_file.filename)
        lect_pref_file.save(generate_output_csvfile_path(lect_pref_filename,'Lecturer_Preferences_files'))
        

        flash('Files Uploaded Successfully!', 'success')

        """ flash(f'population_size : {population_size}')
        flash(f'p_crossover: {p_crossover}')
        flash(f'p_mutation: {p_mutation}')
        flash(f'max_generations: {max_generations}')
        flash(f'optimal_fitness_score: {optimal_fitness_score}')
        flash(f'max_runtime: {max_runtime}')  """
    
    flash_errors(csvform) 
    
    clear_form(csvform)
    

    return render_template('uploadcsvfiles.html', form=csvform)

#output_csvfolder = 'StudentRegistrationfiles'  # Specify the output folder as "timetables"
   
def generate_output_csvfile_path(file_name,output_csvfolder):
        
        foldercsv_path = os.path.join(app.root_path, output_csvfolder)  
        os.makedirs(foldercsv_path, exist_ok=True)
        return os.path.join(foldercsv_path, file_name)


days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = [
    "8:00", "9:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00", "20:00"
]

@app.route('/download')
def download_timetable():

    # timeTable = [ 
    
    #     ["1"], ["2"], ["3"], ["4"], ["5"],
    #     ["6"], ["7"], ["8"], ["9"], ["10"],
    #     ["11"], ["12"], ["13"], ["14"], ["15"],
    #     ["16"], ["17"], ["18"], ["19"], ["20"],
    #     ["21"], ["22"], ["23"], ["24"], ["25"],
    #     ["26"], ["27"], ["28"], ["29"], ["30"],
    #     ["31"], ["32"], ["33"], ["34"], ["35"],
    #     ["36"], ["37"], ["38"], ["39"], ["40"],
    #     ["41"], ["42"], ["43"], ["44"], ["45"],
    #     ["46"], ["47"], ["48"], ["49"], ["50"],
    #     ["51"], ["52"], ["53"], ["54"], ["55"],
    #     ["56"], ["57"], ["58"], ["59"], ["60"],
    #     ["61"], ["62"], ["63"], ["64"], ["65"]
    # ]


    try:
        filepath = os.path.join(os.getcwd(), 'mock_tables.txt')
        with open(filepath, 'r') as file:
            data = file.read()
    except IOError:
        print("An error occurred while reading the file.")
    else:
        timeTables = json.loads(data)
        

    """ timeTables = {
        '0' : [
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
        ["61"], ["62"], ["63"], ["64"], ["65"]] , 
        
        '1' : [
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
        ["61"], ["62"], ["63"], ["64"], ["65"]] , 
        
        '2' : [
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
        ["61"], ["62"], ["63"], ["64"], ["65"]]  
        
    }  """
        

    
    # timetable = {}
    # for day in days_of_week:
    #     timetable[day] = {}
    #     for time_slot in time_slots:
    #         timetable[day][time_slot] = ""

    # for i, day in enumerate(days_of_week):
    #     for j, time_slot in enumerate(time_slots):
    #         index = i + j * len(days_of_week)
    #         if index < len(timeTable):
    #             timetable[day][time_slot] = timeTable[index][0]
                
    
    timetables_dict = {}
    for key, timetable in timeTables.items():
        timetable_dict = {}
        for i, day in enumerate(days_of_week):
            timetable_dict[day] = {}
            for j, time_slot in enumerate(time_slots):
                index = j * len(days_of_week) + i
                if index < len(timetable):
                    if timetable[index] == []:
                        timetable_dict[day][time_slot] = ' '
                    else:    
                        timetable_dict[day][time_slot] = timetable[index]
        timetables_dict[key] = timetable_dict

    # # return render_template('timetable.html', timetable=timetable, days_of_week=days_of_week, time_slots=time_slots)
    return render_template('time.html', timetables=timetables_dict, days_of_week=days_of_week, time_slots=time_slots)



@app.route('/download/pdf')
def download_pdf():
    
    try:
        timetable_url = 'http://127.0.0.1:8080/download'  #URL of your timetable template
        css_file_path = os.path.join(app.root_path, 'static/css/app.css')

        # Fetch the HTML content of the timetable URL
        response = requests.get(timetable_url)
        rendered_html = response.text

        # Generate the PDF using the URL
        output_file_path = generate_output_file_path()
        pdfkit.from_string(rendered_html, output_file_path, css=css_file_path)

        flash('Timetable has been downloaded! Please check your Timetable Folder', 'success')
        return send_file(output_file_path, as_attachment=True)
    
    except OSError:
        flash('Timetable has been downloaded! Please check your Timetable Folder', 'success')
        # flash('An error occurred while generating the PDF.', 'danger')
        # Redirect the user back to the download page
        return redirect(url_for('download_timetable'))



# UWI Time and Place Functions
output_folder = 'timetables'  # Specify the output folder as "timetables"

# Global counter for keeping track of downloaded files
download_counter = 0    
def generate_output_file_path():
        global download_counter
        download_counter += 1
        file_name = f"timetable{download_counter}.pdf"
        folder_path = os.path.join(app.root_path, output_folder)  
        os.makedirs(folder_path, exist_ok=True)
        return os.path.join(folder_path, file_name)

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

# Clear course form 
def clear_form(form):
    form.process(request.form)
    for field in form:
        field.data = ''
        
        
def generate_numbers(total):
    num1 = random.randint(1, total - 2)
    num2 = random.randint(1, total - num1 - 1)
    num3 = total - num1 - num2
    return num1, num2, num3

def generate_values(total):
    print(f"Generating values for total={total}")
    lecture = random.choices(range(1, 8), k=random.randint(1, 7))
    tutorial = random.choices(range(1, 8), k=random.randint(1, 7))
    
    if random.choice([True, False]):
        seminar = []
        while sum(seminar) != total:
            seminar = random.choices(range(1, 8), k=random.randint(1, 7))
        values = {
            'Lecture': lecture,
            'Tutorial': tutorial,
            'Seminar': seminar
        }
    else:
        lab = []
        while sum(lab) != total:
            lab = random.choices(range(1, 8), k=random.randint(1, 7))
        values = {
            'Lecture': lecture,
            'Tutorial': tutorial,
            'Lab': lab
        }
    
    return values

def generate_course_data(course_code):
    
    # count = random.randint(116, 256)
    # print(count)

    # session_types = {
    #     'Lecture': [],
    #     'Tutorial': [],
    #     'Lab': [],
    #     'Seminar': []
    # }

    # # Generate random numbers for Lecture
    # lecture_count = random.randint(1, min(3, count))
    # lecture_numbers = random.sample(range(1, count + 1), lecture_count)
    # if sum(lecture_numbers) > count:
    #     lecture_numbers = random.sample(lecture_numbers, count)
    # session_types['Lecture'] = lecture_numbers

    # # Generate random numbers for Tutorial
    # tutorial_count = random.randint(1, min(9, count - sum(session_types['Lecture'])))
    # tutorial_numbers = random.sample(range(1, count + 1), tutorial_count)
    # if sum(tutorial_numbers) > count:
    #     tutorial_numbers = random.sample(tutorial_numbers, count - sum(session_types['Lecture']))
    # session_types['Tutorial'] = tutorial_numbers

    # # Generate random numbers for Lab
    # lab_count = random.randint(1, min(3, count - sum(session_types['Lecture']) - sum(session_types['Tutorial'])))
    # lab_numbers = random.sample(range(1, count + 1), lab_count)
    # if sum(lab_numbers) > count:
    #     lab_numbers = random.sample(lab_numbers, count - sum(session_types['Lecture']) - sum(session_types['Tutorial']))
    # session_types['Lab'] = lab_numbers

    # # Generate random numbers for Seminar
    # seminar_count = count - sum(session_types['Lecture']) - sum(session_types['Tutorial']) - sum(session_types['Lab'])
    # seminar_numbers = random.sample(range(1, count + 1), seminar_count)
    # if sum(seminar_numbers) > count:
    #     seminar_numbers = random.sample(seminar_numbers, count - sum(session_types['Lecture']) - sum(session_types['Tutorial']) - sum(session_types['Lab']))
    # session_types['Seminar'] = seminar_numbers

    # print(session_types)
    
 
    
    
    # Kerene version
    # count = random.randint(116, 256)
    # print(count)

    # session_types = {
    #     'Lecture': [],
    #     'Tutorial': [],
    #     'Lab': [],
    #     'Seminar': []
    # }

    # remaining_count = count
    # session_types_keys = list(session_types.keys())

    # for session_type in session_types_keys[:-1]:
    #     max_list_size = min(remaining_count, 3) if session_type != 'Tutorial' else min(remaining_count, 9)
    #     list_size = random.randint(1, max_list_size)
    #     max_value = remaining_count - (list_size - 1)

    #     if max_value <= 0:
    #         session_types[session_type] = [remaining_count]
    #         remaining_count = 0
    #         continue

    #     random_values = [random.randint(0, max_value) for _ in range(list_size)]
    #     session_types[session_type] = random_values
    #     remaining_count -= sum(random_values)

    # session_types[session_types_keys[-1]] = [remaining_count]

    # print(session_types)
    
    
    # count = random.randint(116, 256)
    # print(count)
    
    # session_types = {
    #     'Lecture': 0,
    #     'Tutorial': 0,
    #     'Lab': 0,
    #     'Seminar': 0
    # }
    
    # remaining_count = count
    # session_types_keys = list(session_types.keys())
    
    # for i in range(len(session_types_keys) - 1):
    #     random_value = random.randint(1, remaining_count)
    #     session_types[session_types_keys[i]] = random_value
    #     remaining_count -= random_value
    
    # session_types[session_types_keys[-1]] = remaining_count
    
    # print(session_types)
        
        
   
    # count = random.randint(116, 256)
    # print("count")
    # print(count)
    
    # session_types = {
    #     'Lecture': random.randint(1, count),
    #     'Tutorial': random.randint(1, count),
    #     'Lab': random.randint(1, count),
    #     'Seminar': random.randint(1, count)
    # }
    
    # print("session types")
    # print(session_types)
    
    # session_total = sum(session_types.values())
    # print("session total")
    # print(session_total)
    
    # while session_total != count:
    #     difference = count - session_total
    #     session_type = random.choice(list(session_types.keys()))
        
    #     if session_total < count:
    #         session_types[session_type] += difference
    #     else:
    #         if session_types[session_type] > difference:
    #             session_types[session_type] -= difference
        
    #     session_total = sum(session_types.values())
    
    # print("here")
    # course_data = {}
    # course_data[course_code] = {'count': count}
    
    # for session_type, session_count in session_types.items():
    #     session_data = random.sample(range(1, 1000), session_count)
    #     course_data[course_code][session_type] = session_data
    
    return course_data

    

def write_course_data_to_csv(course_data, filename):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        writer2 = csv.writer(csvfile)
        
        if not file_exists:
            writer2.writerow(['Course Code', 'Count', 'Lecture', 'Tutorial', 'Lab', 'Seminar'])
        
        for course_code, course_info in course_data.items():
            count = course_info['count']
            lecture = course_info.get('Lecture', [])
            tutorial = course_info.get('Tutorial', [])
            lab = course_info.get('Lab', [])
            seminar = course_info.get('Seminar', [])
            
            writer2.writerow([course_code, count, lecture, tutorial, lab, seminar])

# Example usage
# course_data = generate_course_data(course_code)
# write_course_data_to_csv(course_data, 'form_registration.csv')
    