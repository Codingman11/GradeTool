import dearpygui.dearpygui as dpg
import os, json
from pathlib import Path
DEFAULT_FONT = Path(__file__).parents[1] / "assets/arialn.ttf"
HL_FONT = Path(__file__).parents[1] / "assets/arialnb.ttf"
from data import StudentInfo, ErrorInfo, Category




#initialize font 
def initialize_font():
    with dpg.font_registry():
        default_font = dpg.add_font(DEFAULT_FONT, 15)
        hl_font = dpg.add_font(HL_FONT, 15) 
    return default_font, hl_font



