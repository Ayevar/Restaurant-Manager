import tkinter as tk
from view import Inventory, Orders, CreateOrder, CreateIngredient
from model import *



# Reference SeaofBTCapp code from and gui-persistent-demo-app
# https://q.utoronto.ca/courses/407671/modules/items/6875607
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Call parent tkinter class
        tk.Tk.__init__(self, *args, **kwargs)

        # set background color
        self.BACKGROUND_COLOR = "#fcf8ed"
        self.HEADER_FONT = ("Roboto", 18)

        self.ingredient_data = IngredientsStorage("ingredients_data")
        self.order_data = OrderStorage("order_data")

        # create a frame container
        container = tk.Frame(self, bg=self.BACKGROUND_COLOR)
        # pack the container
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Create default title bar
        self.sidebar_body = tk.Frame(container, bg="orange", padx=20, pady=20)
        self.sidebar_body.grid(row=0, column=0, sticky="NS", )


        # create container for page content
        self.page_content = tk.Frame(container, bg=self.BACKGROUND_COLOR, padx=20, pady=20)
        self.page_content.grid(row=0, column=1, sticky="NSEW")

        self.pages = {}

        for p in (Inventory, Orders, CreateOrder, CreateIngredient):
            page = p(self.page_content, self)
            self.pages[p] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Inventory)
        # create sidebar buttons

        self.sidebar_title = tk.Label(self.sidebar_body, text="LOGO", fg="white", bg="orange", font="BOLD")
        self.sidebar_title.pack(pady=10)

        self.btn_1 = self.btn(self.sidebar_body,"Inventory", lambda: self.show_frame(Inventory))
        self.btn_1.pack(pady=10)

        self.btn_2 = self.btn(self.sidebar_body,"New Order", lambda: self.show_frame(Orders))
        self.btn_2.pack(pady=10)


    def show_frame(self, next):
        # advance to next frame
        frame = self.pages[next]

        # refresh if the frame has a refresh method
        if hasattr(frame, "refresh"):
            frame.refresh()

        # update frame
        frame.tkraise()

    # create default button style
    def btn(self, parent, text, command):

        btn = tk.Button(parent, text=text,
                               command=command, bg=self.BACKGROUND_COLOR, fg="orange", font="BOLD")
        return btn


app = App()
app.title("Restaurant Manager")
# makes the window full screen
app.state("zoom")
app.resizable(False, False)
app.mainloop()
