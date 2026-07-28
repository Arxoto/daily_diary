# Vibe-Coding

## mattpocock's skills

see <https://github.com/mattpocock/skills>

```bash
# install skills
npx skills@latest add mattpocock/skills
# setup in agent
run /setup-matt-pocock-skills
```

若使用 ClaudeCode 需要对技能目录做兼容

```powershell
# Admin
New-Item -ItemType Directory -Path ".claude" -Force
New-Item -ItemType SymbolicLink -Path ".claude\skills" -Target (Join-Path (Get-Location) ".agents\skills")
```

### 最佳实践

> `/ask-matt` “我有一个需求”、“我要修复一个问题”、“xxx场景，应该如何使用哪些 skills ？”

**Vibe-Coding-Skills**

主线：从需求到交付

- 初始化技能体系 `/setup-matt-pocock-skills`
- 需求分析 `/grill-with-docs`
- 代码实现
  - `/to-spec` 规格化，需求文档和概要设计
  - `/to-tickets` 需求拆解和任务分发
  - `/implement` 实现单点功能，新建 session 完成一个 ticket ，内部自动调用 `/tdd` `/code-review`

支线：切入主线

- 项目架构优化分析 `/improve-codebase-architecture` ，完成后走 `/grill-with-docs`
- 超大模糊需求 `/wayfinder` ，完成后走`/to-spec`
  - 内部自动进行调研 `/research` 和原型验证 `/prototype`
- BUG 排查 `/diagnosing-bugs`
- issue 录入和分类 `/triage`

**By-The-Way**

- 追问式打磨想法 `/grill-me`
- Agent 交接 `/handoff`
- 学习新概念 `/teach`
- 元技能 `/writing-great-skills`

**原语 skills**

- 追问原语 `/grilling`
- 代码模块设计方法论 `/codebase-design`
- 领域建模，维护 ADR `/domain-modeling`
