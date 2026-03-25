from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from ddgs import DDGS


class AgentState(TypedDict, total=False):
    query: str
    results: List[str]
    summary: str
    issues: List[str]



def search(state: AgentState):
    query = state.get("query", "")
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            if "body" in r:
                results.append(r["body"])

    return {"results": results}



def summarize(state: AgentState):
    results = state.get("results", [])
    summary = " ".join(results[:2]) if results else "No data found"
    return {"summary": summary}



def critique(state: AgentState):
    combined = " ".join(state.get("results", []))

    issues = []
    if len(combined) < 200:
        issues.append("Not enough information")
    if "research" not in combined.lower():
        issues.append("Lacks technical depth")

    return {"issues": issues}



def improve(state: AgentState):
    query = state.get("query", "")
    new_query = query + " latest research 2025"
    return {"query": new_query}



def decide(state: AgentState):
    if state.get("issues"):
        return "improve"
    return END



builder = StateGraph(AgentState)

builder.add_node("search", search)
builder.add_node("summarize", summarize)
builder.add_node("critique", critique)
builder.add_node("improve", improve)

builder.set_entry_point("search")

builder.add_edge("search", "summarize")
builder.add_edge("summarize", "critique")

builder.add_conditional_edges("critique", decide)

builder.add_edge("improve", "search")

graph = builder.compile()



result = graph.invoke({
    "query": "latest breakthrough in SNNs"
})

print("\n✅ Final Summary:")
print(result.get("summary", "No summary"))