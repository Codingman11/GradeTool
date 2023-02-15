import dearpygui.dearpygui as dpg
import GradingToolGUI as gui
import dearpygui.demo as demo
from tkinter import filedialog


def main() -> None:

    indent = 20
    dpg.create_context()
    dpg.create_viewport(title="Grading tool", width=1200, height=600, resizable=True)
    default_font, hl_font, title_font = gui.initialize_font()

    student_window = dpg.generate_uuid()
    category_window = dpg.generate_uuid()
    button_window = dpg.generate_uuid()
    data_window = dpg.generate_uuid()

    # dirname = filedialog.askdirectory()
    # gui.add_files_in_folder(dirname)
    with dpg.window(label="Opiskelijat", tag=student_window) as sw:
        button1 = dpg.add_button(label="Press me")

        with dpg.group():
            with dpg.table(header_row=True, width=400,policy=dpg.mvTable_SizingFixedFit, resizable=True, no_host_extendX=True, borders_innerV=True, borders_outerV=True, borders_outerH=True) as student_table:
                
                dpg.add_table_column(label=f'Virhe koodissa', width_fixed=True)
                dpg.add_table_column(label="Lkm", tag="lkm_tag", width_fixed=True)


                for i in range(0, 8):
                    with dpg.table_row():
                        dpg.add_text(label="")
                        dpg.add_input_int(width=250, min_value=-1, min_clamped=True)

            
            

        dpg.bind_item_font(button1, hl_font)
    vp_width = dpg.get_viewport_client_width()
    vp_heigth = dpg.get_viewport_client_height()
    sw_width = dpg.get_item_width(sw)
    sw_height = dpg.get_item_height(sw)
    se_width = vp_width - sw_width
    print("viewport width: ", vp_width, "student_width:", sw_width, "student_heigth", sw_height)
   
    dpg.set_item_width(sw, dpg.get_item_width(student_table))
    print(dpg.get_item_width(student_table))
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
    win_config = dpg.get_item_configuration(sw)
    #demo.show_demo()
    dpg.setup_dearpygui()

  
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


def save_init():
    dpg.save_init_file("layout.ini")

if __name__ == '__main__':
    main()