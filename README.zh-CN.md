# Research Repro Agent 使用说明

Research Repro Agent 是一个 AutoResearch 风格的自动化调研审查框架。它的目标不是生成一段无法追溯的综述文字，而是把调研过程拆成可检查的阶段：确定方向、登记论文、审查论文、生成 Obsidian 笔记库、排序可验证论文、选择 smoke test、记录运行结果、再审查结论。

当前实现是保守的第一版：先用 JSON 文件保存结构化产物，用 markdown 生成 Obsidian 笔记库，不承诺一开始就全自动联网检索和运行重型实验。

## 核心流程

```text
topic
  -> DirectionAgent 确定调研方向
  -> LiteratureAgent 登记候选论文
  -> PaperAuditAgent 审查论文
  -> candidate ranking 排序可验证论文
  -> ObsidianWriterAgent 写入笔记库
  -> ExperimentAgent 对选中论文做 smoke test
  -> ReviewAgent 复查引用、指标和结论边界
```

## 安装

```bash
python -m pip install -r requirements.txt
```

## 最小使用流程

初始化一个调研主题：

```bash
research-repo init --topic "selective context forgetting in LLM inference"
```

登记一篇候选论文：

```bash
research-repo add-paper \
  --title "Example Paper" \
  --url "https://arxiv.org/abs/example" \
  --code-url "https://github.com/example/project" \
  --method-type "benchmark" \
  --relevance 4
```

审查论文：

```bash
research-repo audit-paper --paper-id example-paper
```

排序并选择适合 smoke test 的论文：

```bash
research-repo rank-papers
research-repo select-experiments --top-k 3
```

生成 Obsidian 笔记库：

```bash
research-repo write-vault
```

生成复查记录：

```bash
research-repo review
```

## 输出位置

结构化产物写入：

```text
artifacts/
  briefs/
  papers/
  audits/
  rankings/
  experiments/
  reviews/
```

Obsidian 笔记库写入：

```text
vault/
  总索引.md
  主题地图.md
  调研方向.md
  论文总表.md
  gaps.md
  papers/
  reviews/
  experiments/
  logs/
```

## Smoke Test 策略

实验 Agent 不会对所有论文运行测试。它只在论文审查完成后，根据以下信号选择优先级较高的论文：

- 是否有代码链接；
- topic relevance；
- evidence quality；
- reproducibility value；
- method diversity；
- risk penalty。

默认只选择 `top_k = 3`。smoke test 只验证安装、入口、最小样例或官方 demo，不默认运行高成本训练。

## 文档入口

- `program.md`：人类编写的调研规则和 Agent 约束。
- `docs/architecture.md`：功能与架构设计。
- `docs/autoresearch_loop.md`：AutoResearch 风格循环。
- `docs/obsidian_vault_spec.md`：Obsidian 笔记库规范。
