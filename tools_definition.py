from datetime import datetime, timedelta
from langchain.tools import tool
from datetime import date
from modouls.SQL import sql as sql
#from langchain_openai import ChatOpenAI


@tool
def get_next_three_dates( )-> list:
    """This fuction return 3 optional dates From Comapny Schedual Table.
    Dont use this function for booking an appointment.
    the output is a list of 3 strings, each string is a date in the format: 'Option 1: YYYY-MM-DD at HH:MM ID: 1234'.
    This Function is not booking any appointment, just returning the next 3 available dates."""
    lst = sql.get_schedule()
    id = lst[0][0]
    temp_date = lst[0][1].strftime("%Y-%m-%d")
    temp_time = lst[0][2]
    formatted_first_time = temp_time.strftime('%H:%M')
    first_schedule = f"Option 1: {temp_date} at {formatted_first_time} ID: {id}"
    id= lst[1][0]
    temp_date = lst[1][1].strftime("%Y-%m-%d")
    temp_time = lst[1][2]
    formatted_first_time = temp_time.strftime('%H:%M')
    second_schedule = f"Option 2: {temp_date} at {formatted_first_time} ID: {id}"
    id= lst[2][0]
    temp_date = lst[2][1].strftime("%Y-%m-%d")
    temp_time = lst[2][2]
    formatted_first_time = temp_time.strftime('%H:%M')
    third_schedule = f"Option 3: {temp_date} at {formatted_first_time} ID: {id}"
    return [
        first_schedule,
        second_schedule,
        third_schedule
    ]

    #retrurn  = lst
    # start_date should be a string in the format 'YYYY-MM-DD'
    #today_str = date.today().strftime("%Y-%m-%d")
    #date_obj = datetime.strptime(today_str, "%Y-%m-%d")
    #return [
    #    (date_obj + timedelta(days=3)).strftime("%Y-%m-%d"),
    #    (date_obj + timedelta(days=6)).strftime("%Y-%m-%d"),
    #    (date_obj + timedelta(days=9)).strftime("%Y-%m-%d"),
    #]
    
    
@tool
def end_conversation():
    """End the conversation with a polite message."""
    print("Thank you. This concludes our conversation.")

@tool
def BookMeetingSchduale(booking_details: str)-> str:
    """this fuction get an scheduale slot and update it in the comppany calendar.
    Use this function for booking an appointment.
    After that the meeting is booked."""
    sql.update_schdual_in_db(booking_details)
    msg = f"Thank you. The Meeting is Booked.\n{booking_details}"
    return msg
    #print("Thank you. The Meeting is Booked.")






