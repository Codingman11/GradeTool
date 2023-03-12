import dearpygui.dearpygui as dpg
import GradingToolGUI as gui
import dearpygui.demo as demo
import tkinter as tk
from tkinter import filedialog
from os import path, getcwd
import pathlib

#   V0.1.0 GUI windows added, data structure for student, errors and category added
#   V0.1.1 File director added and sorting the files
#   V0.1.2 Mistakes from problem_list.json added to error window and a functionality between students and selecting mistake 
#   V0.1.3 Data Window added and Feedback window added.
#   V0.1.4 writing graded data to JSON file added. 
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}
#DEFAULT_FONT, NORMAL_FONT, TITLE_FONT = gui.initialize_font()

def main() -> None:

    ######## ASKING DIRECTORY NAME ########
    root = tk.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory()
    

    ######## INITIALIZING DATA AND DPG ########
    categoryList = gui.read_problem_json("Problem_list.json")
    gui.read_json_file()
    #print(category)
    studentWithErrors = gui.readGradedFile()
    student_list = gui.add_files_in_folder(dirname)
    students = tuple(student.name for student in student_list)
    
    dpg.create_context()
    dpg.configure_app(
        docking=True, docking_space=True, init_file="custom_layout.ini"
    )
<<<<<<< Updated upstream
    dpg.create_viewport(title="GradeTool")
=======
    dpg.create_viewport(title="GradeTool", width=1080)
>>>>>>> Stashed changes
    
    student_window = dpg.generate_uuid()
    category_window = dpg.generate_uuid()
    button_window = dpg.generate_uuid()
    data_window = dpg.generate_uuid()

<<<<<<< Updated upstream
=======
    
>>>>>>> Stashed changes
    ######## STUDENT VIEW ########
    with dpg.window(label="Opiskelijat", tag=student_window):
        dpg.add_button(label="SAVE", width=-1, callback=gui.writeToJsonFile, user_data=studentWithErrors)
        dpg.add_separator()
        with dpg.group(horizontal_spacing=2, width=-1):
            dpg.add_listbox(students, num_items=25, tag="student_view", callback=gui.select_student, user_data=[studentWithErrors, categoryList, student_list])
        
    ######## ERROR VIEW ########
    with dpg.window(label="Virheet", tag=category_window, no_scrollbar=False) as cWindow:
        with dpg.group(tag="error_view"):
            for category in categoryList:
                with dpg.tree_node(label=category.name):
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
                            dpg.add_table_column(label="Virheet", width_stretch=True)
                            dpg.add_table_column(label="Lkm", width_fixed=True)
                            
                            for error in category.errors:
                                with dpg.table_row():
                                    dpg.add_text(error.text, tag=error.text)
<<<<<<< Updated upstream
                                    dpg.add_input_int(min_value=-1, min_clamped=True, default_value=0, width=100, tag=error._id, callback=gui.mistakeSelected,  user_data=[studentWithErrors, student_list])
                                    
=======
                                    dpg.add_input_int(min_value=-1, min_clamped=True, default_value=0, width=80, tag=error._id, callback=gui.mistakeSelected,  user_data=[studentWithErrors, student_list, categoryList])
                      
>>>>>>> Stashed changes
    ######## COMMENT VIEW ########
    with dpg.window(label="Feedback", tag=button_window) as bWindow:
        dpg.add_input_text(multiline=True, height=-1, width=-1)

    ######## STUDENT DATA VIEW ########
    with dpg.window(label="Arviointitaulukko", tag=data_window) as dWindow:
        # with dpg.group(horizontal=True):
        #     dpg.add_text("Opiskelijanumero: ")
        #     dpg.add_input_text(tag="student_number", width=200)
        with dpg.group(horizontal=True):
            dpg.add_text("Taso: ", indent=0.1)
            dpg.add_text(student_list[0].group, tag="level")
            dpg.add_text("Arvosana: ")
            dpg.add_text(MAX_GRADE[student_list[0].group], tag="student_grade")
            dpg.add_text("Virhepisteet: ")
            dpg.add_text("0", tag="error_points")

           
    ######## MENUBAR ########
    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(
                label="Save layout",
                callback=lambda: dpg.save_init_file("custom_layout.ini"),
            ),
            dpg.add_menu_item(label="Save graded to file", callback=gui.writeToJsonFile, user_data=studentWithErrors)


    ######## ITEM REGISTRIES ########
    with dpg.item_handler_registry(tag="student handler") as handler:
        dpg.add_item_clicked_handler(callback=gui.select_student, user_data=[studentWithErrors, categoryList, student_list])

    with dpg.item_handler_registry(tag="mistake handler") as mHandler:
        dpg.add_item_clicked_handler(callback=gui.mistakeSelected, user_data=[studentWithErrors, student_list])        
    
    dpg.bind_item_handler_registry("student_view", "student handler")
    dpg.bind_item_handler_registry("error_view", "error handler")
   

    ######## STARTING GUI ########
    #dpg.show_item_registry()
    dpg.setup_dearpygui()
    dpg.set_viewport_pos([0,0])
    dpg.show_viewport()        
    dpg.start_dearpygui()    
    # while dpg.is_dearpygui_running():
    #     jobs = dpg.get_callback_queue()
    #     dpg.run_callbacks(jobs)
    #     dpg.render_dearpygui_frame()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
