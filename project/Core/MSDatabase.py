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
from sqlalchemy import create_engine, String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, Session
import pyodbc


from dotenv import dotenv_values
env = dotenv_values()
db_host = env['MSSQLHOST']
db_port = env['MSSQLPORT']
db_user = env['MSSQLUSER']
db_pass = env['MSSQLPASS']
db_name = env['MSSQLNAME']


DATABASE_URL = "mssql+pyodbc://"+db_user+":"+db_pass+"@"+db_host+":"+db_port+"/"+db_name+"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
engine = create_engine(DATABASE_URL)
Base = sqlalchemy.orm.declarative_base()