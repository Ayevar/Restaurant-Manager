"""
Reference Code, For Lecture 4 Video on how to show a new frame
https://q.utoronto.ca/courses/407671/modules/items/6875607

"""
from datetime import *
import re
import shelve
import tkinter as tk
from tkinter import ttk, messagebox

class Inventory(tk.Frame):
    """
    Inherit from Frame_layout Class and populate page content 
    with a Treeview, button, search, etc
    """

    def __init__(self, parent, controller):

        """
            initialize controller and parent class,
            create basic title labels, treeview, buttons, scrollbar
            and call populate inventory to fill treeview
        """

        # Call controller from parent class
        self.controller = controller

        # Inherit parent super class
        tk.Frame.__init__(self, parent)

        # Create title label
        label = tk.Label(
            self, 
            text="Inventory", 
            fg="orange",
            bg=self.controller.BACKGROUND_COLOR,
            font=self.controller.HEADER_FONT
        )
        label.pack(fill="both", expand=True)

        # Create container for vertical and horizontal scroll bar
        inventory_grid = ttk.Frame(self)
        # configure container row and column to page size

        # Reference: week 10 demo code "simple_treeview_demo.py"
        # Create treeview
        cols = ['name', 'quantity', 'units', 'category', 'cost']
        self.inventory = ttk.Treeview(
            inventory_grid, 
            columns=cols, 
            show="headings", 
            selectmode='browse'
        )

        # Name each column and set alignment
        for col in cols:
            # Create a heading
            self.inventory.heading(col, text=col.title())
            self.inventory.column(col, anchor='w', width=210, stretch=tk.NO)

        # Create button container 
        self.button_frame = tk.Frame(
            self, 
            bg=self.controller.BACKGROUND_COLOR, 
            pady=10
        )
        self.button_frame.pack(side='top', fill="x")

        # BUTTONS

        btn_edit = tk.Button(
            self.button_frame, 
            text="edit", 
            bg="orange",
            command=self.edit_selected
        )

        # Only can edit when a row is selected
        self.inventory.bind(
            "<<TreeviewSelect>>",
            lambda e: btn_edit.config(state="normal")
        )

        # Let user sort for low stock items
        btn_sort = tk.Button(
            self.button_frame,
            text="view low stock",
            bg="orange",
            command=lambda: self.sort_lowstock(self.inventory,"quantity")
        )

        btn_add_ing = tk.Button(
            self.button_frame, 
            text="add ingredient",
            bg="green", 
            fg="white", 
            command=lambda: IngredientPopup(self, on_save=self.add_ingredient)
        )

        btn_delete = tk.Button(
            self.button_frame, 
            text="delete ingredient",
            bg="red", 
            command=self.remove_ingredient
        )

        # Pack buttons with equal padding
        padding = 2
        btn_edit.pack(side="right", padx=padding)
        btn_sort.pack(side="right", padx=padding)
        btn_add_ing.pack(side="left", padx=padding)
        btn_delete.pack(side="left", padx=padding)

        # Pack inventory grid that holds treeview and scrollers 
        inventory_grid.pack()
        self.inventory.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = tk.Scrollbar(
            inventory_grid, orient=tk.VERTICAL, 
            command=self.inventory.yview
        )
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = tk.Scrollbar(
            inventory_grid, orient=tk.HORIZONTAL, 
            command=self.inventory.xview
        )
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        # Configure scrollbar to inventory 
        self.inventory.configure(yscrollcommand=scrollbar_y.set)
        self.inventory.configure(xscrollcommand=scrollbar_x.set)

        inventory_grid.rowconfigure(0, weight=1)
        inventory_grid.columnconfigure(0, weight=1)

        # Populate treeview
        self.populate_inventory()


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

        items = list(tv.get_children(""))
        # Convert to float before sorting
        items.sort(key=lambda x: float(tv.set(x, col)))

        for index, iid in enumerate(items):
            tv.move(iid, tv.parent(iid), index)

    def add_ingredient(self, data):
        """Handles adding the ingredient to DB & treeview."""

        name = data["name"]

        # Save to shelve
        with shelve.open("ingredients_data", writeback=True) as db:
            db[name] = {
                "Quantity": int(data["quantity"]),
                "Unit": data["unit"],
                "Category": data["category"],
                "Cost": float(data["cost"])
            }

        # Add to treeview
        row_values = [
            name,
            data["quantity"],
            data["unit"],
            data["category"],
            data["cost"]
        ]

        self.inventory.insert("", "end", values=row_values)
        self.refresh()


    def remove_ingredient(self):
        """
        User able to remove selected ingredents
        """
        # grab the highlighted row
        selected = self.inventory.focus()
        if not selected:
            return

        values = self.inventory.item(selected, "values")
        name = values[0] # ingredient name is column 0

        # Warning popup
        confirm = messagebox.askyesno(
            "Delete Ingredient",
            f"Are you sure you want to delete '{name}'?"
        )

        if not confirm:
            return  # user canceled

        # Delete from database
        with shelve.open("ingredients_data", writeback=True) as db:
            if name in db:
                del db[name]

        # Remove from treeview
        self.inventory.delete(selected)

    def edit_selected(self):
        """
        Users able to edit data in the ingredent list
        """
        selected = self.inventory.focus()
        if not selected:
            return

        values = self.inventory.item(selected, "values")

        # unpack the row
        data = {
            "name": values[0],
            "quantity": values[1],
            "unit": values[2],
            "category": values[3],
            "cost": values[4],
            "tree_id": selected
        }

        # Open the popup with this data
        IngredientPopup(
            self, 
            on_save=self.update_ingredient, 
            ingredient=data
        )

    def update_ingredient(self, updated):

        """
        If user edits the ingredents list inventory refreshes to
        updates treeview and writes back to shelf file
        """
        # Pop tree_id (might cause issues if missing)
        tree_id = updated.pop("tree_id", None)
        if not tree_id:
            return

        # Read old row values before changing (to get old name)
        old_vals = self.inventory.item(tree_id, "values")
        old_name = old_vals[0] if old_vals else None

        # Update Treeview row (display)
        self.inventory.item(
            tree_id, 
            values=[
                updated["name"],
                updated["quantity"],
                updated["unit"],
                updated["category"],
                updated["cost"]
            ]
        )

        # Update shelve file
        with shelve.open("ingredients_data", writeback=True) as db:
            # if name changed, remove old entry (if exists)
            # (might remove the ability to change names if it messes with the system)
            if old_name and old_name in db and updated["name"] != old_name:
                del db[old_name]

            db[updated["name"]] = {
                "Quantity": int(updated["quantity"]),
                "Unit": updated["unit"],
                "Category": updated["category"],
                "Cost": float(updated["cost"])
            }


class Orders(tk.Frame):

    """
    inherit from Frame_layout Class and populate page content
    with a Treeview, button, search, etc
    """

    def __init__(self, parent, controller):

        """
        initialize controller and parent class,
        create basic title labels, treeview, buttons, scrollbar
        and call populate inventory to fill treeview
        """

        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(
            self, 
            text="Orders", 
            fg="orange", 
            bg=self.controller.BACKGROUND_COLOR,
            font=self.controller.HEADER_FONT, 
            pady=10
        )
        label.pack(fill="both", expand=True)


        # Create datetime object for current time
        # This can be changed for testing
        self.curr_datetime = datetime(2026, 10, 26, 14, 30, 45)
        # self.curr_datetime = datetime.now()

        # Create label that shows total cost of orders
        self.totalcost = tk.Label(
            self, 
            text="Total Costs: $0.00", 
            fg="blue",
            font=("Roboto", 18, "bold"), 
            bg=self.controller.BACKGROUND_COLOR,
            pady=10
        )
        self.totalcost.pack(fill="both", expand=True)

        self.button_frame = tk.Frame(
            self, 
            bg=self.controller.BACKGROUND_COLOR,
            pady=10
        )
        self.button_frame.pack(fill="both", expand=True)

        btn = tk.Button(
            self.button_frame, 
            text="Create New Order", 
            bg="green", 
            fg="white",
            command=lambda: self.controller.show_frame(CreateOrder)
        )
        btn.pack(side='left')

        cancel_button = tk.Button(
            self.button_frame, 
            text="Cancel Order", 
            bg='red',
            fg="white", 
            command=self.cancel_order
        )
        cancel_button.pack(side='right')

        update_button = tk.Button(
            self.button_frame, 
            text="Process Shipped Orders", 
            bg='orange',
            command=self.update_orders
        )
        update_button.pack(side='right')

        orders_grid = tk.Frame(self)
        orders_grid.pack()

        orders_grid.grid_rowconfigure(0, weight=1)
        orders_grid.grid_columnconfigure(0, weight=1)

        orders = [
            'ID', 
            'Ingredient', 
            'Quantity', 
            'Date Ordered', 
            'Arrival Date', 
            'Status', 
            'Price'
        ]
        self.orders = ttk.Treeview(
            orders_grid, 
            columns=orders, 
            show="headings", 
            selectmode='browse'
        )

        for col in orders:
            # Create a heading
            self.orders.heading(col, text=col)
            self.orders.column(col, anchor='w', width=150, stretch=tk.NO)

        self.orders.grid(row=0, column=0, sticky='nsew')

        scrollbar_y = tk.Scrollbar(
            orders_grid, orient=tk.VERTICAL, command=self.orders.yview
        )
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = tk.Scrollbar(
            orders_grid, orient=tk.HORIZONTAL, command=self.orders.xview
        )
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.orders.configure(yscrollcommand=scrollbar_y.set)
        self.orders.configure(xscrollcommand=scrollbar_x.set)

        self.populate_orders()


    def populate_orders(self):
        # using the controller reference, we can access the data
        # Reference: https://github.com/michaelnixon/gui-persistent-demo-app
        orders = self.controller.order_data.get_orders()

        # Look through keys and values in ingredient_data dict
        for name, ord_metadata in orders.items():
            # create a list with the ingredient name
            store_vals = [name]
            # Look through the inner keys in the dict and store their
            # values in list
            for keys, val in ord_metadata.items():
                store_vals.append(val)
            # add the prepared list as a row to the order history
            self.orders.insert("", "end", values=store_vals)


    def refresh(self):
        """
        Update how many items show in inventory
        Prob use treeview ID and look through keys

        Reference: Lab 10 Exercise 2
        """
        total = 0
        orders = self.controller.order_data.get_orders()
        # Look through keys and values in ingredient_data dict
        # delete everything and re-add everything
        for name, ord_metadata in orders.items():
            if ord_metadata['Status'] != 'Cancelled':
                total += ord_metadata['Cost']
    
        for row in self.orders.get_children():
            self.orders.delete(row)
    
        self.totalcost.config(
            text=f'Total Costs: ${total:.2f}', 
            bg=self.controller.BACKGROUND_COLOR
        )
        self.populate_orders()


    def cancel_order(self):
        selected = self.orders.focus()
        if not selected:
            return
    
        values = self.orders.item(selected, "values")
        if messagebox.askyesno(
            'Remove Order?', 
            f'Would you like to remove {values[0]}?'
        ):
            if values[5] == 'Cancelled':
                messagebox.showerror(
                    "Error",
                    "This order is already canceled"
                )
            else:

                # Update Treeview row (display)
                self.orders.item(
                    selected, 
                    values=[
                        values[0],
                        values[1],
                        values[2],
                        values[3],
                        values[4],
                        "Cancelled",
                        values[6]
                    ]
                )

                # Update shelve file
                with shelve.open("order_data", writeback=True) as db:
                    db[values[0]] = {
                        "Ingredient": values[1],
                        "Quantity": int(values[2]),
                        "Date Ordered": values[3],
                        "Arrival Date": values[4],
                        "Status": "Cancelled",
                        "Cost": values[6]
                    }


    def update_orders(self):
        orders = self.controller.order_data.get_orders()
        changed = False
        edits = []

        with shelve.open("order_data", writeback=True) as or_db:
            for name, ord_metadata in orders.items():
                arrival_time = datetime.strptime(
                    ord_metadata["Arrival Date"], 
                    "%y-%m-%d, %H:%M"
                )

                if ord_metadata['Status'] == 'Pending' and arrival_time <= self.curr_datetime:
                    or_db[name] = {
                        "Ingredient": ord_metadata["Ingredient"],
                        "Quantity": ord_metadata["Quantity"],
                        "Date Ordered": ord_metadata["Date Ordered"],
                        "Arrival Date": ord_metadata["Arrival Date"],
                        "Status": "Shipped",
                        "Cost": ord_metadata["Cost"]
                    }
                    edits.append(
                        (ord_metadata["Ingredient"], 
                         ord_metadata["Quantity"])
                    )
                    changed = True

        if changed:
            or_db.close()
            with shelve.open("ingredients_data", writeback=True) as in_db:
                for item in edits:
                    in_db[item[0]] = {
                        "Quantity": int(in_db[item[0]]["Quantity"] + ord_metadata["Quantity"]),
                        "Unit": in_db[item[0]]["Unit"],
                        "Category": in_db[item[0]]["Category"],
                        "Cost": float(in_db[item[0]]["Cost"])
                    }

            self.controller.pages[Inventory].refresh()
            self.refresh()
            
            messagebox.showinfo(
                "Inventory Updated", 
                "Pending Orders have arrived. Inventory updated"
            )
        else:
            messagebox.showinfo(
                "No orders arrived", 
                "No Pending Orders have arrived yet."
            )


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

        self.ing_select = ttk.Combobox(
            self, 
            state='readonly', 
            values=list(ing_dict)
        )
        self.ing_select.set("Select an Ingredient")
        self.ing_select.pack()

        # Combo box allowing user to set which shipping style they want
        self.ship_select = ttk.Combobox(
            self, 
            state='readonly', 
            values=['Same day', '1 day', '3 day']
        )
        self.ship_select.set("Select shipping style")
        self.ship_select.pack(pady=3)

        costslabel = tk.Label(
            self, 
            text="Shipping Costs:", 
            fg="blue",
            font=('Roboto', 10), 
            pady=3, 
            bg=self.controller.BACKGROUND_COLOR
        )
        costslabel.pack()

        costslabel2 = tk.Label(
            self, 
            text="Same Day Shipping = x1.25," 
            "1 Day Shipping = x1.10, "
            "3 Day Shipping = x1.00",
            fg="blue", 
            font=('Roboto', 10), 
            pady=3, 
            bg=self.controller.BACKGROUND_COLOR
        )
        costslabel2.pack()

        # MUST CHECK FOR NUMBER INPUT
        self.quantity_select = tk.Entry(self)
        self.quantity_select.insert(0, "enter quantity")
        self.quantity_select.pack()

        cancel_btn = tk.Button(
            self, 
            text="CANCEL", 
            bg="red", 
            fg="white",
            command=lambda: self.controller.show_frame(Orders)
        )
        cancel_btn.pack()

        order_btn = tk.Button(
            self, 
            text="ORDER", 
            bg="Green",
            command=self.create
        )
        order_btn.pack()


    def create(self):
        print("Ordered item: ", self.ing_select.get())
        print("Quantity item: ", self.quantity_select.get())

        # Send data back to model

        if not self.controller.order_data.create_order(
            self.ing_select.get(),
            self.quantity_select.get(), 
            self.ship_select.get()
        ):
            self.quantity_select.delete(0, tk.END)
            self.quantity_select.insert(0, "Invalid entry")
            return

        self.controller.show_frame(Orders)


    def refresh(self):
        # Reload ingredient names
        ing_dict = self.controller.ingredient_data.get_all_ingredients().keys()
        self.ing_select["values"] = list(ing_dict)

        # Reset selection text
        self.ing_select.set("Select an Ingredient")

        # Clear quantity entry
        self.quantity_select.delete(0, tk.END)
        self.quantity_select.insert(0, "enter quantity")


class IngredientPopup(tk.Toplevel):
    # No set ingredient by default (changing the popup if you're editing vs adding a new ingredient)
    def __init__(self, parent, on_save, ingredient = None):
        super().__init__(parent)

        self.CATEGORIES = [
            "Dairy", 
            "Fats and Oils", 
            "Grains", 
            "Fruits and Vegetables", 
            "Proteins"
        ]
        self.title(
            "Edit Ingredient" if ingredient else "Create New Ingredient"
        )
        self.geometry("400x400")
        self.configure(bg="#fcf8ed")
        self.transient(parent) # stays above parent
        self.grab_set() # makes popup modal

        # Get size of parent grid box
        x, y, width, height = parent.grid_bbox(column=0, row=0)
        self.geometry(f"+50+100")


        self.on_save = on_save
        self.ingredient = ingredient

        # --- Fields ---
        tk.Label(self, text="Ingredient Name").pack(
            anchor="w", padx=10, pady=3
        )
        self.name_var = tk.StringVar(
            value=ingredient["name"] if ingredient else ""
        )
        tk.Entry(self, textvariable=self.name_var).pack(fill="x", padx=10)


        tk.Label(self, text="Quantity").pack(
            anchor="w", padx=10, pady=3
        )

        self.quantity_var = tk.StringVar(
            value=ingredient["quantity"] if ingredient else ""
        )


        if ingredient:
            tk.Entry(self, textvariable=self.quantity_var, state="readonly").pack(
                fill="x", padx=10
            )
        else:
            tk.Entry(self, textvariable=self.quantity_var).pack(
                fill="x", padx=10
            )


        tk.Label(self, text="Unit:").pack(anchor="w", padx=10, pady=3)

        # unit is a string like "5 KG" so split into amount and unit
        if ingredient:
            unit_parts = ingredient["unit"].split()
            unit_amount = unit_parts[0]
            unit_type = unit_parts[1]
        else:
            unit_amount = ""
            unit_type = ""

        self.unit_amount_var = tk.StringVar(value=unit_amount)
        tk.Entry(self, textvariable=self.unit_amount_var).pack(
            fill="x", padx=10
        )

        # preset units
        units = ["MG", "G", "KG", "ML", "L", "PCS"]
        self.unit_var = tk.StringVar()
        cbox2 = ttk.Combobox(
            self, 
            textvariable=self.unit_var, 
            values=units, 
            state="readonly"
        )
        cbox2.pack(fill="x", padx=10)

        if ingredient:
            self.unit_var.set(unit_type)


        tk.Label(self, text="Category").pack(
            anchor="w", padx=10, pady=3
        )
        self.category_var = tk.StringVar()
        cbox = ttk.Combobox(
            self, 
            textvariable=self.category_var, 
            values=self.CATEGORIES, 
            state="readonly"
        )
        cbox.pack(fill="x", padx=10)
        if ingredient:
            self.category_var.set(ingredient["category"])


        tk.Label(self, text="Cost per unit").pack(
            anchor="w", padx=10, pady=3
        )
        self.cost_var = tk.StringVar(
            value=ingredient["cost"] if ingredient else ""
        )
        tk.Entry(self, textvariable=self.cost_var).pack(fill="x", padx=10)


        self.warning_lbl = tk.Label(self, text="")
        self.warning_lbl.pack(anchor="n", padx=10, pady=3)

        # buttons
        tk.Button(
            self, 
            text="Save", 
            command=self.save, 
            bg="orange"
        ).pack(pady=10)

        tk.Button(
            self, 
            text="Cancel", 
            command=self.destroy
        ).pack()


    def save(self):

        qty = self.quantity_var.get()
        cost = self.cost_var.get()
        unit_amt = self.unit_amount_var.get()
        unit_type = self.unit_var.get()
        category = self.category_var.get()

        # check for possible invalid entries
        if (qty.isdigit() and int(qty) > 0 and re.match(r"^\d+(\.\d+)?$", unit_amt) and unit_type != ""
                and category != "" and float(unit_amt) > 0 and re.match(r"^\d+(\.\d{2})?$", cost)):
            data = {
                "name": self.name_var.get(),
                "quantity": int(qty),
                "unit": f"{unit_amt} {unit_type}".strip(),
                "category": category,
                "cost": float(cost)
            }

            if self.ingredient and "tree_id" in self.ingredient:
                data["tree_id"] = self.ingredient["tree_id"]

            self.on_save(data)

            # only exit if entries are valid, otherwise stay to let the user try again
            self.destroy()
        else:
            self.warning_lbl.config(text="Invalid entry")
