import pickle
import shelve

DATA = "restaurant_data.pkl"


class Ingredients:

    """
        This class loads in pickle file data for Ingredients.
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

        # populate database with starter data if it is empty
        self.file = file

        # Reference Week 10 Lecture
        self.db = shelve.open(self.file)

        # REMOVE LATER
        self.db.clear()

        # Reference: https://docs.python.org/3/library/shelve.html
        # If database has not been created (has no keys), then create
        if not list(self.db.keys()):
            # Store each item as a key in the db dict

            self.db["Bread Flour"] = {"Quantity": 13, "Unit": "5 KG", "Category": self.CATEGORIES[2], "Cost": 9.52}
            self.db["Gala Apples"] = {"Quantity": 14, "Unit": "4 LB", "Category": self.CATEGORIES[3], "Cost": 7.99}
            self.db["Chicken Thighs"] = {"Quantity": 16, "Unit": "1.5 KG", "Category": self.CATEGORIES[4], "Cost": 12.35}


    def get_all_ingredients(self):
        """
        Reference Week 10 Lecture

        Return a dict version of the database containing all the
        ingredients in the inventory
        """

        return dict(self.db)

    def get_ingredient(self, n):

        return dict(self.db)[n]


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

    def close(self):

        """Closes the open shelve database"""

        self.db.close()
