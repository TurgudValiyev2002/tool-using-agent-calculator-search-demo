from pathlib import Path
import ast
import operator as op
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path("results")

DOCS = {
    "fedavg": "FedAvg trains local client models and averages their weights on a central server.",
    "rag": "RAG retrieves relevant documents before generating an answer.",
    "edge ai": "Edge AI runs models near sensors to reduce latency and bandwidth use.",
}
TASKS = [
    ("calculator", "What is 17 * 23 + 41?", "17 * 23 + 41"),
    ("search", "What does RAG do before answering?", "rag"),
    ("calculator", "What is (128 / 4) + 19?", "(128 / 4) + 19"),
    ("search", "Why use Edge AI near sensors?", "edge ai"),
]
OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}

def safe_eval(expr):
    node = ast.parse(expr, mode="eval").body
    def walk(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.BinOp):
            return OPS[type(n.op)](walk(n.left), walk(n.right))
        raise ValueError("unsupported expression")
    return walk(node)

def search(query):
    q = query.lower()
    best_key = max(DOCS, key=lambda k: len(set(q.split()) & set(DOCS[k].lower().split())))
    return DOCS[best_key]

def main():
    RESULTS.mkdir(exist_ok=True)
    rows = []
    for tool, question, payload in TASKS:
        if tool == "calculator":
            answer = safe_eval(payload)
        else:
            answer = search(payload)
        rows.append({"question": question, "selected_tool": tool, "tool_input": payload, "answer": answer})
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "agent_trace.csv", index=False)
    usage = df["selected_tool"].value_counts().rename_axis("tool").reset_index(name="count")
    usage.to_csv(RESULTS / "tool_usage.csv", index=False)
    plt.figure(figsize=(5,4))
    plt.bar(usage["tool"], usage["count"], color=["#3d6fb6", "#4a8f5a"])
    plt.ylabel("Number of calls")
    plt.title("Agent Tool Usage")
    plt.tight_layout()
    plt.savefig(RESULTS / "tool_usage.png", dpi=160)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
