# Prompt Quality Scoring Agent

## Overview

This project is a Prompt Quality Scoring Agent built using LangChain and Ollama LLM.
The agent evaluates a user-provided prompt based on five quality criteria and provides:

* Scores for each criterion (0–10)
* A short explanation
* 2–3 suggestions to improve the prompt
* The final overall score (average of the five criteria)

The output is provided as plain text.

---

## Evaluation Criteria

1. **Clarity:** Is the prompt easy to understand and the goal clear?
2. **Specificity / Details:** Are sufficient details and requirements provided?
3. **Context:** Is background, audience, or use case provided?
4. **Output Format & Constraints:** Are output format, tone, or length specified?
5. **Persona defined:** Is a role or perspective assigned?

---

## Installation

1. **Clone the repository**

```bash
git clone <your-github-repo-url>
cd <repo-folder>
```

2. **Create a virtual environment (recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. **Install dependencies**

```bash
pip install langchain_ollama langchain_core
```

---

## Usage

1. Open the main Python file (e.g., `prompt_evaluator.py`) and run:

```bash
python3 prompt_evaluator.py
```

2. You will see a prompt:

```
Enter a prompt to evaluate:
```

3. Type your prompt text and press **Enter**.

4. The agent will output something like:

```
Evaluation Result:
Final Score: 8.2
Clarity: 9
Specificity: 7
Context: 8
Output Format & Constraints: 8
Persona defined: 8

Explanation: The prompt is mostly clear, but could include more context.
Suggestions:
1. Specify the target audience.
2. Include expected output format.
3. Define a persona if needed.
--------------------------------------------------
```

5. The program will continue to prompt for new inputs until you exit (Ctrl+C).

---

