# Agent Write And Review Protocol

This protocol keeps Agent output useful without letting it silently become the final authority.

## Allowed Agent Work

An Agent may:

- extract metadata from notes or structured JSON;
- summarize paper cards that already exist;
- compare methods using provided notes;
- draft section outlines;
- turn experiment outputs into a markdown report;
- produce a list of missing evidence or blocking questions.

An Agent should not:

- invent papers, results, metrics, or citations;
- turn an unsupported idea into a final conclusion;
- hide uncertainty when source material is incomplete;
- overwrite human-reviewed notes without a separate review step.

## Required Review Steps

Before accepting Agent-written text, perform three checks.

Citation check: every factual claim about a paper must point to a paper card, source note, or explicit metadata entry.

Metric check: every claim about an experiment must point to the command, input file, output file, and metric record.

Boundary check: the wording must match the strength of evidence. Use phrases such as "suggests", "in this demo", or "not yet tested" when the evidence is limited.

## Recommended Draft Labels

Use simple status labels in notes or filenames:

- `draft`: Agent-written or rough human text.
- `needs_review`: plausible but not checked.
- `checked`: source and metric links have been reviewed.
- `final`: ready to include in the final report.

## Recheck Checklist

- Does every important claim have a source?
- Does the text distinguish paper claims from evaluator inference?
- Are negative results and weak evidence kept visible?
- Are experiment outputs described without overstating generality?
- Are unresolved questions preserved instead of smoothed over?

## Output Rule

Agent output is accepted only after a human recheck. If the recheck cannot be completed, keep the result as `needs_review`.
