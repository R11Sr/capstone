from app import app
from flask import render_template, flash, request, send_file, redirect, url_for
from app.forms import CourseForm, ParameterForm
from flask import Flask, render_template, make_response, Response
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
from collections import OrderedDict
import ast

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
        population_size = int(pform.population_size.data[0])
        p_crossover =  0.9
        p_mutation = 0.1
        max_generations = int(pform.max_generations.data[0])
        optimal_fitness_score = int(pform.optimal_fitness_score.data[0])  
        max_runtime = int(pform.max_runtime.data[0])

        flash('Parameters Set Successfully!', 'success')

        """ flash(f'population_size : {population_size}')
        flash(f'p_crossover: {p_crossover}')
        flash(f'p_mutation: {p_mutation}')
        flash(f'max_generations: {max_generations}')
        flash(f'optimal_fitness_score: {optimal_fitness_score}')
        flash(f'max_runtime: {max_runtime}') """
    
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



days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = [
    "8:00", "9:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00", "20:00"
]

def read_file(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return file_contents


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
    
    # timeTables = {
    #     '0' : [
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
    #     ["61"], ["62"], ["63"], ["64"], ["65"]] , 
        
    #     '1' : [
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
    #     ["61"], ["62"], ["63"], ["64"], ["65"]] , 
        
    #     '2' : [
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
    #     ["61"], ["62"], ["63"], ["64"], ["65"]]  
        
    # } 
    
    timeTables = {
        "0": [
        
        ["name: BIOC3013-Lecture-2, capacity: 23, location: C5", "name: GEOL3002-Lecture-1, capacity: 9, location: C3", "name: MATH1141-Lecture-3, capacity: 26, location: C2", "name: CHEM2310-Lecture-1, capacity: 32, location: Math Room 2", "name: GEOG1131-Lecture-1, capacity: 44, location: Math Room 1", "name: CHEM1901-Lecture-2, capacity: 43, location: ENG Comp Lab", "name: GEOL2202-Lecture-1, capacity: 34, location: SLT3", "name: PHYS2351-Lecture-2, capacity: 34, location: SLT2", "name: MICR1011-Lecture-1, capacity: 25, location: SLT1", "name: MATH2404-Lecture-1, capacity: 33, location: Physics Lab", "name: CHEM2210-Lecture-2, capacity: 32, location: GEOG Lab 3", "name: BIOC2014-Lecture-3, capacity: 19, location: GEOG Lecture RM 2", "name: INFO2180-Lecture-3, capacity: 114, location: GEOG Lecture RM 1", "name: INFO2100-Lecture-1, capacity: 114, location: GEOG Lab 2", "name: INFO3155-Lecture-1, capacity: 262, location: CompLab", "name: INFO3110-Lecture-3, capacity: 262, location: CompCLR", "name: COMP3901-Lecture-1, capacity: 398, location: None", "name: COMP3161-Lecture-2, capacity: 398, location: None", "name: COMP2340-Lecture-2, capacity: 177, location: None", "name: COMP2211-Lecture-1, capacity: 122, location: None", "name: COMP2190-Lecture-2, capacity: 236, location: None", "name: COMP2171-Lecture-2, capacity: 122, location: None", "name: INFO2110-Lecture-2, capacity: 114, location: None", "name: INFO3180-Lecture-1, capacity: 262, location: None", "name: INFO3170-Lecture-1, capacity: 262, location: None", "name: INFO3105-Lecture-3, capacity: 262, location: None", "name: COMP1161-Lecture-2, capacity: 250, location: None", "name: COMP1127-Lecture-3, capacity: 250, location: None", "name: COMP1126-Lecture-3, capacity: 250, location: None", "name: COMP1220-Lecture-1, capacity: 250, location: None", "name: COMP1210-Lecture-2, capacity: 250, location: None", "name: COMP3220-Lecture-2, capacity: 136, location: None", "name: COMP3101-Lecture-1, capacity: 136, location: None", "name: COMP2201-Lecture-2, capacity: 122, location: None", "name: COMP2140-Lecture-2, capacity: 236, location: None", "name: SWEN3920-Lecture-1, capacity: 116, location: None", "name: SWEN3145-Lecture-1, capacity: 116, location: None", "name: SWEN3101-Lecture-3, capacity: 116, location: None"],
        ["name: BIOC3013-Seminar-1, capacity: 23, location: C5", "name: MATH1141-Lecture-2, capacity: 26, location: C3", "name: GEOL3002-Seminar-1, capacity: 9, location: C2", "name: CHEM1901-Lecture-1, capacity: 43, location: Math Room 2", "name: PHYS2351-Lecture-1, capacity: 34, location: Math Room 1", "name: CHEM2210-Lecture-1, capacity: 32, location: ENG Comp Lab", "name: CHEM2310-Tutorial-2, capacity: 21, location: SLT3", "name: BIOC2014-Lecture-2, capacity: 19, location: SLT2", "name: INFO2180-Lecture-2, capacity: 114, location: SLT1", "name: GEOG1131-Seminar-2, capacity: 44, location: Physics Lab", "name: INFO3110-Lecture-2, capacity: 262, location: GEOG Lab 3", "name: COMP3161-Lecture-1, capacity: 398, location: GEOG Lecture RM 2", "name: GEOL2202-Tutorial-6, capacity: 7, location: GEOG Lecture RM 1", "name: COMP2340-Lecture-1, capacity: 177, location: GEOG Lab 2", "name: COMP2190-Lecture-1, capacity: 236, location: CompLab", "name: INFO2110-Lecture-1, capacity: 114, location: CompCLR", "name: INFO3105-Lecture-2, capacity: 262, location: None", "name: MICR1011-Seminar-1, capacity: 25, location: None", "name: COMP1161-Lecture-1, capacity: 250, location: None", "name: COMP1127-Lecture-2, capacity: 250, location: None", "name: MATH2404-Tutorial-5, capacity: 9, location: None", "name: COMP1126-Lecture-2, capacity: 250, location: None", "name: COMP1210-Lecture-1, capacity: 250, location: None", "name: COMP3220-Lecture-1, capacity: 136, location: None", "name: COMP2201-Lecture-1, capacity: 122, location: None", "name: SWEN3920-Lecture-2, capacity: 116, location: None", "name: SWEN3101-Lecture-2, capacity: 116, location: None", "name: SWEN3145-Tutorial-1, capacity: 30, location: None", "name: INFO2100-Tutorial-1, capacity: 148, location: None", "name: INFO3155-Tutorial-8, capacity: 43, location: None", "name: COMP2140-Tutorial-1, capacity: 153, location: None", "name: COMP3101-Tutorial-1, capacity: 59, location: None", "name: COMP3901-Tutorial-4, capacity: 103, location: None", "name: COMP1220-Tutorial-1, capacity: 54, location: None", "name: COMP2211-Seminar-2, capacity: 122, location: None", "name: COMP2171-Seminar-2, capacity: 122, location: None", "name: INFO3180-Seminar-1, capacity: 262, location: None", "name: INFO3170-Seminar-2, capacity: 262, location: None"], 
        ["name: BIOC3013-Lecture-1, capacity: 23, location: C5", "name: MATH1141-Lecture-1, capacity: 26, location: C3", "name: GEOL3002-Tutorial-2, capacity: 6, location: C2", "name: CHEM2310-Tutorial-1, capacity: 21, location: Math Room 2", "name: BIOC2014-Lecture-1, capacity: 19, location: Math Room 1", "name: INFO2180-Lecture-1, capacity: 114, location: ENG Comp Lab", "name: GEOG1131-Seminar-1, capacity: 44, location: SLT3", "name: CHEM1901-Tutorial-5, capacity: 11, location: SLT2", "name: INFO3110-Lecture-1, capacity: 262, location: SLT1", "name: GEOL2202-Tutorial-5, capacity: 7, location: Physics Lab", "name: COMP2171-Lecture-1, capacity: 122, location: GEOG Lab 3", "name: PHYS2351-Tutorial-5, capacity: 9, location: GEOG Lecture RM 2", "name: INFO3105-Lecture-1, capacity: 262, location: GEOG Lecture RM 1", "name: MICR1011-Tutorial-4, capacity: 6, location: GEOG Lab 2", "name: COMP1127-Lecture-1, capacity: 250, location: CompLab", "name: MATH2404-Tutorial-4, capacity: 9, location: CompCLR", "name: COMP1126-Lecture-1, capacity: 250, location: None", "name: CHEM2210-Seminar-2, capacity: 32, location: None", "name: COMP2140-Lecture-1, capacity: 236, location: None", "name: SWEN3101-Lecture-1, capacity: 116, location: None", "name: SWEN3145-Tutorial-2, capacity: 30, location: None", "name: SWEN3920-Tutorial-1, capacity: 22, location: None", "name: INFO2100-Lab-2, capacity: 148, location: None", "name: INFO3155-Seminar-1, capacity: 262, location: None", "name: COMP2201-Lab-1, capacity: 79, location: None", "name: COMP3101-Tutorial-2, capacity: 59, location: None", "name: COMP3220-Lab-1, capacity: 25, location: None", "name: COMP3901-Tutorial-5, capacity: 103, location: None", "name: COMP3161-Seminar-1, capacity: 398, location: None", "name: COMP1210-Tutorial-1, capacity: 81, location: None", "name: COMP2340-Seminar-1, capacity: 177, location: None", "name: COMP1220-Tutorial-3, capacity: 54, location: None", "name: COMP2211-Seminar-1, capacity: 122, location: None", "name: COMP2190-Tutorial-1, capacity: 307, location: None", "name: COMP1161-Lab-1, capacity: 65, location: None", "name: INFO2110-Seminar-1, capacity: 114, location: None", "name: INFO3180-Tutorial-4, capacity: 85, location: None", "name: INFO3170-Seminar-1, capacity: 262, location: None"], 
        ["name: BIOC3013-Tutorial-5, capacity: 6, location: C5", "name: GEOL3002-Tutorial-1, capacity: 6, location: C3", "name: MATH1141-Seminar-1, capacity: 26, location: C2", "name: CHEM2310-Lab-2, capacity: 21, location: Math Room 2", "name: GEOG1131-Tutorial-1, capacity: 57, location: Math Room 1", "name: CHEM1901-Tutorial-4, capacity: 11, location: ENG Comp Lab", "name: GEOL2202-Tutorial-4, capacity: 7, location: SLT3", "name: PHYS2351-Tutorial-4, capacity: 9, location: SLT2", "name: MICR1011-Tutorial-5, capacity: 6, location: SLT1", "name: MATH2404-Tutorial-3, capacity: 9, location: Physics Lab", "name: CHEM2210-Seminar-1, capacity: 32, location: GEOG Lab 3", "name: BIOC2014-Seminar-2, capacity: 19, location: GEOG Lecture RM 2", "name: SWEN3101-Lab-1, capacity: 30, location: GEOG Lecture RM 1", "name: INFO2180-Tutorial-8, capacity: 19, location: GEOG Lab 2", "name: SWEN3145-Tutorial-3, capacity: 30, location: CompLab", "name: SWEN3920-Tutorial-2, capacity: 22, location: CompCLR", "name: INFO2100-Lab-1, capacity: 148, location: None", "name: INFO3155-Tutorial-7, capacity: 43, location: None", "name: COMP2140-Tutorial-2, capacity: 153, location: None", "name: INFO3110-Seminar-1, capacity: 262, location: None", "name: COMP2201-Tutorial-1, capacity: 79, location: None", "name: COMP3101-Seminar-1, capacity: 136, location: None", "name: COMP3220-Lab-2, capacity: 25, location: None", "name: COMP3901-Tutorial-3, capacity: 103, location: None", "name: COMP3161-Tutorial-3, capacity: 172, location: None", "name: COMP1210-Tutorial-2, capacity: 81, location: None", "name: COMP2340-Tutorial-5, capacity: 46, location: None", "name: COMP1220-Tutorial-2, capacity: 54, location: None", "name: COMP2211-Tutorial-9, capacity: 18, location: None", "name: COMP1126-Tutorial-1, capacity: 46, location: None", "name: COMP2190-Lab-1, capacity: 307, location: None", "name: COMP1127-Tutorial-1, capacity: 46, location: None", "name: COMP2171-Seminar-1, capacity: 122, location: None", "name: COMP1161-Tutorial-1, capacity: 65, location: None", "name: INFO2110-Tutorial-4, capacity: 37, location: None", "name: INFO3105-Tutorial-1, capacity: 57, location: None", "name: INFO3180-Tutorial-3, capacity: 85, location: None", "name: INFO3170-Tutorial-1, capacity: 114, location: None"], 
        ["name: BIOC3013-Tutorial-4, capacity: 6, location: C5", "name: MATH1141-Tutorial-7, capacity: 5, location: C3", "name: CHEM2310-Lab-1, capacity: 21, location: C2", "name: CHEM1901-Tutorial-3, capacity: 11, location: Math Room 2", "name: GEOL2202-Tutorial-3, capacity: 7, location: Math Room 1", "name: PHYS2351-Tutorial-3, capacity: 9, location: ENG Comp Lab", "name: MICR1011-Tutorial-3, capacity: 6, location: SLT3", "name: MATH2404-Tutorial-2, capacity: 9, location: SLT2", "name: CHEM2210-Tutorial-9, capacity: 5, location: SLT1", "name: BIOC2014-Seminar-1, capacity: 19, location: Physics Lab", "name: SWEN3101-Tutorial-1, capacity: 30, location: GEOG Lab 3", "name: INFO2180-Tutorial-7, capacity: 19, location: GEOG Lecture RM 2", "name: SWEN3145-Tutorial-4, capacity: 30, location: GEOG Lecture RM 1", "name: SWEN3920-Tutorial-3, capacity: 22, location: GEOG Lab 2", "name: INFO3155-Tutorial-6, capacity: 43, location: CompLab", "name: COMP2140-Seminar-2, capacity: 236, location: CompCLR", "name: INFO3110-Tutorial-7, capacity: 49, location: None", "name: COMP2201-Tutorial-2, capacity: 79, location: None", "name: COMP3101-Tutorial-3, capacity: 59, location: None", "name: COMP3220-Tutorial-1, capacity: 25, location: None", "name: COMP3901-Tutorial-2, capacity: 103, location: None", "name: COMP3161-Tutorial-2, capacity: 172, location: None", "name: COMP1210-Tutorial-3, capacity: 81, location: None", "name: COMP2340-Tutorial-4, capacity: 46, location: None", "name: COMP1220-Tutorial-4, capacity: 54, location: None", "name: COMP2211-Tutorial-8, capacity: 18, location: None", "name: COMP1126-Tutorial-2, capacity: 46, location: None", "name: COMP1127-Tutorial-2, capacity: 46, location: None", "name: COMP2171-Tutorial-7, capacity: 23, location: None", "name: COMP1161-Tutorial-2, capacity: 65, location: None", "name: INFO2110-Tutorial-3, capacity: 37, location: None", "name: INFO3105-Tutorial-2, capacity: 57, location: None", "name: INFO3180-Tutorial-2, capacity: 85, location: None", "name: INFO3170-Tutorial-3, capacity: 114, location: None"], 
        ["name: BIOC3013-Tutorial-3, capacity: 6, location: C5", "name: MATH1141-Tutorial-6, capacity: 5, location: C3", "name: CHEM1901-Tutorial-2, capacity: 11, location: C2", "name: GEOL2202-Tutorial-2, capacity: 7, location: Math Room 2", "name: PHYS2351-Tutorial-2, capacity: 9, location: Math Room 1", "name: MICR1011-Tutorial-2, capacity: 6, location: ENG Comp Lab", "name: MATH2404-Tutorial-1, capacity: 9, location: SLT3", "name: CHEM2210-Tutorial-8, capacity: 5, location: SLT2", "name: BIOC2014-Tutorial-4, capacity: 6, location: SLT1", "name: SWEN3101-Tutorial-2, capacity: 30, location: Physics Lab", "name: INFO2180-Tutorial-6, capacity: 19, location: GEOG Lab 3", "name: SWEN3145-Tutorial-5, capacity: 30, location: GEOG Lecture RM 2", "name: SWEN3920-Tutorial-4, capacity: 22, location: GEOG Lecture RM 1", "name: INFO3155-Tutorial-5, capacity: 43, location: GEOG Lab 2", "name: COMP2140-Seminar-1, capacity: 236, location: CompLab", "name: INFO3110-Tutorial-6, capacity: 49, location: CompCLR", "name: COMP3220-Tutorial-2, capacity: 25, location: None", "name: COMP3901-Tutorial-1, capacity: 103, location: None", "name: COMP3161-Tutorial-1, capacity: 172, location: None", "name: COMP1210-Tutorial-4, capacity: 81, location: None", "name: COMP2340-Tutorial-3, capacity: 46, location: None", "name: COMP1220-Tutorial-5, capacity: 54, location: None", "name: COMP2211-Tutorial-7, capacity: 18, location: None", "name: COMP1126-Tutorial-3, capacity: 46, location: None", "name: COMP1127-Tutorial-3, capacity: 46, location: None", "name: COMP2171-Tutorial-6, capacity: 23, location: None", "name: COMP1161-Tutorial-3, capacity: 65, location: None", "name: INFO2110-Tutorial-2, capacity: 37, location: None", "name: INFO3105-Tutorial-3, capacity: 57, location: None", "name: INFO3180-Tutorial-1, capacity: 85, location: None", "name: INFO3170-Tutorial-2, capacity: 114, location: None"],
        ["name: BIOC3013-Tutorial-2, capacity: 6, location: C5", "name: MATH1141-Tutorial-5, capacity: 5, location: C3", "name: CHEM1901-Tutorial-1, capacity: 11, location: C2", "name: GEOL2202-Tutorial-1, capacity: 7, location: Math Room 2", "name: PHYS2351-Tutorial-1, capacity: 9, location: Math Room 1", "name: MICR1011-Tutorial-1, capacity: 6, location: ENG Comp Lab", "name: MATH2404-Lab-2, capacity: 9, location: SLT3", "name: CHEM2210-Tutorial-7, capacity: 5, location: SLT2", "name: BIOC2014-Tutorial-3, capacity: 6, location: SLT1", "name: SWEN3101-Tutorial-3, capacity: 30, location: Physics Lab", "name: INFO2180-Tutorial-5, capacity: 19, location: GEOG Lab 3", "name: SWEN3145-Seminar-1, capacity: 116, location: GEOG Lecture RM 2", "name: SWEN3920-Tutorial-5, capacity: 22, location: GEOG Lecture RM 1", "name: INFO3155-Tutorial-4, capacity: 43, location: GEOG Lab 2", "name: INFO3110-Tutorial-5, capacity: 49, location: CompLab", "name: COMP3220-Tutorial-3, capacity: 25, location: CompCLR", "name: COMP3901-Lab-1, capacity: 103, location: None", "name: COMP1210-Seminar-1, capacity: 250, location: None", "name: COMP2340-Tutorial-2, capacity: 46, location: None", "name: COMP1220-Tutorial-6, capacity: 54, location: None", "name: COMP2211-Tutorial-6, capacity: 18, location: None", "name: COMP1126-Tutorial-4, capacity: 46, location: None", "name: COMP1127-Tutorial-4, capacity: 46, location: None", "name: COMP2171-Tutorial-5, capacity: 23, location: None", "name: COMP1161-Tutorial-4, capacity: 65, location: None", "name: INFO2110-Tutorial-1, capacity: 37, location: None", "name: INFO3105-Tutorial-4, capacity: 57, location: None"], 
        ["name: BIOC3013-Tutorial-1, capacity: 6, location: C5", "name: MATH1141-Tutorial-4, capacity: 5, location: C3", "name: CHEM1901-Lab-2, capacity: 11, location: C2", "name: GEOL2202-Lab-1, capacity: 7, location: Math Room 2", "name: PHYS2351-Lab-1, capacity: 9, location: Math Room 1", "name: MATH2404-Lab-1, capacity: 9, location: ENG Comp Lab", "name: CHEM2210-Tutorial-6, capacity: 5, location: SLT3", "name: BIOC2014-Tutorial-2, capacity: 6, location: SLT2", "name: SWEN3101-Tutorial-4, capacity: 30, location: SLT1", "name: INFO2180-Tutorial-4, capacity: 19, location: Physics Lab", "name: SWEN3145-Seminar-2, capacity: 116, location: GEOG Lab 3", "name: SWEN3920-Tutorial-6, capacity: 22, location: GEOG Lecture RM 2", "name: INFO3155-Tutorial-3, capacity: 43, location: GEOG Lecture RM 1", "name: INFO3110-Tutorial-4, capacity: 49, location: GEOG Lab 2", "name: COMP3220-Tutorial-4, capacity: 25, location: CompLab", "name: COMP1210-Seminar-2, capacity: 250, location: CompCLR", "name: COMP2340-Tutorial-1, capacity: 46, location: None", "name: COMP1220-Seminar-1, capacity: 250, location: None", "name: COMP2211-Tutorial-5, capacity: 18, location: None", "name: COMP1126-Tutorial-5, capacity: 46, location: None", "name: COMP1127-Tutorial-5, capacity: 46, location: None", "name: COMP2171-Tutorial-4, capacity: 23, location: None", "name: COMP1161-Tutorial-5, capacity: 65, location: None", "name: INFO3105-Tutorial-5, capacity: 57, location: None"],
        ["name: MATH1141-Tutorial-3, capacity: 5, location: C5", "name: CHEM1901-Lab-1, capacity: 11, location: C3", "name: CHEM2210-Tutorial-5, capacity: 5, location: C2", "name: BIOC2014-Tutorial-1, capacity: 6, location: Math Room 2", "name: SWEN3101-Tutorial-5, capacity: 30, location: Math Room 1", "name: INFO2180-Tutorial-3, capacity: 19, location: ENG Comp Lab", "name: SWEN3920-Tutorial-7, capacity: 22, location: SLT3", "name: INFO3155-Tutorial-2, capacity: 43, location: SLT2", "name: INFO3110-Tutorial-3, capacity: 49, location: SLT1", "name: COMP3220-Tutorial-5, capacity: 25, location: Physics Lab", "name: COMP2211-Tutorial-4, capacity: 18, location: GEOG Lab 3", "name: COMP1126-Tutorial-6, capacity: 46, location: GEOG Lecture RM 2", "name: COMP1127-Tutorial-6, capacity: 46, location: GEOG Lecture RM 1", "name: COMP2171-Tutorial-3, capacity: 23, location: GEOG Lab 2", "name: INFO3105-Tutorial-6, capacity: 57, location: CompLab"], 
        ["name: MATH1141-Tutorial-2, capacity: 5, location: C5", "name: CHEM2210-Tutorial-4, capacity: 5, location: C3", "name: INFO2180-Tutorial-2, capacity: 19, location: C2", "name: SWEN3920-Seminar-1, capacity: 116, location: Math Room 2", "name: INFO3155-Tutorial-1, capacity: 43, location: Math Room 1", "name: INFO3110-Tutorial-2, capacity: 49, location: ENG Comp Lab", "name: COMP3220-Tutorial-6, capacity: 25, location: SLT3", "name: COMP2211-Tutorial-3, capacity: 18, location: SLT2", "name: COMP1126-Tutorial-7, capacity: 46, location: SLT1", "name: COMP1127-Tutorial-7, capacity: 46, location: Physics Lab", "name: COMP2171-Tutorial-2, capacity: 23, location: GEOG Lab 3", "name: INFO3105-Seminar-1, capacity: 262, location: GEOG Lecture RM 2"], 
        ["name: MATH1141-Tutorial-1, capacity: 5, location: C5", "name: CHEM2210-Tutorial-3, capacity: 5, location: C3", "name: INFO2180-Tutorial-1, capacity: 19, location: C2", "name: SWEN3920-Seminar-2, capacity: 116, location: Math Room 2", "name: INFO3110-Tutorial-1, capacity: 49, location: Math Room 1", "name: COMP3220-Tutorial-7, capacity: 25, location: ENG Comp Lab", "name: COMP2211-Tutorial-2, capacity: 18, location: SLT3", "name: COMP1126-Seminar-1, capacity: 250, location: SLT2", "name: COMP1127-Seminar-1, capacity: 250, location: SLT1", "name: COMP2171-Tutorial-1, capacity: 23, location: Physics Lab"], 
        ["name: CHEM2210-Tutorial-2, capacity: 5, location: C5", "name: INFO2180-Lab-1, capacity: 19, location: C3", "name: COMP2211-Tutorial-1, capacity: 18, location: C2"], 
        ["name: CHEM2210-Tutorial-1, capacity: 5, location: C5"], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
                
        "1": [
            ["name: SWEN3101-Tutorial-1, capacity: 30, location: C5", "name: BIOC2014-Tutorial-2, capacity: 6, location: C3", "name: INFO3155-Tutorial-5, capacity: 43, location: C3", "name: COMP2340-Tutorial-4, capacity: 46, location: C3", "name: COMP2140-Seminar-1, capacity: 236, location: Math Room 1", "name: INFO3170-Seminar-1, capacity: 262, location: Math Room 1", "name: COMP1220-Lecture-1, capacity: 250, location: SLT2"],
            ["name: SWEN3101-Tutorial-2, capacity: 30, location: C5", "name: BIOC2014-Tutorial-1, capacity: 6, location: C3", "name: INFO3155-Tutorial-2, capacity: 43, location: C3", "name: COMP2340-Tutorial-3, capacity: 46, location: C3", "name: COMP2140-Lecture-2, capacity: 236, location: SLT3", "name: INFO3105-Lecture-1, capacity: 262, location: SLT3"],
            ["name: SWEN3101-Tutorial-3, capacity: 30, location: C5", "name: COMP2340-Tutorial-5, capacity: 46, location: C3", "name: GEOL3002-Tutorial-2, capacity: 6, location: C3", "name: COMP1220-Tutorial-4, capacity: 54, location: C2", "name: COMP2171-Lecture-1, capacity: 122, location: SLT1"], ["name: SWEN3145-Tutorial-5, capacity: 30, location: C5", "name: PHYS2351-Tutorial-2, capacity: 9, location: C3", "name: COMP1127-Tutorial-5, capacity: 46, location: C3", "name: COMP3901-Tutorial-4, capacity: 103, location: C3", "name: MATH1141-Tutorial-5, capacity: 5, location: C2", "name: CHEM2310-Tutorial-2, capacity: 21, location: C2"], 
            ["name: COMP2140-Tutorial-1, capacity: 153, location: C5", "name: INFO3105-Tutorial-2, capacity: 57, location: C3", "name: COMP1220-Tutorial-6, capacity: 54, location: C2", "name: SWEN3101-Lab-1, capacity: 30, location: C2"], 
            ["name: GEOL2202-Tutorial-3, capacity: 7, location: C3"], 
            ["name: INFO2110-Tutorial-1, capacity: 37, location: C5", "name: INFO3105-Tutorial-1, capacity: 57, location: C3", "name: BIOC2014-Seminar-2, capacity: 19, location: Math Room 1", "name: INFO3105-Seminar-1, capacity: 262, location: Math Room 1", "name: COMP2140-Seminar-2, capacity: 236, location: Math Room 1", "name: SWEN3101-Lecture-2, capacity: 116, location: SLT1"], 
            ["name: INFO2110-Tutorial-2, capacity: 37, location: C5", "name: INFO3155-Tutorial-6, capacity: 43, location: C3", "name: BIOC2014-Seminar-1, capacity: 19, location: Math Room 1", "name: INFO3110-Seminar-1, capacity: 262, location: Math Room 1", "name: COMP2340-Seminar-1, capacity: 177, location: ENG Comp Lab"], 
            ["name: BIOC3013-Tutorial-5, capacity: 6, location: C5", "name: INFO2180-Tutorial-8, capacity: 19, location: C3", "name: INFO3155-Tutorial-1, capacity: 43, location: C3", "name: INFO2110-Tutorial-4, capacity: 37, location: C2", "name: PHYS2351-Tutorial-3, capacity: 9, location: C2"], 
            ["name: BIOC3013-Tutorial-4, capacity: 6, location: C5", "name: INFO2180-Tutorial-7, capacity: 19, location: C3", "name: INFO3110-Tutorial-6, capacity: 49, location: C3", "name: INFO2100-Lab-1, capacity: 148, location: C2", "name: CHEM2210-Seminar-1, capacity: 32, location: Math Room 1"],
            ["name: MICR1011-Tutorial-2, capacity: 6, location: C5", "name: COMP3220-Tutorial-4, capacity: 25, location: C3", "name: PHYS2351-Lab-1, capacity: 9, location: C2", "name: INFO2180-Lab-1, capacity: 19, location: C2"], 
            ["name: BIOC3013-Tutorial-3, capacity: 6, location: C5", "name: INFO2180-Tutorial-6, capacity: 19, location: C3", "name: INFO3110-Tutorial-3, capacity: 49, location: C3", "name: PHYS2351-Lecture-1, capacity: 34, location: SLT3", "name: INFO2110-Lecture-2, capacity: 114, location: SLT2"], 
            ["name: BIOC3013-Tutorial-2, capacity: 6, location: C5", "name: INFO2180-Tutorial-5, capacity: 19, location: C3", "name: INFO3110-Tutorial-4, capacity: 49, location: C3", "name: CHEM2210-Lecture-2, capacity: 32, location: SLT2", "name: INFO2180-Lecture-1, capacity: 114, location: SLT2"], 
            ["name: MICR1011-Tutorial-4, capacity: 6, location: C5", "name: COMP3220-Tutorial-3, capacity: 25, location: C3", "name: PHYS2351-Tutorial-1, capacity: 9, location: C2", "name: INFO2100-Lab-2, capacity: 148, location: C2"], 
            ["name: MICR1011-Tutorial-5, capacity: 6, location: C5", "name: COMP3220-Tutorial-2, capacity: 25, location: C3", "name: COMP1126-Seminar-1, capacity: 250, location: ENG Comp Lab", "name: COMP2211-Seminar-2, capacity: 122, location: ENG Comp Lab", "name: INFO3110-Lecture-2, capacity: 262, location: SLT3"], 
            ["name: MICR1011-Tutorial-3, capacity: 6, location: C5", "name: COMP3220-Tutorial-1, capacity: 25, location: C3", "name: COMP1210-Seminar-2, capacity: 250, location: ENG Comp Lab", "name: COMP2171-Seminar-1, capacity: 122, location: ENG Comp Lab", "name: GEOL3002-Lecture-1, capacity: 9, location: SLT3", "name: COMP2211-Lecture-1, capacity: 122, location: SLT1", "name: CHEM1901-Lecture-1, capacity: 43, location: SLT1", "name: COMP1161-Lecture-2, capacity: 250, location: SLT1"],
            ["name: COMP1210-Tutorial-3, capacity: 81, location: C5", "name: INFO3105-Tutorial-4, capacity: 57, location: C3", "name: COMP3101-Tutorial-3, capacity: 59, location: C3", "name: COMP2211-Tutorial-8, capacity: 18, location: C3", "name: GEOL2202-Tutorial-2, capacity: 7, location: C2"], 
            ["name: COMP1210-Tutorial-4, capacity: 81, location: C5", "name: INFO3105-Tutorial-5, capacity: 57, location: C3", "name: COMP3101-Tutorial-2, capacity: 59, location: C3", "name: COMP2211-Tutorial-6, capacity: 18, location: C3", "name: GEOL2202-Tutorial-1, capacity: 7, location: C2"], 
            ["name: MICR1011-Tutorial-1, capacity: 6, location: C5", "name: SWEN3101-Tutorial-4, capacity: 30, location: C3", "name: COMP3220-Lecture-2, capacity: 136, location: SLT1"], 
            ["name: INFO3180-Tutorial-4, capacity: 85, location: C5", "name: INFO2180-Tutorial-3, capacity: 19, location: C3", "name: GEOG1131-Seminar-1, capacity: 44, location: ENG Comp Lab", "name: COMP1127-Lecture-2, capacity: 250, location: SLT3", "name: CHEM2310-Lecture-1, capacity: 32, location: SLT2", "name: PHYS2351-Lecture-2, capacity: 34, location: SLT2"], 
            ["name: MATH2404-Tutorial-5, capacity: 9, location: C5", "name: SWEN3920-Tutorial-7, capacity: 22, location: C3", "name: MATH1141-Tutorial-1, capacity: 5, location: C2", "name: COMP2190-Lecture-1, capacity: 236, location: SLT3"], 
            ["name: MATH2404-Tutorial-4, capacity: 9, location: C5", "name: SWEN3920-Tutorial-5, capacity: 22, location: C3", "name: COMP1127-Tutorial-6, capacity: 46, location: C3", "name: COMP3901-Tutorial-1, capacity: 103, location: C3", "name: COMP2140-Tutorial-2, capacity: 153, location: C2", "name: INFO3180-Seminar-1, capacity: 262, location: Math Room 2"],
            ["name: MATH1141-Tutorial-6, capacity: 5, location: C5", "name: SWEN3920-Tutorial-4, capacity: 22, location: C3", "name: COMP3901-Tutorial-5, capacity: 103, location: C3", "name: COMP2211-Tutorial-1, capacity: 18, location: C2", "name: MATH1141-Tutorial-2, capacity: 5, location: C2", "name: PHYS2351-Tutorial-5, capacity: 9, location: C2", "name: COMP3161-Lecture-2, capacity: 398, location: SLT1"],
            ["name: MATH1141-Tutorial-4, capacity: 5, location: C5", "name: COMP3901-Tutorial-3, capacity: 103, location: C3", "name: SWEN3920-Tutorial-1, capacity: 22, location: C3", "name: CHEM2310-Tutorial-1, capacity: 21, location: C2", "name: COMP1220-Tutorial-5, capacity: 54, location: C2", "name: COMP3901-Lab-1, capacity: 103, location: C2", "name: COMP2201-Lecture-2, capacity: 122, location: SLT2", "name: MATH1141-Lecture-1, capacity: 26, location: SLT1", "name: COMP3161-Lecture-1, capacity: 398, location: SLT1"],
            ["name: INFO3180-Tutorial-2, capacity: 85, location: C5", "name: INFO2180-Tutorial-1, capacity: 19, location: C3", "name: BIOC2014-Lecture-2, capacity: 19, location: SLT2", "name: INFO3170-Lecture-1, capacity: 262, location: SLT1", "name: COMP2140-Lecture-1, capacity: 236, location: SLT1"], 
            ["name: SWEN3145-Tutorial-2, capacity: 30, location: C3"], 
            ["name: INFO3180-Tutorial-3, capacity: 85, location: C5", "name: INFO2180-Tutorial-2, capacity: 19, location: C3", "name: BIOC2014-Lecture-1, capacity: 19, location: SLT1", "name: SWEN3101-Lecture-3, capacity: 116, location: SLT1", "name: COMP2340-Lecture-2, capacity: 177, location: SLT1"], 
            ["name: MATH2404-Tutorial-3, capacity: 9, location: C5", "name: SWEN3920-Tutorial-6, capacity: 22, location: C3", "name: COMP1127-Tutorial-4, capacity: 46, location: C3", "name: COMP3161-Tutorial-3, capacity: 172, location: C3", "name: COMP2171-Tutorial-5, capacity: 23, location: C2", "name: MATH1141-Seminar-1, capacity: 26, location: Math Room 2"], 
            ["name: MATH2404-Tutorial-2, capacity: 9, location: C5", "name: SWEN3145-Tutorial-1, capacity: 30, location: C3", "name: COMP1127-Tutorial-1, capacity: 46, location: C3", "name: COMP3161-Tutorial-1, capacity: 172, location: C3", "name: COMP2171-Tutorial-2, capacity: 23, location: C2", "name: MATH1141-Lecture-3, capacity: 26, location: SLT2"], 
            ["name: MATH2404-Tutorial-1, capacity: 9, location: C5", "name: SWEN3920-Tutorial-3, capacity: 22, location: C3", "name: COMP1126-Tutorial-6, capacity: 46, location: C3", "name: COMP2190-Lab-1, capacity: 307, location: C2", "name: MATH2404-Lab-2, capacity: 9, location: C2", "name: BIOC3013-Seminar-1, capacity: 23, location: C2", "name: INFO3170-Seminar-2, capacity: 262, location: Math Room 1", "name: SWEN3920-Seminar-2, capacity: 116, location: Math Room 1", "name: COMP2340-Lecture-1, capacity: 177, location: SLT3", "name: MATH2404-Lecture-1, capacity: 33, location: SLT1", "name: BIOC2014-Lecture-3, capacity: 19, location: SLT1", "name: INFO3155-Lecture-1, capacity: 262, location: SLT1", "name: INFO2110-Lecture-1, capacity: 114, location: SLT1"],
            ["name: SWEN3145-Tutorial-3, capacity: 30, location: C3"],
            ["name: SWEN3145-Tutorial-4, capacity: 30, location: C5", "name: COMP1161-Tutorial-5, capacity: 65, location: C3", "name: INFO3155-Tutorial-8, capacity: 43, location: C3", "name: COMP3161-Tutorial-2, capacity: 172, location: C3", "name: COMP2171-Tutorial-7, capacity: 23, location: C2", "name: COMP1220-Tutorial-1, capacity: 54, location: C2"],
            ["name: COMP1210-Tutorial-1, capacity: 81, location: C5", "name: COMP3220-Tutorial-5, capacity: 25, location: C3", "name: INFO3155-Tutorial-3, capacity: 43, location: C3", "name: COMP2211-Tutorial-7, capacity: 18, location: C3", "name: GEOL2202-Lab-1, capacity: 7, location: C2"], 
            ["name: COMP1210-Tutorial-2, capacity: 81, location: C5", "name: INFO3105-Tutorial-3, capacity: 57, location: C3", "name: COMP3101-Tutorial-1, capacity: 59, location: C3", "name: COMP2211-Tutorial-2, capacity: 18, location: C3", "name: COMP1161-Lab-1, capacity: 65, location: C2", "name: SWEN3145-Seminar-1, capacity: 116, location: Math Room 1", "name: INFO3155-Seminar-1, capacity: 262, location: Math Room 1", "name: COMP1161-Lecture-1, capacity: 250, location: SLT3", "name: COMP2171-Lecture-2, capacity: 122, location: SLT1"],
            ["name: INFO3180-Tutorial-1, capacity: 85, location: C5", "name: INFO2100-Tutorial-1, capacity: 148, location: C3", "name: BIOC3013-Lecture-1, capacity: 23, location: SLT1", "name: INFO2180-Lecture-3, capacity: 114, location: SLT1", "name: CHEM2210-Lecture-1, capacity: 32, location: SLT1"],
            ["name: COMP3220-Tutorial-6, capacity: 25, location: C3"],
            ["name: CHEM2210-Tutorial-6, capacity: 5, location: C5", "name: SWEN3920-Tutorial-2, capacity: 22, location: C3", "name: COMP1127-Tutorial-2, capacity: 46, location: C3", "name: COMP3901-Tutorial-2, capacity: 103, location: C3", "name: MATH1141-Tutorial-3, capacity: 5, location: C2", "name: COMP2171-Tutorial-6, capacity: 23, location: C2"],
            ["name: CHEM2210-Tutorial-8, capacity: 5, location: C5", "name: COMP1126-Tutorial-7, capacity: 46, location: C3", "name: CHEM1901-Tutorial-4, capacity: 11, location: C2", "name: COMP2171-Tutorial-4, capacity: 23, location: C2", "name: MICR1011-Seminar-1, capacity: 25, location: Math Room 1", "name: CHEM1901-Lecture-2, capacity: 43, location: SLT1", "name: COMP1127-Lecture-1, capacity: 250, location: SLT1"], 
            ["name: CHEM2210-Tutorial-9, capacity: 5, location: C5", "name: COMP1126-Tutorial-4, capacity: 46, location: C3", "name: CHEM1901-Tutorial-1, capacity: 11, location: C2", "name: COMP2171-Tutorial-3, capacity: 23, location: C2", "name: COMP1210-Lecture-1, capacity: 250, location: SLT2", "name: COMP3220-Lecture-1, capacity: 136, location: SLT2", "name: MICR1011-Lecture-1, capacity: 25, location: SLT1"], 
            [], 
            ["name: COMP3220-Tutorial-7, capacity: 25, location: C3"],
            ["name: CHEM2210-Tutorial-7, capacity: 5, location: C5", "name: COMP1126-Tutorial-5, capacity: 46, location: C3", "name: COMP2171-Tutorial-1, capacity: 23, location: C2", "name: COMP3220-Lab-2, capacity: 25, location: C2", "name: COMP1126-Lecture-3, capacity: 250, location: SLT2", "name: INFO3105-Lecture-3, capacity: 262, location: SLT2", "name: SWEN3145-Lecture-1, capacity: 116, location: SLT1"],
            ["name: GEOG1131-Tutorial-1, capacity: 57, location: C5", "name: INFO2180-Tutorial-4, capacity: 19, location: C3", "name: INFO3110-Tutorial-1, capacity: 49, location: C3", "name: GEOL3002-Tutorial-1, capacity: 6, location: C3", "name: COMP2190-Tutorial-1, capacity: 307, location: C2", "name: MATH2404-Lab-1, capacity: 9, location: C2", "name: COMP2190-Lecture-2, capacity: 236, location: SLT2"],
            ["name: CHEM1901-Tutorial-5, capacity: 11, location: C5", "name: COMP1161-Tutorial-4, capacity: 65, location: C3", "name: INFO3110-Tutorial-7, capacity: 49, location: C3", "name: COMP2211-Tutorial-4, capacity: 18, location: C3", "name: COMP1220-Seminar-1, capacity: 250, location: C2"],
            [],
            ["name: BIOC2014-Tutorial-4, capacity: 6, location: C3"], 
            ["name: INFO3170-Tutorial-1, capacity: 114, location: C5", "name: COMP1161-Tutorial-2, capacity: 65, location: C3", "name: COMP2201-Tutorial-1, capacity: 79, location: C3", "name: COMP1220-Tutorial-2, capacity: 54, location: C2", "name: COMP3101-Seminar-1, capacity: 136, location: Math Room 1"], 
            ["name: INFO3170-Tutorial-2, capacity: 114, location: C5", "name: COMP1161-Tutorial-3, capacity: 65, location: C3", "name: COMP2201-Tutorial-2, capacity: 79, location: C3", "name: COMP1220-Tutorial-3, capacity: 54, location: C2", "name: COMP3161-Seminar-1, capacity: 398, location: Math Room 1", "name: COMP2211-Seminar-1, capacity: 122, location: ENG Comp Lab", "name: GEOL2202-Lecture-1, capacity: 34, location: SLT3", "name: COMP3901-Lecture-1, capacity: 398, location: SLT1", "name: COMP2201-Lecture-1, capacity: 122, location: SLT1"], 
            ["name: INFO3170-Tutorial-3, capacity: 114, location: C5", "name: COMP1161-Tutorial-1, capacity: 65, location: C3", "name: COMP2211-Tutorial-9, capacity: 18, location: C3", "name: GEOL2202-Tutorial-4, capacity: 7, location: C2", "name: COMP3101-Lecture-1, capacity: 136, location: SLT3"],
            [], ["name: INFO3105-Tutorial-6, capacity: 57, location: C3"], 
            ["name: CHEM2210-Tutorial-5, capacity: 5, location: C5", "name: COMP1126-Tutorial-2, capacity: 46, location: C3", "name: COMP2201-Lab-1, capacity: 79, location: C2", "name: COMP3220-Lab-1, capacity: 25, location: C2", "name: COMP1126-Lecture-2, capacity: 250, location: SLT2", "name: INFO3110-Lecture-1, capacity: 262, location: SLT2", "name: SWEN3920-Lecture-2, capacity: 116, location: SLT1"],
            ["name: CHEM1901-Tutorial-3, capacity: 11, location: C5", "name: COMP1127-Tutorial-7, capacity: 46, location: C3", "name: INFO3110-Tutorial-5, capacity: 49, location: C3", "name: COMP2211-Tutorial-5, capacity: 18, location: C3", "name: COMP1210-Seminar-1, capacity: 250, location: C2", "name: SWEN3920-Seminar-1, capacity: 116, location: ENG Comp Lab", "name: INFO3110-Lecture-3, capacity: 262, location: SLT3", "name: COMP1126-Lecture-1, capacity: 250, location: SLT3"],
            ["name: CHEM1901-Tutorial-2, capacity: 11, location: C5", "name: COMP1127-Tutorial-3, capacity: 46, location: C3", "name: INFO3110-Tutorial-2, capacity: 49, location: C3", "name: COMP2211-Tutorial-3, capacity: 18, location: C3", "name: COMP1127-Seminar-1, capacity: 250, location: Math Room 1", "name: SWEN3920-Lecture-1, capacity: 116, location: SLT1", "name: INFO3180-Lecture-1, capacity: 262, location: SLT1", "name: COMP1127-Lecture-3, capacity: 250, location: SLT1"],
            [], 
            ["name: BIOC2014-Tutorial-3, capacity: 6, location: C3"],
            ["name: CHEM2210-Tutorial-4, capacity: 5, location: C5", "name: COMP1126-Tutorial-3, capacity: 46, location: C3", "name: CHEM1901-Lab-2, capacity: 11, location: C2", "name: CHEM2310-Lab-2, capacity: 21, location: C2", "name: COMP1210-Lecture-2, capacity: 250, location: SLT1", "name: INFO3105-Lecture-2, capacity: 262, location: SLT1"],
            ["name: CHEM2210-Tutorial-2, capacity: 5, location: C5", "name: BIOC3013-Tutorial-1, capacity: 6, location: C3", "name: INFO2110-Tutorial-3, capacity: 37, location: C2", "name: SWEN3145-Seminar-2, capacity: 116, location: Math Room 1", "name: CHEM2210-Seminar-2, capacity: 32, location: Math Room 1", "name: MATH1141-Lecture-2, capacity: 26, location: SLT2", "name: INFO2100-Lecture-1, capacity: 114, location: SLT1", "name: BIOC3013-Lecture-2, capacity: 23, location: SLT1"],
            ["name: CHEM2210-Tutorial-3, capacity: 5, location: C5", "name: COMP1126-Tutorial-1, capacity: 46, location: C3", "name: CHEM1901-Lab-1, capacity: 11, location: C2", "name: CHEM2310-Lab-1, capacity: 21, location: C2"], 
            [],
            ["name: PHYS2351-Tutorial-4, capacity: 9, location: C3"],
            ["name: GEOL2202-Tutorial-6, capacity: 7, location: C5", "name: INFO3155-Tutorial-7, capacity: 43, location: C3", "name: COMP2340-Tutorial-1, capacity: 46, location: C3", "name: SWEN3101-Tutorial-5, capacity: 30, location: C3"],
            ["name: GEOL2202-Tutorial-5, capacity: 7, location: C5", "name: INFO3155-Tutorial-4, capacity: 43, location: C3", "name: COMP2340-Tutorial-2, capacity: 46, location: C3", "name: SWEN3101-Lecture-1, capacity: 116, location: SLT1"], 
            ["name: CHEM2210-Tutorial-1, capacity: 5, location: C5", "name: MATH1141-Tutorial-7, capacity: 5, location: C3", "name: GEOG1131-Seminar-2, capacity: 44, location: C2", "name: COMP2171-Seminar-2, capacity: 122, location: Math Room 2", "name: GEOL3002-Seminar-1, capacity: 9, location: Math Room 1", "name: INFO2110-Seminar-1, capacity: 114, location: ENG Comp Lab", "name: GEOG1131-Lecture-1, capacity: 44, location: SLT3", "name: INFO2180-Lecture-2, capacity: 114, location: SLT2"],
            []]
    }
        
    # timeTable = [
    #     ["name: BIOC3013-Lecture-2, capacity: 23, location: C5", "name: GEOL3002-Lecture-1, capacity: 9, location: C3", "name: MATH1141-Lecture-3, capacity: 26, location: C2"], ["name: COMP3801-Tutorial-3, capacity: 20, location : C3, name: COMP2140-Seminar-1, capacity: 119, location: SLT3"],
    #     ["name: CHEM2310-Lecture-1, capacity: 32, location: Math Room 2", "name: GEOG1131-Lecture-1, capacity: 44, location: Math Room 1"], ["name: CHEM1901-Lecture-2, capacity: 43, location: ENG Comp Lab", "name: GEOL2202-Lecture-1, capacity: 34, location: SLT3", "name: PHYS2351-Lecture-2, capacity: 34, location: SLT2"], ["name: MICR1011-Lecture-1, capacity: 25, location: SLT1", "name: MATH2404-Lecture-1, capacity: 33, location: Physics Lab", "name: CHEM2210-Lecture-2, capacity: 32, location: GEOG Lab 3"],
    #     ["name: MATH1151-Seminar-1, capacity: 30, location: Math Room 1, name: GEOG1131-Seminar-1, capacity: 18, location: GEOG Lecture RM 2"], ["name: MATH1151-Lecture-1, capacity: 30, location: Math Room 2, name: CHEM3010-Lecture-1, capacity: 16, location: Math Room 1"], ["name: GEOG1232-Lecture-1, capacity: 3, location: GEOG Lecture RM 1, name: COMP3220-tutorial-1, capacity: 36, location: CR1"], ["name: CHEM2111-Tutorial-1,capacity: 4, location: Math Room 2, name: COMP3912-Lecture-1, capacity: 72, location: C2"], ["name: PHYS1422-Lecture-1, capacity: 21, location: SLT3, name: MICR2211-Seminar-1, capacity: 19, location: GEOG Lab 3"],
    #     ["name: INFO2180-Lecture-3, capacity: 114, location: GEOG Lecture RM 1", "name: INFO2100-Lecture-1, capacity: 114, location: GEOG Lab 2"], ["name: MATH3424-Lecture-1, capacity: 10, location: Math Room 2, name: CHEM3010-Lecture-1, capacity: 16, location: Math Room 1"],  ["name: CHEM2110-Tutorial-1, capacity: 32, location: C3, name: CHEM2402-Tutorial-2, capacity: 27, location: Math Room 2"], ["name: CHEM2402-Tutorial-1, capacity: 27, location: Math Room 1, name: COMP2140-Seminar-2, capacity: 119, location: SLT3"], ["name: COMP3912-Tutorial-1, capacity: 72, location: C2, name: COMP2140-Seminar-1, capacity: 119, location: SLT3"],
    #     ["name: GEOG2233-Seminar-1, capacity: 19, location: GEOG Lecture 2, name: MATH3405-Lecture-1, capacity: 18, location: Math Room 1"], ["name: CHEM2310-Lecture-1, capacity: 55, location: C2"], ["name: PHYS2351-Lecture-1, capacity: 34, location: Math Room 1", "name: CHEM2210-Lecture-1, capacity: 32, location: ENG Comp Lab"], [""], ["name: CHEM2310-Tutorial-2, capacity: 21, location: SLT3", "name: BIOC2014-Lecture-2, capacity: 19, location: SLT2", "name: INFO2180-Lecture-2, capacity: 114, location: SLT1"],
    #     ["name: GEOG1131-Seminar-2, capacity: 44, location: Physics Lab", "name: INFO3110-Lecture-2, capacity: 262, location: GEOG Lab 3"], ["name: CHEM2011-Lab-1, capacity: 48, location: GEOG Lab 2, name: COMP3702-Lecture-1, capacity: 24, location: CompCLR"], ["name: CHEM3010-Seminar-1,capacity: 16, location: Math Room 1, name: MICR1010-Lecture-1, capacity: 28, location: Math Room 2"], [""], ["name: CHEM2211-Lecture-1, capacity: 16, location: C3, name: COMP3702-Lecture-1, capacity: 24, location: SLT2"],
    #     ["name: PHYS3341-Lecture-1, capacity: 14, location: Physics Lab"], ["name: COMP2211-Tutorial-1, capacity: 21, location: C3"], ["name: CHEM3010-Seminar-1,capacity: 16, location: Math Room 1"], [""], ["name: COMP2140-Seminar-2, capacity: 119, location: SLT3, name: CHEM2211-Lecture-1, capacity: 16, location: C3"],
    #     ["name: PHYS3341-Lecture-1, capacity: 14, location: Physics Lab, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: COMP3220-Seminar-1, capacity: 136, location: SLT3, name: COMP2171-Lab-1, capacity: 30, location: CLR"], ["name: COMP2171-Lab-2, capacity: 30, location: CLR"], [""], ["name: COMP2802-Lecture-1, capacity: 123, location: SLT3, name: CHEM2211-Lecture-1, capacity: 16, location: C3"],
    #     ["name: COMP3410-Lecture-1, capacity: 14, location: COMPCLR, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: GEOG3131-Lecture-1, capacity: 34, location: GEOG Lecture RM 2, name: COMP2171-Lab-1, capacity: 30, location: CLR"], ["name: COMP2171-Lab-2, capacity: 30, location: CLR"], ["name: COMP2140-Lecture-1, capacity: 119, location: SLT1"], ["name: ELET1405-Seminar-1, capacity: 20, location: Math Room 1, name: COMP2802-Lecture-1, capacity: 123, location: SLT3"],
    #     ["name: MICR1010-Seminar-1, capacity: 28, location: ENG Comp Lab, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: COMP2171-Lab-1, capacity: 30, location: CLR, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: CHEM2111-Tutorial-1, capacity: 4, location: Math Room 1"], ["name: SWEN3101-Tutorial-1, capacity: 24, location: C2 name: GEOL2201-Seminar-1, capacity: 26, location: GEOG Lecture RM 1"], [" name: ELET2210-Tutorial-1, capacity: 19, location: C3, name: COMP2201-Seminar-1,capacity: 64, location: C2"],
    #     ["name: MATH3424-Seminar-1, capacity: 10, location: Math Room 1, name: MICR1010-Seminar-1, capacity: 28, location: ENG Comp Lab"], ["name: GEOG3131-Lecture-2, capacity: 4, location: GEOG Lecture RM 2, name: COMP2171-Lab-1, capacity: 30, location: CLR"], ["name: GEOG3131-Tutorial-1, capacity: 4, location: GEOG Lecture RM 2, name: GEOL1104-Tutorial-1, capacity: 155, location: SLT2"], ["name: CHEM2011-Seminar-1, capacity: 37, location: GEOG Lab 2, name: PHYS1411-Seminar-1,capacity: 25, location: ENG Comp Lab"], ["name: COMP2201-Seminar-1,capacity: 64, location: C2, name: COMP3702-Lecture-1, capacity: 24, location: SLT2"],
    #     ["name: CHEM2310-Tutorial-1, capacity: 5, location: C2"], ["name: ELET1405-Seminar-1, capacity: 20, location: GEOG Lab 2"], ["name: GEOL1104-Tutorial-1, capacity: 155, location: SLT2"], ["name: ELET1405-Seminar-2, capacity: 20, location: GEOG Lab 2"], ["name: COMP3702-Lecture-1, capacity: 24, location: SLT2"],
    #     ["name: CHEM2310-Tutorial-1, capacity: 5, location: C2"], ["name: ELET1405-Seminar-1, capacity: 20, location: GEOG Lab 2"], ["name: BIOL2312-Tutorial-1, capacity: 7, location: CompCLR name: MATH2407-Seminar-1, capacity: 22, location: C3"], ["name: ELET1405-Seminar-2, capacity: 20, location: GEOG Lab 2"], ["name: GEOG2231-Lecture-1, capacity: 26, location: GEOG Lecture RM 1"]
    # ]
    
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
                    timetable_dict[day][time_slot] = timetable[index][0]
        timetables_dict[key] = timetable_dict

    # return render_template('timetable.html', timetable=timetable, days_of_week=days_of_week, time_slots=time_slots)
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
    