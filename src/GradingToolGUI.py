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



def add_files_in_folder(dirname):
    student_list = []
    files = os.listdir(dirname)


    
def read_problem_json(filename):
    errorList = []
    categoryList = []
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
                    category = Category(name = current_category, errors=errorList)
                    current_category = next_category
                    categoryList.append(category)
                    errorList.clear()   
                    
                    
            category = Category(name = current_category, errors= errorList)
            current_category = next_category
            categoryList.append(category)
            errorList.clear()
            

    except FileNotFoundError as e:
        print("File not found", e)



    return categoryList


def addCategoryList(categoryList, errorList, current_category) -> list:
    category = Category()
    category.name = current_category
    category.errors = errorList
    categoryList.append(category)
    errorList.clear()
    
    return categoryList

#How to determine whether it is exam or project
def stripFilename(dirname, file):
    print(file)






    


