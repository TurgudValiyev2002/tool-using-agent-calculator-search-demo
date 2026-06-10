# Tool-Using Agent: Calculator and Search Demo

![Project overview](assets/readme_project_overview.png)

Figure: minimal agent workflow for routing tasks to tools and saving the trace.


## Motivation

Agentic AI systems become more useful when they can choose tools instead of trying to answer everything from memory. This project demonstrates a small tool-using agent with two tools: calculator and local document search.

## Project Goal

We built a simple agent loop that selects a tool, sends the right input to that tool, and saves the full trace.

## Problem Description

The agent receives four tasks: two arithmetic questions and two knowledge questions. Arithmetic questions should go to the calculator, while knowledge questions should go to local search.

## Tools

Python, pandas, matplotlib, a safe arithmetic evaluator, and a small local search function.

## Method

The agent uses a fixed routing policy: calculator tasks are evaluated with a safe AST-based evaluator, and search tasks retrieve from a small local document dictionary.

## Hyperparameters

No model was trained. The fixed settings are 4 tasks, 2 tools, and 3 local search documents.

## Results

The agent used the calculator twice and search twice. The full trace is saved in `results/agent_trace.csv`, and tool counts are saved in `results/tool_usage.csv`.

## Interpretation

The demo shows the basic structure of tool use: decide the tool, prepare tool input, execute the tool, and return the answer. The main limitation is that routing is rule-based rather than learned or LLM-driven.

## Conclusion

Tool use is a practical pattern for agentic systems. A stronger version should add natural language routing, error handling, and tool-result verification.

## How To Run

```bash
pip install -r requirements.txt
python 1_tool_using_agent_demo.py
```
