from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatOllama(model="qwen3:0.6b", temperature=0)
parser = StrOutputParser()


system_prompt = """
You are a prompt quality evaluator.

Evaluate the prompt based on the following criteria:
1. Clarity (0-10): Is the prompt easy to understand and goal clear?
2. Specificity / Details (0-10): Are details and requirements sufficient?
3. Context (0-10): Is background, audience, or use case provided?
4. Output Format & Constraints (0-10): Are output format, tone, or length specified?
5. Persona defined (0-10): Is a role or perspective assigned?


Tasks:
1. Assign a score (0-10) for each criterion.
2. Provide a short explanation of your evaluation.
3. Give 2-3 suggestions to improve the prompt.
4. Calculate the final score as the average of the five criteria.

Provide the output as plain text.
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])


evaluation_chain = prompt_template | llm | parser

def evaluate_user_prompt(user_prompt: str):
    response = evaluation_chain.invoke({"input": user_prompt})
    return response

if __name__ == "__main__":
    while True:
        user_prompt_text = input("Enter a prompt to evaluate:\n")
        result = evaluate_user_prompt(user_prompt_text)
        print("\nEvaluation Result:\n", result)
        print("-" * 50)
