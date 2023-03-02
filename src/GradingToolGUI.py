import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
from data import StudentInfo, ErrorInfo, Category, ExamInfo
import itertools

DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"
FILENAME = "master.json"
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}

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



# if (exam == False):
#     student = StudentInfo("Pekka", "32322", "Minimi", ["TEsti", "Testi"])
#     print(student.name, student.student_number, student.group, student.feedback)
# else:
    # student = ExamInfo("Pekka", "23232", "F", ["eadf", "sadf"], "T2")
    # print(student.name, student.student_number, student.group, student.feedback, student.exam_level)



#Adding the folder files to student
def add_files_in_folder_default(sender, app_data):
    student_list = []
    files = os.listdir(app_data["current_path"])

    for file in files:
        print(file)


def add_files_in_folder(dirname):
    student_list = []
    
    #TODO need to check whether it has sub folder or no
    group = str(dirname).split('/')[-1]
    files = os.listdir(dirname)

    for file in files:
        student_name = str(file).strip().replace("_", " ")
        student = StudentInfo(name=student_name, group = group)
        student_list.append(student)
        
    return student_list
# def callback(sender, app_data):
#     print("sender: ", sender)
#     print("app_data: ", app_data)

def select_student(sender, app_data, user_data):

    studentWithErrors, categoryList, student_list = user_data[0], user_data[1], user_data[2]
    student_name = str(app_data)
    studentObject = findStudent(student_name, student_list) 
    updateTable(categoryList, studentWithErrors, student_name)
    
    if (studentObject != None):
        updateDataWindow(studentObject)
    
def findStudent(student_name, student_list) -> StudentInfo:
    return next((x for x in student_list if x.name == student_name), None)

def updateDataWindow(studentObject):
    dpg.set_value("level", studentObject.group)
    dpg.set_value("student_grade", str(MAX_GRADE[studentObject.group]))
    
def updateTable(categoryList, studentWithErrors, student):
    for category in categoryList:
        for error in category.errors:
            if (student in studentWithErrors.keys() and error._id in studentWithErrors[student].keys()):
                dpg.set_value(error._id, studentWithErrors[student][error._id])
            else:
                dpg.set_value(error._id, 0)
    
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
    
    #Finding the student object from list

def readJsonFile(studentWithErrors):
    try:
        if os.path.isfile(FILENAME):

            with open(FILENAME, "r", encoding="utf-8") as file:
                if (len(file) != 0):
                    studentWithErrors = json.load(file)
                else:
                    pass
    except FileNotFoundError as e:
        print("File not found ", e)
    


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






    


