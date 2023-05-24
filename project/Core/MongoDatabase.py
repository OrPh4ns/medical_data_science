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

env = dotenv_values()
db_host = env['MONGOHOST']
db_port = env['MONGOPORT']
mongoclient = pymongo.MongoClient("mongodb://"+db_host+":"+db_port)
