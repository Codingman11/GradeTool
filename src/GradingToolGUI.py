import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"


class ERRORINFO:
    error = ("",)
    text = ""
    errorpoints = 0
    amount = 0
    alternative = []
    exclude = []

class CATEGORY:
    name = ""
    category_sum = 0

class STUDENTINFO:
    name = ""
    student_number = ""
    exam_level = ""
    group = ""
    feedback = ""


#font family 
print("{}".format(DEFAULT_FONT))
def initialize_font():
    with dpg.font_registry():
        default_font = dpg.add_font(DEFAULT_FONT, 15)
        hl_font = dpg.add_font(HL_FONT, 15) 

        

    return default_font, hl_font