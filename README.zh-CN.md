# Research Repro Agent 使用说明

Research Repro Agent 是一个可复用的科研工作流模板。它不是完整自动化平台，而是把“读论文、整理证据、检查代码库、生成复现计划、让 Agent 写草稿、人工复查”这几件事组织成一套可以交给同学照着做的流程。

当前仓库自带一个最小 demo：读取一份结构化论文评估 JSON，扫描当前代码库，然后生成一份复现导向报告。

## 1. 安装

先克隆仓库并进入目录：

```bash
git clone https://github.com/Vestuallung/research-repo-agent.git
cd research-repo-agent
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

当前 MVP 只使用 Python 标准库，所以 `requirements.txt` 里没有额外运行时依赖。保留这个文件是为了让以后加依赖时入口不变。

## 2. 运行 Demo

直接运行脚本：

```bash
bash scripts/run_demo.sh
```

脚本实际执行的是：

```bash
PYTHONPATH=src python -m research_repro_agent.cli \
  --paper-eval examples/hneurons_evaluation.json \
  --repo . \
  --out examples/demo_reproduce_report.md
```

看到类似下面的输出就说明运行成功：

```text
Research Repro Agent
========================================================================
[1/4] Paper Agent
  claims       : 3 extracted

[2/4] Repo Agent
  dependencies : pyproject.toml, requirements.txt

[3/4] Planner Agent
  risk level   : high

[4/4] Reporter
  report       : examples/demo_reproduce_report.md
  status       : completed
========================================================================
```

## 3. 查看输出

生成报告在：

```text
examples/demo_reproduce_report.md
```

报告主要看四块：

- `Paper Signals`：论文类型、标签、分数和风险等级。
- `Claims`：论文主张以及支持程度。
- `Repository Signals`：代码库入口、依赖文件、配置文件和测试文件。
- `Reproduction Tasks`：下一步复现应该先做什么。

这个 demo 使用的是样例评估文件：

```text
examples/hneurons_evaluation.json
```

它只是用来演示流程，不代表仓库已经完成了对应论文的真实复现。

## 4. 套用到自己的研究项目

推荐把自己的项目也按三层组织：

```text
your-project/
  data/        # 论文清单、元数据、样例输入
  notes/       # 单篇论文卡片、阅读笔记
  experiments/ # 可运行的小实验或 demo
  docs/        # 综述大纲、Agent 写作协议、最终报告
```

使用流程：

1. 先确定研究问题，不要一开始就让 Agent 写大段综述。
2. 每篇论文先写一张 paper card，记录标题、方法、主张、证据、局限。
3. 把 paper cards 分组，形成相关工作地图和项目大纲。
4. 准备一个能跑的小实验或代码库扫描任务。
5. 让 Agent 基于已有 notes 和实验输出写草稿。
6. 人工复查引用、指标和结论边界。
7. 只把复查过的内容放进最终报告。

## 5. Agent 写作与复查

Agent 可以做：

- 提取论文元数据。
- 总结已有笔记。
- 生成对比表。
- 根据实验输出生成报告。
- 列出缺失证据和阻塞问题。

Agent 不应该直接做：

- 编造论文、指标或实验结果。
- 把没有证据的判断写成结论。
- 在没有人工复查时覆盖正式笔记。

更完整的规则见：

```text
docs/agent_write_review_protocol.md
```

## 6. 建议阅读顺序

第一次使用时按这个顺序看：

```text
README.zh-CN.md
docs/reusable_research_workflow.md
docs/project_outline_template.md
docs/agent_write_review_protocol.md
examples/demo_reproduce_report.md
```

其中：

- `docs/reusable_research_workflow.md` 解释完整研究流程。
- `docs/project_outline_template.md` 给出项目报告大纲。
- `docs/agent_write_review_protocol.md` 规定 Agent 写入和人工复查边界。

## 7. 常见问题

如果提示找不到 `research_repro_agent`，说明没有设置本地源码路径。使用脚本 `bash scripts/run_demo.sh` 可以避免这个问题；手动运行时需要保留：

```bash
PYTHONPATH=src
```

如果报告生成了但内容看起来很少，说明输入 JSON 本身信息有限。这个工具不会凭空补论文细节，它只把已有结构化输入和代码库扫描结果整理成可复查报告。

如果要分析别的代码库，把 `--repo .` 换成目标仓库路径即可：

```bash
PYTHONPATH=src python -m research_repro_agent.cli \
  --paper-eval examples/hneurons_evaluation.json \
  --repo /path/to/target/repo \
  --out examples/target_repo_report.md
```
