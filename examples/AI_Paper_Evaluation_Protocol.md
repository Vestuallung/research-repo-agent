# AI Paper Evaluation Protocol v1.0

## 1. Purpose

This document defines a strict, machine-friendly evaluation protocol for AI/ML papers, with special care for large-model, multimodal, and agent papers.

It is designed for two use cases:

1. Human reviewers who want a structured and reproducible paper review workflow.
2. Large models that need to output stable, comparable, and auditable paper evaluations.

This protocol is intentionally stricter than a casual reading note. It separates:

- `quality`: how well the paper supports its claims.
- `interest`: how novel, useful, or field-relevant the paper is.

The protocol is derived from common review and reproducibility expectations reflected in official guidance from NeurIPS, ICML, ICLR, ACL Rolling Review, TMLR, JMLR, and AAAI.

## 2. Design Principles

### 2.1 Claims Before Hype

The first question is not "Is this exciting?" but "Are the main claims actually supported?"

### 2.2 Paper-Type Awareness

Theory papers, empirical method papers, benchmark papers, systems papers, and surveys should not be judged by exactly the same weight vector.

### 2.3 Reproducibility Is Part of Quality

For empirical AI papers, missing reproducibility details are not cosmetic defects. They reduce trust.

### 2.4 Ethics and Data Governance Are Gating Factors

For high-risk model, dataset, safety, or human-subject work, ethics, licensing, privacy, and release safeguards can cap the final score.

### 2.5 Significance Is Not the Same as Soundness

A paper may be modest but sound. A paper may be exciting but weak. These must be scored separately.

### 2.6 Venue Prestige Must Not Affect Scoring

Do not inflate scores because the paper is from a famous lab, a strong benchmark, or a prestigious venue.

### 2.7 LLM Reviewers Must Surface Uncertainty

If extraction is uncertain because of OCR issues, missing appendix, ambiguous notation, or inaccessible code/data, the evaluator must say so explicitly.

## 3. Scope

This protocol applies to:

- machine learning
- natural language processing
- computer vision
- multimodal learning
- reinforcement learning
- interpretability
- AI safety and alignment
- LLM and foundation-model papers
- agent papers
- dataset and benchmark papers
- systems, efficiency, and inference papers
- survey, position, and reproduction papers

It does not replace domain-specific expert review in areas such as medicine, law, or hardware design.

## 4. Review Workflow

Every evaluation must follow this order.

### Step 0. Metadata

Record:

- title
- authors, if visible
- venue or source
- year
- URL or file path
- evaluation date

### Step 1. Paper Type Classification

Assign exactly one `primary_type`:

- `empirical_method`
- `theory`
- `dataset_benchmark`
- `system_efficiency`
- `survey_position`
- `reproduction_negative_result`

Assign zero or more `secondary_tags`:

- `llm`
- `multimodal`
- `agent`
- `safety_alignment`
- `human_subjects`
- `dataset_release`
- `closed_model`
- `benchmarking_only`

### Step 2. Main Claim Extraction

Extract `1-5` primary claims from the paper.

Each claim must be stated in plain language and tagged with one of:

- `theoretical`
- `empirical`
- `causal`
- `interpretive`
- `benchmark`
- `systems`
- `resource`

### Step 3. Evidence Mapping

For each primary claim, record:

- where the evidence appears
- what kind of evidence is used
- whether the evidence directly supports the claim

Use the following support scale:

- `2 = directly supported`
- `1 = partially or indirectly supported`
- `0 = unsupported, contradicted, or too weak`

If any top-level claim receives `0`, this triggers a hard cap rule later.

### Step 4. Binary Compliance Checklist

Complete the relevant checklists in Section 8 using:

- `yes`
- `partial`
- `no`
- `na`

### Step 5. Quantitative Scoring

Score each core dimension from `0` to `5` using Section 6 and the weight table in Section 7.

### Step 6. Red-Flag and Cap Rules

Apply the cap and penalty rules in Section 9.

### Step 7. Final Outputs

Produce:

- `quality_score` out of 100
- `interest_score` out of 100
- `overall_score` out of 100
- `confidence` from 1 to 5
- `decision_band`
- `top_strengths`
- `top_weaknesses`
- `blocking_questions`

## 5. Hard Rules for LLM-Based Evaluation

If a large model is used to evaluate the paper, it must obey the following rules.

1. Do not evaluate from abstract only.
2. Read at least: abstract, introduction, method, main results, limitations or ethics, and references to supplementary material if core claims depend on them.
3. Do not assume code exists unless the paper or supplement explicitly provides it.
4. Do not assume missing baselines were run.
5. If a table contradicts the text, treat this as a serious flaw.
6. If notation or OCR is corrupted, lower confidence and mark `extraction_uncertainty`.
7. Separate "paper says" from "evaluator infers".
8. If the work is high-risk and safeguards are absent, do not give a high final score even if the technical section is strong.

## 6. Core Dimensions and Score Anchors

All core dimensions use the same `0-5` anchor scale.

### 6.1 Universal Anchor Scale

- `5 = excellent`: rigorous, clear, and complete enough that a strong reviewer would have only minor reservations.
- `4 = strong`: convincing overall, with limited non-fatal gaps.
- `3 = acceptable`: main claims are supported, but there are clear weaknesses or missing details.
- `2 = weak`: important gaps remain; trust is limited.
- `1 = poor`: major weaknesses undermine confidence in the main contribution.
- `0 = missing or contradictory`: the dimension is absent, self-contradictory, or fatally flawed.

### 6.2 Core Dimension Definitions

#### D1. Claim Precision and Scope Control

Question: Are the main claims clearly stated, internally consistent, and appropriately bounded?

High score requires:

- clear claim statements
- assumptions stated
- limitations acknowledged
- no internal contradiction between text, equations, tables, and conclusions

#### D2. Originality

Question: Does the paper add genuinely new knowledge, framing, evidence, or methodology?

High score can come from:

- a new algorithm
- a new theoretical result
- a new dataset or benchmark
- a new empirical finding that changes how people think
- a careful reproduction with significant new diagnostic insight

State-of-the-art alone does not guarantee a high originality score.

#### D3. Technical Soundness

Question: Is the method, argument, proof, or system technically correct and appropriately designed?

High score requires:

- correct math or logic
- appropriate methodology
- proper control of confounders
- correct and fair comparisons
- no obvious leakage or invalid assumptions

#### D4. Evidence and Evaluation Quality

Question: Do experiments, proofs, analyses, or case studies actually support the claims?

High score requires:

- relevant baselines
- meaningful ablations or controls
- robustness checks when needed
- error analysis or failure cases when claims are broad
- uncertainty reporting when performance gaps matter

#### D5. Reproducibility and Transparency

Question: Could a competent researcher reproduce or verify the main claims from the provided material?

High score requires:

- clear setup
- hyperparameters or theorem assumptions
- data or model access path
- environment or compute details
- seed or run-count reporting when randomness matters

#### D6. Significance and Usefulness

Question: If the paper is correct, how useful is it to the relevant research community?

This includes:

- conceptual importance
- practical value
- likely downstream influence
- usefulness to a niche but real subcommunity

Do not over-penalize sound niche papers just because they are not trendy.

#### D7. Clarity and Context

Question: Is the paper readable, well-structured, and properly contextualized relative to prior work?

High score requires:

- clear motivation
- understandable figures or tables
- correct positioning against prior work
- explicit discussion of what is and is not new

#### D8. Ethics, Safety, Data Governance, and Compliance

Question: Does the paper responsibly handle risks tied to data, models, people, and release?

Relevant items include:

- broader impact or risk discussion
- safeguards for dangerous capabilities
- licenses and terms of use
- privacy and consent
- human-subject reporting
- IRB or equivalent review where applicable

## 7. Weight Tables

Compute each weighted score as:

`weighted_dimension_score = weight * raw_score / 5`

Then sum to get the subtotal out of 100.

If a dimension is truly not applicable, redistribute its weight proportionally across the remaining dimensions, but only when `na` is justified.

### 7.1 Quality Score Weights by Primary Type

| Dimension | empirical_method | theory | dataset_benchmark | system_efficiency | survey_position | reproduction_negative_result |
|---|---:|---:|---:|---:|---:|---:|
| D1 Claim Precision and Scope Control | 10 | 12 | 10 | 10 | 14 | 10 |
| D2 Originality | 12 | 12 | 10 | 10 | 8 | 6 |
| D3 Technical Soundness | 18 | 32 | 16 | 18 | 18 | 20 |
| D4 Evidence and Evaluation Quality | 22 | 10 | 20 | 22 | 16 | 26 |
| D5 Reproducibility and Transparency | 16 | 12 | 18 | 16 | 10 | 20 |
| D6 Significance and Usefulness | 10 | 12 | 10 | 10 | 14 | 8 |
| D7 Clarity and Context | 6 | 6 | 6 | 6 | 10 | 5 |
| D8 Ethics, Safety, Data Governance, and Compliance | 6 | 4 | 10 | 8 | 10 | 5 |
| Total | 100 | 100 | 100 | 100 | 100 | 100 |

### 7.2 Interest Score Weights

Interest is scored separately to avoid mixing "exciting" with "correct."

Use this formula for all paper types:

- D2 Originality: 35
- D6 Significance and Usefulness: 40
- D7 Clarity and Context: 10
- evaluator-rated `community_interest`: 15

`interest_score = sum(weight * raw / 5)`

For `community_interest`, use:

- `5 = very likely to be discussed, reused, or taught`
- `4 = likely useful to an active subcommunity`
- `3 = relevant but not especially memorable`
- `2 = narrow or incremental`
- `1 = little expected follow-up`
- `0 = not meaningfully interesting even if correct`

### 7.3 Overall Score

Use:

`overall_score = 0.75 * quality_score + 0.25 * interest_score`

This keeps quality primary.

## 8. Binary Compliance Checklists

Use `yes / partial / no / na`.

For machine use, convert to:

- `yes = 1.0`
- `partial = 0.5`
- `no = 0.0`
- `na = excluded`

Compute:

`compliance_rate = sum(applicable item scores) / number_of_applicable_items`

### 8.1 Universal Checklist

- main claims are clearly identifiable
- main claims match abstract and conclusion
- limitations are explicitly discussed
- related work is sufficient for the claim being made
- no obvious contradictions across text, equations, figures, or tables
- main evaluation metric is defined
- comparison setting is fair and comparable
- essential details are in paper or supplement with explicit pointers
- risks or misuse are discussed when relevant
- licenses, terms, or provenance are discussed when external assets are used

### 8.2 Theory Checklist

- all assumptions are stated clearly
- all main formal claims are stated formally
- proofs are complete or complete proofs are referenced in supplement
- proof intuition is provided for nontrivial results
- theorem assumptions are reasonable for the intended claim
- if practical claims are made, empirical evidence or careful caveats are provided

### 8.3 Empirical Method Checklist

- datasets are described and justified
- train, validation, and test setup is clear
- strong baselines are included or absence is justified
- ablations or control experiments are included
- hyperparameters are reported
- hyperparameter selection procedure is reported
- number of runs is reported when randomness matters
- variation or uncertainty is reported
- failure cases or limitations are shown
- compute setup is reported

### 8.4 Dataset and Benchmark Checklist

- collection protocol is described
- annotation protocol is described
- quality control is described
- split construction is described
- contamination or overlap risks are discussed
- license and release terms are clear
- privacy, consent, or sensitive content handling is described
- benchmark metric validity is justified
- benchmark cannot be trivially gamed, or limitations are discussed

### 8.5 System and Efficiency Checklist

- hardware platform is clearly reported
- throughput, latency, memory, and quality metrics are all reported where relevant
- comparison hardware and software stacks are fair
- measurement methodology is described
- end-to-end cost tradeoff is reported
- implementation constraints or engineering assumptions are disclosed

### 8.6 Survey and Position Checklist

- scope is clearly bounded
- coverage is balanced rather than cherry-picked
- alternative views or counterarguments are fairly represented
- taxonomy or synthesis adds value beyond list-making
- claims of trend or consensus are evidenced

### 8.7 Reproduction and Negative Result Checklist

- original claim or paper is clearly identified
- reproduction target setup is faithfully reconstructed
- deviations from original setup are documented
- added analyses provide diagnostic value
- failure to reproduce is backed by concrete evidence rather than speculation

### 8.8 LLM-Specific Add-On Checklist

- model name, version, and access mode are specified
- prompt template or instruction format is specified
- decoding parameters are specified
- context window or truncation policy is specified if relevant
- benchmark contamination or memorization risk is discussed
- model availability and reproducibility path are described
- token or API cost is reported when material
- evaluator model usage is disclosed if an LLM judge is used

### 8.9 Agent-Specific Add-On Checklist

- environment, tools, and APIs are specified
- tool versions or interfaces are pinned or described
- success metric is explicit
- time or step budget is explicit
- human intervention policy is explicit
- multiple-run evaluation is used when stochasticity matters
- judge model or judge prompt is disclosed if used
- contamination or benchmark overfitting risk is discussed
- cost breakdown is reported when substantial

### 8.10 Human-Subjects Add-On Checklist

- participant recruitment is described
- instructions or task framing is described
- compensation is described
- risks are discussed
- IRB or equivalent approval is stated when required

## 9. Cap and Penalty Rules

These rules make the protocol strict enough for automated use.

### 9.1 Hard Caps

If any of the following holds, cap `overall_score` as specified.

| Flag                                  | Condition                                                                                               | Score Cap |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------: |
| `internal_contradiction_major`        | core method, label definition, theorem, or result is internally inconsistent                            |        55 |
| `main_claim_unsupported`              | any top-2 main claim has support score `0`                                                              |        50 |
| `unfair_or_missing_key_baseline`      | empirical claim relies on comparison but the key baseline is absent or unfairly configured              |        60 |
| `reproducibility_missing_major`       | empirical, dataset, or system paper lacks enough detail for competent rerun or verification             |        65 |
| `statistics_missing_for_small_gains`  | paper claims improvement from small differences but reports no run variability or significance evidence |        60 |
| `high_risk_ethics_unaddressed`        | dangerous release, privacy, consent, or licensing issues are materially unaddressed                     |        45 |
| `benchmark_contamination_unaddressed` | LLM or agent paper uses public benchmarks but does not discuss contamination when this matters          |        70 |
| `judge_model_opaque`                  | core conclusion depends on an LLM judge but judge prompt, model, or validation is absent                |        65 |

### 9.2 Soft Penalties

Apply these after weighted scoring and before hard caps.

- missing failure analysis in broad-claim empirical paper: `-3`
- compute not reported in costly large-scale paper: `-3`
- hyperparameter search procedure absent: `-3`
- no model or data release path and no adequate explanation: `-5`
- supplementary material contains essential content not summarized in main paper: `-2`
- overclaiming beyond shown evidence: `-5`

### 9.3 Compliance-Based Adjustment

If `compliance_rate < 0.60`, subtract `5`.

If `compliance_rate < 0.45`, subtract `10`.

This does not replace hard caps.

## 10. Confidence Scale

Confidence is not a paper score. It is the evaluator's confidence in the review.

- `5 = very high`: checked core claims carefully, including equations or appendix where needed
- `4 = high`: read carefully and verified most critical points
- `3 = medium`: enough for a responsible assessment, but some details were not checked deeply
- `2 = low`: important parts may be misunderstood or inaccessible
- `1 = very low`: mostly a tentative impression

## 11. Decision Bands

Use these bands after penalties and caps.

| Overall Score | Decision Band | Interpretation |
|---:|---|---|
| 85-100 | `excellent` | strong paper; suitable for deep reading and confident citation |
| 70-84 | `solid` | worthwhile paper; useful and mostly trustworthy |
| 55-69 | `mixed` | read selectively; useful ideas but cite with caution |
| 40-54 | `weak` | idea-level value only; not reliable as strong evidence |
| 0-39 | `poor` | low trust; not worth close reading unless directly relevant |

## 12. Minimal Natural-Language Output Template

Every evaluation should include these fields in prose:

1. `One-sentence verdict`
2. `Primary type and tags`
3. `Top 3 claims`
4. `Main supporting evidence`
5. `Main red flags`
6. `Quality / Interest / Overall / Confidence`
7. `Whether this paper is worth deep reading`

## 13. Machine-Readable Output Format

Use the following JSON template.

```json
{
  "schema_version": "AIPER-1.0",
  "metadata": {
    "title": "",
    "venue": "",
    "year": null,
    "source": "",
    "evaluation_date": ""
  },
  "paper_type": {
    "primary_type": "empirical_method",
    "secondary_tags": ["llm", "agent"]
  },
  "claim_table": [
    {
      "claim_id": "C1",
      "claim_text": "",
      "claim_type": "empirical",
      "evidence_locations": ["Sec. 4", "Table 2"],
      "support_score": 2,
      "notes": ""
    }
  ],
  "checklists": {
    "universal": {},
    "type_specific": {},
    "add_on": {}
  },
  "dimension_scores_raw_0_to_5": {
    "D1_claim_precision": 0,
    "D2_originality": 0,
    "D3_technical_soundness": 0,
    "D4_evidence_evaluation": 0,
    "D5_reproducibility": 0,
    "D6_significance": 0,
    "D7_clarity_context": 0,
    "D8_ethics_compliance": 0,
    "community_interest": 0
  },
  "derived_scores": {
    "quality_score": 0.0,
    "interest_score": 0.0,
    "overall_score_pre_penalty": 0.0,
    "penalty_points": 0.0,
    "overall_score_final": 0.0,
    "compliance_rate": 0.0
  },
  "flags": {
    "internal_contradiction_major": false,
    "main_claim_unsupported": false,
    "unfair_or_missing_key_baseline": false,
    "reproducibility_missing_major": false,
    "statistics_missing_for_small_gains": false,
    "high_risk_ethics_unaddressed": false,
    "benchmark_contamination_unaddressed": false,
    "judge_model_opaque": false,
    "extraction_uncertainty": false
  },
  "confidence": 3,
  "decision_band": "mixed",
  "top_strengths": [
    ""
  ],
  "top_weaknesses": [
    ""
  ],
  "blocking_questions": [
    ""
  ],
  "one_sentence_verdict": ""
}
```

## 14. Recommended Calculation Order

1. Classify paper type.
2. Extract claims.
3. Score claim support.
4. Fill checklists.
5. Score D1-D8 and `community_interest`.
6. Compute `quality_score`.
7. Compute `interest_score`.
8. Compute `overall_score_pre_penalty`.
9. Apply soft penalties.
10. Apply hard caps.
11. Assign confidence and decision band.

## 15. Interpretation Notes

### 15.1 Sound but Incremental

A sound, modest paper can still score well on quality and only moderately on interest. This is acceptable.

### 15.2 Exciting but Weak

A flashy claim with thin evidence should score high on interest at most, but low on quality.

### 15.3 Closed-Model Papers

Closed access does not force rejection, but it should reduce reproducibility unless the authors provide a meaningful verification path.

### 15.4 LLM Judge Usage

If an LLM judge is central to the conclusion, the judge setup is part of the method, not a side detail.

### 15.5 Benchmarking-Only Papers

Pure benchmark tables without careful analysis, contamination discussion, or evaluator validation should not receive high evidence scores.

## 16. Common Failure Modes the Evaluator Must Detect

- claim text stronger than the actual result
- theorem proven under assumptions too narrow for the stated conclusion
- cherry-picked qualitative examples standing in for quantitative evidence
- unfair baseline tuning
- missing ablations for a multi-component method
- hidden evaluator dependence
- data leakage or contamination
- no uncertainty estimates despite tiny metric gains
- no compute disclosure in expensive large-model work
- overgeneralization from one benchmark family
- ethics or licensing discussed superficially in a high-risk setting

## 17. Reference Basis

This protocol was synthesized from the common structure and expectations visible in official review or reproducibility guidance from the following sources:

- NeurIPS Paper Checklist: claims, proofs, reproducibility, experimental settings, significance reporting, compute, ethics, licenses, human subjects  
  [https://neurips.cc/public/guides/PaperChecklist](https://neurips.cc/public/guides/PaperChecklist)
- ICML Reviewer Instructions: soundness, presentation, significance, originality, limitations, confidence  
  [https://icml.cc/Conferences/2026/ReviewerInstructions](https://icml.cc/Conferences/2026/ReviewerInstructions)
- ICLR Reviewer Guide: clarity, technical correctness, experimental rigor, reproducibility, claim support  
  [https://iclr.cc/Conferences/2026/ReviewerGuide](https://iclr.cc/Conferences/2026/ReviewerGuide)  
  [https://iclr.cc/Conferences/2024/ReviewerGuide](https://iclr.cc/Conferences/2024/ReviewerGuide)
- ICLR Author Guide on reproducibility statements  
  [https://iclr.cc/Conferences/2024/AuthorGuide](https://iclr.cc/Conferences/2024/AuthorGuide)
- ACL Rolling Review review form: summary, strengths, weaknesses, soundness, excitement, overall assessment  
  [https://aclrollingreview.org/reviewform](https://aclrollingreview.org/reviewform)
- TMLR acceptance criteria and reviewer guide: claims must be supported by accurate, convincing, and clear evidence; interest is secondary to correctness  
  [https://jmlr.org/tmlr/acceptance-criteria.html](https://jmlr.org/tmlr/acceptance-criteria.html)  
  [https://www.jmlr.org/tmlr/reviewer-guide.html](https://www.jmlr.org/tmlr/reviewer-guide.html)
- JMLR reviewer guide: goals, description, evaluation, significance, technical correctness  
  [https://www.jmlr.org/reviewer-guide.html](https://www.jmlr.org/reviewer-guide.html)
- AAAI reproducibility checklist and submission instructions: pseudocode, assumptions, seeds, hardware, metrics, run counts, statistical tests, hyperparameters, code and data appendices  
  [https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/](https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/)  
  [https://aaai.org/conference/aaai/aaai-26/submission-instructions/](https://aaai.org/conference/aaai/aaai-26/submission-instructions/)

## 18. Recommended Local Use

When using this protocol in notes or automation:

- keep the raw JSON output
- keep a short prose summary next to it
- record uncertainty explicitly
- never treat `overall_score` as a substitute for reading the paper when the paper is central to your own work
