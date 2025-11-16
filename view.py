"""
Reference Code, For Lecture 4 Video on how to show a new frame
https://q.utoronto.ca/courses/407671/modules/items/6875607

"""

import tkinter as tk
from tkinter import ttk

from PIL.ImageOps import expand

HEADER_FONT = ("Roboto", 24)



# Reference SeaofBTCapp code from,
# https://q.utoronto.ca/courses/407671/modules/items/6875607
class Frame_layout(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Call parent tkinter class
        tk.Tk.__init__(self, *args, **kwargs)

        # create a frame container
        container = tk.Frame(self, bg="white")

        # pack the container
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        self.sidebar_body = tk.Frame(container, bg="orange", padx=20, pady=20)
        self.sidebar_body.grid(row=0, column=0, sticky="NS", )


        # create container for page content
        self.page_content = tk.Frame(container, bg="white", padx=20, pady=20)
        self.page_content.grid(row=0, column=1, sticky="NSEW")

        self.pages = {}

        for p in (Inventory, Orders):
            page = p(self.page_content, self)
            self.pages[p] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.change_page(Inventory)
        # create sidebar buttons

        self.sidebar_title = tk.Label(self.sidebar_body, text="LOGO", fg="white", bg="orange", font=HEADER_FONT)
        self.sidebar_title.pack(pady=10)

        self.btn_1 = self.btn(self.sidebar_body,"Inventory", lambda: self.change_page(Inventory))
        self.btn_1.pack(pady=10)

        self.btn_2 = self.btn(self.sidebar_body,"New Order", lambda: self.change_page(Orders))
        self.btn_2.pack(pady=10)


    def change_page(self, next):
        # advance to next frame
        frame = self.pages[next]
        # update frame
        frame.tkraise()

    # create default button style
    def btn(self, parent, text, command):

        btn = tk.Button(parent, text=text,
                               command=command, bg="white", fg="orange", font="BOLD")
        return btn

class Inventory(tk.Frame):

    """
        inherit from Frame_layout Class and populate page content
        with a Treeview, button, search, etc
    """

    def __init__(self, parent, controller):

        """ create labels and create treeview"""

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Inventory", fg="orange", bg="white",
                         font=HEADER_FONT, pady= 10)
        label.pack(fill="x", expand=True)


        # To-Do: Create button options [edit, sort, etc]


        # Reference: week 10 demo code "simple_treeview_demo.py"
        # Create treeview
        self.inventory = ttk.Treeview(self, columns=["Quantity", "Units", "Category", "Cost"], selectmode='browse')

        # Name each column
        self.inventory.heading("#0", text="Name")
        self.inventory.heading("Quantity", text="Quantity")
        self.inventory.heading("Units", text="Units")
        self.inventory.heading("Category", text="Category")
        self.inventory.heading("Cost", text="Cost")

        self.inventory.pack()


    def sort(self):
        """ Use code from slides"""
        pass



class Orders(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Orders", fg="orange", bg="white",
                         font=HEADER_FONT, pady=10)
        label.pack(fill="both", expand=True)
