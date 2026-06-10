# Report: Tool-Using Agent Demo

## Motivation

We built a small agent demo to understand how a system can use tools for tasks that require calculation or retrieval.

## Problem

The agent handled four tasks: two arithmetic questions and two knowledge questions.

## Method

Calculator tasks used a safe AST evaluator. Search tasks retrieved answers from a small local document store.

## Hyperparameters

No model was trained. The setup used 4 tasks, 2 tools, and 3 local documents.

## Results

The agent selected the calculator twice and search twice. The full trace and tool-usage chart were saved in `results/`.

## Interpretation

The workflow demonstrates tool routing and traceability. The limitation is that the routing policy is fixed and not language-model based.

## Conclusion

Tool use is a core idea in agentic AI. This project gives a clear minimal example.
