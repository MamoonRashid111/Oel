# Drift & Failure Analysis Report

**Total Negative Feedbacks Analyzed:** 5

## Error Distribution
category
Tool Error      4
Context Miss    1

## Detailed Failure Logs
 id     category                                               reason                                                                              input
  1   Tool Error Rule-based analysis: Failure detected in core logic.                                                What is the dosage for Amoxicillin?
  4   Tool Error Rule-based analysis: Failure detected in core logic.                                                 What are the symptoms of COVID-19?
  7   Tool Error Rule-based analysis: Failure detected in core logic.                                                 Can I take aspirin with ibuprofen?
 10   Tool Error Rule-based analysis: Failure detected in core logic.                                                             Diet for hypertension.
 11 Context Miss Rule-based analysis: Failure detected in core logic. from document Neurological emergencies and conditions require rapid identification

## Action Plan
1. **Prompt Tuning:** Address common 'Hallucination' patterns by strengthening grounding instructions.
2. **Tool Refinement:** Check RAG retrieval thresholds for 'Context Miss' errors.
