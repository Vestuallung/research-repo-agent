# Reusable Research Workflow

This workflow is for small research projects where papers, experiments, Agent-written notes, and final reports need to stay auditable.

## 1. Define The Research Question

Input: a topic, a rough motivation, and one concrete question.

Output: a short problem statement with scope boundaries.

Pass condition: a classmate can tell what is included, what is excluded, and what result would count as progress.

## 2. Build A Paper Library

Input: papers, metadata, PDFs or links, and short notes.

Output: one structured paper card per paper.

Each paper card should include title, year, venue or source, method type, main claim, evidence type, limitations, and relevance to the research question.

Pass condition: every later summary can point back to one or more paper cards.

## 3. Form A Topic Map And Outline

Input: paper cards.

Output: a topic map and a first outline.

Group papers by technical role rather than by reading order. Typical groups include problem definition, method family, benchmark, system design, evaluation, and failure mode.

Pass condition: the outline explains why each section exists.

## 4. Run A Small Experiment Or Demo

Input: a minimal dataset, a script, and a clear output path.

Output: a report with command, data, result file, and interpretation.

Pass condition: another person can rerun the command and find the generated output.

## 5. Let An Agent Draft From Existing Material

Input: paper cards, outline, experiment report, and explicit writing target.

Output: a draft section, comparison table, checklist, or report.

Pass condition: the Agent only uses provided sources and marks uncertainty instead of inventing missing evidence.

## 6. Human Recheck

Input: Agent draft and source materials.

Output: accepted text, revised text, or a list of unresolved questions.

Check three things every time: citation support, metric support, and conclusion boundary.

Pass condition: no final claim depends only on Agent wording.

## 7. Final Report

Input: reviewed outline, checked notes, and experiment outputs.

Output: a report with background, related work, method comparison, experiment record, limitations, and next steps.

Pass condition: claims, sources, and experiment outputs can be traced without guessing.
