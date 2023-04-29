from langchain.agents import Tool
from langchain.prompts import BaseChatPromptTemplate
from typing import List
from langchain.schema import HumanMessage

class AutonomousAgentPromptTemplate(BaseChatPromptTemplate):
    template: str
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")

        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "

        kwargs["agent_scratchpad"] = thoughts

        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])

        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])

        formatted = self.template.format(**kwargs)

        return [HumanMessage(content=formatted)]