import modouls.tools_definition as ts
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# Define the tools
#tools = [add_numbers, get_country_capital]
tools = [ts.get_next_three_dates, ts.end_conversation, ts.BookMeetingSchduale]
# Define the LLM (language model)
llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0)

# Main agent: Handles chat and decides when to call advisor
main_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an assistant in a softare company that recruit for python developer position."
     "If the user wants to schedule an appointment, respond: 'I will check available slots for you.' Otherwise, answer normally."
     "If the user want to book sepcifice appointment, respond: 'I will book the appointment for you.'"
     "If the user wants to know more about the position, respond: 'Certainly! Here is more information about the position.'"
     "If the user want to finfish  the conversation , respond: 'Thank you. This concludes our conversation.'Otherwise, answer normally."),
     MessagesPlaceholder(variable_name="history"),
     MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

main_agent = create_openai_tools_agent(llm, tools=[], prompt=main_prompt)
main_executor = AgentExecutor(agent=main_agent, tools=[], verbose=False)


# Memory store for user sessions
store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Wrap the main agent executor with memory
main_agent_with_memory = RunnableWithMessageHistory(
    main_executor,
    get_session_history=get_history,
    input_messages_key="input",
    history_messages_key="history"
)


# Advisor agent: Receives the conversation, extracts the desired date, and suggests slots
schedual_advisor_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an appointment advisor. Extract any preferred dates from the full conversation. "
     "Then, suggest 3 possible appointment slots for the user, in this format:\n"
     "- Option 1: ...\n- Option 2: ...\n- Option 3: ...\n"
     "You can use the tools provided"
     "If no date is found, suggest generic options for next week."),
     MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

schedual_advisor_agent = create_openai_tools_agent(llm, tools, prompt=schedual_advisor_prompt)
schedual_advisor_executor = AgentExecutor(agent=schedual_advisor_agent, tools=tools, verbose=False)


# Advisor book agent: Receives the conversation, boook Secicfied appointment to the company calendar
book_advisor_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an book appointment advisor. after giving an appointment slot, you need to book it in the company calendar."
     "It is Mandatory to Arrange the input in this format: '2024-01-02 at 16:00 ID: 7309'"
     "You can use the tools provided"
     "If no date is given,  do nothing."
     "If no error occure in the booking process, respond: 'Thank you. The Meeting is Booked.'"
     "If  error occure in the booking process, respond: 'Error Occure . Lets try later.'"
     "Otherwise, answer normally."),
     MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

book_advisor_agent = create_openai_tools_agent(llm, tools, prompt=book_advisor_prompt)
book_advisor_executor = AgentExecutor(agent=book_advisor_agent, tools=tools, verbose=False)

# Advisor agent: Info abut the position 
info_advisor_prompt = ChatPromptTemplate.from_messages([
    ("system", 
    "You are an  advisor that give additional information about the position. and aim  to achedual ameeting with the user."
    "If the user wants to know more about the position,provide any information you have abut it.'"
    "The Position is a Python Developrt in software company in the usa."
   # "If the user didnt suggest to schedual ameeting , respond: 'Certainly! Can i Suggest you to schedual a meeting .' Otherwise, answer normally."
    "You can use the tools provided"),
     MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

info_advisor_agent = create_openai_tools_agent(llm, tools, prompt=info_advisor_prompt)
info_advisor_executor = AgentExecutor(agent=info_advisor_agent, tools=tools, verbose=False)


# Advisor agent: Finish the conversation
exit_advisor_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an  advisor that finish the conversation"
     "If the user wants to finish, respond: 'I will check available slots for you.' Otherwise, answer normally."
     "You can use the tools provided"),
     MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

exit_advisor_agent = create_openai_tools_agent(llm, tools, prompt=exit_advisor_prompt)
exit_advisor_executor = AgentExecutor(agent=exit_advisor_agent, tools=tools, verbose=False)



def orchestrate_conversation_with_memory(user_input, session_id)-> str:
    """
    Handles one turn of user input for the main agent (with memory),
    and if needed, passes the full memory/history to the advisor agent.
    """
    # Main agent receives latest user message (memory auto-injects context)
    main_output = main_agent_with_memory.invoke({"input": user_input},config={"configurable": {"session_id": session_id}})["output"]
    user_output = main_output  # Default to main agent's response
    advisor_response = ""  # Initialize advisor response
    print("Main Agent:", main_output)
    print("\n")
    # If scheduling is detected, advisor gets *full conversation* from memory
    if "I will check available slots for you" in main_output:
        # Retrieve full history from memory
        full_history = store[session_id].messages
        full_convo = "\n".join([f"{m.type.capitalize()}: {m.content}" for m in full_history])
        advisor_response = schedual_advisor_executor.invoke({"input": full_convo})["output"]
        print("\n\n")
        print("Advisor Agent:\n", advisor_response)
     
    elif "I will book the app" in main_output:
        full_history = store[session_id].messages
        full_convo = "\n".join([f"{m.type.capitalize()}: {m.content}" for m in full_history])
        advisor_response = book_advisor_executor.invoke({"input": full_convo})["output"]
        print("\n\n")
        print("Advisor Agent:\n", advisor_response)
    
    elif "Thank you. This concludes our conversation" in main_output:
        full_history = store[session_id].messages
        full_convo = "\n".join([f"{m.type.capitalize()}: {m.content}" for m in full_history])
        advisor_response = exit_advisor_executor.invoke({"input": full_convo})["output"]
        print("\n\n")
        print("Advisor Agent:\n", advisor_response)
    elif "Certainly! Here is more information about the position" in main_output:
        full_history = store[session_id].messages
        full_convo = "\n".join([f"{m.type.capitalize()}: {m.content}" for m in full_history])
        advisor_response = info_advisor_executor.invoke({"input": full_convo})["output"]
        print("\n\n")
        print("Advisor Agent:\n", advisor_response)

    if len(advisor_response) > 0:
        user_output = advisor_response   
    return user_output  

#session_id = rnd.randint(1000, 999999)  # Unique session ID for each conversation
#print(f"Session ID: {session_id}\n")
# Turn 1
#orchestrate_conversation_with_memory("Hi! I want to learn about your company.", session_id=session_id)

# Turn 2
#orchestrate_conversation_with_memory("I'd like to schedule an appointment on 2024-09-02.", session_id=session_id)
# ...keep calling per turn as needed...
# Turn 3
#orchestrate_conversation_with_memory("Lets finish the conversation", session_id=session_id)
# ...keep calling per turn as needed...