# One-Page Report: Tool-Using Agent Demo

## Motivation

Tool agents should be tested on routing mistakes, not only successful examples. We added ambiguous and unsupported tasks to make the evaluation more realistic.

## Method

The agent routes each question to a calculator, local search, or no tool. Arithmetic is evaluated with a restricted AST parser. Search uses a small local knowledge base.

## Evaluation

The task set has 11 examples, including clean calculator questions, search questions, unsupported questions, and ambiguous mixed questions.

## Results

Tool selection accuracy was 0.8182. Answer check accuracy was 0.9091. There were two no-tool/failure cases.

## Interpretation

The agent works on simple tasks but struggles when a question contains both a number and a conceptual request. This caused a calculator routing error. The result shows the limitation of hand-written routing rules.

## Conclusion

The demo is more useful because it includes failure cases. A stronger version should use a better router and a larger task set.
