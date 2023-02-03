import dearpygui.dearpygui as dpg
import GradingToolGUI as gui
dpg.create_context()
dpg.create_viewport(title="Grading tool", width=1200, height=600, resizable=True, always_on_top=True)
dpg.setup_dearpygui()

default_font, hl_font = gui.initialize_font()

with dpg.window(label="Opiskelijat", pos=(0,0)):
    
    button1  = dpg.add_button(label="TESTI")
    dpg.bind_font(hl_font)




dpg.show_viewport(maximized=True)


while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()