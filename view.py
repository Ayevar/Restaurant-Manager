"""
Reference Code, For Lecture 4 Video on how to show a new frame
https://q.utoronto.ca/courses/407671/modules/items/6875607

"""
import re
import shelve
import tkinter as tk
from tkinter import ttk

from select import select


class Inventory(tk.Frame):

    """
        inherit from Frame_layout Class and populate page content
        with a Treeview, button, search, etc
    """

    def __init__(self, parent, controller):

        """ create labels and create treeview

            TO DO:
            - Put into grid layout
            - Add functions
            - Finish Orders page

        """

        self.controller = controller

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Inventory", fg="orange",
                         bg=self.controller.BACKGROUND_COLOR,
                         font=self.controller.HEADER_FONT)
        label.pack(fill="both", expand=True)

        # Reference: week 10 demo code "simple_treeview_demo.py"
        # Create treeview
        cols = ['name', 'quantity', 'units', 'category', 'cost']

        self.inventory = ttk.Treeview(self, columns=cols, show="headings",
                                      selectmode='browse')
        # Name each column and set alignment
        for col in cols:
            # Create a heading
            self.inventory.heading(col, text=col.title())
            self.inventory.column(col, anchor='w')


        # To-Do: Create button options functions [edit, sort, etc]
        self.button_frame = tk.Frame(self, bg=self.controller.BACKGROUND_COLOR,
                                     pady= 10)
        self.button_frame.pack(fill="both", expand=True)

        # BUTTONS
        btn_edit = tk.Button(self.button_frame, text="edit", bg="orange",
                             state='disabled')

        btn_sort = tk.Button(self.button_frame, text="view low stock",
                             bg="orange",
                             command=lambda: self.sort_lowstock(self.inventory,
                                                                "quantity"))

        btn_add_ing = tk.Button(self.button_frame, text="add ingredient",
                             bg="orange",
                             command=lambda: IngredientPopup(self, on_save=self.add_ingredient))

        btn_edit.pack(side="right")
        btn_sort.pack(side="right")
        btn_add_ing.pack(side="right")
        self.populate_inventory()

        self.inventory.pack()


    def populate_inventory(self):
        # using the controller reference, we can access the data
        # Reference: https://github.com/michaelnixon/gui-persistent-demo-app
        ingredients = self.controller.ingredient_data.get_all_ingredients()

        # Look through keys and values in ingredient_data dict
        for name, ing_metadata in ingredients.items():
            # create a list with the ingredient name
            store_vals = [name]
            # Look through the inner keys in the dict and store their
            # values in list
            for keys, val in ing_metadata.items():
                store_vals.append(val)
            # add the prepared list as a row to the inventory
            self.inventory.insert("", "end", values=store_vals)


    def refresh(self):
        """
        Update how many items show in inventory
        Prob use treeview ID and look through keys

        Reference: Lab 10 Exercise 2
        """

        # delete everything and re-add everything
        for row in self.inventory.get_children():
            self.inventory.delete(row)

        self.populate_inventory()



    def sort_lowstock(self, tv, col):
        """
        Sorts through tree columns
        Reference: Week 10 Lecture Slides
        Reference: GUI Programming, p. 385

        EDIT: updated to consider int and floats
        """

        itemlist = list(tv.get_children(''))
        # Convert to float before sorting
        itemlist.sort(key=lambda x: float(tv.set(x, col)))
        for index, iid in enumerate(itemlist):
            tv.move(iid, tv.parent(iid), index)

    def add_ingredient(self, data):
        """Handles adding the ingredient to DB & treeview."""

        name = data["name"]

        # --- Save to shelve ---
        with shelve.open("ingredients_data", writeback=True) as db:
            db[name] = {
                "Quantity": data["Quantity"],
                "Unit": data["Unit"],
                "Category": data["Category"],
                "Cost": data["Cost"]
            }

        # --- Add to Treeview ---
        row_values = [
            name,
            data["Quantity"],
            data["Unit"],
            data["Category"],
            data["Cost"]
        ]

        self.inventory.insert("", "end", values=row_values)

        # Optional: refresh for good measure
        self.refresh()

    def remove_ingredient(self):
        pass


class Orders(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="Orders", fg="orange", bg=self.controller.BACKGROUND_COLOR,
                         font=self.controller.HEADER_FONT, pady=10)
        label.pack(fill="both", expand=True)

        btn = tk.Button(self, text="Create New Order", bg="orange",
                             command=lambda: self.controller.show_frame(CreateOrder))
        btn.pack()


class CreateOrder(tk.Frame):
    """
        Allow user to order new stock of ingredient.
        This will update the quantity of ingredient in inventory
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Reference Lab 9 Exercise 2
        # Reference https://docs.python.org/3/library/tkinter.ttk.html

        ing_dict = self.controller.ingredient_data.get_all_ingredients().keys()

        self.ing_select = ttk.Combobox(self, values=list(ing_dict))
        self.ing_select.set("Select an Ingredient")
        self.ing_select.pack()

        # MUST CHECK FOR NUMBER INPUT
        self.quantity_select = tk.Entry(self)
        self.quantity_select.insert(0, "enter quantity")
        self.quantity_select.pack()

        cancel_btn = tk.Button(self, text="CANCEL", bg="red", fg="white",
                        command=lambda: self.controller.show_frame(Orders))
        cancel_btn.pack()

        order_btn = tk.Button(self, text="ORDER", bg="Green",
                               command=self.create)
        order_btn.pack()

    def create(self):
        print("Ordered item: ",self.ing_select.get())
        print("Quantity item: ", self.quantity_select.get())

        # Send data back to model

        if not self.controller.order_data.create_order(self.ing_select.get(),
                                                   self.quantity_select.get()):
            self.quantity_select.delete(0, tk.END)
            self.quantity_select.insert(0, "Invalid entry")
            return

        self.controller.show_frame(Orders)



class CreateIngredient (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller


class IngredientPopup(tk.Toplevel):
    def __init__(self, parent, on_save, ingredient = None):
        super().__init__(parent)
        self.CATEGORIES = ["Dairy", "Fats and Oils", "Grains", "Fruits and Vegetables", "Proteins"]

        self.title("Edit Ingredient" if ingredient else "Create New Ingredient")
        self.geometry("300x400")
        self.transient(parent)   # stays above parent
        self.grab_set()          # makes popup modal

        self.on_save = on_save
        self.ingredient = ingredient

        # --- Fields ---
        tk.Label(self, text="Ingredient Name").pack(anchor="w", padx=10, pady=3)
        self.name_var = tk.StringVar(value=ingredient["name"] if ingredient else "")
        tk.Entry(self, textvariable=self.name_var).pack(fill="x", padx=10)

        tk.Label(self, text="Quantity").pack(anchor="w", padx=10, pady=3)
        self.quantity_var = tk.StringVar(value=ingredient["amount"] if ingredient else "")
        tk.Entry(self, textvariable=self.quantity_var).pack(fill="x", padx=10)


        tk.Label(self, text="Unit:").pack(anchor="w", padx=10, pady=3)

        self.unit_amount_var = tk.StringVar(value=ingredient["unit"] if ingredient else "")
        tk.Entry(self, textvariable=self.unit_amount_var).pack(fill="x", padx=10)

        units = ["MG", "G", "KG", "ML", "L", "PCS"]
        self.unit_var = tk.StringVar()
        cbox2 = ttk.Combobox(self, textvariable=self.unit_var, values=units, state="readonly")
        cbox2.pack(fill="x", padx=10)
        if ingredient:
            self.unit_var.set(ingredient["unit"])

        tk.Label(self, text="Category").pack(anchor="w", padx=10, pady=3)
        self.category_var = tk.StringVar()
        cbox = ttk.Combobox(self, textvariable=self.category_var, values=self.CATEGORIES)
        cbox.pack(fill="x", padx=10)
        if ingredient:
            self.category_var.set(ingredient["category"])

        tk.Label(self, text="Cost per unit").pack(anchor="w", padx=10, pady=3)
        self.cost_var = tk.StringVar(value=ingredient["amount"] if ingredient else "")
        tk.Entry(self, textvariable=self.cost_var).pack(fill="x", padx=10)


        self.warning_lbl = tk.Label(self, text="")
        self.warning_lbl.pack(anchor="n", padx=10, pady=3)

        # --- Buttons ---
        tk.Button(self, text="Save", command=self.save, bg="orange").pack(pady=10)
        tk.Button(self, text="Cancel", command=self.destroy).pack()

    def save(self):

        qty = self.quantity_var.get()
        cost = self.cost_var.get()
        unit_amt = self.unit_amount_var.get()

        # validate
        if qty.isdigit() and int(qty) > 0 and unit_amt.isdigit() and int(unit_amt) > 0 and re.match(r"^\d+(\.\d{2})?$", cost):
            data = {
                "name": self.name_var.get(),
                "Quantity": int(qty),
                "Unit": self.unit_amount_var.get() + " " + self.unit_var.get(),
                "Category": self.category_var.get(),
                "Cost": float(cost)
            }

            self.on_save(data)
            self.destroy()
        else:
            self.warning_lbl.config(text="Invalid entry")
