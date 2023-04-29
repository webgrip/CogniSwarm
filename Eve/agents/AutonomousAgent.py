from functools import partial
from json import tool
import os
import math
from array import array
from langchain.llms.base import BaseLLM
from langchain.prompts import load_prompt
from langchain.vectorstores import Weaviate
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import BaseRetriever
import weaviate
from .GenerativeAgent import GenerativeAgent

# Helper function to create a default memory retriever
def create_new_memory_retriever_default():
    client = weaviate.Client(url=os.getenv("WEAVIATE_HOST"), additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")})
    embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = Weaviate(client, "Paragraph", "content", embedding=embeddings_model, relevance_score_fn=relevance_score_fn)
    return TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, other_score_keys=["importance"], k=15)

# Relevance score function
def relevance_score_fn(score: float) -> float:
    return 1.0 - score / math.sqrt(2)

class AutonomousAgent:

    def make_agent(self, name: str, age: int, traits: str, status: str, llm: BaseLLM, daily_summaries: array, reflection_threshold: int = 8, memory_retriever: BaseRetriever = create_new_memory_retriever_default(), verbose: bool = False):
        return GenerativeAgent(
            name=name,
            age=age,
            traits=traits,
            status=status,
            reflection_threshold=reflection_threshold,
            memory_retriever=memory_retriever,
            llm=llm,
            daily_summaries=daily_summaries,
            verbose=verbose
        )

    def get_prompt(self, generative_agent: GenerativeAgent, tools):

        


        


        #prompt = load_prompt("prompts/ryan.json")
        #prompt.partial()
        return load_prompt("prompts/ryan.json")
    
    #.format(
    #        task=objective,
    #        objective=objective,
    #        agent_name=generative_agent.name,
    #        operating_system=operating_system,
    #        tool_names=tool_names,
    #        tools_summary=tools_summary,
    #        agent_summary=generative_agent.get_summary(True)
    #    )