from dotenv import load_dotenv
import os


from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
