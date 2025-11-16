import tkinter as tk
from tkinter import Image

from view import *
from model import *

root = Frame_layout()
# make background white
root.title("Restaurant Manager")
# Remove default title bar
# root.overrideredirect(True)

# makes the window full screen
root.state("zoom")
root.resizable(False, False)
root.mainloop()
