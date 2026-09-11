# 翻墙指南 · 网络工具资料库

项目主页：[fanqiang.guide](https://fanqiang.guide)

面向中文读者的网络工具、客户端、协议及路由器生态资料。当前是数据与文档快照，网站和 AI 问答尚未部署。

数据版本：v0.1-2026-09-11。公开上传包版本：v0.1-2026-09-12。

- **310 个独立条目**：206 条已核对第一方资料概要，103 条目录候选，1 条历史线索。
- **100 条项目关系**，**58 条华硕型号与固件支持声明**，**771 个来源 URL**。
- 已核对概要不等于已安装、安全审计或逐版本兼容测试；型号支持声明不等于插件兼容。

## 阅读入口

- [全部分类与资料卡](export/INDEX-v0.1-2026-09-11.md)
- [华硕与梅林生态](knowledge/merlin-guide-v0.1-2026-09-11.md)
- [华硕型号与固件支持声明](knowledge/merlin-model-matrix-v0.1-2026-09-11.md)
- [分类和关联](knowledge/taxonomy-v0.1-2026-09-11.md)

## 数据与检索

| 文件 | 用途 |
|---|---|
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

这是可读取、可查询的数据快照。内部采集输入、抓取原文及完整重建工具未随此包发布；部分记录保留原始相对证据路径作为出处元数据，对应原文文件不在仓库中。更新资料时需要重新核验并保持 JSON、Markdown、SQLite 和检索集一致。

来源包含项目官网、维护者文档及公开目录。项目名称和第三方资料权利归各自权利人；收录不代表官方关联或质量背书。本仓库未为第三方项目重新授予许可。
