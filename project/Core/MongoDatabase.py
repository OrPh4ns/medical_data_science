"""
  ******************************************************************************
  * @project AMDS
  * @file    MongoDatabase.py
  * @author  THM Gesundheit Team
  * @brief   Configuration of Mongo database
  * @date    24.05.2023
  ******************************************************************************
"""

import pymongo
from dotenv import dotenv_values


# Load environment variables from the .env file
env = dotenv_values()
# Retrieve MongoDB connection details from the environment variables
db_host = env['MONGOHOST']
db_port = env['MONGOPORT']
try:
    mongoclient = pymongo.MongoClient("mongodb://" + db_host + ":" + db_port)
    # select the right database
    db = mongoclient['dicom']
    # select the right collection
    collection = db['dicom_header']
except:
    print("MongoDB connection error")