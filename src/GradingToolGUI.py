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

exam = True

if (exam == False):
    student = StudentInfo("Pekka", "32322", "Minimi", ["TEsti", "Testi"])
    print(student.name, student.student_number, student.group, student.feedback)
else:
    student = ExamInfo("Pekka", "23232", "F", ["eadf", "sadf"], "T2")
    print(student.name, student.student_number, student.group, student.feedback, student.exam_level)

def add_files_in_folder(dirname):
    student_list = []
    files = os.listdir(dirname)

    
    
        


#How to determine whether it is exam or project
def stripFilename(dirname, file):
    print(file)






    


