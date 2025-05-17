import os
from dotenv import load_dotenv

# # === Load environment variables from .env file ===
# load_dotenv()

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain_core.tracers.langchain import LangChainTracer
from langchain.callbacks.manager import CallbackManager

# === Step 1: Set LangSmith tracing variables directly ===
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "LLM-GPT4o-Reasoning"

# === Step 2: Set OpenAI Key ===
os.environ["OPENAI_API_KEY"] = "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"

# === Step 3: Define Tools ===
def calculator(x: str) -> str:
    try:
        return str(eval(x))
    except:
        return "Invalid expression"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for evaluating math expressions like '3 * (2 + 1)'"
    )
]

# === Step 4: Setup LangSmith tracer ===
tracer = LangChainTracer()
callback_manager = CallbackManager([tracer])

# === Step 5: Create LLM + Agent ===
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    callback_manager=callback_manager
)

# === Step 6: Get user input ===
question = input("💬 Ask a math question: ")
response = agent.run(question)
print("✅ Final Answer:", response)
