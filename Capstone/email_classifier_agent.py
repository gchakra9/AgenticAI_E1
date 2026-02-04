from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Literal, Dict
from langchain_ollama import ChatOllama


llm = ChatOllama(model="Qwen3:0.6b", temperature=0)


class EmailClassification(TypedDict):
    intent: Literal[
        "question",
        "bug_report",
        "billing_issue",
        "feature_request",
        "technical_issue"
    ]
    urgency: Literal["low", "medium", "high"]
    topic: Literal[
        "account",
        "billing",
        "bug",
        "feature_request",
        "technical"
    ]
    summary: str

class EmailAgentState(TypedDict):
    email_content: str
    sender_email: str
    email_id: str

    classification: EmailClassification
    search_results: List[str]
    draft_response: str
    messages: List[str]

    needs_human_review: bool

# -------------------------------
# Nodes
# -------------------------------
def read_email(state: EmailAgentState) -> EmailAgentState:
    state["messages"].append("Email read and parsed")
    return state

def classify_email(state: EmailAgentState) -> EmailAgentState:
    prompt = f"""
Read the following email and classify it.

Email:
{state['email_content']}

Output format:
Intent: <one of question, bug_report, billing_issue, feature_request, technical_issue>
Urgency: <low, medium, high>
Topic: <account, billing, bug, feature_request, technical>
Summary: <brief summary of email>
"""
   
    response = llm.invoke(prompt).content.strip().split("\n")

    
    intent = "question"
    urgency = "low"
    topic = "account"
    summary = ""

    for line in response:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "intent":
            intent = value
        elif key == "urgency":
            urgency = value
        elif key == "topic":
            topic = value
        elif key == "summary":
            summary = value

    state["classification"] = EmailClassification(
        intent=intent,
        urgency=urgency,
        topic=topic,
        summary=summary
    )

    # Decide if human review is needed
    if intent in ["technical_issue"] or urgency == "high":
        state["needs_human_review"] = True
    else:
        state["needs_human_review"] = False

    return state

def doc_search(state: EmailAgentState) -> EmailAgentState:
    topic = state["classification"]["topic"]
    
    # Dummy Knowledge Base Q&A
    kb_articles = {
        "account": [
            "Q: How do I reset my password?\nA: You can reset your password by clicking 'Forgot Password' on the login page and following the instructions.",
            "Q: How do I change my account email?\nA: Go to Account Settings > Email > Edit to update your email address."
        ],
        "billing": [
            "Q: I was charged twice for my subscription!\nA: Please contact billing support at billing@example.com to resolve duplicate charges.",
            "Q: How do I upgrade my plan?\nA: You can upgrade your subscription in the Billing section of your account dashboard."
        ],
        "bug": [
            "Q: The export feature crashes when I select PDF format.\nA: This is a known bug. Please ensure you are using the latest app version; our team is working on a fix.",
            "Q: App crashes on file upload.\nA: Please try uploading smaller files (<5MB) or update your app."
        ],
        "feature_request": [
            "Q: Can you add dark mode to the mobile app?\nA: Thank you for the suggestion! Dark mode is under consideration for future releases.",
            "Q: Add multi-language support.\nA: We are planning to include multi-language support in upcoming updates."
        ],
        "technical": [
            "Q: Our API integration fails intermittently with 504 errors.\nA: Please check your request rate and ensure your server is responding within the timeout period. Contact support if the issue persists.",
            "Q: Cannot log in after password reset.\nA: Clear your browser cache and cookies, then try again."
        ]
    }

    # Select relevant KB articles based on topic
    state["search_results"] = kb_articles.get(topic, ["No relevant KB articles found."])
    state["messages"].append("Knowledge base searched with relevant Q&A")
    
    return state


def bug_tracker(state: EmailAgentState) -> EmailAgentState:
    summary = state["classification"]["summary"]
    state["messages"].append(f"Bug created in tracker: {summary}")
    return state

def human_review(state: EmailAgentState) -> EmailAgentState:
    state["messages"].append("Escalated to human support")
    state["needs_human_review"] = True
    return state

def draft_reply(state: EmailAgentState) -> EmailAgentState:
    classification = state["classification"]
    kb = "\n".join(state["search_results"])
    prompt = f"""
Write a professional customer support reply.

Email summary:
{classification['summary']}

Urgency:
{classification['urgency']}

Helpful info:
{kb}
"""
    state["draft_response"] = llm.invoke(prompt).content
    state["messages"].append("Draft reply created")
    return state

def send_or_escalate(state: EmailAgentState) -> EmailAgentState:
    if state["needs_human_review"]:
        state["messages"].append("Waiting for human approval")
    else:
        state["messages"].append("Auto-reply sent to customer")
    return state


def route_after_classification(state: EmailAgentState) -> str:
    topic = state["classification"]["topic"]
    if topic == "bug":
        return "bug_tracker"
    elif topic in ["account", "billing", "technical"]:
        return "doc_search"
    else:
        return "human_review"

# -------------------------------
# Build Graph
# -------------------------------
graph = StateGraph(EmailAgentState)

graph.add_node("read_email", read_email)
graph.add_node("classify_email", classify_email)
graph.add_node("doc_search", doc_search)
graph.add_node("bug_tracker", bug_tracker)
graph.add_node("human_review", human_review)
graph.add_node("draft_reply", draft_reply)
graph.add_node("send_or_escalate", send_or_escalate)

graph.set_entry_point("read_email")

graph.add_edge("read_email", "classify_email")

graph.add_conditional_edges(
    "classify_email",
    route_after_classification,
    {
        "doc_search": "doc_search",
        "bug_tracker": "bug_tracker",
        "human_review": "human_review",
    },
)

graph.add_edge("doc_search", "draft_reply")
graph.add_edge("bug_tracker", "draft_reply")
graph.add_edge("human_review", "draft_reply")

graph.add_edge("draft_reply", "send_or_escalate")
graph.add_edge("send_or_escalate", END)

email_agent = graph.compile()

# -------------------------------
# Helper function to create state from user input
# -------------------------------
def create_state_from_user_input() -> EmailAgentState:
    print("Please enter the following email details:")
    email_content = input("Email content: ").strip()
    sender_email = input("Sender email: ").strip()
    email_id = input("Email ID: ").strip()

    classification: EmailClassification = {
        "intent": "question",
        "urgency": "low",
        "topic": "account",
        "summary": "",
    }

    state: EmailAgentState = {
        "email_content": email_content,
        "sender_email": sender_email,
        "email_id": email_id,
        "classification": classification,
        "search_results": [],
        "draft_response": "",
        "messages": [],
        "needs_human_review": False,
    }

    return state

# -------------------------------
# Run the agent
# -------------------------------
if __name__ == "__main__":
    initial_state = create_state_from_user_input()
    final_state = email_agent.invoke(initial_state)

    print("\n--- FINAL OUTPUT ---")
    print("Classification:", final_state["classification"])
    print("Draft Response:\n", final_state["draft_response"])
    print("Messages:", final_state["messages"])

graph_image = email_agent.get_graph(xray=True).draw_mermaid_png()
with open("email_agent.png", "wb") as f:
    f.write(graph_image)