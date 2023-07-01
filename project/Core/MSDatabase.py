"""
  ******************************************************************************
  * @project AMDS
  * @file    MSDatabase.py
  * @author  THM Gesundheit Team
  * @brief   Configuration of Microsoft database
  * @date    24.05.2023
  ******************************************************************************
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from Core.Base import Base

import pyodbc
from dotenv import dotenv_values

# Load environment variables from the .env file
env = dotenv_values()
# Retrieve database connection details from the environment variables
db_host = env['MSSQLHOST']
db_port = env['MSSQLPORT']
db_user = env['MSSQLUSER']
db_pass = env['MSSQLPASS']
db_name = env['MSSQLNAME']

# Construct the database URL for the SQLAlchemy engine
DATABASE_URL = "mssql+pyodbc://"+db_user+":"+db_pass+"@"+db_host+":"+db_port+"/"+db_name+"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# Set the Base class for declarative models
Base = Base

# Create a local session factory
session_local = sessionmaker(autocommit=False, autoflush=True, bind=engine)
# Connect to the database
con = engine.connect()
# Create an SQLAlchemy inspector for the engine
ins = sqlalchemy.inspect(engine)


def get_db(session):
    """
    this functions obtains a session object for querying the database
    :return:
    """
    database = session()
    try:
        yield database
    finally:
        database.close()


db = next(get_db(session_local))


def init_db():
    """
    initializes the statistics database
    """
    Base.metadata.create_all(bind=engine)
