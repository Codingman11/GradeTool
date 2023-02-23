import dearpygui.dearpygui as dpg
import GradingToolGUI as gui
import dearpygui.demo as demo
from tkinter import filedialog
from os import path

#   V0.1.0 GUI windows added, data structure for student, errors and category added
#   V0.1.1 File director added and sorting the files 

def main() -> None:

    # Initializing all data structures

    indent = 20
    dpg.create_context()

    dpg.configure_app(docking=True, docking_space=True,
                      load_init_file='custom_layout.ini')

    default_font, hl_font, title_font = gui.initialize_font()

    student_window = dpg.generate_uuid()
    category_window = dpg.generate_uuid()
    button_window = dpg.generate_uuid()
    data_window = dpg.generate_uuid()

    dirname = filedialog.askdirectory()
    gui.add_files_in_folder(dirname)


    dpg.create_viewport(title="Grading tool", width=1200,
                        height=600, resizable=True)
    with dpg.window(label="Opiskelijat", tag=student_window):
       
        pass

    with dpg.window(label="Virheet", tag=category_window) as cWindow:
        
        with dpg.group():
            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, resizable=True, no_host_extendX=True, borders_innerV=True, borders_outerV=True, borders_outerH=True) as student_table:

                dpg.add_table_column(label=f'Virhe koodissa', width_fixed=True)
                dpg.add_table_column(
                    label="Lkm", tag="lkm_tag")

                for i in range(0, 8):
                    with dpg.table_row():
                        dpg.add_text(label="")
                        dpg.add_input_int(
                            width=500, min_value=-1, min_clamped=True)

    with dpg.window(label="Toiminnot", tag=button_window) as bWindow:
        pass

    with dpg.window(label="Opiskelija", tag=data_window) as dWindow:
        pass

  
    # dpg.bind_item_font(button1, hl_font)
    # vp_width = dpg.get_viewport_client_width()
    # vp_heigth = dpg.get_viewport_client_height()
    # sw_width = dpg.get_item_width(sw)
    # sw_height = dpg.get_item_height(sw)
    # se_width = vp_width - sw_width
    # print("viewport width: ", vp_width, "student_width:", sw_width, "student_heigth", sw_height)

    # dpg.set_item_width(sw, dpg.get_item_width(student_table))
    # print(dpg.get_item_width(student_table))
    # with dpg.window(label="Ongelmat koodissa", tag=category_window):
    #     button2 = dpg.add_button(label="Press me")
    #     dpg.bind_item_font(button2, hl_font)

    # with dpg.window(label="Toiminnallisuudet", tag=BUTTON_WINDOW):
    #     button3 = dpg.add_button(label="Press me")
    #     dpg.bind_item_font(button3, hl_font)

    # with dpg.window(label="Tiedot", tag=DATA_WINDOW):
    #     button4 = dpg.add_button(label="Press me")
    #     dpg.bind_item_font(button4, hl_font)

    # print(gui.student)
    # win_config = dpg.get_item_configuration(sw)
    # demo.show_demo()
    
    dpg.show_item_registry()


    dpg.setup_dearpygui()

    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        

    dpg.destroy_context()





if __name__ == '__main__':
    main()
