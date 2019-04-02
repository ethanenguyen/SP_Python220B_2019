"""
This program will read and write data to a mongoDB database
"""

import logging
import csv
import pymongo
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """Initiates the connection settings"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connects to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Disconnects from MongoDB"""
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name and three csv files and creates/populates a new
       MongoDB database with the data. It then returns two tuples: The first contains a record
       count of the number of products, customers and rentals added. The second contains a count
       of any errors that occurred in products, customers, and rentals"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.rental_company

        product = db["product"]
        customer = db["customer"]
        rentals = db["rentals"]

        try:
            with open(product_file, 'r') as product_csv:
                csv_reader = csv.reader(product_csv, delimiter=',', quotechar='"')
                for row in csv_reader:
                    result = product.insert_one(row)
        except FileNotFoundError:
            LOGGER.error("could not find %s", product_file)

        try:
            with open(customer_file, 'r') as customer_csv:
                csv_reader = csv.reader(customer_csv, delimiter=',', quotechar='"')
                for row in csv_reader:
                    result = customer.insert_one(row)
        except FileNotFoundError:
            LOGGER.error("could not find %s", customer_file)

        try:
            with open(rentals_file, 'r') as rentals_csv:
                csv_reader = csv.reader(rentals_csv, delimiter=',', quotechar='"')
                for row in csv_reader:
                    result = rentals.insert_one(row)
        except FileNotFoundError:
            LOGGER.error("could not find %s", rentals_file)

def show_available_products():
    """Returns a Python dictionary of products listed as available"""

def show_rentals(product_id):
    """Return a Python dictionary from users that have rented products matching the product_id"""

if __name__ == "__main__":