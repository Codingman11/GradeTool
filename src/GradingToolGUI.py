__version__ = "0.2.5"
__author__ = "JP"

import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
from data import StudentInfo, ErrorInfo, Category
from collections import defaultdict


#Initializing the fonts, filenames, max_grades

FILENAME = {"minimi": "master_minimi.json", "perus": "master_perus.json", "tavoite": "master_tavoite.json"}
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



######## FINDING THE CORRECT DATA DEPENDING ON WHAT WE WANT TO GET  ########
def find_student(student_name, student_list) -> StudentInfo:
    return next((x for x in student_list if x.name == student_name), None)

def find_category(category_list, category_name):
    return next((c for c in category_list if c.name == category_name ), None)

def find_feedback(category, error_id):
    return next((error.feedback for error in category.errors if error._id == error_id), None)

def find_values(category, error_id):
    return next((error.values for error in category.errors if error._id == error_id),0)

def find_error(category, error_id):
    return next((error for error in category.errors if error._id == error_id), None)

def get_student_number(sender, app_data, userdata):
    studentWithErrors, student_list = userdata[0], userdata[1]
    current_student = find_student(dpg.get_value("student_view"), student_list)
    current_student.student_number = app_data
    studentWithErrors[current_student.name]["student_number"] = app_data 

######## Adding the folder files to student  ########

def add_files_in_folder(dirname, studentWithErrors, category_dict, category_list):
    student_list = []
    group = str(dirname).split('/')[-1]
    files = os.listdir(dirname)
    
    
    
    studentWithErrors = correct_errorpoints(studentWithErrors, category_list, group) #Correcting the errorpoints and values
    for file in files:
        student_name = str(file).strip().replace("_", " ")
        category_status = CATEGORY_STATUS.copy()
        if student_name in studentWithErrors:
            data_student = studentWithErrors[student_name]
            category_dict, errorpoints = calculateCategoryPoints(data_student.get(ERROR,{}), category_dict)
            
            student = StudentInfo(name=student_name, group = group, grade=data_student["grade"], errorpoints=data_student["errorpoints"], 
                                  error_list=add_feedbacks_to_student(data_student), moodle_comment=category_status, student_number = data_student["student_number"])
            
        else:
            student = StudentInfo(name=student_name, group = group, grade=MAX_GRADE[group], moodle_comment=category_status, student_number="", error_list={})
        updateCategoryStatus(student, category_dict)
        student_list.append(student)    
    
    return student_list

#Adding the feedback to student error_list. Also indexing each error feedback and check whether it is same as in feedback list. 
    # IF NOT SAME FEEDBACK -> The feedback text from feedback list. 
    # OTHERWISE -> default feedback from its error key. 
        
def add_feedbacks_to_student(data_student):
    
    temp_feedback = {}
    temp_feedback_list = data_student["feedback"]
    for index, (k, v) in enumerate(data_student[ERROR].items()):
        if not k:
            continue
        if temp_feedback_list[index] != v["feedback"]:
            temp_feedback[k] = temp_feedback_list[index]
        else:
            temp_feedback[k] = v["feedback"]

    return temp_feedback

######## Comparing between each error value from master.json to problem_list.json values  ########
def correct_errorpoints(studentWithErrors, category_list, group):
    temp_dict = studentWithErrors.copy()

    for student_name, student_items in temp_dict.items():
        total_points = 0
        for error_id, error_items in student_items[ERROR].items():
            category = find_category(category_list, error_items[CATEGORY])
            error_values = find_values(category, error_id)
            iAmount = error_items[AMOUNT]
            error_value = getTheErrorValue(error_values, iAmount)
            
            if (error_value != error_items[ERRORVALUE]):
                temp_dict[student_name][ERROR][error_id][ERRORVALUE] = error_value
                
            total_points += error_value
            
        temp_dict[student_name]["errorpoints"] = total_points
        temp_dict[student_name]["grade"] = checkGrade(total_points, group)

    return temp_dict

######## When the user select a student from the student view########
def select_student(sender, app_data, user_data):

    studentWithErrors, categoryList, student_list = user_data[0], user_data[1], user_data[2]
    student_name = str(app_data)
    studentObject = find_student(student_name, student_list) 
    updateTable(categoryList, studentWithErrors, student_name)
    
    if (studentObject != None):
        updateDataWindow(studentObject)
        dpg.set_value("student_number", studentObject.student_number)
    
    return 
######## Updating the data window ########
def updateDataWindow(studentObject):
    dpg.set_value("level", studentObject.group)
    dpg.set_value("student_number", studentObject.student_number)
    dpg.set_value("student_grade", str(studentObject.grade))
    dpg.set_value("feedback_input", convertFeedbackToString(studentObject.error_list.values()))
    dpg.set_value("error_points", studentObject.errorpoints)
    
    return
######## Updating the mistakes window ########
def updateTable(categoryList, studentWithErrors, student):
    for category in categoryList:
        for error in category.errors:
            if (student in studentWithErrors.keys() and error._id in studentWithErrors[student][ERROR].keys()):
                dpg.set_value(error._id, studentWithErrors[student][ERROR][error._id][AMOUNT])
            else:
                dpg.set_value(error._id, 0)
    
    return


######## Mistake/Error is selected ########
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

 
    #Indexing the student, error_values, category data
    current_student = find_student(student_name, student_list)

    current_category = find_category(category_list, category_name)
    current_values = find_values(current_category, sender)
    current_feedback = find_feedback(current_category, sender)
    current_value = getTheErrorValue(current_values, current_amount)


    
    if (student_name != None):
        #print(current_amount)
        studentWithErrors[student_name][ERROR][sender][AMOUNT] = current_amount
        studentWithErrors[student_name][ERROR][sender][CATEGORY] = current_category.name
        
        
        if current_amount == 0:
            #Checking the current_amount and checking if it exists
            if keys_exists(studentWithErrors, sender):
                deleteError(studentWithErrors.get(student_name, {}), sender)
                      
        
            if sender in current_student.error_list.keys():
                del current_student.error_list[sender]
            

        elif current_amount > 0 or current_amount == -1:

            studentWithErrors[student_name][ERROR][sender][AMOUNT] = current_amount
            
            
            studentWithErrors[student_name][ERROR][sender][ERRORVALUE] = current_value
            studentWithErrors[student_name][ERROR][sender]["feedback"] = current_feedback
            
            
            if sender in current_student.error_list.keys():
                if (current_student.error_list[sender] != current_feedback):
                    pass
            else:
                current_student.error_list[sender] = current_feedback  
            

    student = studentWithErrors.get(student_name, {})
    category_dict = calculateErrorPoints(current_student, student.get(ERROR, {}), category_dict)
    current_student.grade = checkGrade(current_student.errorpoints, current_student.group)
    
    dpg.split_frame()
    updateDataWindow(current_student)
    
    return
    
#Getting the value from the mistake amount
def getTheErrorValue(current_values, current_amount) -> float:
    sCurrent_amount = str(current_amount)
    if (sCurrent_amount in current_values.keys()):
        
        temp_value = current_values[sCurrent_amount]
    elif current_amount == -1:
        temp_value = current_values["All"]
    else:
        for i in range(current_amount-1, 0, -1):
            if (str(i) in current_values.keys()):
                #print(current_values[str(i)])
                temp_value = current_values[str(i)]
                break
        else:
            temp_value = 0
    
    return temp_value

#Student feedback list contains error ID, 

def hasStudentError(current_student, sender):
    for error in current_student.error_list:
        if error._id == sender:
            return error
        
    return None
    
#Caluclate the student errorpoints when mistakeSelected is called
def calculateErrorPoints(current_student, studentFromDict, category_dict):
    
    

    #temp_category_status = []
    #category_dict = dict((k,0) for k in category_dict)


    if (len(studentFromDict) != 0):
        
        category_dict, errorpoints = calculateCategoryPoints(studentFromDict, category_dict)
        updateCategoryStatus(current_student, category_dict)
        # for key, values in studentFromDict.items():
        #     #print(f'KEY; {key} and values {values}')
        #     errorpoints += float(values[ERRORVALUE])
            
            
        #     for k, v in values.items():
                
        #         if (k == CATEGORY):
        #             category = v
        #         if (k == ERRORVALUE):
        #             error_value = v
          
        #     ready = tuple([category, error_value])
        #     temp_category_status.append(ready)
            
        # if len(temp_category_status) != 0:
        #     for index, category in enumerate(temp_category_status):
        #         category_dict[category[0]] += round(category[1], 1)
        
        
        # for index, (key, values) in enumerate(category_dict.items()):
        #     if values < 1:
        #         current_student.moodle_comment[index] = "OK"
        #     elif 1 <= values < 2:
        #         current_student.moodle_comment[index] = "Kesken"
        #     elif values >= 2:
        #         current_student.moodle_comment[index] = "EiOk"

   
         
    current_student.errorpoints = round(errorpoints, 1)
    return category_dict

######## Calculating the category points after correcting errorpoints from json ########

def calculateCategoryPoints(studentFromDict, category_dict):
    
    temp_category_status = []
    errorpoints = 0.0
    category_dict = dict((k,0) for k in category_dict)
    for key, values in studentFromDict.items():
        errorpoints += float(values[ERRORVALUE])
        for k, v in values.items():
            
            if (k == CATEGORY):
                category = v
            if (k == ERRORVALUE):
                error_value = v
        
        temp_category_with_errorvalue = tuple([category, error_value])
        temp_category_status.append(temp_category_with_errorvalue)
        
    if len(temp_category_status) != 0:
        for index, category in enumerate(temp_category_status):
            category_dict[category[0]] += round(category[1], 1)

    return category_dict, errorpoints

######## Updating each category status to the student ########
def updateCategoryStatus(student, category_dict):
    
    for index, (key, values) in enumerate(category_dict.items()):
        if values < 1:
            student.moodle_comment[index] = "OK"
        elif 1 <= values < 2:
            student.moodle_comment[index] = "Kesken"
        elif values >= 2:
            student.moodle_comment[index] = "EiOk"
    
    return 

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
    pass
    student_list, studentWithErrors = user_data[0], user_data[1]
    current_student = find_student(dpg.get_value("student_view"), student_list)
    texts = dpg.get_value(sender).split("\n")
    
    #print(texts)
    for index, (k, v) in enumerate(current_student.error_list.items()): 
        if (studentWithErrors[current_student.name][ERROR][k] != texts[index]):
            
            # print(index, k, v)
            current_student.error_list[k] = texts[index]
        # for text in texts:
        #     if text == v:
        #         continue
        #     elif text != v:
        #         
                
    #print(current_student.error_list)
        
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
            studentWithErrors[student.name]["feedback"] = list(student.error_list.values())
            print(studentWithErrors[student.name]["feedback"])
        else:
            studentWithErrors[student.name]["grade"] = MAX_GRADE.get(student.group)
            studentWithErrors[student.name]["feedback"] = list(student.error_list)
            
        
        studentWithErrors[student.name]["student_number"] = student.student_number
        studentWithErrors[student.name]["errorpoints"] = student.errorpoints
        
    return
def deleteError(studentWithErrors, remove_key):
    if (isinstance(studentWithErrors, dict)):
        for key in list(studentWithErrors.keys()):
            if (key == remove_key):
                print(key)
                del studentWithErrors[key]
                
            else:
                deleteError(studentWithErrors[key], remove_key)
    
    
    

#Writing graded student to master.json
def writeToJsonFile(sender, app_data, user_data):
    studentWithErrors, student_list, group = user_data[0], user_data[1], user_data[2]    
    checkEmptyKeys(studentWithErrors)
    updateDictBeforeWriting(studentWithErrors, student_list)
    writeCommentFile("comments.txt", student_list)
    try:
        with open(FILENAME[group], "w", encoding="utf-8") as outfile:
            json.dump(studentWithErrors, outfile, indent=4, ensure_ascii=False)
    except FileNotFoundError as e:
        print("File not found", e)

#Reading master.json and returning dict

def checkEmptyKeys(studentWithErrors):
    
    for key in studentWithErrors.copy():
        if len(studentWithErrors[key]) == 0:
            studentWithErrors.pop(key)

    

######## READING GRADED STUDENT FROM JSON ########
def readGradedFile(group):
    studentWithErrors = {}
    try:
        with open(FILENAME[group], "r", encoding="utf-8") as file:
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
                if (len(student.error_list) != 0):
                    feedback_list = list(student.error_list.values())
                    fhandle.writelines('\n'.join(feedback_list))
                    fhandle.write("\n\n")
                
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
                    errorInfo = ErrorInfo(_id, text, values, amount, feedback)
                    errorList.append(errorInfo)
                    
                    
            ##### The last item #####
            category = Category(name = current_category, errors=errorList)
            current_category = next_category
            categoryList.append(category)
            errorList = []            

    except FileNotFoundError as e:
        print("File not found", e)
    #print(category_dict)
    return categoryList, category_dict



    

