# 翻墙指南 · 网络工具资料库

项目主页：[fanqiang.guide](https://fanqiang.guide)

面向中文读者的翻墙与科学上网工具资料库，整理客户端、代理协议、OpenWrt、华硕梅林固件及路由器生态。通过 GitHub Actions 每日检查已收录 GitHub 项目的版本和仓库状态，无需额外服务账号或 API Key。

[![每日更新工具资料](https://github.com/mtmpss/Fanqiang-Guide/actions/workflows/update-library.yml/badge.svg)](https://github.com/mtmpss/Fanqiang-Guide/actions/workflows/update-library.yml)

**从这里开始：[按分类找工具](CATALOG.md) · [查看版本与检查报告](UPDATES.md) · [华硕梅林资料](knowledge/merlin-guide-v0.1-2026-09-11.md)**

基础资料快照：v0.1-2026-09-11。自动检查流程：v0.1-2026-09-12。最新观测时间见检查报告。独立网站和 AI 问答尚未部署。

- **310 个独立条目**：206 条已核对第一方资料概要，103 条目录候选，1 条历史线索。
- **100 条项目关系**，**58 条华硕型号与固件支持声明**，**771 个来源 URL**。
- 已核对概要不等于已安装、安全审计或逐版本兼容测试；型号支持声明不等于插件兼容。

## 阅读入口

- [完整分类目录与自动更新的项目动态](CATALOG.md)
- [自动检查报告与追踪范围](UPDATES.md)
- [全部分类与资料卡](export/INDEX-v0.1-2026-09-11.md)
- [华硕与梅林生态](knowledge/merlin-guide-v0.1-2026-09-11.md)
- [华硕型号与固件支持声明](knowledge/merlin-model-matrix-v0.1-2026-09-11.md)
- [分类和关联](knowledge/taxonomy-v0.1-2026-09-11.md)

## 自动更新

计划每天北京时间 **06:17** 检查一次；也可在 [Actions](https://github.com/mtmpss/Fanqiang-Guide/actions/workflows/update-library.yml) 点击 **Run workflow** 立即运行。运行只使用 GitHub 自带的临时令牌和公开 API。

更新范围是已映射 GitHub 仓库的访问结果、归档状态、最近推送时间和最新正式 Release。全部条目都会保留在分类目录中；非 GitHub 项目或未明确对应仓库的条目会说明未自动追踪。检查失败保留上次成功值并标出时间，不把失败解释为软件停用。

版本检查不会自动提升资料的人工核验状态，也不表示已验证设备或插件兼容性。详细规则、数据分工及调度限制见[自动更新说明](knowledge/automatic-updates-v0.1-2026-09-12.md)。

## 数据与检索

| 文件 | 用途 |
|---|---|
| data/upstream.json | 自动检查的最新仓库与 Release 观测值，与基础资料快照分别标明日期 |
| export/library-v0.1-2026-09-11.json / .jsonl | 完整结构化资料及核验范围 |
| export/cards/ | 每个实体一份中文 Markdown 卡片 |
| export/sources-v0.1-2026-09-11.jsonl | 公开来源索引 |
| export/relationships-v0.1-2026-09-11.jsonl | 有出处的项目关系 |
| export/rag-reviewed-v0.1-2026-09-11.jsonl | 第一方资料概要检索集 |
| export/rag-compatibility-v0.1-2026-09-11.jsonl | 单独的型号支持声明检索集 |
| export/rag-all-v0.1-2026-09-11.jsonl | 包含待核验线索的研究资料集 |
| export/review-queue-v0.1-2026-09-11.jsonl | 逐条待核验清单 |
| export/library-v0.1-2026-09-11.sqlite | 本地全文检索数据库 |

从仓库根目录执行（Python 标准库，无需模型 API）：

```sh
python -X utf8 scripts/search_library.py 梅林 --reviewed
python -X utf8 scripts/search_library.py RT-AX58U
python -X utf8 scripts/search_library.py Android --kind client
```

## 使用与维护说明

`primary_reviewed` 表示已读取第一方材料并核对记录声明的字段；`reference_only` 和 `historical_reference` 仍是待核验线索。使用 `reviewed_fields`、`notes`、日期及引用判断每项结论的范围，不能把整条记录里的旧目录快照都视为已证实事实。

RAG 初期优先用 `rag-reviewed`；设备问题另检索型号声明。回答保留来源和版本限制，不把未核验线索当作配置成功的保证。

带日期的导出文件保留首次整理时的资料快照。上游动态单独记录在 `data/upstream.json`，由 `scripts/build_catalog.py` 生成当前目录与检查报告；已有 SQLite 和 RAG 快照不包含后续自动观测值。这样不会把历史资料误标为本次已核验内容。

初始采集输入、抓取原文及全套历史重建工具未发布；部分记录保留原始相对证据路径作为出处元数据，对应原文文件不在仓库中。已公开的自动更新脚本可以独立运行，无需这些原始输入。

来源包含项目官网、维护者文档及公开目录。项目名称和第三方资料权利归各自权利人；收录不代表官方关联或质量背书。本仓库未为第三方项目重新授予许可。
