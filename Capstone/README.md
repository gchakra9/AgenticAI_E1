# AI-Powered Customer Support Email Agent

## Overview

This project implements an **AI-powered customer support agent** that can automatically handle customer emails from reading to drafting replies, while intelligently escalating complex cases to human agents when required. The agent is designed using **LangGraph** with an **LLM (Qwen3)** for classification and response generation.

The agent is capable of:

* Reading and parsing incoming emails.
* Classifying emails by **urgency** and **topic**.
* Searching a knowledge base for relevant information.
* Drafting professional responses.
* Escalating complex or high-priority issues to human agents.
* Handling follow-up actions if necessary.

---

## Architecture

The agent is implemented as a **state graph** with nodes representing discrete steps in the email processing workflow.

### Core Components

1. **LLM**: Used for email classification and drafting replies.
2. **EmailAgentState**: Stores the current state of the email, including content, classification, KB search results, draft response, messages, and whether human review is needed.
3. **State Graph Nodes**: Each node represents a specific processing step (read email, classify email, search KB, etc.).
4. **Routing Logic**: Determines which path the email should take based on classification.

---

### State Definitions

#### EmailClassification

```python
EmailClassification:
    intent: Literal["question", "bug_report", "billing_issue", "feature_request", "technical_issue"]
    urgency: Literal["low", "medium", "high"]
    topic: Literal["account", "billing", "bug", "feature_request", "technical"]
    summary: str
```

#### EmailAgentState

```python
EmailAgentState:
    email_content: str
    sender_email: str
    email_id: str

    classification: EmailClassification
    search_results: List[str]
    draft_response: str
    messages: List[str]
    needs_human_review: bool
```

---

## Workflow

The agent processes emails through the following steps:

1. Read Email (`read_email`):

   * Parses incoming email content.
   * Adds a log message confirming the email has been read.

2. Classify Email (`classify_email`):

   * Uses the LLM to classify email intent, urgency, topic, and generate a summary.
   * Determines if human review is required:

     * Any High urgency or Bug/Technical Issue triggers human review.

3. Route Based on Classification (`route_after_classification`):

   * `bug` → `bug_tracker`
   * `account`, `billing`, `technical` → `doc_search`
   * Others → `human_review`

4. Document Search (`doc_search`):

   * Queries a dummy knowledge base for relevant Q&A based on the email topic.
   * Example KB entries:

     Account: How to reset password, change email.
     Billing: Duplicate charge, plan upgrade.
     Bug: Export crashes, file upload issues.
     Feature Request: Dark mode, multi-language support.
     Technical: API 504 errors, login issues.

5. Bug Tracker (`bug_tracker`):

   * Logs bug reports into a dummy tracking system.

6. Human Review (`human_review`):

   * Escalates complex or high-priority emails to a human agent.
   * Marks `needs_human_review = True`.

7. Draft Reply(`draft_reply`):

   * Generates a professional response using the LLM.
   * Incorporates knowledge base content when available.

8. Send or Escalate (`send_or_escalate`):

   * If `needs_human_review` → waits for human approval.
   * Otherwise → auto-sends the reply.

---



## Installation

```bash
# Clone repository
git clone <repo-url>
cd <repo-folder>

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies**:

* langgraph
* langchain_ollama
* Python 3.13+

---

## Usage

The agent can run with dummy or user-provided input.

```python
from email_agent import get_initial_state, email_agent

# Create initial state (user input)
initial_state = get_initial_state(
    email_content="I was charged twice for my subscription this month!",
    sender_email="user@example.com",
    email_id="email-001"
)

# Run the agent
final_state = email_agent.invoke(initial_state)

# View results
print("Classification:", final_state["classification"])
print("Draft Response:", final_state["draft_response"])
print("Messages:", final_state["messages"])
```

---

## Escalation Logic

* Emails with High urgency or Bug/Technical Issue → escalated to a human agent.
* Auto-replies are sent only if the email is low urgency and solvable via KB content.

---

## Follow-ups

* If an email is escalated (`needs_human_review=True`), the system waits for human approval before sending the reply.
* For low-priority emails, auto-replies are dispatched immediately using relevant KB answers.

---

## Design Considerations

Stateful Design: `EmailAgentState` tracks all necessary information for processing.
Extensible KB: `doc_search` can be connected to a real knowledge base or FAQ API/Vector DB.
Flexible Routing: Easy to add new topics or intents with minimal code changes.
LLM-Powered: Handles both classification and response generation, making it dynamic and adaptable.

---


