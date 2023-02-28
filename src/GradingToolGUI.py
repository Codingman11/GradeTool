import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
from data import StudentInfo, ErrorInfo, Category, ExamInfo


DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"

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

    studentWithErrors = user_data[0]
    categoryList = user_data[1]
    student = str(app_data)
    
    # found = keys_exits(studentWithErrors, student)
    # print(found)
    # for category in categoryList:
    #     for error in category.errors:
    #         if (found):
    #             dpg.set_value(error.error_id, studentWithErrors[student][error.error_id])
    #         else:
    #             dpg.set_value(error.error_id, 0)
    if (student not in studentWithErrors.keys()):
        for category in categoryList:
            for error in category.errors:
                dpg.set_value(error.error_id, 0)
    else:
        for category in categoryList:
            for error in category.errors:
                if error.error_id in studentWithErrors[student].keys():
                    dpg.set_value(error.error_id, studentWithErrors[student][error.error_id])
    #print(f"sender: {sender}, app_data: {app_data}, user data: {user_data}")    
    #print(f"sender: {sender}, app_data: {app_data}")
    
    
    
    #print(f"Sender: {sender}, app_data: {app_data}")
    
    #print(f"Errors: {studentErrors} and \n categoryList {categoryList}")

def keys_exits(dictionary, keys):
    nested_dict = dictionary
    for key in keys:
        try:
            nested_dict = nested_dict[key]
        except KeyError:
            return False
    return True
    
def mistakeSelected(sender, app_data, studentWithErrors):
    student = dpg.get_value("student_view")
    error_value = dpg.get_value(sender)
    if student not in studentWithErrors.keys():
        studentWithErrors[student] = {}
        studentWithErrors[student][sender] = error_value
    else:
        studentWithErrors[student][sender] = error_value
    print(studentWithErrors)

def clearTableValues(sender, app_data, categoryList):
    for category in categoryList:
        for error in category.errors:
            dpg.set_value(error.error_id, 2)
            

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

                next_category = problem["category"]
                if (next_category == current_category):
                    errorInfo = ErrorInfo()
                    errorInfo.error_id = problem["ID"]
                    errorInfo.text = problem["text"]
                    errorInfo.values = problem["error_values"]
                    errorInfo.feedback = problem["feedback"]
                    errorList.append(errorInfo)
                else:
    
                    category = Category(name= current_category, errors=errorList)
                    current_category = next_category
                    categoryList.append(category)
                    # for category in categoryList:
                    #     print(category)
                    errorList = []   
                    
        
           
            category = Category(name = current_category, errors=errorList)
            current_category = next_category
            categoryList.append(category)
            errorList = []            

    except FileNotFoundError as e:
        print("File not found", e)

    return categoryList






    


