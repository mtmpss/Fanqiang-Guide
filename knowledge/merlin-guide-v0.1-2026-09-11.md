# 华硕/梅林与路由器生态知识库说明 v0.1

核验日期：2026-09-11。本文依据公开的项目说明整理，未刷机、未安装插件、未提供节点或订阅。它是库的结构与兼容性核验入口，不是刷机操作手册。

## 梅林需要作为一个完整生态收录

用户搜索“梅林”时，可能在找原版固件、扩展机型分支、国内改版、软件中心、代理插件或教程。知识库应该先消除这些歧义，再把相关项目连接起来。

| 层级 | 应收录实体 | 解决的问题 |
| --- | --- | --- |
| 硬件 | 完整型号、硬件修订、SoC、内存、存储 | 设备究竟是什么 |
| 固件 | ASUSWRT、Asuswrt-Merlin、GNUton、KoolCenter 官改/梅改 | 设备能运行哪套系统 |
| 扩展环境 | Entware、amtm、KoolShare rogsoft、iStore | 软件通过什么机制安装和维护 |
| 应用插件 | fancyss、MerlinClash、OpenClash、PassWall2、HomeProxy、Nikki | 用户在哪里配置和管理代理 |
| 核心/协议 | Mihomo、sing-box、Xray；具体协议 | 实际由什么程序处理流量 |
| 网络配套 | DNS、策略路由、多 WAN、访客网络 | 不同设备和不同流量怎么走 |
| 使用知识 | 场景、前置条件、配置逻辑、诊断、回退 | 用户如何完成任务并恢复问题 |

ASUSWRT 是华硕固件体系；原版 Merlin 在此基础上开发，并通过用户脚本、Entware、amtm 扩展能力。GNUton 的重点是额外机型支持。KoolCenter 梅改在原版 Merlin 上加入软件中心所需的组件。以上是不同项目与依赖关系，不能把它们合并成一个“梅林下载”。来源：[Merlin 项目说明](https://github.com/RMerl/asuswrt-merlin.ng/wiki/About-Asuswrt)、[GNUton](https://github.com/gnuton/asuswrt-merlin.ng)、[KoolCenter 梅改发布说明](https://www.koolcenter.com/t/topic/5072/1)。

Merlin 本身的固件身份不代表已安装透明代理。fancyss 明确面向带软件中心的 ASUSWRT/梅林衍生固件；MerlinClash 则说明自己使用 Mihomo。知识库需要把插件、核心、配置与服务连接条件分别写清。[fancyss](https://github.com/hq450/fancyss)、[MerlinClash](https://github.com/rts600/MerlinClash/blob/main/README.md)。

amtm 是终端脚本管理菜单；Entware 是软件包环境；KoolCenter 软件中心和它们不是同一个产品。原版 Merlin Wiki 中也列有 DNS、VPN、访客网络和监控脚本，因此华硕生态不能只保留代理插件。[amtm Wiki](https://github.com/RMerl/asuswrt-merlin.ng/wiki/AMTM)、[Entware](https://github.com/Entware/Entware)、[rogsoft](https://github.com/koolshare/rogsoft)。

## 兼容性矩阵必须按具体组合建立

项目目录记录的 supported_models 仍保留 null。已另建 merlin-model-matrix.json，完整提取本次原版 Merlin/GNUton 支持清单中的 58 条型号名称与固件支持声明（39 条列表内支持、19 条明确不再支持）；全部 tested=false。逐发布包、插件兼容和刷机结果尚未核验。下面是检索中已看到的差异示例，不构成刷机推荐。

| 设备关键词 | 已核验的来源声明 | 仍需核验 |
| --- | --- | --- |
| RT-AX58U V1 | 原版 Merlin Supported Devices 列出 V1 | 硬件标识、实际发布包和分支 |
| RT-AX58U V2 | GNUton README 列出 V2 | 不可误用 V1 固件 |
| RT-AX82U V1/V2 | GNUton README 分列两种修订 | 两种修订各自的发布包 |
| GT-BE98 / GT-BE98_PRO | GNUton 列 GT-BE98；原版 Merlin 列 GT-BE98_PRO | 名称相近不能互换固件 |
| RT-AC68U | 原版 Merlin 页面列为不再支持 | 历史固件与其他分支是否仍维护 |
| DSL-AC68U | GNUton 另列 DSL-AC68U | 不能与 RT-AC68U 混同 |
| RT-AX89X 与 fancyss | fancyss 说明 SoC 位宽和固件运行位宽可能不同 | 插件包必须匹配固件实际 ABI |

来源：[原版 Merlin 支持设备](https://github.com/RMerl/asuswrt-merlin.ng/wiki/Supported-Devices)、[GNUton 型号分组](https://github.com/gnuton/asuswrt-merlin.ng)、[fancyss 平台与机型表](https://github.com/hq450/fancyss)。

正式矩阵建议使用以下组合键：

`型号 + 硬件修订 + 固件项目 + 固件分支/版本 + 系统架构/ABI + 插件版本`

每行再记录：证据地址与日期、支持状态、下载校验入口、前置组件、可用空间、已知冲突、是否经过本库实测、可恢复路径。不能用“同品牌”“同芯片”“页面能打开”填充支持状态。

## OpenWrt 是另一条完整分支

OpenWrt 提供系统及软件包基础，LuCI 提供网页管理界面，ImmortalWrt、iStoreOS、Lean LEDE 等分别有自己的变更范围。OpenClash、PassWall/PassWall2、HomeProxy、Nikki 等才是代理应用层。Mihomo 和 sing-box 也不应分别在每个插件下面重复建成新工具。[OpenWrt](https://github.com/openwrt/openwrt)、[ImmortalWrt](https://github.com/immortalwrt/immortalwrt)、[iStoreOS](https://github.com/istoreos/istoreos)。

iStore 的作者特别说明：软件中心能装上，不代表其中所有插件的依赖都满足。Nikki 则明确给出 OpenWrt、Linux 内核和 firewall4 前置要求。这些条件应当成为筛选字段，不能藏在一篇长教程末尾。[iStore](https://github.com/linkease/istore)、[Nikki](https://github.com/nikkinikki-org/OpenWrt-nikki)。

本轮额外收录 FreshTomato、Gargoyle、Padavan 与 GL.iNet 官方系统，便于用户从自己的设备出发寻找方案；这些固件也各有型号及功能限制。

## 后续知识文章的组织方式

同一项目页回答“它是什么、适用环境、需要什么、与谁关联、信息核验到了哪一步”。教程页围绕用户任务组织，并引用项目页，避免重复维护版本资料。

优先文章：

1. 家中多设备统一管理：主路由、旁路由与单机客户端的选择依据。
2. 华硕用户如何识别原厂、原版 Merlin、GNUton、官改和梅改。
3. 插件、核心、协议、订阅和规则分别负责什么。
4. 同为 ARM 为什么包不能通用：硬件、内核与用户空间 ABI。
5. DNS 解析与代理出口如何协同，为什么“能解析”不代表“能连通”。
6. 按设备、SSID、域名选择出口；OpenVPN/WireGuard 与透明代理的关系。
7. 固件更新前的资料核对、配置备份、冲突检查与回退资料入口。
8. 不可用时按本地网络、DNS、核心、服务端、规则逐层诊断。

这些是编写队列；本轮没有把队列中的操作描述成已经验证的教程。
