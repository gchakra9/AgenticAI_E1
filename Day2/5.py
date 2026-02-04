from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOllama(model="gemma2:2b")

system_prompt = """
You are a market research analyst. Generate a market analysis brief from the provided articles and reports. 
Include a SWOT analysis, top 3 trends with citations, and a narrative summary. 
Output JSON with keys: SWOT, trends, citations, and a separate narrative summary. 
Context: {documents}
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("{documents}")
])



while True:
    text = input("Enter the sample documents: ")
    response = llm.invoke(template.format(
                    documents = text
                ))
    print(f"Assistant : {response.text}")