__version__ = "0.1.3"
__author__ = "JP"

import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
from typing import Dict, Any
from data import StudentInfo, ErrorInfo, Category, ExamInfo
from tkinter import filedialog, Tk
from collections import defaultdict
from functools import partial


#Initializing the fonts, filenames, max_grades
DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"
FILENAME = "master.json"
ARVOSTELLUT = "Arvostellut.json"
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}
AMOUNT, ERRORVALUE, ERROR, CATEGORY = 'amount', 'value', 'error', 'category'



#TODO 

# Write data to master.json
# Copy the text to clipboard


# Menubar valitse tiedosto

#FIXME
#Fix the function when the user input the value by hand.


CATEGORY_TEXTS = [
                "toiminnallisuus tehtäväksiannon mukaan ja CodeGradesta läpi",
                "tiedostorakenne useita tiedostoja (ei arvioida minimitasolla)",
                "tyyliohjeen mukaiset alkukommentit",
                "ohjelmarakenne pääohjelma ja aliohjelmat",
                "perusoperaatiot tulostus, syöte, valintarakenne, toistorakenne",
                "tiedonvälitys parametrit ja paluuarvot, ei globaaleja muuttujia",
                "tiedostonkäsittely luku ja kirjoittaminen",
                "tietorakenteet tietue/struct, linkitetty lista",
                "dynaaminen muistinhallinta: malloc, free, NULL",
                "virheenkäsittely muistin- ja tiedostonkäsittelyssä",
                "analyysien toteutus",
                "Makefile palautettu ja make tuottaa toimivan ohjelman (ei arvioida minimitasolla)",
            ]

CATEGORY_STATUS = []
for i in range(0,12):
    CATEGORY_STATUS.append("OK")
    



#initialize font 
def initialize_font():
    with dpg.font_registry():
        default_font = dpg.add_font(DEFAULT_FONT, 25)
        hl_font = dpg.add_font(HL_FONT, 15)
        title_font = dpg.add_font(HL_FONT, 22)
    return default_font, hl_font, title_font


#Adding the folder files to student

def add_files_in_folder(dirname, studentWithErrors):
    student_list = []
    

    group = str(dirname).split('/')[-1]
    files = os.listdir(dirname)
    
    for file in files:
        student_name = str(file).strip().replace("_", " ")
        if student_name in studentWithErrors:
            data_student = studentWithErrors[student_name]
            student = StudentInfo(name=student_name, group = group, grade=data_student["grade"], errorpoints=data_student["errorpoints"], feedback=data_student["feedback"], moodle_comment=CATEGORY_STATUS)
        else:
            student = StudentInfo(name=student_name, group = group, grade=MAX_GRADE[group], moodle_comment=CATEGORY_STATUS)
                  

        student_list.append(student)    
    
    return student_list


def select_student(sender, app_data, user_data):

    #previous student
    
    studentWithErrors, categoryList, student_list = user_data[0], user_data[1], user_data[2]
    student_name = str(app_data)
    studentObject = findStudent(student_name, student_list) 
    updateTable(categoryList, studentWithErrors, student_name)
    

    if (studentObject != None):
        updateDataWindow(studentObject)
        print(studentObject.moodle_comment)
    


def updateDataWindow(studentObject):
    dpg.set_value("level", studentObject.group)

    dpg.set_value("student_grade", str(studentObject.grade))
    dpg.set_value("feedback_input", convertFeedbackToString(studentObject.feedback))
    dpg.set_value("error_points", studentObject.errorpoints)
    

def updateTable(categoryList, studentWithErrors, student):
    for category in categoryList:
        for error in category.errors:
            if (student in studentWithErrors.keys() and error._id in studentWithErrors[student][ERROR].keys()):
                dpg.set_value(error._id, studentWithErrors[student][ERROR][error._id][AMOUNT])
            else:
                dpg.set_value(error._id, 0)
    
    
    #Finding the student object from list

    
def mistakeSelected(sender, app_data, user_data):
    
    student_name = dpg.get_value("student_view")
    
    
    #StudentWithErrors is dictionary for updating the students who have errors
    #Getting user_data
    studentWithErrors = user_data[0]
    student_list = user_data[1]
    category_list = user_data[2]
    category_dict = user_data[3]
    #Getting from GUI Data
    category_name = dpg.get_item_parent(dpg.get_item_parent(sender))
    current_amount =  dpg.get_value(sender)
    sCurrent_amount = str(current_amount)
 
    #Indexing the student data and error data
    current_student = findStudent(student_name, student_list)

    current_category = findTheCategory(category_list, category_name)
    current_values = findTheValues(current_category, sender)
    current_feedback = findTheFeedback(current_category, sender)
    
    student = studentWithErrors.get(student_name, {})
 
    studentWithErrors[student_name][ERROR][sender][AMOUNT] = current_amount
    studentWithErrors[student_name][ERROR][sender][CATEGORY] = current_category.name
    if (current_amount == 0 and keys_exists(studentWithErrors, sender)):
        studentWithErrors = deleteError(studentWithErrors.get(student_name, {}), sender)
    
    if (current_amount > 0):
        
        if (sCurrent_amount not in current_values.keys()):
            pass
        
        else:
            studentWithErrors[student_name][ERROR][sender][ERRORVALUE] = current_values[sCurrent_amount]
        studentWithErrors[student_name][ERROR][sender][CATEGORY] = category_name
    if current_amount == -1:
        studentWithErrors[student_name][ERROR][sender][ERRORVALUE] = current_values["All"]
        studentWithErrors[student_name][ERROR][sender][CATEGORY] = category_name


        
        
    
        
    if (current_student != None and current_feedback not in current_student.feedback and current_amount != 0):
        current_student.feedback.append(current_feedback)
    elif (current_amount == 0 and current_feedback in current_student.feedback):
        current_student.feedback.remove(current_feedback)

    #print(studentWithErrors)
    category_dict = calculateErrorPoints(current_student, student.get(ERROR, {}), category_dict)


    
    
    
    current_student.grade = checkGrade(current_student.errorpoints, current_student.group)
    dpg.split_frame()
    updateDataWindow(current_student)

def calculateCategorySum(studentWithErrors, student_list):
    
   
    pass

#Caluclate the student errorpoints when mistakeSelected is called
def calculateErrorPoints(current_student, studentFromDict, category_dict):
    
    errorpoints = 0.0
    
    
    
    print(f'STUDENT: {studentFromDict}')
    for key, values in studentFromDict.items():
        
        errorpoints += float(values[ERRORVALUE])
        category_dict[values[CATEGORY]] = round(errorpoints, 1)
        #print(f'CATEGORY is {category_dict[key]} and CHANGES: {category_dict[values[CATEGORY]]}')
        
    print(f'AFTER: {category_dict}')
    for index, (key, values) in enumerate(category_dict.items()):
        #print(f'INDEX: {index}, KEY: {key} AND VALUES: {values}')
       
        if values < 1:
            current_student.moodle_comment[index] = "OK"
        elif 1 <= values < 2:
            current_student.moodle_comment[index] = "Kesken"
        elif values >= 2:
            current_student.moodle_comment[index] = "EiOk"
        else:
            print("NOT FOUND")
            
    category_dict = dict((k,0) for k in category_dict)
    print(f'CLEARED: {category_dict}')
    current_student.errorpoints = round(errorpoints, 1)
    return category_dict

#Checking the student grade based on errorpoints
def checkGrade(errorpoints, group):
    if errorpoints >= 0 and errorpoints < 1:
        grade = MAX_GRADE[group]
    elif errorpoints >= 1 and errorpoints < 2:
        grade = 0 if (group == list(MAX_GRADE.keys())[0]) else MAX_GRADE.get(group) - 1
    else:
        grade = 0 
    return grade




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


    
def updateDictBeforeWriting(studentWithErrors, student_list):
    
    for student in student_list:
        if student.name in studentWithErrors:
            
            studentWithErrors[student.name]["grade"] = student.grade
            studentWithErrors[student.name]["feedback"] = student.feedback
        else:
            studentWithErrors[student.name]["grade"] = MAX_GRADE.get(student.group)
            studentWithErrors[student.name]["errorpoints"] = student.errorpoints
            studentWithErrors[student.name]["feedback"] = student.feedback
        studentWithErrors[student.name]["errorpoints"] = student.errorpoints
        
    return
def deleteError(studentWithErrors, remove_key):
    print(remove_key)
    if (isinstance(studentWithErrors, dict)):
        for key in list(studentWithErrors.keys()):
            if (key == remove_key):
                studentWithErrors.pop(key)
            else:
                deleteError(studentWithErrors[key], remove_key)
    

#Writing graded student to master.json
def writeToJsonFile(sender, app_data, user_data):
    studentWithErrors, student_list = user_data[0], user_data[1]    
    checkEmptyKeys(studentWithErrors)
    updateDictBeforeWriting(studentWithErrors, student_list)
    try:
        with open(FILENAME, "w", encoding="utf-8") as outfile:
            json.dump(studentWithErrors, outfile, indent=4, ensure_ascii=False)
    except FileNotFoundError as e:
        print("File not found", e)

#Reading master.json and returning dict

def checkEmptyKeys(studentWithErrors):
    
    for key in studentWithErrors.copy():
        if len(studentWithErrors[key]) == 0:
            studentWithErrors.pop(key)
    # if not studentWithErrors: return d
    # _new = studentWithErrors.copy()
    # for key in _new.keys():
    #     if not _new.get(key):
    #         del studentWithErrors[key]
    #     elif isinstance(_new[key], dict):
    #         checkEmptyKeys(_new[key])
    # return _new
    

######## READING GRADED STUDENT FROM JSON ########
def readGradedFile():

    studentWithErrors = {}

    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                studentWithErrors = nested_defaultdict(json.load(file))
            except:
                print("JSON LOAD FAILED")
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


#Update the feedback window
def updateText(sender, app_data, user_data):
    if (convertFeedbackToString(user_data) != dpg.get_value(sender)):
        user_data.clear()
        user_data.append(dpg.get_value(sender).split("\n"))

def convertFeedbackToString(feedbacks):
    text= "\n".join(map(str,feedbacks))
    return text
#COMPLETE FUNCTIONS ATM

def read_problem_json(filename):
    errorList, categoryList, category_dict = [], [], defaultdict(float)
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
                    category_dict[current_category] = 0
                   
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
    print(category_dict)
    return categoryList, category_dict


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





    


