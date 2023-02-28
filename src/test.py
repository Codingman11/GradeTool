import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Tutorial"):

    with dpg.collapsing_header(label="Collapsing Header"):
        dpg.add_button(label="Button 1")
        dpg.add_button(label="Button 2")
        dpg.add_button(label="Button 3")

dpg.create_viewport(title="Custom Title", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
