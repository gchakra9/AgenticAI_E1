from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOllama(model="gemma2:2b")

system_prompt = """
You are a project manager drafting a client email. 
Write a formal email summarizing project progress, upcoming milestones, and request feedback. 
Include placeholders for [Client Name], [Project Name], and [Deadline]. 
Add a bullet list of action items.
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("{project_details}")
])



while True:
    project_details = input("Enter the project details/context: ")
    response = llm.invoke(template.format(
        project_details=project_details
    ))
    print(f"Assistant : {response.text}")
