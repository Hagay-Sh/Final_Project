from datetime import datetime, timedelta
from langchain.tools import tool
#from langchain_openai import ChatOpenAI


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
import random as rnd

@tool
def get_next_three_dates(start_date: datetime)-> list:
    """This fuction recieves a date and then return 3 optional dates"""
    # start_date should be a string in the format 'YYYY-MM-DD'
    date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    return [
        (date_obj + timedelta(days=3)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=6)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=9)).strftime("%Y-%m-%d"),
    ]
    
    
@tool
def end_conversation():
    """End the conversation with a polite message."""
    print("Thank you. This concludes our conversation.")








