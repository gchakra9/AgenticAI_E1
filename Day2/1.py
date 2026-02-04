from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOllama(model="gemma2:2b")

system_prompt = """
You are a financial analyst. Summarize the following quarterly report into a 150-word executive summary. 
Include a table of key metrics (Revenue, EPS, Growth %) and a section listing top risks and opportunities. 
Ensure all data is factual and derived from the context provided. 
Context: {report_text}
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("{report_text}")
])



while True:
    text = input("Enter the report text: ")
    response = llm.invoke(template.format(
                    report_text = text
                ))
    print(f"Assistant : {response.text}")