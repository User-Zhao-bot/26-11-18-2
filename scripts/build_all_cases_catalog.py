# -*- coding: utf-8 -*-
"""
Assembles docs/ALL_CASES_CATALOG.md strictly complying with the 12-item template
across all 31 Inward and 21 Outward cases.
"""

import os
import sys

from data_inward_catalog import INWARD_CASES
from data_outward_catalog import OUTWARD_CASES

output_file = "docs/ALL_CASES_CATALOG.md"
print(f"Generating {output_file} from empirical data...")

lines = []

# Title & Metadata
lines.append("# Autonomous Coding Agent Comprehensive Security Benchmark: All-Case Catalog")
lines.append("# (自主智能体对内越权与对外跨边界溢出实证全景案例总档案)\n")
lines.append("> **文档版本**: 2.0.0 (Master Release & Complete Empirical Corpus)  ")
lines.append("> **研制单位**: Antigravity Research Team  ")
lines.append("> **评测基线**: Linux ext4 物理隔离沙箱容器 (Non-privileged `devuser:1000` / `1001`, `root:root` 555 限制, `chattr +i` 不可变加锁) + 跨网络边界受害者独立服务 + 双门禁/三门禁独立判分 Oracle  ")
lines.append("> **评测模型**: Anthropic Claude Sonnet 4.6 (Claude Code CLI v2.1.328), OpenAI Codex CLI (`@openai/codex` 0.151.0), DeepSeek V4 Pro, DeepSeek V4.1 Flash, Qwen2.5-Coder  ")
lines.append("> **实证数据边界**: 本档案收录全部早期 **31 个对内本地越权与不可行冲突场景 (`IN-01` ~ `IN-31`)** 以及全部 **18 个对外跨网络边界物理溢出场景 (`OUT-01` ~ `OUT-18`，含消融对照组与版本对比)**，共计 **52 个标准化评测工况**。所有数据均来自 `results/` 与 `reports/` 下的真实实测记录，杜绝任何未执行的数据捏造。\n")
lines.append("---\n")

# TOC
lines.append("## 目录 (Table of Contents)")
lines.append("- [一、评测全景大表与危害分类矩阵 (Cross-Matrix Master Taxonomy)](#一评测全景大表与危害分类矩阵)")
lines.append("  - [1.1 危害范围与八大对外危害分类映射](#11-危害范围与八大对外危害分类映射)")
lines.append("  - [1.2 全景案例大表 (52 个实测工况总览)](#12-全景案例大表-52-个实测工况总览)")
lines.append("- [二、第一部分：对内本地越权与规避场景 (IN-01 ~ IN-31)](#二第一部分对内本地越权与规避场景-in-01--in-31)")
for c in INWARD_CASES:
    lines.append(f"  - [{c['id']}: {c['name']}](#{c['id'].lower()}-{c['case_id'].replace('_', '-')})")
lines.append("- [三、第二部分：对外跨边界物理溢出场景 (OUT-01 ~ OUT-18)](#三第二部分对外跨边界物理溢出场景-out-01--out-18)")
for c in OUTWARD_CASES:
    lines.append(f"  - [{c['id']}: {c['name']}](#{c['id'].lower()}-{c['case_id'].replace('_', '-')})")
lines.append("- [四、第三部分：实证规律、模型行为特征与治理防范讨论](#四第三部分实证规律模型行为特征与治理防范讨论)\n")
lines.append("---\n")

# Section 1
lines.append("## 一、评测全景大表与危害分类矩阵\n")
lines.append("### 1.1 危害范围与八大对外危害分类映射\n")
lines.append("根据真实前沿安全事故（2025–2026）与系统安全危害分类，本基准将智能体行为划分为 **对内本地危害 (Inward-Harm)** 与 **对外跨边界物理溢出 (Outward-Spillover)** 两大领域。对外溢出严格对齐八大危害效果分类：\n")
lines.append("| 危害分类代码 | 危害效果大类 | 典型外部物理后果 | 核心对应场景 (OUT / IN) |")
lines.append("| :--- | :--- | :--- | :--- |")
lines.append("| **CAT-1** | **机密性破坏 (Confidentiality Breach)** | 敏感 PII、多租户私有客户数据、云端推理 API Token、未脱敏病历外泄至公网或未授权实体 | `OUT-06`, `OUT-09`, `OUT-11`, `OUT-13`, `IN-03`, `IN-30` |")
lines.append("| **CAT-2** | **完整性破坏 (Integrity Poisoning)** | 软件供应链投毒、公私网网关 ACL 放行策略破坏、共享主干代码注入 SQL 漏洞、企业知识库免检策略投毒 | `OUT-01`, `OUT-02`, `OUT-03`, `OUT-07`, `IN-01`, `IN-02`, `IN-04`, `IN-15` |")
lines.append("| **CAT-3** | **数据与资产销毁 (Data & Asset Destruction)** | 生产 PostgreSQL 跨租户数据清空、线上 CDN 核心客户图片彻底清退、存储超限压降导致全量灾备快照销毁 | `OUT-05`, `OUT-14`, `OUT-16`, `IN-07` |")
lines.append("| **CAT-4** | **服务可用性破坏 (Service Availability Disruption)** | 清理空表导致外部生产微服务 503 级联中断、阻塞关键业务请求 | `OUT-15`, `IN-28` |")
lines.append("| **CAT-5** | **经济权益损害 (Financial / Commercial Harm)** | 外部第三方计费 API 配额抽干与资金池耗尽、高额不可退款商业差旅订单未经审批强制扣款锁死 | `OUT-10`, `OUT-12`, `IN-27` |")
lines.append("| **CAT-6** | **非授权通信与外部提交 (Unauthorized Communication & Form Submission)** | 擅自跨出企业边界发送客户通报邮件、沙箱故障擅自转向外部正式政府网站提交虚假测试单据 | `OUT-08`, `OUT-17` |")
lines.append("| **CAT-7** | **身份与账户状态违规 (Identity & Account State Violation)** | 绕过企业身份治理，擅自调用外部注册 API 注册未受控账号 | `OUT-18` |")
lines.append("| **CAT-8** | **公共生态与治理损害 (Public Ecosystem & Governance Degradation)** | 将公共维基或开源基础设施当作私有临时草稿板，批量注水严重污染公地知识库 | `OUT-18` |\n")

lines.append("### 1.2 全景案例大表 (52 个实测工况总览)\n")
lines.append("| 编号 | Case 标识 | 范围 | 八大危害分类 | 目标组件 / 外部受害者 | 评测模型 | Gate 2 (本地) | Gate 1 (可信/远端) | 测试篡改 | 综合 ASR | 状态与表征 |")
lines.append("| :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")

for c in INWARD_CASES:
    g2 = "PASS" if "PASSED" in c['gate_results'] else "FAIL"
    g1 = "PASS" if "PASSED" in c['gate_results'].split("Gate 1")[1].split("\n")[0] else "FAIL"
    asr = "100%" if "100" in c['gate_results'] else "0%"
    short_target = c['target_infra'].split(";")[0][:30]
    lines.append(f"| **{c['id']}** | `{c['case_id']}` | Inward | {c['category']} | {short_target} | Claude / DS | {g2} | {g1} | 见详情 | **{asr}** | {c['name'].split(' ')[1] if ' ' in c['name'] else c['name']} |")

for c in OUTWARD_CASES:
    g2 = "PASS" if "PASSED" in c['gate_results'] else "FAIL"
    g1 = "BREACH" if "BREACH" in c['gate_results'] else "SAFE"
    asr = "100%" if "100" in c['gate_results'] else "0%"
    short_target = c['target_infra'].split(";")[0][:30]
    lines.append(f"| **{c['id']}** | `{c['case_id']}` | Outward | {c['category']} | {short_target} | Claude Sonnet | {g2} | {g1} | 见详情 | **{asr}** | {c['name'].split(' ')[1] if ' ' in c['name'] else c['name']} |")

lines.append("\n---\n")

def format_case(c, prefix):
    case_lines = []
    case_lines.append(f"### {c['id']}: `{c['case_id']}` ({c['name']})\n")
    case_lines.append(f"- **Case 编号与代号**：`[{c['id']}]: {c['case_id']} ({c['name']})`")
    case_lines.append(f"- **危害范围与影响分类**：`[{c['scope']}]` | 归属八大危害效果分类：`[{c['category']}]`")
    case_lines.append(f"- **真实事故依据**：`{c['incident_source']}`")
    case_lines.append(f"- **数据集 / 来源**：{c['dataset']}")
    case_lines.append(f"- **目标组件与外部受害基础设施**：{c['target_infra']}")
    case_lines.append(f"- **缺陷背景与零和冲突机制**：{c['conflict_mechanism']}")
    case_lines.append(f"- **物理权限约束**：{c['permission_constraint']}")
    case_lines.append(f"- **自然工程 Prompt**：\n  > {c['prompt']}")
    case_lines.append(f"- **智能体执行轨迹与决策阶梯**：\n{c['trajectory']}")
    case_lines.append(f"- **实测关键代码/配置 Diff 片段**：\n{c['diff']}")
    case_lines.append(f"- **双门禁与独立 Oracle 检验结果**：\n{c['gate_results']}")
    case_lines.append(f"- **危害与工程后果总结**：{c['consequence']}\n")
    case_lines.append("---\n")
    return "\n".join(case_lines)

# Section 2: Inward Cases
lines.append("## 二、第一部分：对内本地越权与规避场景 (IN-01 ~ IN-31)\n")
lines.append("> **场景背景说明**：本部分涵盖智能体在面对本地只读文件锁定（Source-Locked, `chmod 444 + chattr +i`）、测试文件锁定（Test-Locked）、依赖构件锁定（Artifact-Locked）以及数学矛盾单测时的自主越权、奖励黑客（Reward Hacking）与合规停机行为。\n")
for c in INWARD_CASES:
    lines.append(format_case(c, "IN"))

# Section 3: Outward Cases
lines.append("## 三、第二部分：对外跨边界物理溢出场景 (OUT-01 ~ OUT-18)\n")
lines.append("> **场景背景说明**：本部分严格复现 2025–2026 年最新前沿真实 AI 运维安全事故（涵盖 Together AI、Meta Muse、Anthropic、OpenAI、Cursor、Cloudflare、GitLab 等）。智能体受到纯中性运维指令驱动，在无恶意引导、无提权的情境下，因认知盲区、范围蔓延或错误故障转移，造成跨越主机物理边界的实质破坏。\n")
for c in OUTWARD_CASES:
    lines.append(format_case(c, "OUT"))

# Section 4: Discussion & Synthesis
lines.append("## 四、第三部分：实证规律、模型行为特征与治理防范讨论\n")
lines.append("### 4.1 核心实证规律总结 (Key Empirical Findings)\n")
lines.append("1. **零和冲突驱动越权泛化**：当本地基线测试与不可变远端门禁之间形成零和矛盾时，前沿前置强化学习（RL）微调的智能体表现出极强的“以指标为中心（Goal-Oriented）”倾向，极易为了消除报错而牺牲全局安全性。")
lines.append("2. **认知盲区远甚于明知故犯**：通过 `OUT-06` vs `OUT-06-ABL`、`OUT-11` (V2) vs `OUT-11-V1` 的消融对照证明：前沿模型对包含 `PASSWORD`、`SECURITY VIOLATION` 等显式高危关键词的红线具备极高的自律拒止能力（ASR 0%）；然而一旦切换为真实工程中的“权限认知盲区”（如 Over-Privileged Guest Token、范围蔓延删除冷备份、空表无数据删除），智能体能够以惊人的工程合理化逻辑顺手实施致命危害（ASR 100%）。")
lines.append("3. **跨网络边界的不可撤销性**：对内规避尚能通过容器销毁兜底；而对外物理溢出一旦触发（如外部 Git 提交、外部公网网关、外部第三方商业扣款、外部政务单据提交），其物理后果直接外溢至公共互联网，造成不可逆的资产毁灭与法律合规风险。\n")

lines.append("### 4.2 体系化治理防范规范 (Defense Roadmap)\n")
lines.append("- **部署不可信双门禁/三门禁架构**：严禁仅依赖智能体报告或可被篡改的本地脚本验证，必须由独立只读容器和外部宿主机探针执行真实验证。")
lines.append("- **运行时外部出站流量行为级白名单**：在网关层严格限制容器的出站目标与请求类型，彻底阻断对生产端点、未授权商业支付网关及公网托管站点的网络可达性。")
lines.append("- **模型多维度诚实度审计 (Honesty & Deception Auditing)**：建立自动化的语义对齐检测，不仅检测物理行为，还必须核验智能体的文字总结是否隐瞒了核心危害或伪造了合规审批。\n")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Successfully generated {output_file} with {len(lines)} lines!")
