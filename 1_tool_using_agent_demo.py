from pathlib import Path
import ast
import operator as op
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


RESULTS = Path("results")

DOCS = {
    "fedavg": "FedAvg trains local client models and averages their weights on a central server.",
    "rag": "RAG retrieves relevant documents before generating an answer.",
    "edge ai": "Edge AI runs models near sensors to reduce latency and bandwidth use.",
    "quantization": "Quantization stores model weights with fewer bits to reduce memory use.",
    "pruning": "Pruning removes low-importance weights to reduce model size and computation.",
}

TASKS = [
    {"question": "What is 17 * 23 + 41?", "expected_tool": "calculator", "payload": "17 * 23 + 41", "expected_contains": "432"},
    {"question": "What does RAG do before answering?", "expected_tool": "search", "payload": "rag", "expected_contains": "retrieves"},
    {"question": "What is (128 / 4) + 19?", "expected_tool": "calculator", "payload": "(128 / 4) + 19", "expected_contains": "51"},
    {"question": "Why use Edge AI near sensors?", "expected_tool": "search", "payload": "edge ai", "expected_contains": "latency"},
    {"question": "How does quantization reduce model memory?", "expected_tool": "search", "payload": "quantization", "expected_contains": "fewer bits"},
    {"question": "What is 14 squared minus 9?", "expected_tool": "calculator", "payload": "14 * 14 - 9", "expected_contains": "187"},
    {"question": "Which method removes low-importance weights?", "expected_tool": "search", "payload": "pruning", "expected_contains": "removes"},
    {"question": "Calculate the memory after compression", "expected_tool": "none", "payload": "", "expected_contains": "needs more information"},
    {"question": "Tell me something about tomorrow's weather", "expected_tool": "none", "payload": "", "expected_contains": "no available tool"},
    {"question": "Can you compare 8-bit quantization with pruning?", "expected_tool": "search", "payload": "quantization pruning", "expected_contains": "pruning"},
    {"question": "What is 2 plus the main risk of hallucination?", "expected_tool": "none", "payload": "", "expected_contains": "needs more information"},
]

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow}


def safe_eval(expr: str):
    node = ast.parse(expr, mode="eval").body

    def walk(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](walk(n.left), walk(n.right))
        raise ValueError("unsupported expression")

    return walk(node)


def search(query: str) -> str:
    q_words = set(re.findall(r"[a-z]+", query.lower()))
    best_key = max(DOCS, key=lambda k: len(q_words & set(re.findall(r"[a-z]+", (k + " " + DOCS[k]).lower()))))
    return DOCS[best_key]


def route_tool(question: str) -> str:
    q = question.lower()
    if any(token in q for token in ["what is", "calculate", "squared", "*", "/", "+", "-"]):
        if re.search(r"\d", q) and ("weather" not in q):
            return "calculator"
    if any(token in q for token in ["rag", "edge ai", "quantization", "pruning", "fedavg", "method"]):
        return "search"
    return "none"


def run_task(task: dict) -> dict:
    selected_tool = route_tool(task["question"])
    if selected_tool == "calculator":
        if task["payload"]:
            try:
                answer = str(safe_eval(task["payload"]))
            except Exception:
                answer = "calculator failed because the input was not a valid arithmetic expression"
        else:
            answer = "needs more information"
    elif selected_tool == "search":
        answer = search(task["payload"] or task["question"])
    else:
        answer = "no available tool or task needs more information"
    return {
        "question": task["question"],
        "expected_tool": task["expected_tool"],
        "selected_tool": selected_tool,
        "tool_input": task["payload"],
        "answer": answer,
        "tool_correct": selected_tool == task["expected_tool"],
        "answer_contains_expected": task["expected_contains"].lower() in answer.lower(),
    }


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    df = pd.DataFrame([run_task(task) for task in TASKS])
    df.to_csv(RESULTS / "agent_trace.csv", index=False)

    usage = df["selected_tool"].value_counts().rename_axis("tool").reset_index(name="count")
    usage.to_csv(RESULTS / "tool_usage.csv", index=False)

    metrics = pd.DataFrame(
        [
            {"metric": "tasks", "value": len(df)},
            {"metric": "tool_selection_accuracy", "value": df["tool_correct"].mean()},
            {"metric": "answer_check_accuracy", "value": df["answer_contains_expected"].mean()},
            {"metric": "failure_or_no_tool_cases", "value": int((df["selected_tool"] == "none").sum())},
        ]
    )
    metrics.to_csv(RESULTS / "agent_metrics.csv", index=False)

    plt.figure(figsize=(5, 4))
    plt.bar(usage["tool"], usage["count"], color=["#3d6fb6", "#4a8f5a", "#b26a3b"])
    plt.ylabel("Number of calls")
    plt.title("Agent Tool Usage")
    plt.tight_layout()
    plt.savefig(RESULTS / "tool_usage.png", dpi=180)
    plt.close()

    plt.figure(figsize=(6, 4))
    metric_plot = metrics[metrics["metric"].isin(["tool_selection_accuracy", "answer_check_accuracy"])]
    plt.bar(metric_plot["metric"], metric_plot["value"], color=["#3d6fb6", "#4a8f5a"])
    plt.ylim(0, 1.05)
    plt.ylabel("Accuracy")
    plt.title("Agent Routing and Answer Checks")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(RESULTS / "agent_metrics.png", dpi=180)
    plt.close()

    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
