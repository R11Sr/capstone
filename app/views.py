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
        flash(error_message, 'error')
    
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
        flash(error_message, 'error')
    
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
        flash(error_message, 'error')
    
    
    clear_form(pform)
    

    return render_template('setParameters.html', form=pform)



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
    
    timeTable = [
        ["name: COMP3801-Tutorial-2, capacity: 28, location : C3, name: ELET3430-Tutorial-2, capacity: 40, location: Math Room 1"], ["name: ELET3430-Tutorial-1, capacity: 40, location: Math Room 1 name: COMP3652-Tutorial-1, capacity: 5, location: Math Room 2"], ["name: COMP2171-Seminar-1, capacity: 64, location: SLT1, name: COMP2190-Seminar-1, capacity: 119, location: SLT3"], ["name: COMP3901-Seminar-1, capacity: 19, location: C3 name: INFO2100-Tutorial-1, capacity: 18, location: Math Room 1"], ["name: COMP3801-Tutorial-3, capacity: 20, location : C3, name: COMP2140-Seminar-1, capacity: 119, location: SLT3"],
        ["name: COMP3801-Tutorial-1, capacity: 26, location : C3 name: GEOG3331-Tutorial-1, capacity: 4, location: GEOG Lecture RM 2"], ["name: MATH1151-Lecture-1, capacity: 30, location: Math Room 2, name: PHYS1422-Lecture-2, capacity: 51, location: SLT3"], ["name: GEOG1232-Lecture-1, capacity: 3, location: GEOG Lecture RM 1, name: COMP3220-Seminar-1, capacity: 136, location: SLT2"], ["name: COMP2171-Seminar-2, capacity: 64, location: C3, name: COMP3912-Lecture-1, capacity: 72, location: C2"], ["name: COMP2140-Seminar-1, capacity: 119, location: SLT3, name: ELET1405-Seminar-1, capacity: 20, location: COMPCLR"],
        ["name: MATH1151-Seminar-1, capacity: 30, location: Math Room 1, name: GEOG1131-Seminar-1, capacity: 18, location: GEOG Lecture RM 2"], ["name: MATH1151-Lecture-1, capacity: 30, location: Math Room 2, name: CHEM3010-Lecture-1, capacity: 16, location: Math Room 1"], ["name: GEOG1232-Lecture-1, capacity: 3, location: GEOG Lecture RM 1, name: COMP3220-tutorial-1, capacity: 36, location: CR1"], ["name: CHEM2111-Tutorial-1,capacity: 4, location: Math Room 2, name: COMP3912-Lecture-1, capacity: 72, location: C2"], ["name: PHYS1422-Lecture-1, capacity: 21, location: SLT3, name: MICR2211-Seminar-1, capacity: 19, location: GEOG Lab 3"],
        ["name: MATH2401-Lecture-1, capacity: 34, location: C3, name: GEOG1232-Seminar-1, capacity: 39, location: GEOG Lecture RM 2"], ["name: MATH3424-Lecture-1, capacity: 10, location: Math Room 2, name: CHEM3010-Lecture-1, capacity: 16, location: Math Room 1"],  ["name: CHEM2110-Tutorial-1, capacity: 32, location: C3, name: CHEM2402-Tutorial-2, capacity: 27, location: Math Room 2"], ["name: CHEM2402-Tutorial-1, capacity: 27, location: Math Room 1, name: COMP2140-Seminar-2, capacity: 119, location: SLT3"], ["name: COMP3912-Tutorial-1, capacity: 72, location: C2, name: COMP2140-Seminar-1, capacity: 119, location: SLT3"],
        ["name: GEOG2233-Seminar-1, capacity: 19, location: GEOG Lecture 2, name: MATH3405-Lecture-1, capacity: 18, location: Math Room 1"], ["name: CHEM2310-Lecture-1, capacity: 55, location: C2"], ["name: CHEM2310-Lecture-2, capacity: 55, location: C2, name: MICR1010-Lecture-1, capacity: 28, location: Math Room 2"], [""], ["name: GEOL2201-Seminar-1, capacity: 26, location: GEOG Lecture RM 2, name: COMP3912-Tutorial-1, capacity: 72, location: C2"],
        ["name: MATH2401-Lecture-2, capacity: 34, location: C3, name: PHYS3341-Lecture-1, capacity: 14, location: Physics Lab"], ["name: CHEM2011-Lab-1, capacity: 48, location: GEOG Lab 2, name: COMP3702-Lecture-1, capacity: 24, location: CompCLR"], ["name: CHEM3010-Seminar-1,capacity: 16, location: Math Room 1, name: MICR1010-Lecture-1, capacity: 28, location: Math Room 2"], [""], ["name: CHEM2211-Lecture-1, capacity: 16, location: C3, name: COMP3702-Lecture-1, capacity: 24, location: SLT2"],
        ["name: PHYS3341-Lecture-1, capacity: 14, location: Physics Lab"], ["name: COMP2211-Tutorial-1, capacity: 21, location: C3"], ["name: CHEM3010-Seminar-1,capacity: 16, location: Math Room 1"], [""], ["name: COMP2140-Seminar-2, capacity: 119, location: SLT3, name: CHEM2211-Lecture-1, capacity: 16, location: C3"],
        ["name: PHYS3341-Lecture-1, capacity: 14, location: Physics Lab, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: COMP3220-Seminar-1, capacity: 136, location: SLT3, name: COMP2171-Lab-1, capacity: 30, location: CLR"], ["name: COMP2171-Lab-2, capacity: 30, location: CLR"], [""], ["name: COMP2802-Lecture-1, capacity: 123, location: SLT3, name: CHEM2211-Lecture-1, capacity: 16, location: C3"],
        ["name: COMP3410-Lecture-1, capacity: 14, location: COMPCLR, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: GEOG3131-Lecture-1, capacity: 34, location: GEOG Lecture RM 2, name: COMP2171-Lab-1, capacity: 30, location: CLR"], ["name: COMP2171-Lab-2, capacity: 30, location: CLR"], ["name: COMP2140-Lecture-1, capacity: 119, location: SLT1"], ["name: ELET1405-Seminar-1, capacity: 20, location: Math Room 1, name: COMP2802-Lecture-1, capacity: 123, location: SLT3"],
        ["name: MICR1010-Seminar-1, capacity: 28, location: ENG Comp Lab, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: COMP2171-Lab-1, capacity: 30, location: CLR, name: GEOL1104-Lecture-1, capacity: 155, location: SLT2"], ["name: CHEM2111-Tutorial-1, capacity: 4, location: Math Room 1"], ["name: SWEN3101-Tutorial-1, capacity: 24, location: C2 name: GEOL2201-Seminar-1, capacity: 26, location: GEOG Lecture RM 1"], [" name: ELET2210-Tutorial-1, capacity: 19, location: C3, name: COMP2201-Seminar-1,capacity: 64, location: C2"],
        ["name: MATH3424-Seminar-1, capacity: 10, location: Math Room 1, name: MICR1010-Seminar-1, capacity: 28, location: ENG Comp Lab"], ["name: GEOG3131-Lecture-2, capacity: 4, location: GEOG Lecture RM 2, name: COMP2171-Lab-1, capacity: 30, location: CLR"], ["name: GEOG3131-Tutorial-1, capacity: 4, location: GEOG Lecture RM 2, name: GEOL1104-Tutorial-1, capacity: 155, location: SLT2"], ["name: CHEM2011-Seminar-1, capacity: 37, location: GEOG Lab 2, name: PHYS1411-Seminar-1,capacity: 25, location: ENG Comp Lab"], ["name: COMP2201-Seminar-1,capacity: 64, location: C2, name: COMP3702-Lecture-1, capacity: 24, location: SLT2"],
        ["name: CHEM2310-Tutorial-1, capacity: 5, location: C2"], ["name: ELET1405-Seminar-1, capacity: 20, location: GEOG Lab 2"], ["name: GEOL1104-Tutorial-1, capacity: 155, location: SLT2"], ["name: ELET1405-Seminar-2, capacity: 20, location: GEOG Lab 2"], ["name: COMP3702-Lecture-1, capacity: 24, location: SLT2"],
        ["name: CHEM2310-Tutorial-1, capacity: 5, location: C2"], ["name: ELET1405-Seminar-1, capacity: 20, location: GEOG Lab 2"], ["name: BIOL2312-Tutorial-1, capacity: 7, location: CompCLR name: MATH2407-Seminar-1, capacity: 22, location: C3"], ["name: ELET1405-Seminar-2, capacity: 20, location: GEOG Lab 2"], ["name: GEOG2231-Lecture-1, capacity: 26, location: GEOG Lecture RM 1"]
    ]
    
    
#     timetable = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [<name: SWEN3101-Tutorial-1, session: Tutorial, capacity: 24>, <name: SWEN3145-Seminar-1, session: Seminar, capacity: 56>, <name:r, capacity: 119>, <name: COMP2201-Seminar-1, session: Seminar, capacity: 64>, <name: COMP3101-Seminar-1, session: Seminar, capacity: 136>, <name:al, capacity: 32>, <name: COMP1220-Seminar-1, session: Seminar, capacity: 59>, <name: COMP1126-Tutorial-1, session: Tutorial, capacity: 79>, <namerial, capacity: 159>, <name: INFO3105-Tutorial-1, session: Tutorial, capacity: 43>, <name: INFO3170-Tutorial-1, session: Tutorial, capacity: 43>, 
# Tutorial, capacity: 72>, <name: COMP2171-Seminar-1, session: Seminar, capacity: 64>, <name: COMP2190-Seminar-1, session: Seminar, capacity: 119>,  Tutorial, capacity: 155>, <name: COMP3161-Tutorial-1, session: Tutorial, capacity: 86>, <name: COMP3901-Seminar-1, session: Seminar, capacity: 19: Tutorial, capacity: 85>, <name: INFO2100-Tutorial-1, session: Tutorial, capacity: 18>, <name: INFO2180-Seminar-1, session: Seminar, capacityession: Tutorial, capacity: 2>, <name: MATH2404-Seminar-1, session: Seminar, capacity: 14>, <name: MICR1011-Seminar-1, session: Seminar, capacity:on: Seminar, capacity: 19>, <name: CHEM1901-Tutorial-1, session: Tutorial, capacity: 8>, <name: GEOG1131-Seminar-1, session: Seminar, capacity: 18: Tutorial, capacity: 36>, <name: GEOL3002-Tutorial-1, session: Tutorial, capacity: 6>, <name: BIOC3013-Seminar-1, session: Seminar, capacity: 14 Seminar, capacity: 26>, <name: GEOG1231-Tutorial-1, session: Tutorial, capacity: 7>, <name: MICR1010-Seminar-1, session: Seminar, capacity: 28>,  Tutorial, capacity: 19>, <name: PHYS1412-Seminar-1, session: Seminar, capacity: 29>, <name: MATH2401-Seminar-1, session: Seminar, capacity: 34>, utorial, capacity: 7>, <name: CHEM2011-Seminar-1, session: Seminar, capacity: 37>, <name: PHYS1411-Seminar-1, session: Seminar, capacity: 25>, <naorial, capacity: 7>, <name: COMP3802-Tutorial-1, session: Tutorial, capacity: 4>, <name: GEOG2131-Seminar-1, session: Seminar, capacity: 29>, <namr, capacity: 30>, <name: GEOL1101-Tutorial-1, session: Tutorial, capacity: 8>, <name: BIOC1021-Tutorial-1, session: Tutorial, capacity: 23>, <nameial, capacity: 10>, <name: ELET2430-Tutorial-1, session: Tutorial, capacity: 6>, <name: ELET3211-Seminar-1, session: Seminar, capacity: 16>, <name, capacity: 36>, <name: MATH3401-Seminar-1, session: Seminar, capacity: 15>, <name: MATH3405-Seminar-1, session: Seminar, capacity: 10>, <name: CH
# capacity: 35>, <name: ELET3430-Tutorial-1, session: Tutorial, capacity: 4>, <name: COMP3652-Tutorial-1, session: Tutorial, capacity: 5>, <name: CH
# capacity: 30>, <name: COMP3801-Tutorial-1, session: Tutorial, capacity: 26>, <name: GEOG3331-Tutorial-1, session: Tutorial, capacity: 4>, <name: M capacity: 2>, <name: PHYS3300-Seminar-1, session: Seminar, capacity: 15>, <name: COMP2802-Seminar-1, session: Seminar, capacity: 22>, <name: MATHcity: 30>, <name: GEOL1103-Seminar-1, session: Seminar, capacity: 23>, <name: GEOL2201-Seminar-1, session: Seminar, capacity: 26>, <name: GEOG2332: 24>, <name: MATH2403-Seminar-1, session: Seminar, capacity: 21>, <name: PHYS3341-Seminar-1, session: Seminar, capacity: 14>, <name: ELET1400-Tut: 4>, <name: GEOG1232-Seminar-1, session: Seminar, capacity: 34>, <name: GEOG1132-Tutorial-1, session: Tutorial, capacity: 17>, <name: CHEM3010-Se 8>, <name: ELET2420-Tutorial-1, session: Tutorial, capacity: 18>, <name: BIOC3014-Seminar-1, session: Seminar, capacity: 28>, <name: CHEM2111-Tut4>, <name: MATH1152-Tutorial-1, session: Tutorial, capacity: 7>, <name: COMP3410-Seminar-1, session: Seminar, capacity: 22>, <name: PHYS3351-Semin <name: MICR2211-Seminar-1, session: Seminar, capacity: 19>, <name: CHEM1902-Seminar-1, session: Seminar, capacity: 22>, <name: MATH3402-Tutorial-
# <name: CHEM3011-Tutorial-1, session: Tutorial, capacity: 4>, <name: MATH2407-Seminar-1, session: Seminar, capacity: 22>, <name: MATH3403-Tutorial-ame: PHYS3565-Seminar-1, session: Seminar, capacity: 8>, <name: COMP3162-Tutorial-1, session: Tutorial, capacity: 22>, <name: BIOC3011-Seminar-1, : COMP3192-Seminar-1, session: Seminar, capacity: 26>, <name: PHYS2296-Tutorial-1, session: Tutorial, capacity: 7>, <name: ELET1405-Seminar-1, sesLET2410-Seminar-1, session: Seminar, capacity: 25>, <name: PHYS2200-Tutorial-1, session: Tutorial, capacity: 11>, <name: GEOG3333-Tutorial-1, sess
# PHYS1421-Tutorial-1, session: Tutorial, capacity: 14>, <name: BIOL2312-Tutorial-1, session: Tutorial, capacity: 7>, <name: GEOL2203-Tutorial-1, se MATH3424-Seminar-1, session: Seminar, capacity: 12>], [], [], [], []]
    
#     timetable = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [ [], [], [], [], [<name: SWEN3101-Tutorial-1, session: Tutorial, capacity: 24>, <name: SWEN3920-Tutorial-1, session: Tutorial, capacity: 10>, <namorial, capacity: 10>, <name: MATH2411-Tutorial-1, session: Tutorial, capacity: 6>, <name: ELET2430-Tutorial-1, session: Tutorial, capacity: 6>, <ntorial, capacity: 7>, <name: GEOG2232-Tutorial-1, session: Tutorial, capacity: 5>, <name: PHYS1421-Tutorial-1, session: Tutorial, capacity: 14>, <
# Tutorial, capacity: 11>, <name: CHEM2210-Tutorial-1, session: Tutorial, capacity: 2>, <name: BIOC1021-Tutorial-1, session: Tutorial, capacity: 23>: Tutorial, capacity: 8>, <name: PHYS2296-Tutorial-1, session: Tutorial, capacity: 7>, <name: COMP1161-Tutorial-1, session: Tutorial, capacity: 15: Tutorial, capacity: 16>, <name: COMP3162-Tutorial-1, session: Tutorial, capacity: 22>, <name: GEOG3131-Tutorial-1, session: Tutorial, capacitssion: Tutorial, capacity: 4>, <name: CHEM2110-Tutorial-1, session: Tutorial, capacity: 32>, <name: CHEM3011-Tutorial-1, session: Tutorial, capaciession: Tutorial, capacity: 85>, <name: INFO2100-Tutorial-1, session: Tutorial, capacity: 18>, <name: GEOG2331-Tutorial-1, session: Tutorial, capa session: Tutorial, capacity: 7>, <name: COMP1210-Tutorial-1, session: Tutorial, capacity: 32>, <name: COMP1126-Tutorial-1, session: Tutorial, cap-1, session: Tutorial, capacity: 341>, <name: CHEM2111-Tutorial-1, session: Tutorial, capacity: 4>, <name: ELET2210-Tutorial-1, session: Tutorial,ial-1, session: Tutorial, capacity: 19>, <name: GEOG1132-Tutorial-1, session: Tutorial, capacity: 17>, <name: GEOL1104-Tutorial-1, session: Tutoritorial-1, session: Tutorial, capacity: 155>, <name: COMP3161-Tutorial-1, session: Tutorial, capacity: 86>, <name: COMP3912-Tutorial-1, session: Tu0-Tutorial-1, session: Tutorial, capacity: 72>, <name: COMP2211-Tutorial-1, session: Tutorial, capacity: 21>, <name: COMP3911-Tutorial-1, session:3002-Tutorial-1, session: Tutorial, capacity: 6>, <name: GEOG3331-Tutorial-1, session: Tutorial, capacity: 4>, <name: MATH1142-Tutorial-1, sessionEM1901-Tutorial-1, session: Tutorial, capacity: 8>, <name: CHEM2310-Tutorial-1, session: Tutorial, capacity: 5>, <name: COMP3652-Tutorial-1, sessiEM2402-Tutorial-1, session: Tutorial, capacity: 27>, <name: GEOG2231-Seminar-1, session: Seminar, capacity: 26>, <name: MATH3424-Seminar-1, sessio3011-Seminar-1, session: Seminar, capacity: 10>, <name: GEOG2233-Seminar-1, session: Seminar, capacity: 19>, <name: MATH3405-Seminar-1, session: S-Seminar-1, session: Seminar, capacity: 18>, <name: ELET2405-Seminar-1, session: Seminar, capacity: 36>, <name: ELET3211-Seminar-1, session: Semininar-1, session: Seminar, capacity: 26>, <name: MATH2404-Seminar-1, session: Seminar, capacity: 14>, <name: COMP3192-Seminar-1, session: Seminar, -1, session: Seminar, capacity: 14>, <name: GEOG2131-Seminar-1, session: Seminar, capacity: 29>, <name: CHEM2311-Seminar-1, session: Seminar, capa
# session: Seminar, capacity: 10>, <name: PHYS1411-Seminar-1, session: Seminar, capacity: 25>, <name: COMP3410-Seminar-1, session: Seminar, capacitysion: Seminar, capacity: 14>, <name: MATH2401-Seminar-1, session: Seminar, capacity: 34>, <name: GEOG1232-Seminar-1, session: Seminar, capacity: 3: Seminar, capacity: 19>, <name: MICR1010-Seminar-1, session: Seminar, capacity: 28>, <name: GEOL2201-Seminar-1, session: Seminar, capacity: 26>,eminar, capacity: 35>, <name: COMP1220-Seminar-1, session: Seminar, capacity: 59>, <name: MATH1151-Seminar-1, session: Seminar, capacity: 30>, <naar, capacity: 119>, <name: GEOG1131-Seminar-1, session: Seminar, capacity: 18>, <name: COMP2140-Seminar-1, session: Seminar, capacity: 119>, <namer, capacity: 19>, <name: ELET1405-Seminar-1, session: Seminar, capacity: 20>, <name: COMP3220-Seminar-1, session: Seminar, capacity: 136>, <name: 
# capacity: 22>, <name: GEOG3132-Seminar-1, session: Seminar, capacity: 19>, <name: CHEM2011-Seminar-1, session: Seminar, capacity: 37>, <name: GEOLcity: 29>, <name: COMP3702-Seminar-1, session: Seminar, capacity: 24>, <name: COMP2201-Seminar-1, session: Seminar, capacity: 64>, <name: COMP2802: 10>, <name: COMP2171-Seminar-1, session: Seminar, capacity: 64>, <name: PHYS1422-Seminar-1, session: Seminar, capacity: 21>, <name: SWEN3145-Sem, <name: MICR2211-Seminar-1, session: Seminar, capacity: 19>, <name: PHYS3341-Seminar-1, session: Seminar, capacity: 14>, <name: MATH2403-Seminar-ame: COMP3191-Seminar-1, session: Seminar, capacity: 12>, <name: CHEM2211-Seminar-1, session: Seminar, capacity: 16>, <name: CHEM3010-Seminar-1, s CHEM3110-Seminar-1, session: Seminar, capacity: 16>], [], [], [], []]
    
    
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
        flash('An error occurred while generating the PDF.', 'danger')
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

    
    