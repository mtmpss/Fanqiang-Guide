# 自动更新说明

这个仓库使用 GitHub Actions 定时检查公开 GitHub 项目。无需购买知识库产品，无需用户提供外部 API Key，也不依赖自建服务器或运行中的个人电脑。

## 自动更新什么

- 已收录且有明确 GitHub 仓库地址的项目：仓库访问结果、归档/禁用标记、最近推送时间、GitHub 返回的最新正式 Release 及其发布日期。
- [完整分类目录](../CATALOG.md)：全部资料条目及对应的版本、仓库状态和原始资料卡。
- [自动检查报告](../UPDATES.md)：追踪覆盖范围、最后检查时间、失败项目及其上次成功观测值。

GitHub 最新正式 Release 不包含草稿或预发布版本；没有 Release 不代表没有版本或停止维护。项目是否归档只表示 GitHub 仓库自身的标记。

自动化不会安装上游程序、执行上游脚本或实测设备。仓库访问成功不能证明条目身份、软件质量、刷机可行性或插件兼容性。教程、人工核验状态和华硕型号支持声明仍以资料中标出的依据为准。

## 什么时候更新

- 每天计划在北京时间 **06:17** 运行一次（UTC 22:17）。GitHub 可能延迟调度。
- 修改更新脚本、来源配置、测试或本工作流时，主分支自动验证并检查一次。
- 需要立即检查时，进入 [Actions](https://github.com/mtmpss/Fanqiang-Guide/actions/workflows/update-library.yml)，选择 **Run workflow**。

定时任务只在默认分支运行。公开仓库连续 60 天没有仓库活动时，GitHub 会停用定时工作流。本仓库会提交实际检查结果与检查日期；若长期运行失败或任务被停用，仍需在 Actions 中恢复。GitHub 调度属于尽力执行，不能保证永久无人干预。

## 数据如何维护

| 文件 | 角色 |
|---|---|
| `export/library-v0.1-2026-09-11.json` 及同日期资料卡 | 初始人工整理快照，保留原核验范围 |
| `config/upstream-repositories.json` | 条目与 GitHub 仓库的明确对应关系；每个条目恰好被映射或列入排除原因 |
| `data/upstream.json` | 自动更新的上游观测值，记录本次状态与上次成功时间 |
| `CATALOG.md`、`UPDATES.md` | 从初始资料、来源配置与自动观测值生成的阅读页面 |

同一个字段只在它所属的数据层更新。日期化 JSON、JSONL、SQLite 和 RAG 文件是历史快照，不会伪装成本次检查后的数据；查询最新仓库/版本信息请使用自动观测文件或分类目录。新增条目需要同时补充基础资料和映射，生成器会检查覆盖关系。

仓库改名或重定向时，程序会标记 `redirect_blocked`，保留原映射供核对，不自动跟随新的地址。未成功获取的新状态不会覆盖上次成功的数据；页面会标明旧值的时间。404 表示本次无法公开访问，不自动判定项目已删除；单次连接失败也不会删除资料。

## 无需外部接入的原理

Actions 使用 GitHub 自动创建的临时 `GITHUB_TOKEN` 读取公开 API，并将三个生成文件提交回本仓库。没有个人访问令牌、模型 Key、自定义 Secret 或服务器账号。机器人提交仅以 `github-actions[bot]` 署名。

采集有超时、重试和并发限制。系统性鉴权/配额故障会让工作流失败并停止发布；部分项目访问异常则在报告中保留旧值和失败状态。发布使用普通 Git 推送，遇到并发修改不会强制覆盖主分支。下一次运行从当前仓库状态继续。

更新与生成在同一次工作流中完成，不依赖机器人提交再次触发其他工作流。修改逻辑先运行离线测试，只有通过后才进入自动检查。

本阶段自动追踪现有清单，不会自动将搜索结果收录成推荐项目，也不会调用 AI 重写教程。

## 维护者手动验证

Python 3.13，仅使用标准库：

```sh
python -m unittest discover -s tests -v
python scripts/build_catalog.py
```

完整采集建议使用 Actions 中的 **Run workflow**，由 GitHub 提供 API 额度；无需在本机配置令牌。单个项目失败可查看 Actions 步骤摘要与自动检查报告。

## 官方说明

- [GitHub Actions 自动令牌](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [定时工作流及其限制](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [GitHub 最新正式 Release 接口](https://docs.github.com/en/rest/releases/releases#get-the-latest-release)
- [GITHUB_TOKEN 的触发行为](https://docs.github.com/en/actions/concepts/security/github_token)
