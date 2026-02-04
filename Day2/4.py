from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOllama(model="gemma2:2b")

system_prompt = """
You are a meeting assistant. Summarize the following transcript into structured Markdown with sections: Decisions and Action Items. For each action item, include owner, deadline, and confidence score. Context: {transcript_text}
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template("{transcript_text}")
])



while True:
    text = input("Enter the transcript text: ")
    response = llm.invoke(template.format(
                    transcript_text = text
                ))
    print(f"Assistant : {response.text}")