from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOllama(model="gemma2:2b")

system_prompt = """
You are an HR compliance auditor. Review the following policy text and identify missing compliance clauses, ambiguous language, and suggest improvements. 
Return output in JSON format with keys: issues, severity, recommendations. 
Cite references where applicable. 
Context: {policy_text}
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("{policy_text}")
])



while True:
    text = input("Enter the policy text: ")
    response = llm.invoke(template.format(
                    policy_text = text
                ))
    print(f"Assistant : {response.text}")