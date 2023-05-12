__version__ = "0.3.2"
__author__ = "JP"

import dearpygui.dearpygui as dpg
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
import GradingToolGUI as gui
import json


#   V0.1.0 GUI windows added, data structure for student, errors and category added
#   V0.1.1 File director added and sorting the files
#   V0.1.2 Mistakes from problem_list.json added to error window and a functionality between students and selecting mistake 
#   V0.1.3 Data Window added and Feedback window added.
#   V0.1.4 Feedback window added and student's feedback based on mistakes are added. 
#   V0.2.0 The gradetool is working expect a few bugs
#   V0.2.1 Each category's first problem didnt show up in the program --> FIXED
#   V0.3.0 Fixing the error_value indexing and feedback is added. The feedback can be modified.
#   V0.3.1 Comments.txt for each submission level. If problem_list.json is updated --> correcting the errorpoints, 
#          feedback and category. Also indexing category status updated.
#   V0.3.2 Added for checking whether it is first submission, second submission (Korjauspalautus). Also settings.json for Finnish and Englinsh langauges. 
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}

#You can edit this based on your screen size and adjust the font size
DEFAULT_WIDTH = 1200
DEFAULT_SIZE = 28
#DEFAULT_FONT, NORMAL_FONT, TITLE_FONT = gui.initialize_font()
DEFAULT_FONT = Path(__file__).parents[1] / "assets/Dosis-Medium.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"
SETTINGS_PATH = Path(__file__).parents[1] / "utils/settings.json"

def load_settings():
    with open(SETTINGS_PATH, "r", encoding="utf-8") as s_json:
        return json.load(s_json)

SETTINGS = load_settings()
DATA = SETTINGS["lang"]["FIN"] 
    



def main() -> None:

    ######## INITIALIZING SETTINGS DATA ########
    
    
    ######## ASKING DIRECTORY NAME ########
    root = tk.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory()
   
    group = str(dirname).split("/")[-1]
    ######## INITIALIZING DATA  ########
    categoryList, category_dict = gui.read_problem_json("Problem_list_C.json")
    studentWithErrors = gui.readGradedFile(group)
    
    student_list = gui.add_files_in_folder(dirname, studentWithErrors, category_dict, categoryList)
    students = tuple(student.name for student in student_list)
    
    
    ######## INITIALIZING DPG LAYOUT  ########
    dpg.create_context()
    dpg.configure_app(
        docking=True, docking_space=True, init_file="custom_layout.ini"
    )
    dpg.create_viewport(title="GradeTool")
    
    student_window = dpg.generate_uuid()
    category_window = dpg.generate_uuid()
    button_window = dpg.generate_uuid()
    data_window = dpg.generate_uuid()

    #IMPORTING THE FONT FAMILY
    with dpg.font_registry():
        default_font = dpg.add_font(DEFAULT_FONT, DEFAULT_SIZE)
        hl_font = dpg.add_font(HL_FONT, 17)
        title_font = dpg.add_font(HL_FONT, 22)
    
    ######## STUDENT VIEW ########
    with dpg.window(label=DATA["students"], tag=student_window):
        dpg.add_button(label=DATA["save"], width=-1, callback=gui.writeToJsonFile, user_data=[studentWithErrors, student_list, group])
        dpg.add_separator()
        with dpg.group(horizontal_spacing=2, width=-1):
            dpg.add_listbox(students, num_items=25, tag="student_view", callback=gui.select_student, user_data=[studentWithErrors, categoryList, student_list])
        
    ######## ERROR VIEW ########
    with dpg.window(label=DATA["category"], tag=category_window, no_scrollbar=False) as cWindow:
        with dpg.group(tag="error_view"):
            for category in categoryList:
                with dpg.tree_node(label=category.name, user_data=category.name):
                        with dpg.table(
                            header_row=True,
                            policy=dpg.mvTable_SizingStretchProp,
                            resizable=True,
                            borders_innerV=True,
                            borders_outerV=True,
                            borders_outerH=True,
                            borders_innerH=True,
                            tag=category.name
                        ):
                            dpg.add_table_column(label=DATA["errors"], width_stretch=True)
                            dpg.add_table_column(label=DATA["amount"], width_fixed=True)
                            
                            for error in category.errors:
                                with dpg.table_row():
                                    dpg.add_text(error.text, tag=error.text)
                                    dpg.add_input_int(min_value=-1, min_clamped=True, default_value=0, width=-1,tag=error._id, callback=gui.mistakeSelected,  user_data=[studentWithErrors, student_list, categoryList, category_dict])
                      
    ######## COMMENT VIEW ########
    with dpg.window(label=DATA["feedbacks"], tag=button_window) as bWindow:
        dpg.add_input_text(multiline=True, height=-1, label="", width=-1 ,tag="feedback_input", callback=gui.updateText, user_data=[student_list, studentWithErrors])
        
    ######## STUDENT DATA VIEW ########
    with dpg.window(label=DATA["evaluation"], tag=data_window) as dWindow:
        with dpg.group(horizontal=True, horizontal_spacing=10):
            dpg.add_text(DATA["level"] + ": ", indent=0.1)
            dpg.add_text(student_list[0].group, tag="level")
            dpg.add_text(DATA["grade"] + ": ")
            dpg.add_text(MAX_GRADE[student_list[0].group], tag="student_grade")
            dpg.add_text(DATA["errorpoints"] + ": ")
            dpg.add_text("0", tag="error_points")
        with dpg.group(horizontal=True):
            dpg.add_text(DATA["student_number"] + ": ")
            dpg.add_input_text(tag="student_number", width=-1, callback=gui.get_student_number, user_data=[studentWithErrors, student_list])
        
    ######## MENUBAR ########
    with dpg.viewport_menu_bar():
        with dpg.menu(label=DATA["file"]):
            dpg.add_menu_item(
                label="Save layout",
                callback=lambda: dpg.save_init_file("custom_layout.ini"),
            ),
            dpg.add_menu_item(label="Save graded to file", callback=gui.writeToJsonFile, user_data=studentWithErrors)
        with dpg.menu(label="Settings"):
            with dpg.menu(label=DATA["change_language"]):
                
                dpg.add_menu_item(label=DATA["language"][0])
                dpg.add_menu_item(label=DATA["language"][1])
  

    ######## ITEM REGISTRIES ########
    with dpg.item_handler_registry(tag="student handler") as handler:
        dpg.add_item_clicked_handler(callback=gui.select_student, user_data=[studentWithErrors, categoryList, student_list])
    
    with dpg.item_handler_registry(tag="mistake handler") as mHandler:
        dpg.add_item_clicked_handler(callback=gui.mistakeSelected, user_data=[studentWithErrors, student_list, categoryList, category_dict])        
        
    dpg.bind_item_handler_registry("student_view", "student handler")
    dpg.bind_item_handler_registry("error_view", "error handler")
    
    dpg.bind_font(default_font)

    ######## STARTING GUI ########
    dpg.setup_dearpygui()
    dpg.set_viewport_pos([0,0])
    
    if len(studentWithErrors) != 0:
        current_student_name = dpg.get_value("student_view")
        current_student = gui.find_student(current_student_name, student_list)
        gui.updateDataWindow(current_student)
        gui.calculateErrorPoints(current_student, studentWithErrors.get(current_student_name, {}).get('error', {}), category_dict)
        gui.updateTable(categoryList, studentWithErrors, current_student.name)
        
    dpg.set_viewport_width(DEFAULT_WIDTH)
    dpg.show_viewport()        
    dpg.start_dearpygui()    
    # while dpg.is_dearpygui_running():
    #     jobs = dpg.get_callback_queue()
    #     dpg.run_callbacks(jobs)
    #     dpg.render_dearpygui_frame()
    dpg.destroy_context()

if __name__ == "__main__":
    main()



    
    