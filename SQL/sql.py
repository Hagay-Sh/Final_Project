import sqlalchemy as db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

def update_schedule( in_date, in_time, in_position, in_available):
    """This fuction recieves a date and update the sql database with the new schedule"""
    # Create Connection to Sql Server "Tech"
    SERVER = 'HAGAY_SHMOOL'
    DATABASE = 'Tech'
    DRIVER = 'ODBC+Driver+17+for+SQL+Server'
    # If you want to use environment variables for credentials, uncomment the following lines:  
    # Load environment variables from .env file
    load_dotenv()
    USERNAME = os.getenv('SQL_USERNAME')
    PASSWORD = os.getenv('SQL_PASSWORD')
    DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
    # Using SqlAlchemy we're starting the connection
    engine = db.create_engine(DATABASE_CONNECTION)
    connection = engine.connect()
    Base = declarative_base()
    class Schedule(Base):
        __tablename__ = 'schedule'
        ScheduleID = Column(Integer, primary_key=True)
        date = Column(String)
        time = Column(String)
        position = Column(String)
        available = Column(String)

    session = sessionmaker(bind=engine)
    #date_string = "2025-06-18"
    date_string = in_date
    date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
    #time_string = "21:21:00"
    time_string = in_time
    time_object = datetime.strptime(time_string, "%H:%M:%S").time()
    new_event = Schedule( date=date_object,time=time_object, position=in_position, available=in_available)
    session.add(new_event)
    session.commit()
    session.close()
    connection.close()  # --> Close the connection to the database
    return



#metadata =db.MetaData()
#pd.set_option('display.max_rows', None) # --> Code to set the property display.max_rows to None --> it means that we will "see" all rows of the DataFrame in our case "data"
#data = pd.read_sql_query(text("Select * from Schedule"),connection) # --> Query database and save result to a DataFrame
#dp = db.Table('Schedule',metadata,autoload_with=engine)
#print(dp.columns.keys())  # --> Table Metadata
#query = db.select(dp)                   # --> query: is the object containing our "select statement" on "dp" object that has "Dim_Products", So "query" = "select * from Dim_Products"
#ResultProxy = connection.execute(query)   # --> ResultProxy: The object returned by the .execute() method. It can be used in a variety of ways to get the data returned by the query
#ResultSet = ResultProxy.fetchall()        # --> The actual data asked for in the query when using a fetch method such as .fetchall() on a ResultProxy.
 #Session = sessionmaker(bind=engine)
#session = Session()