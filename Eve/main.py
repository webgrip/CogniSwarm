import sys
import time
import asyncio
import aiohttp

from retriever import WeaviateHybridSearchRetrieverWrapper
from langchain import OpenAI, LLMChain
from langchain.agents import (
    initialize_agent,
    load_tools,
    AgentType,
    ZeroShotAgent,
)
#from langchain.callbacks import AimCallbackHandler
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.tracers import LangChainTracer
from langchain.schema import Document
from langchain.memory import (
    ConversationBufferMemory,
    ReadOnlySharedMemory,
)
from langchain.prompts import PromptTemplate
from text_processing import TextProcessing
from tools import create_tools
from langchain.agents import Tool
from searxng_wrapper import SearxNGWrapper

# import lime

async def generate_concurrently(questions):
    agents = []
    
    for _ in questions:
        manager = CallbackManager([StdOutCallbackHandler()])
        llm = OpenAI(temperature=0, callback_manager=manager)
        async_tools = load_tools(["llm-math", "searxng"], llm=llm, aiosession=aiosession, callback_manager=manager)
        create_tools(llm_chain=llm_chain, memory=readonlymemory, callback_manager=manager)
        agents.append(
            initialize_agent(async_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, callback_manager=manager)
        )
        tasks = [async_agent.arun(q) for async_agent, q in zip(agents, questions)]
        await asyncio.gather(*tasks)

    s = time.perf_counter()
    await asyncio.run(generate_concurrently())
    elapsed = time.perf_counter() - s
    print(f"Concurrent executed in {elapsed:0.2f} seconds.")

def generate_serially(questions):
    for q in questions:
        tools = load_tools(["searxng"], llm_chain=llm_chain)
        agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
        agent.run(q)

def findOpenApiDocumentationUrl(name):
    return search('does $name have an openapi spec? Give that to me')

def NLPProcessing():
     # Slightly tweak the instructions from the default agent
    openapi_format_instructions = """Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: what to instruct the AI Action representative.
        Observation: The Agent's response
        (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer. User can't see any of my observations, API responses, links, or tools.
        Final Answer: the final answer to the original input question with the right amount of detail

        When responding with your Final Answer, remember that the person you are responding to CANNOT see any of your Thought/Action/Action Input/Observations, so if there is any relevant information there you need to include it explicitly in your response."""

    speak_toolkit = NLAToolkit.from_llm_and_url(llm, findOpenApiDocumentationUrl("speak"), "https://api.speak.com/openapi.yaml")
    klarna_toolkit = NLAToolkit.from_llm_and_url(llm, findOpenApiDocumentationUrl("speak"), "https://www.klarna.com/us/shopping/public/openai/v0/api-docs/")

    natural_language_tools = speak_toolkit.get_tools() + klarna_toolkit.get_tools()
    mrkl = initialize_agent(natural_language_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                        verbose=True, agent_kwargs={"format_instructions":openapi_format_instructions})

def process_data(data, mode):
    
    text_processing = TextProcessing()

    # Customize the number of sections based on the mode
    num_sections = {
        'dry': 0,
        'minimal': 1,
        'full': len(data["sections"])
    }[mode]

    estimated_total_tokens = 0
    estimated_total_duration = 0
    total_cost = 0
    cost_per_token = 0.0006  # You can adjust this

    for i in range(num_sections):
        # Create document
        section_text = data["sections"][i]["text"]
        section_title = data["sections"][i]["title"]
        
        document = Document(
            text=section_text,
            meta={
                "name": section_title,
                "url": data["url"]
            }
        )

        document.meta["sentiment"] = text_processing.analyze_sentiment(section_text)

        document.meta["summary"] = text_processing.get_summary(section_text)

        tokens = text_processing.count_tokens(section_text)
        document.meta["tokens"] = tokens

        estimated_duration = len(section_text) / 2000 * 5  # Assumes 2000 tokens per second
        estimated_total_duration += estimated_duration
        estimated_total_tokens += tokens
        cost = tokens * cost_per_token * estimated_duration
        total_cost += cost
        
        document.meta["cost"] = cost

        
        document_store.write_documents([document])

        # Log metadata
        


def x():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dry"
    
    
    #explainer = lime.LimeTextExplainer(...)
    
    tracer = LangChainTracer()
    tracer.load_default_session()
    manager = CallbackManager([StdOutCallbackHandler(), tracer])

    openai = OpenAI(temperature=0, callback_manager=manager)
    
    memory = ConversationBufferMemory(memory_key="chat_history")
    readonlymemory = ReadOnlySharedMemory(memory=memory)

    template = """Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [human_input_required, bash, search, summarize]
        Action Input: what to instruct the AI Action representative.
        Observation: The Agent's response
        (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer. User can't see any of my observations, API responses, links, or tools.
        Final Answer: the final answer to the original input question with the right amount of detail

        When responding with your Final Answer, remember that the person you are responding to CANNOT see any of your Thought/Action/Action Input/Observations, so if there is any relevant information there you need to include it explicitly in your response.

        Chat history: {chat_history}

        Question: {input}

        {agent_scratchpad}
        
    """
    

    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )

    # Create LLMChain object with prompt
    llm_chain = LLMChain(prompt=prompt, llm=openai, verbose=True)

    tools = create_tools(llm_chain=llm_chain, memory=readonlymemory, manager=manager)

    tools = [
        Tool(
            name="Intermediate Answer",
            func=SearxNGWrapper().run,
            description="useful for when you need to ask with search"
        )
    ]


    ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

    agent = initialize_agent(
        tools,
        openai,
        memory=readonlymemory,
        agent=AgentType.SELF_ASK_WITH_SEARCH,
        callback_manager=manager,
        max_execution_time=5,
        max_iterations=10,
        early_stopping_method="generate",
        #return_intermediate_steps=True,
        verbose=True,
    )

    start_time = time.time()

    result = agent.run("Create a task list for the following tasks that a 'developer' agent AI use execute: write a python file exactly like this one, except it should tell this one what to do. I want it to continuously create 5 tasks for itself, and the 'developer' (this script) that make the most sense to proceed with, keeping the goal in mind.")
    print(result)

    #process_data(result,  mode)

    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


    #aim_callback = AimCallbackHandler(
    #    repo=".",
    #    experiment_name="scenario 1: OpenAI LLM",
    #)

    #aim_callback.flush_tracker(langchain_asset=agent, reset=False, finish=True)
    
if __name__ == "__main__":
    x()