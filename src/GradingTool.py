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




def main() -> None:

    # Initializing all data structures

    root = tk.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory()
    
    categoryList = gui.read_problem_json("Problem_list.json")

    student_list = gui.add_files_in_folder(dirname)
    
    studentWithErrors = {}
 
    students = tuple(student.name for student in student_list)
    
    indent = 20
    dpg.create_context()

    dpg.configure_app(
        docking=True, docking_space=True, load_init_file="custom_layout.ini"
    )
    dpg.create_viewport(title="GradeTool")
    default_font, hl_font, title_font = gui.initialize_font()

    student_window = dpg.generate_uuid()
    category_window = dpg.generate_uuid()
    button_window = dpg.generate_uuid()
    data_window = dpg.generate_uuid()


    #dpg.add_file_dialog(directory_selector=True, show=True, tag="file_dialoag_id", callback=gui.add_files_in_folder)
    with dpg.window(label="Opiskelijat", tag=student_window):

        with dpg.group(width=400):
            dpg.add_listbox(students, num_items=25, tag="student_view", callback=gui.select_student, user_data=[studentWithErrors, categoryList])
        
    with dpg.window(label="Virheet", tag=category_window) as cWindow:

      
        with dpg.group(tag="error_view"):
            for category in categoryList:
                with dpg.tree_node(label=category.name):
                        with dpg.table(
                            header_row=True,
                            policy=dpg.mvTable_SizingStretchSame,
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
                                    dpg.add_input_int(min_value=-1, min_clamped=True, default_value=0, width=100, tag=error.error_id, callback=gui.mistakeSelected, user_data=studentWithErrors)

    with dpg.window(label="Toiminnot", tag=button_window) as bWindow:
        pass

    with dpg.window(label="Arviointitaulukko", tag=data_window) as dWindow:
        pass

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(
                label="Save layout",
                callback=lambda: dpg.save_init_file("custom_layout.ini"),
            )

    with dpg.item_handler_registry(tag="student handler") as handler:
        dpg.add_item_clicked_handler(callback=gui.select_student, user_data=[studentWithErrors, categoryList])

   
    with dpg.item_handler_registry(tag="mistake handler") as mHandler:
        dpg.add_item_clicked_handler(callback=gui.mistakeSelected, user_data=studentWithErrors)
    #TODO How to reset the error window after clicking student
        
    dpg.bind_item_handler_registry("student_view", "student handler")
    dpg.bind_item_handler_registry("error_view", "error handler")
    categories = dpg.get_item_children("error_view")[1]
    print(dpg.get_item_children(categories[0]))


    dpg.show_item_registry()
    dpg.setup_dearpygui()

    dpg.show_viewport()
    current = ""
    

    
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        
        


    dpg.destroy_context()

if __name__ == "__main__":
    main()
