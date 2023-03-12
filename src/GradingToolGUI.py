import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
from typing import Dict, Any
from data import StudentInfo, ErrorInfo, Category, ExamInfo
<<<<<<< Updated upstream
import itertools
=======
from collections import defaultdict
from functools import partial
>>>>>>> Stashed changes

DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"
FILENAME = "master.json"
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}
AMOUNT, ERRORVALUE = 'amount', 'value'

#TODO 
# Error calculator
    # Buttons + amd - for changing error amount
    # Nothing correct button
# Update the data
# Select the folder
# Write data to master.json
# Copy the text to clipboard
# 



#initialize font 
def initialize_font():
    with dpg.font_registry():
        default_font = dpg.add_font(DEFAULT_FONT, 15)
        hl_font = dpg.add_font(HL_FONT, 15)
        title_font = dpg.add_font(HL_FONT, 22)
    return default_font, hl_font, title_font





def add_files_in_folder(dirname):
    student_list = []
    

    group = str(dirname).split('/')[-1]
    files = os.listdir(dirname)

    for file in files:
        student_name = str(file).strip().replace("_", " ")
        student = StudentInfo(name=student_name, group = group, grade=MAX_GRADE[group])
        student_list.append(student)
        
    return student_list


def select_student(sender, app_data, user_data):

    studentWithErrors, categoryList, student_list = user_data[0], user_data[1], user_data[2]
    student_name = str(app_data)
    studentObject = findStudent(student_name, student_list) 
    updateTable(categoryList, studentWithErrors, student_name)
    
    if (studentObject != None):
        updateDataWindow(studentObject)
    
    print(studentWithErrors)
    # for key, values in studentWithErrors.items():
    #     print(f"Student is {key}, error is {values}")
    


def updateDataWindow(studentObject):
    dpg.set_value("level", studentObject.group)
    dpg.set_value("student_grade", str(studentObject.grade))
    dpg.set_value("feedback_input", convertFeedbackToString(studentObject.feedback))
    dpg.set_value("error_points", studentObject.errorpoints)

def updateTable(categoryList, studentWithErrors, student):
    for category in categoryList:
        for error in category.errors:
            if (student in studentWithErrors.keys() and error._id in studentWithErrors[student].keys()):
                dpg.set_value(error._id, studentWithErrors[student][error._id][AMOUNT])
            else:
                dpg.set_value(error._id, 0)
    
def writeToJsonFile(sender, app_data, studentWithErrors):
    pass
 
    
def mistakeSelected(sender, app_data, user_data):
    
    student_name = dpg.get_value("student_view")
    
    #StudentWithErrors is dictionary for updating the students who have errors
    #Getting user_data
    studentWithErrors = user_data[0]
    student_list = user_data[1]
    category_list = user_data[2]
    
    #Getting from GUI Data
    category_name = dpg.get_item_parent(dpg.get_item_parent(sender))
    current_amount = dpg.get_value(sender)

    #Indexing the student data and error data
    current_student = findStudent(student_name, student_list)
    current_category = findTheCategory(category_list, category_name)
    current_values = findTheValues(current_category, sender)
    current_feedback = findTheFeedback(current_category, sender)
    
    
    if (current_amount == 0 and keys_exists(studentWithErrors, sender)):
        del studentWithErrors[student_name]
    else:
        studentWithErrors[student_name][sender][AMOUNT] = current_amount
        studentWithErrors[student_name][sender][ERRORVALUE] = current_values

    if (current_student != None and current_feedback not in current_student.feedback and current_amount != 0):
        current_student.feedback.append(current_feedback)
    elif (current_amount == 0 and current_feedback in current_student.feedback):
        current_student.feedback.remove(current_feedback)
    
    print(studentWithErrors)

    dpg.split_frame()
    
    
    calculateErrorPoints(current_student, studentWithErrors[student_name], current_amount)
    current_student.grade = checkGrade(current_student.errorpoints, current_student.group)
    dpg.split_frame()
    updateDataWindow(current_student)

def newEntry(studentWithErrors, student_name, sender, amount, error_value):
    return studentWithErrors.setdefault(str(student_name), {}).setdefault(str(sender), {}).setdefault(AMOUNT, amount).setdefault(ERRORVALUE, error_value)

def keys_exists(element, *keys):
    if not isinstance(element, dict):
        raise AttributeError("Dict as first argumement")
    if len(keys) == 0:
        raise AttributeError("keys_exists() expects at least two arguments, one given")
    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

#Caluclate the student errorpoints when mistakeSelected is called
def calculateErrorPoints(current_student, studentFromDict, current_amount):
    errorpoints = 0
    for key, values in studentFromDict.items():
        sAmount, iAmount = str(values[AMOUNT]), values[AMOUNT]
        error_values = values[ERRORVALUE]

        if (current_amount == -1):
            errorpoints = -1
            break
        elif (sAmount not in error_values.keys()):
            errorpoints += error_values["All"]
        else:
            errorpoints += error_values[sAmount]

    current_student.errorpoints = round(errorpoints, 1)
    return

#Checking the student grade based on errorpoints
def checkGrade(errorpoints, group):
    if errorpoints >= 0 and errorpoints < 1:
        grade = MAX_GRADE[group]
    elif errorpoints >= 1 and errorpoints < 2:
        grade = 0 if (group == MAX_GRADE.keys()[0]) else MAX_GRADE[group] - 1
    else:
        grade = 0 
    return grade

def checkErrorValue(studentWithErrors, current_values):

    pass
    
    
    

#Writing graded student to master.json
def writeToJsonFile(sender, app_data, studentWithErrors):    
    try:
        with open(FILENAME, "w", encoding="utf-8") as outfile:
            json.dump(studentWithErrors, outfile, indent=4, ensure_ascii=False)
    except FileNotFoundError as e:
        print("File not found", e)
    
def mistakeSelected(sender, app_data, user_data):
    student_name = dpg.get_value("student_view")
    studentWithErrors = user_data[0]
    student_list = user_data[1]
    error_value = dpg.get_value(sender)
    student = findStudent(student_name, student_list)
    if student_name not in studentWithErrors.keys():
        studentWithErrors[student_name] = {}
        studentWithErrors[student_name][sender] = error_value
    else:
        studentWithErrors[student_name][sender] = error_value
    
    student.errorlist = studentWithErrors
    
    
    

######## READING GRADED STUDENT FROM JSON ########
def readGradedFile():
    try:
        if os.path.isfile(FILENAME):

            with open(FILENAME, "r", encoding="utf-8") as file:
                try:
                    studentWithErrors = nested_defaultdict(json.load(file))
                except:
                    studentWithErrors = nested_defaultdict()
                
    except FileNotFoundError as e:
        print("File not found ", e)
    

    return studentWithErrors




def nested_defaultdict(existing=None, **kwargs):
    if existing == None:
        existing = {}
    if not isinstance(existing, dict):
        return existing
    existing = {key: nested_defaultdict(val) for key, val in existing.items()}
    return defaultdict(nested_defaultdict, existing, **kwargs)
#How to determine whether it is exam or project
def stripFilename(dirname, file):
    print(file)
    

#COMPLETE FUNCTIONS ATM

def read_problem_json(filename):
    errorList, categoryList = [], []
    try:
        with open(filename, "r", encoding="utf-8") as f_json:
            data = json.load(f_json)
            current_category = data["violations"][0]["category"]
            for problem in data["violations"]:
                _id = problem["ID"]
                text = problem["text"]
                values = problem["error_values"]
                feedback = problem["feedback"]
                next_category = problem["category"]
                if (next_category == current_category):
                    errorInfo = ErrorInfo(_id, text, values, feedback)
                    errorList.append(errorInfo)
                else:
                    category = Category(name= current_category, errors=errorList)
                    current_category = next_category
                    categoryList.append(category)
                    errorList = []   
                    
            ##### The last item #####
            category = Category(name = current_category, errors=errorList)
            current_category = next_category
            categoryList.append(category)
            errorList = []            

    except FileNotFoundError as e:
        print("File not found", e)
    
    return categoryList


def findStudent(student_name, student_list) -> StudentInfo:
    return next((x for x in student_list if x.name == student_name), None)

def findTheCategory(category_list, category_name):
    return next((c for c in category_list if c.name == category_name ), None)

def findTheFeedback(category, error_id):
    return next((error.feedback for error in category.errors if error._id == error_id), None)

def findTheValues(category, error_id):
    return next((error.values for error in category.errors if error_id == error_id),0)

def tree():
    return defaultdict(tree)





    


