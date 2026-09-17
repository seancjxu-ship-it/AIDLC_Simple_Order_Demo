# AIDLC Simple Order Demo / AIDLC 极简订单演示

## English

This repository is a deliberately small GitHub project for demonstrating an AIDLC workflow with Hermes-style agents and Huawei Cloud MaaS.

The business request is simple: make `cancel_order` idempotent. The initial baseline intentionally contains two defects, so the first quality gate is expected to fail. An AIDLC agent should read the specification, produce a minimal change, run the deterministic tests, and open a pull request.

### What the demo proves

- A repository can be discovered and summarized before code generation.
- Requirements, design, tasks, code, tests, and evidence can be traced together.
- The model proposes a change; deterministic tests decide whether it may continue.
- The agent works through a pull request and does not write directly to `main`.

### Repository size

- One business source file.
- Four unit tests.
- No third-party Python dependencies.
- Two intentional baseline defects.

### Run the first gate

```bash
python -m unittest discover -s tests -v
```

Expected initial result: two tests pass and two tests fail or error. This red gate is intentional.

### Suggested demo flow

1. Create a GitHub repository and upload these files.
2. Protect the `main` branch and require the `AIDLC Quality Gate` check.
3. Create an issue using `demo/GITHUB_ISSUE.md`.
4. Ask the AIDLC framework to inspect the repository and implement the issue.
5. Review the generated SDD trace, proposed diff, token usage, tests, and evidence.
6. Merge only after all four tests pass.

## 中文

这是一个刻意保持极简的 GitHub 项目，用于演示基于 Hermes 风格 Agent 和华为云 MaaS 的 AIDLC 流程。

业务需求很简单：让 `cancel_order` 支持幂等。初始基线故意保留两个缺陷，因此第一轮质量门禁应当失败。AIDLC Agent需要读取规格、生成最小修改、执行确定性测试并创建Pull Request。

### Demo证明什么

- 在生成代码之前发现并理解代码仓。
- 将需求、设计、任务、代码、测试和证据串成可追踪链路。
- 模型负责提出修改，确定性测试负责决定是否允许继续。
- Agent通过Pull Request工作，不直接写入`main`。

### 仓库规模

- 一个业务源码文件。
- 四个单元测试。
- 不依赖第三方Python包。
- 初始版本包含两个预置缺陷。

### 执行第一轮门禁

```powershell
python -m unittest discover -s tests -v
```

预期初始结果：两个测试通过，两个测试失败或报错。这个红色门禁是刻意设计的。

### 建议演示流程

1. 创建GitHub仓库并上传这些文件。
2. 保护`main`分支，并把`AIDLC Quality Gate`设为必需检查。
3. 使用`demo/GITHUB_ISSUE.md`创建Issue。
4. 让AIDLC框架检查仓库并实现Issue。
5. 检查SDD追踪、代码差异、Token使用、测试和证据。
6. 四个测试全部通过后才允许合并。

