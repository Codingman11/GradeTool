__version__ = "0.1.3"
__author__ = "JP"

import dearpygui.dearpygui as dpg
import GradingToolGUI as gui
import tkinter as tk
from tkinter import filedialog


#   V0.1.0 GUI windows added, data structure for student, errors and category added
#   V0.1.1 File director added and sorting the files
#   V0.1.2 Mistakes from problem_list.json added to error window and a functionality between students and selecting mistake 
#   V0.1.3 Data Window added and Feedback window added.
#   V0.1.4 Feedback window added and student's feedback based on mistakes are added. 
MAX_GRADE = {"minimi": 1, "perus": 3, "tavoite": 5}
CATEGORY_TEXTS = [
                "toiminnallisuus tehtäväksiannon mukaan ja CodeGradesta läpi",
                "tiedostorakenne useita tiedostoja",
                "ohjeiden mukaiset alkukommentit",
                "ohjelmarakenne pääohjelma ja aliohjelmat",
                "perusoperaatiot tulostus, syöte, valintarakenne, toistorakenne",
                "tiedonvälitys parametrit ja paluuarvot, ei globaaleja muuttujia",
                "tiedostonkäsittely luku ja kirjoittaminen",
                "tietorakenteet lista, luokka ja olio",
                "poikkeustenkäsittely tiedostonkäsittelyssä",
                "analyysien toteutus",
                "toteutuksen selkeys, ymmärrettävä, ylläpidettävä ja laajennettava",
            ]
#DEFAULT_FONT, NORMAL_FONT, TITLE_FONT = gui.initialize_font()
def askFile(student_list): 
    student_list.clear()
    root = tk.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory()
    student_list = gui.add_files_in_folder(dirname)




def main() -> None:

    ######## ASKING DIRECTORY NAME ########
    root = tk.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory()
    #default_font, hl_font, title_font = gui.initialize_font()
   
    ######## INITIALIZING DATA AND DPG ########
    categoryList = gui.read_problem_json("Problem_list.json")
    # gui.read_json_file()
    #print(category)
    studentWithErrors = gui.readGradedFile()
    student_list = gui.add_files_in_folder(dirname)
    students = tuple(student.name for student in student_list)
    
    dpg.create_context()
    dpg.configure_app(
        docking=True, docking_space=True, init_file="custom_layout.ini"
    )
    dpg.create_viewport(title="GradeTool", width=1080)
    
    student_window = dpg.generate_uuid()
    category_window = dpg.generate_uuid()
    button_window = dpg.generate_uuid()
    data_window = dpg.generate_uuid()

    
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
                            dpg.add_table_column(label="Virheet", width_stretch=True)
                            dpg.add_table_column(label="Lkm", width_fixed=True)
                            
                            for error in category.errors:
                                with dpg.table_row():
                                    dpg.add_text(error.text, tag=error.text)
                                    dpg.add_input_int(min_value=-1, min_clamped=True, default_value=0, width=80, tag=error._id, callback=gui.mistakeSelected,  user_data=[studentWithErrors, student_list, categoryList])
                      
    ######## COMMENT VIEW ########
    with dpg.window(label="Feedback", tag=button_window) as bWindow:
        dpg.add_input_text(multiline=True, height=-1, label="", width=-1, tag="feedback_input", callback=gui.updateText, user_data=CATEGORY_TEXTS)
        
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
            #dpg.add_menu_item(label="Choose folder", callback=gui.askFileTest, user_data=student_list)




    ######## ITEM REGISTRIES ########
    with dpg.item_handler_registry(tag="student handler") as handler:
        dpg.add_item_clicked_handler(callback=gui.select_student, user_data=[studentWithErrors, categoryList, student_list, CATEGORY_TEXTS])
    
    with dpg.item_handler_registry(tag="mistake handler") as mHandler:
        dpg.add_item_clicked_handler(callback=gui.mistakeSelected, user_data=[studentWithErrors, student_list, categoryList])        
        

    dpg.bind_item_handler_registry("student_view", "student handler")
    dpg.bind_item_handler_registry("error_view", "error handler")
  
    # dpg.bind_item_handler_registry("category_tree", "tree handler")


    
    
    ######## STARTING GUI ########
    #dpg.show_item_registry()
    #dpg.show_style_editor()
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



    