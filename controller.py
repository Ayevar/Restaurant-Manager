import tkinter as tk
from view import Inventory, Orders, CreateOrder
from model import *
from datetime import *
from PIL import Image, ImageTk



# Reference SeaofBTCapp code from and gui-persistent-demo-app
# https://q.utoronto.ca/courses/407671/modules/items/6875607
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Call parent tkinter class
        tk.Tk.__init__(self, *args, **kwargs)

        # Create Logo
        # Reference Lab week 10 exercise 1
        logo_img = Image.open("Logo.png")
        logo_img = logo_img.resize(
            (logo_img.width // 4, logo_img.height // 4)
        )
        self.logo = ImageTk.PhotoImage(logo_img)

        # Set project style
        self.BACKGROUND_COLOR = "#fcf8ed"
        self.HEADER_FONT = ("Roboto", 24, "bold")

        # Data storage
        self.ingredient_data = IngredientsStorage("ingredients_data")
        self.order_data = OrderStorage("order_data")

        # Create a frame container
        container = tk.Frame(self, bg=self.BACKGROUND_COLOR)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Create default title bar
        self.sidebar_body = tk.Frame(
            container, bg="orange", padx=20, pady=20
        )
        self.sidebar_body.grid(row=0, column=0, sticky="NS")

        # Create container for page content
        self.page_content = tk.Frame(
            container, bg=self.BACKGROUND_COLOR, padx=20, pady=20
        )
        self.page_content.grid(row=0, column=1, sticky="NSEW")

        self.pages = {}

        for p in (Inventory, Orders, CreateOrder):
            page = p(self.page_content, self)
            self.pages[p] = page
            page.grid(row=0, column=0, sticky="nsew")
            page.configure(bg="#fcf8ed")

        self.show_frame(Inventory)
        # Create sidebar buttons

        self.sidebar_logo = tk.Label(
            self.sidebar_body, image=self.logo, bg="orange"
        )
        self.sidebar_logo.pack(pady=10)

        curr_date = f'DATE: \n{date.today()}'

        self.time_lbl = tk.Label(
            self.sidebar_body,
            text= curr_date,
            bg= "orange",
            fg= "blue",
            font= "BOLD"
        )
        self.time_lbl.pack(pady=10)

        self.btn_1 = self.btn(
            self.sidebar_body,"Inventory", 
            lambda: self.show_frame(Inventory)
        )
        self.btn_1.pack(pady=10)

        self.btn_2 = self.btn(
            self.sidebar_body,"New Order", 
            lambda: self.show_frame(Orders)
        )
        self.btn_2.pack(pady=10)

    def show_frame(self, next_page):
        # Advance to next page
        frame = self.pages[next_page]

        # Refresh the frame if it has a refresh() method
        if hasattr(frame, "refresh"):
            frame.refresh()

        # Update frame
        frame.tkraise()

    # Create default button style
    def btn(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command, 
            bg=self.BACKGROUND_COLOR,
            fg="orange", 
            font="bold"
        )

# Run application
app = App()
app.title("Restaurant Manager")
app.iconphoto(True, app.logo)
app.call('wm', 'iconphoto', app._w, app.logo)
app.configure(bg="#fcf8ed")
app.state("zoomed") # Sets as full screen
app.resizable(False, False)
app.mainloop()
