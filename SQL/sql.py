import sqlalchemy as db
from sqlalchemy import Date, create_engine, text, update, DateTime, Time
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String, create_engine
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'Schedule'  # name of the table in the DB
    ScheduleId = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    position= Column(String)
    available = Column(String)  


def get_schedule()-> list:
   # """This function retrieves the schedule from the SQL database and returns it as a DataFrame."""
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
    
    # Query database and save result to a DataFrame
    data = pd.read_sql_query(text("SELECT * FROM schedule where Schedule.available='1' and Schedule.position = 'Python Dev' ORDER BY date ASC, time ASC;"), connection)
    first_three = data[['ScheduleID','date','time']].head(3).to_records(index=False).tolist()
    connection.close()  # --> Close the connection to the database
    return first_three




def update_schdual_in_db(booking_details: str)-> str:
    """This function receives a booking details string and updates the SQL database with the new schedule.
    After that the meeting is booked."""
    
    tmp_arr = booking_details.split(" ")
    #print(booking_details)
    day = tmp_arr[0]
    time_s = tmp_arr[2]
    if 'ID' in booking_details:
        id = tmp_arr[4]  # Extracting the ID from the booking details
    position = "Python Dev"
    available = "0"
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
    # 2. Create session class
    Session = sessionmaker(bind=engine)
    # 3. Create session instance
    if 'ID' in booking_details:
        session = Session()
        session.query(User)\
        .filter(User.ScheduleId == id )\
        .update({User.date: day, User.time: time_s, User.position: position, User.available: available})
        session.commit()
    else:
        session = Session()
        session.query(User)\
        .filter(User.date == day and User.time == time_s)\
        .update({User.date: day, User.time: time_s, User.position: position, User.available: available})
        session.commit()
    
    connection.close()  # --> Close the connection to the database
    return "Thank you. The Meeting is Booked."







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