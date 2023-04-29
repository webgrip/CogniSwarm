import os
import math
import weaviate

from typing import Optional

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.tracers import LangChainTracer
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental.autonomous_agents.baby_agi import BabyAGI
from langchain.vectorstores import Weaviate
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.output_parsers import ( RetryWithErrorOutputParser, PydanticOutputParser )
from pydantic import BaseModel, Field, validator
from langchain import PromptTemplate
from prompts.AutonomousAgentPromptTemplate import AutonomousAgentPromptTemplate
from output_parsers.CustomOutputParser import CustomOutputParser
from langchain.agents import AgentType
from langchain.agents import initialize_agent

from agents.AutonomousAgent import AutonomousAgent
from tools import create_tools

from langchain.chat_models import ChatOpenAI

from langchain.chains import RetrievalQA
from datetime import datetime
import platform
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)


WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "")
WEAVIATE_VECTORIZER = os.getenv("WEAVIATE_VECTORIZER", "")

tracer = LangChainTracer()
tracer.load_session('test')
callback_manager = CallbackManager([StdOutCallbackHandler(), tracer])

openai = OpenAI(callback_manager=callback_manager)

memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=memory)

client = weaviate.Client(
    url=WEAVIATE_HOST,
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},
)

client.schema.delete_all()

schema = {
    "classes": [
        {
            "class": "Paragraph",
            "vectorizer": "text2vec-openai",
              "moduleConfig": {
                "text2vec-openai": {
                  "model": "ada",
                  "modelversion": "002",
                  "type": "text"
                }
              },
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "The content of the paragraph",
                    "moduleConfig": {
                        "text2vec-openai": {
                          "skip": False,
                          "vectorizePropertyName": False
                        }
                      },
                    "name": "content",
                },
            ],
        },
    ]
}
client.schema.create(schema)


embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")

def relevance_score_fn(score: float) -> float:
    return 1.0 - score / math.sqrt(2)

vectorstore = Weaviate(client, "Paragraph", "content", embedding=embeddings_model, relevance_score_fn=relevance_score_fn)
retriever = TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, other_score_keys=["importance"], k=15)

llm = OpenAI(model="text-davinci-003", temperature=0.415, max_tokens=1500, streaming=True, callback_manager=callback_manager)

##### IDEA: Make a prompt, and let this thing generate the descriptions of what it is and what it's doing, still keep the {objective}
#### TODO Playwright


## THIS IS A TOOL

todo_prompt = PromptTemplate.from_template("You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}")
todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt, callback_manager=callback_manager)

tools = create_tools(callback_manager=callback_manager)


# Make multiple vectorstores, one for memory of tasks, one for memory of autonomous agent, one for general memory?

vectorstore_info = VectorStoreInfo(
    name="Memory",
    description="Useful for when you need to quickly access memory of events and people and things that happened recently or longer ago. Always do this first whenever you need external information.",
    vectorstore=vectorstore
)

toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

llm = OpenAI(model="text-davinci-003", temperature=0.415, max_tokens=1500, streaming=True, callback_manager=callback_manager)
             

agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    callback_manager=callback_manager
)

memory_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

tools.append(
    Tool(
        name="TODO",
        func=todo_chain.run,
        description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
        callback_manager=callback_manager,
        return_direct=True
    )
)

tools.append(
    Tool(
        name="Memory",
        func=memory_chain.run,
        description="Always do this first. Useful for when you need to access memory of events or people or things that happened recently or longer ago.",
        callback_manager=callback_manager,
        return_direct=True
    )
)

#prompt = ZeroShotAgent.create_prompt(
#    tools=tools,
#    prefix="You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}.",
#    suffix="Question: {task}\n{agent_scratchpad}",
#    input_variables=["objective", "task", "context", "agent_scratchpad"],
#)

OBJECTIVE = "Write me a detailed prompt that's meant to be used for an AGI to execute specific specialized tasks"


tools_summary = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
tool_names = ", ".join([tool.name for tool in tools])
allowed_tools = [tool.name for tool in tools]


with open('prompts/ryan.txt', 'rb') as fp:
            template = fp.read()

parser = CustomOutputParser()
formatted_prompt = AutonomousAgentPromptTemplate(
    input_variables=[ "operating_system", "objective", "task", "agent_name", "input", "intermediate_steps", "agent_scratchpad"],
#output_keys=['intermediate_steps', 'output'],
    partial_variables={"agent_summary": generative_agent.get_summary(True)},
    #output_parser=parser,
    template=template,
    tools=tools
)

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={
        #"output_parser": parser,
        #"system_message": self.system_message
    },
    #agent_kwargs=
    #    {
    #        'llm_chain':llm_chain,
    #        'allowed_tools': tool_names
    #    }
    #,
    early_stopping_method="generate",
    callback_manager=callback_manager,
    memory=readonlymemory,
    
    llm_chain=LLMChain(
        llm=llm,
        prompt=formatted_prompt,
        callback_manager=callback_manager,
        memory=readonlymemory,
        output_key='output'
    ),
    allowed_tools=tool_names,
)

baby_agi = BabyAGI.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    task_execution_chain=agent_executor,
    verbose=True,
    max_iterations=10
)

baby_agi(
    {
        "objective": OBJECTIVE,
        "task": OBJECTIVE,
        "agent_name": "Ryan",
        "operating_system": operating_system,
        "tool_names": tool_names,
        "tools_summary": tools_summary,
        "agent_summary": autonomousAgent.get_summary(True)
    },
)