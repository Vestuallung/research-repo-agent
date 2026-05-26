# Xiaomi Token Plan Application Draft

## 04 Agent or AI-Driven Result

我正在构建一个面向科研论文评估与实验复现的多 Agent 原型 `Research Repro Agent`。它解决的核心痛点是：AI 论文中的关键复现信息往往分散在正文、附录、README、配置文件、训练脚本和实验日志中，学生或研究者需要花大量时间手工对齐论文主张、实验设置、代码入口和失败原因。

当前项目包含四个核心角色。`Paper Agent` 负责从结构化论文评估中提取论文类型、主要主张、证据支持度、质量分数、风险标记和阻塞问题；`Repo Agent` 负责扫描本地或 GitHub 代码库，识别依赖文件、训练或评估入口、配置文件、测试文件和示例数据；`Planner Agent` 负责把论文风险和代码结构对齐，生成最小复现计划、smoke test 和缺失信息清单；后续的 `Debugger Agent` 会读取终端日志，定位依赖冲突、路径错误、参数缺失和数据格式问题。

我之前已经完成了一个 AI 论文标准化评估协议和样例评估结果，现在将其包装为该 Agent 工作流的评估内核。当前 MVP 已经可以读取标准化论文评估 JSON，扫描代码库结构，并输出 `reproduce_report.md`。后续会加入长上下文论文读取、代码库理解和多轮日志诊断，因此会产生真实的 token 消耗，尤其适用于课程科研训练、论文阅读小组和个人复现实验。

## 05 Proof and Impact

可提交材料：

- GitHub 项目链接：上传 `Research Repro Agent` 仓库。
- 终端运行截图：展示从 `examples/hneurons_evaluation.json` 生成 `examples/demo_reproduce_report.md`。
- 工作流截图或录屏：展示 Paper Agent、Repo Agent、Planner Agent 到 Reporter 的输出链路。
- 样例报告：提交生成后的 `demo_reproduce_report.md`。

建议身份表述：

我是计算机专业本科生，关注 AI Agent 在科研阅读、论文评估和实验复现中的应用。目前正在开发一个面向 AI 论文复现的多 Agent 原型，希望申请 token plan 用于长上下文论文理解、代码库分析、多 Agent 协作规划和实验日志诊断。
