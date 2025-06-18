import sqlalchemy as db
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import os

# Create Connection to Sql Server "Tech"
SERVER = 'HAGAY_SHMOOL'
DATABASE = 'Tech'
DRIVER = 'ODBC+Driver+17+for+SQL+Server'
# If you want to use environment variables for credentials, uncomment the following lines:  
# Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv('USERNAME_1')
PASSWORD = os.getenv('PASSWORD_1')
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
# Using SqlAlchemy we're starting the connection
engine = db.create_engine(DATABASE_CONNECTION)
connection = engine.connect()
metadata =db.MetaData()

pd.set_option('display.max_rows', None) # --> Code to set the property display.max_rows to None --> it means that we will "see" all rows of the DataFrame in our case "data"
data = pd.read_sql_query(text("Select * from Schedule"),connection) # --> Query database and save result to a DataFrame

