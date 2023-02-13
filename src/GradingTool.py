import dearpygui.dearpygui as dpg
import GradingToolGUI as gui



# CATEGORY_WINDOW = item_id["windows"]["cateogry_window"]
# BUTTON_WINDOW = item_id["windows"]["button_window"]
# DATA_WINDOW = item_id["windows"]["data_window"]
def main() -> None:


    dpg.create_context()
    dpg.create_viewport(title="Grading tool", width=1200, height=600, resizable=True, always_on_top=True)
    default_font, hl_font, title_font = gui.initialize_font()

    with dpg.window(label="Opiskelijat", tag=item_id["windows"]["student_window"]):
        button1 = dpg.add_button(label="Press me")
        dpg.bind_item_font(button1, hl_font)

    # with dpg.window(label="Ongelmat koodissa", tag=CATEGORY_WINDOW):
    #     button2 = dpg.add_button(label="Press me")
    #     dpg.bind_item_font(button2, hl_font)

    
    # with dpg.window(label="Toiminnallisuudet", tag=BUTTON_WINDOW):
    #     button3 = dpg.add_button(label="Press me")
    #     dpg.bind_item_font(button3, hl_font)


    # with dpg.window(label="Tiedot", tag=DATA_WINDOW):
    #     button4 = dpg.add_button(label="Press me")
    #     dpg.bind_item_font(button4, hl_font)

    # print(gui.student)
    
    
    dpg.setup_dearpygui()


    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


def save_init():
    dpg.save_init_file("layout.ini")

if __name__ == '__main__':
    main()