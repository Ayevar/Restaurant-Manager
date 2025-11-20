import sqlite3
import shelve
from datetime import *

ING_DATA = "ingredients_data"
ORD_DATA = "order_data"

class IngredientsStorage:

    """
        This class loads in shelve file data for Ingredients.
        It also allows ingredients to be added to and deleted from
        the data.

        Our understanding of Shelve comes from the Week 10 lecture. We
        will reference it several times in this file
    """

    def __init__(self, file):

        """
            Create the different ingredient categories and create database
            if it has not already been created.
        """

        # Create ingredient categories list
        self.CATEGORIES = ["Dairy", "Fats and Oils", "Grains", "Fruits and Vegetables", "Proteins"]

        # populate database with starter data
        self.file = file

        # Reference Week 10 Lecture
        # Open using 'with' so that shelf closes automatically
        # to avoid error
        with shelve.open(self.file) as db:
            db.clear()
            # Reference: https://docs.python.org/3/library/shelve.html
            # If database has not been created (has no keys), then create
            if not list(db.keys()):
                # Store each item as a key in the db dict

                db["Bread Flour"] = {"Quantity": 17, "Unit": "5 KG", "Category": self.CATEGORIES[2], "Cost": 9.52}
                db["Gala Apples"] = {"Quantity": 19, "Unit": "4 LB", "Category": self.CATEGORIES[3], "Cost": 7.99}
                db["Chicken Thighs"] = {"Quantity": 10, "Unit": "1.5 KG", "Category": self.CATEGORIES[4], "Cost": 12.35}


    def get_all_ingredients(self):
        """
        Reference Week 10 Lecture

        Return a dict version of the database containing all the
        ingredients in the inventory
        """
        with shelve.open(self.file) as db:
            return dict(db)

    def get_ingredient(self, n):
        """
            return single ingredient
        """
        with shelve.open(self.file) as db:
            return dict(db.get(n))


    def add_ingredient(self):
        """
        Reference Week 10 Lecture

        add new ingredient type (key) to the database, ensure
        ingredient does not already exist (all info matches)
        """
        pass

    def remove_ingredient(self):
        """
        remove ingredient key to the database, ensure
        ingredient is in database before deleting key.

        *** Could return true or false here for clarity and updating
        """
        pass

class OrderStorage:
    """
        load and update user order data.

        Example of data structure:
            Orders = {Order 1: {Ingredient: "milk",
            "Quantity": 3}
    """

    def __init__(self, file):

        # populate database with starter data
        self.file = file
        self.order_number = ""
        # Reference: https://docs.python.org/3/library/datetime.html
        # use datetime to get current time
        self.order_data = datetime.now()


        # USED TO CHECK IF ANYTHING IS BEING STORED
        # with shelve.open(self.file) as or_db:
        #     print(dict(or_db))
        #     or_db.clear()


    def create_order(self, ingredient, quantity):

        # Open ingredient database and order database
        with shelve.open(ING_DATA) as i_db:
            # Check if ingredient is in database
            if ingredient in dict(i_db).keys() and isinstance(quantity, int):
                with shelve.open(self.file) as or_db:
                    # create a tag for the current order number
                    self.order_number = f'Order #{len(or_db)+1}'
                    or_db[self.order_number] = {"Ingredient": ingredient,
                                                    "Quantity": quantity}
                    # Update ingredient data
                    # Store the current row data of ingredient key
                    selected_ing = i_db[ingredient]
                    selected_ing['Quantity'] += quantity
                    # Update ingredient in database
                    i_db[ingredient] = selected_ing
                    print("New item data:", i_db[ingredient])
                    return True

        return False
