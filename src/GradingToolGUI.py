__version__ = "0.2.0"
__author__ = "JP"

import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
from typing import Dict, Any
from data import StudentInfo, ErrorInfo, Category, ExamInfo
from tkinter import filedialog, Tk
from collections import defaultdict, OrderedDict
from functools import partial
import pprint

#Initializing the fonts, filenames, max_grades
DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"
FILENAME = "master.json"
ARVOSTELLUT = "Arvostellut.json"
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}
AMOUNT, ERRORVALUE, ERROR, CATEGORY = 'amount', 'value', 'error', 'category'
START_STUDENT_TEXT = "--opiskelija--"


#TODO 

# Write data to master.json
# Copy the text to clipboard


# Menubar valitse tiedosto

#FIXME
#Fix the function when the user input the value by hand.


CATEGORY_TEXTS = [
                "Toiminnallisuus tehtäväksiannon mukaan ja CodeGradesta läpi",
                "Tiedostorakenne useita tiedostoja (ei arvioida minimitasolla)",
                "Tyyliohjeen mukaiset alkukommentit",
                "Ohjelmarakenne pääohjelma ja aliohjelmat",
                "Perusoperaatiot tulostus, syöte, valintarakenne, toistorakenne",
                "Tiedonvälitys parametrit ja paluuarvot, ei globaaleja muuttujia",
                "Tiedostonkäsittely luku ja kirjoittaminen",
                "Tietorakenteet tietue/struct, linkitetty lista",
                "Dynaaminen muistinhallinta: malloc, free, NULL",
                "Virheenkäsittely muistin- ja tiedostonkäsittelyssä",
                "Analyysien toteutus",
                "Makefile palautettu ja make tuottaa toimivan ohjelman (ei arvioida minimitasolla)",
            ]

CATEGORY_STATUS = ["Ok"]*len(CATEGORY_TEXTS)


FAIL_LIMIT = {"minimi": 1, "perus": 2, "tavoite": 2}
PASS_TEXT = {"PASS": "Hyväksytty", "FAIL": "Korjattava"}
SUBMISSION = "1"
SUBMISSION_LEVEL = {"minimi": "minimitaso", "perus": "perustaso", "tavoite": "tavoitetaso"}

#initialize font 
def initialize_font():
    with dpg.font_registry():
        default_font = dpg.add_font(DEFAULT_FONT, 25)
        hl_font = dpg.add_font(HL_FONT, 15)
        title_font = dpg.add_font(HL_FONT, 22)
    return default_font, hl_font, title_font


#Adding the folder files to student

def add_files_in_folder(dirname, studentWithErrors, category_dict, category_list):
    student_list = []
    

    group = str(dirname).split('/')[-1]
    files = os.listdir(dirname)
    
    for file in files:
        temp_error_list = []
        student_name = str(file).strip().replace("_", " ")
        category_status = CATEGORY_STATUS.copy()
        if student_name in studentWithErrors:
            data_student = studentWithErrors[student_name]
            for k, v in data_student[ERROR].items():
                temp_error = ErrorInfo(_id = k, text = "",  values = v[ERRORVALUE], amount = v[AMOUNT], feedback= v["feedback"])
                temp_error_list.append(temp_error)
            student = StudentInfo(name=student_name, group = group, grade=data_student["grade"], errorpoints=data_student["errorpoints"], 
                                  error_list=temp_error_list, moodle_comment=category_status, student_number = data_student["student_number"])
            calculateErrorPoints(student, data_student.get(ERROR, {}), category_dict)

        else:
            student = StudentInfo(name=student_name, group = group, grade=MAX_GRADE[group], moodle_comment=category_status, student_number="", error_list=[])
                  
        
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
        
        dpg.set_value("student_number", studentObject.student_number)
    


def updateDataWindow(studentObject):
    dpg.set_value("level", studentObject.group)
    dpg.set_value("student_number", studentObject.student_number)
    dpg.set_value("student_grade", str(studentObject.grade))
    for errors in studentObject.error_list:
        print(errors.feedback)
    dpg.set_value("feedback_input", convertFeedbackToString([errors.feedback for errors in studentObject.error_list]))
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
    current_error = findTheError(current_category, sender)
    
    print(current_category)
    
    if (student_name != None):
        studentWithErrors[student_name][ERROR][sender][AMOUNT] = current_amount
        
        if (temp_error := hasStudentError(current_student, sender)) == None:
                temp_error = ErrorInfo(_id = sender, text = app_data,  values = current_values[sCurrent_amount], amount = current_amount, feedback=current_feedback)
                current_student.error_list.append(temp_error)
        else:
            temp_error.amount = current_amount
            if sCurrent_amount in current_values.keys():
                temp_error.values = current_values[sCurrent_amount] 
            elif current_amount == -1:
                temp_error.values = current_values["All"]
            else:
                for i in range(current_amount-1, 0, -1):
                    if str(i) in current_values.keys():
                        temp_error.values = current_values[str(i)]
                        break
                else:
                    temp_error.values = 0
            temp_error.feedback = current_feedback
        
    #Checking the current_amount and checking if it exists
    if (current_amount == 0 and keys_exists(studentWithErrors, sender)):
        studentWithErrors = deleteError(studentWithErrors.get(student_name, {}), sender)
    
    if (current_amount > 0):
        
        
        
        if (sCurrent_amount not in current_values.keys()):
            pass
        else:
            studentWithErrors[student_name][ERROR][sender][ERRORVALUE] = current_values[sCurrent_amount]
            
        
        #studentWithErrors[student_name][ERROR][sender][CATEGORY] = category_name
    if current_amount == -1:
        studentWithErrors[student_name][ERROR][sender][ERRORVALUE] = current_values["All"]
        current_error.amount = current_values[sCurrent_amount]
        

    studentWithErrors[student_name][ERROR][sender][CATEGORY] = current_category.name
        
    
    # TODO CHANGE THE .feedback to better name
    # if (current_student != None and current_error not in current_student.error_list and current_amount != 0):
    #     studentWithErrors[student_name][ERROR][sender]["feedback"] = current_feedback

    #     print(f'ERROR: ', current_error)
    #     current_student.error_list.append(current_error)
    #     print(f'ErrorInfo in the list: {current_student.error_list}')
    #     print(studentWithErrors[student_name])
    if (current_amount == 0 and current_error in current_student.error_list):
        current_student.error_list.remove(current_feedback)

    print("CURRENT STUDENT'S ERRORLIST: ", current_student.error_list)

    student = studentWithErrors.get(student_name, {})
    category_dict = calculateErrorPoints(current_student, student.get(ERROR, {}), category_dict)

    current_student.grade = checkGrade(current_student.errorpoints, current_student.group)
    dpg.split_frame()
    updateDataWindow(current_student)
    
#Student feedback list contains error ID, 

def hasStudentError(current_student, sender):
    for error in current_student.error_list:
        if error._id == sender:
            return error
        
    return None
    
#Caluclate the student errorpoints when mistakeSelected is called
def calculateErrorPoints(current_student, studentFromDict, category_dict):
    
    errorpoints = 0.0
    category_dict1 = OrderedDict(sorted(studentFromDict.items(), key=lambda item: item[1][CATEGORY])) 

    testi = []
    category_dict = dict((k,0) for k in category_dict)

   

    for key, values in studentFromDict.items():
        errorpoints += float(values[ERRORVALUE])
        
        for k, v in values.items():
            if (k == CATEGORY):
                category = v
            if (k == ERRORVALUE):
                error_value = v
        ready = tuple([category, error_value])
        testi.append(ready)
        
    if len(testi) != 0:
        for index, category in enumerate(testi):
            category_dict[category[0]] += round(category[1], 1)
      
    
    for index, (key, values) in enumerate(category_dict.items()):
        if values < 1:
            current_student.moodle_comment[index] = "OK"
        elif 1 <= values < 2:
            current_student.moodle_comment[index] = "Kesken"
        elif values >= 2:
            current_student.moodle_comment[index] = "EiOk"

   
         
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


#Update the feedback window when the user write something in feedback window
def updateText(sender, app_data, user_data):
    student_list, studentWithErrors = user_data[0], user_data[1]
    current_student = findStudent(dpg.get_value("student_view"), student_list)
    texts = dpg.get_value(sender).split("\n")
    
    
    # for key, values in studentWithErrors[current_student.name][ERROR].items():
    #     texts.append(f'{key}: {values["feedback"]}\n')
    #     print(texts)
    for index, feedback in enumerate(current_student.error_list):
        if texts[index] != feedback:
            current_student.error_list[index] = texts[index]
    if (convertFeedbackToString(texts) != dpg.get_value(sender)):
        texts.clear()
        texts.append(dpg.get_value(sender).split("\n"))


def convertFeedbackToString(feedbacks):
    text= "\n".join(map(str,feedbacks))
    return text


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
            #studentWithErrors[student.name]["feedback"] = student.errorlist
        else:
            studentWithErrors[student.name]["grade"] = MAX_GRADE.get(student.group)
            studentWithErrors[student.name]["errorpoints"] = student.errorpoints
            #studentWithErrors[student.name]["feedback"] = student.errorlist
            
        
        studentWithErrors[student.name]["student_number"] = student.student_number
        studentWithErrors[student.name]["errorpoints"] = student.errorpoints
        
    return
def deleteError(studentWithErrors, remove_key):
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
    writeCommentFile("comments.txt", student_list)
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
        studentWithErrors = nested_defaultdict()
    
    
        
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

##write generated feedback to .txt file and ready for validating before importing to Moodle
def writeCommentFile(filename, student_list):  
    try:
        with open(filename, "w", encoding="UTF-8") as fhandle:
            for student in student_list:
                fhandle.write(f'{START_STUDENT_TEXT}, {student.name}, {student.student_number}, {student.grade}:\n')
                if (student.errorpoints >= FAIL_LIMIT[student.group]):
                    fhandle.write(f'Harjoitustyön {SUBMISSION_LEVEL[student.group]} palautus {SUBMISSION} on {PASS_TEXT["FAIL"]}.\n')
                else:
                    fhandle.write(f'Harjoitustyön {SUBMISSION_LEVEL[student.group]} palautus {SUBMISSION} on {PASS_TEXT["PASS"]}.\n')
                texts = list(map(': '.join, zip(CATEGORY_TEXTS, student.moodle_comment)))
                fhandle.writelines('\n'.join(texts))
                fhandle.write("\n\n")
                # if (len(student.feedback) != 0):
                #     fhandle.writelines('\n'.join(student.feedback))
                #     fhandle.write("\n\n")
                
    except OSError as err:
        print(f"Error to open file '{filename}':\n{err}")


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
                amount = 0
                feedback = problem["feedback"]
            
                next_category = problem["category"]
                if (next_category == current_category):
                    errorInfo = ErrorInfo(_id, text, values, amount, feedback)
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
    #print(category_dict)
    return categoryList, category_dict


def findStudent(student_name, student_list) -> StudentInfo:
    return next((x for x in student_list if x.name == student_name), None)

def findTheCategory(category_list, category_name):
    return next((c for c in category_list if c.name == category_name ), None)

def findTheFeedback(category, error_id):
    return next((error.feedback for error in category.errors if error._id == error_id), None)

def findTheValues(category, error_id):
    return next((error.values for error in category.errors if error_id == error_id),0)

def findTheError(category, error_id):
    return next((error for error in category.errors if error_id == error_id), None)

def get_student_number(sender, app_data, userdata):
    studentWithErrors, student_list = userdata[0], userdata[1]
    current_student = findStudent(dpg.get_value("student_view"), student_list)
    current_student.student_number = app_data
    studentWithErrors[current_student.name]["student_number"] = app_data 
    
def tree():
    return defaultdict(tree)





    


