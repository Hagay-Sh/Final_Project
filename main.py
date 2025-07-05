import sys
import os
from Agents import agents as ags  # Now you can import it
import random as rnd
from datetime import datetime, timedelta


session_id = rnd.randint(1000, 999999)  # Unique session ID for each conversation
print(f"Session ID: {session_id}\n")
#start_date = "2024-09-02"  # Example start date in 'YYYY-MM-DD' format
#date_obj = datetime.strptime(start_date, "%Y-%m-%d")
#print(f"Date : {date_obj}\n")

# The Conversation starts here
ags.orchestrate_conversation_with_memory("Hi! I want to learn about your company.", session_id=session_id)
#ags.orchestrate_conversation_with_memory("Hi! Iwant to learn abut yoyr services.", session_id=session_id)
ags.orchestrate_conversation_with_memory("Hi! i would like to make apointment for interview.", session_id=session_id)
ags.orchestrate_conversation_with_memory("I'd like to schedule the first option", session_id=session_id)