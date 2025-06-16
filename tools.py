from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from datetime import datetime, timedelta


@tool
def get_next_three_dates(start_date):
    'This fuction recieves a date and then return 3 optional dates'
    # start_date should be a string in the format 'YYYY-MM-DD'
    date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    return [
        (date_obj + timedelta(days=3)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=6)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=9)).strftime("%Y-%m-%d"),
    ]
    
    

@tool
def multiply(a: int) -> int:
    """Multiply a number by 2."""
    return a * 2

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

@tool
def get_country_capital(country: str) -> str:
    """Return the capital city of a given country."""
    capitals = {
        "France": "Paris",
        "Israel": "Jerusalem",
        "USA": "Washington, D.C."
    }
    return capitals.get(country, "Unknown")

# Define the tools
#tools = [add_numbers, get_country_capital]
tools = [get_next_three_dates]


# Define the LLM (language model)
llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0)

# Main agent: Handles chat and decides when to call advisor
main_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an assistant in a company. If the user wants to schedule an appointment, respond: "
     "'I will check available slots for you.' Otherwise, answer normally."),
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
advisor_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an appointment advisor. Extract any preferred dates from the full conversation. "
     "Then, suggest 3 possible appointment slots for the user, in this format:\n"
     "- Option 1: ...\n- Option 2: ...\n- Option 3: ...\n"
     "You can use the tools provided"
     "If no date is found, suggest generic options for next week."),
     MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

advisor_agent = create_openai_tools_agent(llm, tools, prompt=advisor_prompt)
advisor_executor = AgentExecutor(agent=advisor_agent, tools=tools, verbose=True)

def orchestrate_conversation_with_memory(user_input, session_id="user1"):
    """
    Handles one turn of user input for the main agent (with memory),
    and if needed, passes the full memory/history to the advisor agent.
    """


    # Main agent receives latest user message (memory auto-injects context)
    main_output = main_agent_with_memory.invoke({"input": user_input},config={"configurable": {"session_id": session_id}})["output"]
    print("Main Agent:", main_output)
    print("\n")

    # If scheduling is detected, advisor gets *full conversation* from memory
    if "I will check available slots for you" in main_output:
        
        # Retrieve full history from memory
        full_history = store[session_id].messages
        full_convo = "\n".join([f"{m.type.capitalize()}: {m.content}" for m in full_history])
        
        advisor_response = advisor_executor.invoke({"input": full_convo})["output"]
        print("\n\n")
        print("Advisor Agent:\n", advisor_response)
        
        

session_id = "user77"
# Turn 1
orchestrate_conversation_with_memory("Hi! I want to learn about your company.", session_id=session_id)

# Turn 2
orchestrate_conversation_with_memory("I'd like to schedule an appointment on 2024-09-02.", session_id=session_id)
# ...keep calling per turn as needed...

