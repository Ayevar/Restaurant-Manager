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

        """USE TO CLEAR ALL DATA"""
        # with shelve.open(self.file) as db:
        #     db.clear()


        """Use to create some auto testing data"""
        # with shelve.open(self.file) as db:
        #     if not list(db.keys()):
        #         db["Bread Flour"] = {"Quantity": 17,
        #                              "Unit": "5 KG",
        #                              "Category": self.CATEGORIES[2],
        #                              "Cost": 9.52
        #                             }
        #         db["Gala Apples"] = {"Quantity": 19,
        #                              "Unit": "4 LB",
        #                              "Category": self.CATEGORIES[3],
        #                              "Cost": 7.99
        #                             }
        #         db["Chicken Thighs"] = {"Quantity": 10,
        #                                 "Unit": "1.5 KG",
        #                                 "Category": self.CATEGORIES[4],
        #                                 "Cost": 12.35
        #                             }



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


    def add_ingredient(self, ingredient: str) -> bool:
        """
        Reference Week 10 Lecture

        add new ingredient type (key) to the database (by name only), ensure
        ingredient does not already exist (all info matches)
        """
        if ingredient in list(self.db.keys()):
            return False
        else:
            self.db[ingredient] = {
                "Quantity": "-", 
                "Unit": "-", 
                "Category": "-", 
                "Cost": "-"
            }
            return True


    def remove_ingredient(self, ingredient: str) -> bool:
        """
        remove ingredient key to the database, ensure
        ingredient is in database before deleting key.

        *** Returns True if ingredient is in database, False if successfully deleted
        """
        if ingredient not in list(self.db.keys()):
            return False
        else:
            self.db[ingredient].pop()
            return True


class OrderStorage:
    """
    load and update user order data.


    Example of data structure:
        Orders = {"Ingredient": ingredient, "Quantity": quantity,
        "Date Ordered": current_time, "Arrival Date": arrival_time,
        "Status": "Pending", "Cost": price}
    """

    def __init__(self, file):

        # populate database with starter data
        self.file = file
        self.order_number = ""

        # Reference: https://docs.python.org/3/library/datetime.html
        # use datetime to get current time
        self.order_data = datetime.now()

        """USE TO CLEAR DATA"""
        # with shelve.open(self.file) as db:
        #     db.clear()

        
    def get_orders(self):
        """
        Reference Week 10 Lecture

        Return a dict version of the database containing all the
        order history
        """
        with shelve.open(self.file) as db:
            return dict(db)


    def get_order(self, n):
        """
            Reference Week 10 Lecture
            return single order
        """
        with shelve.open(self.file) as db:
            return dict(db.get(n))


    def create_order(self, ingredient, quantity, shipping='Same Day'):

        """
        Create an order object in the data. Check if valid ingredient is being
        considered, if quantity is a digit entry and when arrival date for
        object should be set too.

        :param ingredient:
        :param quantity:
        :param shipping:
        :return:
        """


        # Open ingredient database and order database
        with shelve.open(ING_DATA, writeback=True) as i_db:

            # Check if ingredient is in database and quantity is valid
            if ingredient in dict(i_db).keys() and quantity.isdigit() and int(quantity) >= 1:
                with shelve.open(self.file) as or_db:

                    # quantity is made up of only numbers, so convert to an int
                    quantity = int(quantity)

                    # create a tag for the current order number
                    self.order_number = f'Order #{len(or_db) + 1}'
                    # Get the current time and save it in our dictionary as a String
                    current_time = datetime.now().strftime("%y-%m-%d, %H:%M")
                    arrival_time = datetime.strptime(current_time, "%y-%m-%d, %H:%M")
                    if shipping == '1 day':
                        price = 1.10
                        arrival_time += timedelta(days=1)
                    elif shipping == '3 day':
                        price = 1
                        arrival_time += timedelta(days=3)
                    else:
                        price = 1.25
                        arrival_time += timedelta(hours=6)
                    arrival_time = arrival_time.strftime("%y-%m-%d, %H:%M")
                    price = round(i_db[ingredient]["Cost"]*price, 2) * quantity
                    or_db[self.order_number] = {"Ingredient": ingredient, 
                                                "Quantity": quantity, 
                                                "Date Ordered": current_time,
                                                "Arrival Date": arrival_time, 
                                                "Status": "Pending", 
                                                "Cost": price
                                            }
                    return True
        return False


    def remove_order(self, order: str) -> bool:
        """
        remove ingredient key to the database, ensure
        ingredient is in database before deleting key.

        *** Returns True if ingredient is in database, False if successfully deleted
        """
        if order not in list(self.db.keys()):
            return False
        else:
            self.db[int(order)]['Status'] = 'Cancelled'
            return True
