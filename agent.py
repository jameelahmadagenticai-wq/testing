
from langgraph.graph import StateGraph, END
from typing import TypedDict

from search import search
from scraper import scrape
from summarizer import summarize
from critique import critique

# -------------------------
# STATE (shared data)
# -------------------------
class AgentState(TypedDict):
    topic: str
    query: str
    combined_text: str
    summary: str
    critique: dict
    iteration: int
    logs: list

MAX_ITERATIONS = 3
THRESHOLD = 7

# -------------------------
# NODES
# -------------------------

def search_node(state: AgentState):
    query = state["query"]
    logs = state["logs"]

    logs.append(f"\n🔍 Iteration {state['iteration']+1} - Query: {query}")

    results = search(query)

    combined_text = ""

    for r in results:
        logs.append(f"🌐 Fetching: {r['link']}")
        content = scrape(r["link"])

        if len(content) < 200:
            continue

        combined_text += content

    if not combined_text:
        combined_text = " ".join([r["title"] for r in results])

    return {
        "combined_text": combined_text,
        "logs": logs
    }


def summarize_node(state: AgentState):
    summary = summarize(state["combined_text"])
    logs = state["logs"]

    logs.append(f"\n📝 Summary:\n{summary}")

    return {
        "summary": summary,
        "logs": logs
    }


def critique_node(state: AgentState):
    critique_result = critique(state["summary"])
    logs = state["logs"]

    logs.append(f"\n🧠 Critique:\n{critique_result}")

    return {
        "critique": critique_result,
        "logs": logs
    }


# -------------------------
# DECISION (LOOP CONTROL)
# -------------------------
def should_continue(state: AgentState):
    score = state["critique"]["score"]
    iteration = state["iteration"]

    if score >= THRESHOLD:
        state["logs"].append("\n✅ Good enough summary.")
        return END

    if iteration >= MAX_ITERATIONS - 1:
        state["logs"].append("\n⚠️ Max iterations reached.")
        return END

    # improve query
    new_query = state["topic"] + " " + state["critique"]["improved_query"]

    return "update_query"


def update_query_node(state: AgentState):
    new_query = state["topic"] + " " + state["critique"]["improved_query"]

    return {
        "query": new_query,
        "iteration": state["iteration"] + 1
    }


# -------------------------
# BUILD GRAPH
# -------------------------
builder = StateGraph(AgentState)

builder.add_node("search", search_node)
builder.add_node("summarize", summarize_node)
builder.add_node("critique", critique_node)
builder.add_node("update_query", update_query_node)

# flow
builder.set_entry_point("search")

builder.add_edge("search", "summarize")
builder.add_edge("summarize", "critique")

builder.add_conditional_edges(
    "critique",
    should_continue,
    {
        "update_query": "update_query",
        END: END
    }
)

builder.add_edge("update_query", "search")

graph = builder.compile()


# -------------------------
# MAIN FUNCTION (same API)
# -------------------------
def autonomous_agent(topic):
    result = graph.invoke({
        "topic": topic,
        "query": topic,
        "combined_text": "",
        "summary": "",
        "critique": {},
        "iteration": 0,
        "logs": []
    })

    return result["summary"], result["logs"]