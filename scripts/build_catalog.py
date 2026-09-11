#!/usr/bin/env python3
"""Render the complete catalog and GitHub observations; never modify snapshots.

Only entity.repository determines monitoring identity. A successful GitHub request
does not verify that a reference-only entity is the project it claims to be.
"""

import argparse
import html
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PATH = Path("export/library-v0.1-2026-09-11.json")
MANIFEST_PATH = Path("config/upstream-repositories.json")
CARD_SUFFIX = "-v0.1-2026-09-11.md"
# Existing GitHub accounts can end in a hyphen (for example wangyu-).
OWNER = r"[A-Za-z0-9][A-Za-z0-9-]{0,38}"
REPOSITORY = r"[A-Za-z0-9_.-]{1,100}"
ROOT_URL = re.compile(rf"https://github\.com/({OWNER})/({REPOSITORY})/?\Z")
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
KINDS = {
    "client": "客户端", "core": "代理核心", "protocol": "协议",
    "transport": "传输与外层方案", "concept": "基础概念", "firmware": "路由器固件",
    "router_plugin": "路由器插件", "package_ecosystem": "软件包生态",
    "deployment": "部署工具", "panel": "管理面板", "rules": "规则集",
    "dns": "DNS 工具", "subscription": "订阅管理", "browser_extension": "浏览器扩展",
    "vpn": "VPN", "mesh": "组网工具", "diagnostic": "诊断工具",
    "library": "开发库", "directory": "资料目录", "historical": "历史项目",
}
REVIEW = {
    "primary_reviewed": "已阅读第一方来源；未作安装保证",
    "reference_only": "仅参考目录线索；项目身份未核验",
    "historical_reference": "历史资料；未确认当前可用",
}
EXCLUSIONS = {
    "missing_repository": "未填写 repository",
    "non_github_repository": "非 GitHub 仓库",
    "invalid_repository_mapping": "地址不是有效的 GitHub 根仓库",
}


def cell(value):
    """Remote strings become plain single-line table text, not Markdown/HTML."""
    if value is None:
        return "未记录"
    text = re.sub(r"[\x00-\x1f\x7f\u2028\u2029]+", " ", str(value))
    text = " ".join(text.split())
    text = html.escape(text, quote=True)
    for char in "\\|`[]*_{}()":
        text = text.replace(char, "&#%d;" % ord(char))
    return text or "未记录"


def github_root(value):
    """Return owner/repo only for a strict HTTPS root URL; no inference."""
    if not isinstance(value, str):
        return None
    match = ROOT_URL.fullmatch(value)
    if not match:
        return None
    owner, repo = match.groups()
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not repo or repo in {".", ".."}:
        return None
    return owner + "/" + repo


def exclusion_reason(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return "missing_repository"
    if isinstance(value, str):
        try:
            hostname = urlsplit(value).hostname
        except ValueError:
            hostname = None
        if hostname and hostname.lower() != "github.com":
            return "non_github_repository"
    return "invalid_repository_mapping"


def validate_library(library):
    if not isinstance(library, list):
        raise ValueError("library must be a JSON list")
    seen = set()
    for entity in library:
        if not isinstance(entity, dict) or not isinstance(entity.get("id"), str):
            raise ValueError("every entity needs a string id")
        entity_id = entity["id"]
        if not ID.fullmatch(entity_id) or entity_id in seen:
            raise ValueError("invalid or duplicate entity id: " + entity_id)
        seen.add(entity_id)
        if not isinstance(entity.get("name"), str) or not isinstance(entity.get("kind"), str):
            raise ValueError("entity needs name and kind: " + entity_id)
        if not isinstance(entity.get("platforms"), list):
            raise ValueError("platforms must be a list: " + entity_id)
        if not all(isinstance(p, str) for p in entity["platforms"]):
            raise ValueError("platforms must contain strings: " + entity_id)
        if not isinstance(entity.get("verification"), dict):
            raise ValueError("verification must be an object: " + entity_id)


def make_manifest(library):
    validate_library(library)
    repos, excluded = {}, []
    for entity in sorted(library, key=lambda item: item["id"]):
        full_name = github_root(entity.get("repository"))
        if full_name is None:
            excluded.append({"entity_id": entity["id"], "reason": exclusion_reason(entity.get("repository"))})
            continue
        key = full_name.casefold()
        row = repos.setdefault(key, {"full_name": full_name, "entity_ids": []})
        row["full_name"] = min(row["full_name"], full_name)
        row["entity_ids"].append(entity["id"])
    return {"schema_version": 1, "repositories": [repos[k] for k in sorted(repos)], "excluded": excluded}


def validate_manifest(library, manifest):
    """Require exactly one mapping or exclusion per entity, matching repository."""
    expected = make_manifest(library)
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise ValueError("manifest schema_version must be 1")
    if not isinstance(manifest.get("repositories"), list) or not isinstance(manifest.get("excluded"), list):
        raise ValueError("manifest repositories and excluded must be lists")
    actual, seen_repos = {}, set()
    for row in manifest["repositories"]:
        if not isinstance(row, dict) or not isinstance(row.get("full_name"), str):
            raise ValueError("invalid manifest repository")
        name = row["full_name"]
        if github_root("https://github.com/" + name) != name or name.casefold() in seen_repos:
            raise ValueError("invalid or duplicate manifest repository: " + name)
        seen_repos.add(name.casefold())
        if not isinstance(row.get("entity_ids"), list) or not row["entity_ids"]:
            raise ValueError("repository entity_ids must be a nonempty list")
        for entity_id in row["entity_ids"]:
            if not isinstance(entity_id, str) or entity_id in actual:
                raise ValueError("entity occurs more than once in manifest")
            actual[entity_id] = ("repository", name.casefold())
    for row in manifest["excluded"]:
        if not isinstance(row, dict) or not isinstance(row.get("entity_id"), str) or row.get("reason") not in EXCLUSIONS:
            raise ValueError("invalid manifest exclusion")
        entity_id = row["entity_id"]
        if entity_id in actual:
            raise ValueError("entity occurs more than once in manifest: " + entity_id)
        actual[entity_id] = ("excluded", row["reason"])
    wanted = {}
    for row in expected["repositories"]:
        wanted.update({entity_id: ("repository", row["full_name"].casefold()) for entity_id in row["entity_ids"]})
    wanted.update({row["entity_id"]: ("excluded", row["reason"]) for row in expected["excluded"]})
    if actual != wanted:
        raise ValueError("manifest must cover every catalog entity exactly once using its repository field")


def validate_state(state):
    if not isinstance(state, dict) or type(state.get("schema_version")) is not int or state["schema_version"] != 1:
        raise ValueError("state schema_version must be 1")
    if not isinstance(state.get("repositories"), dict):
        raise ValueError("state repositories must be an object")
    run = state.get("last_run")
    if run is not None:
        if not isinstance(run, dict):
            raise ValueError("state last_run must be an object or null")
        for key in ("repository_count", "ok_count", "error_count"):
            if type(run.get(key)) is not int or run[key] < 0:
                raise ValueError("invalid last_run count: " + key)
        if run["ok_count"] + run["error_count"] != run["repository_count"]:
            raise ValueError("last_run counts do not add up")
    seen = set()
    for name, row in state["repositories"].items():
        if name.casefold() in seen or not isinstance(row, dict):
            raise ValueError("duplicate or invalid state repository")
        seen.add(name.casefold())
        if row.get("repository_status") not in {"ok", "unavailable", "error"}:
            raise ValueError("invalid repository_status")
        if row.get("release_status") not in {"ok", "none", "error", "not_checked"}:
            raise ValueError("invalid release_status")
        for key in ("repository", "release"):
            if row.get(key) is not None and not isinstance(row[key], dict):
                raise ValueError(key + " must be an object or null")


def date_text(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?", value):
        return "时间未记录"
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return "时间无效"
    return cell(value)


def release_url(value):
    if not isinstance(value, str) or re.search(r"[\x00-\x20\x7f<>\\]", value):
        return None
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment:
        return None
    parts = parsed.path.split("/")
    if len(parts) < 6 or parts[3:5] != ["releases", "tag"] or not parts[5]:
        return None
    if github_root("https://github.com/" + "/".join(parts[1:3])) is None:
        return None
    decoded = unquote(parsed.path)
    if re.search(r"[\x00-\x20\x7f<>\\]", decoded) or re.search(r"%(?![0-9A-Fa-f]{2})", parsed.path):
        return None
    return "https://github.com" + quote(parsed.path, safe="/%-._~:@!$&'()*+,;=")


def card_link(entity):
    return "[" + cell(entity["name"]) + "](export/cards/" + entity["id"] + CARD_SUFFIX + ")"


def repo_observation(row, detailed=False):
    if row is None:
        return "尚未检查"
    status = row["repository_status"]
    data = row.get("repository")
    if status == "ok":
        prefix = "检查成功：" + date_text(row.get("checked_at"))
    elif status == "unavailable":
        prefix = "本次不可用（不等于已删除）：" + date_text(row.get("checked_at"))
    else:
        prefix = "本次获取失败：" + date_text(row.get("checked_at"))
    if isinstance(data, dict):
        flags = []
        if type(data.get("archived")) is bool:
            flags.append("已归档" if data["archived"] else "未归档")
        else:
            flags.append("归档状态未记录")
        if data.get("disabled") is True:
            flags.append("已禁用")
        snapshot = "；".join(flags)
        if status != "ok":
            snapshot = "沿用旧记录：" + snapshot + "（最后成功 " + date_text(row.get("repository_last_success_at")) + "）"
        prefix += "；" + snapshot
        if detailed:
            actual = github_root(data.get("html_url"))
            label = "返回仓库" if status == "ok" else "旧记录仓库"
            if actual:
                prefix += "；" + label + "：[" + cell(actual) + "](<https://github.com/" + actual + ">)"
            else:
                prefix += "；" + label + "链接无效或缺失"
            prefix += "；" + ("最近推送 " if status == "ok" else "旧记录推送 ") + date_text(data.get("pushed_at"))
    elif status == "ok":
        prefix += "；元数据未记录"
    if status != "ok" and row.get("error_code"):
        prefix += "；错误 " + cell(row["error_code"])
    return prefix


def release_observation(row):
    if row is None:
        return "尚未检查"
    status = row["release_status"]
    if status == "none":
        return "检查成功，未发现 Release（" + date_text(row.get("release_last_success_at") or row.get("checked_at")) + "）"
    data = row.get("release")
    if status == "error":
        prefix = "本次 Release 获取失败"
    elif status == "not_checked":
        prefix = "本次未检查 Release"
    else:
        prefix = "最近一次成功观察"
    if isinstance(data, dict):
        tag = cell(data.get("tag_name"))
        link = release_url(data.get("html_url"))
        item = "[" + tag + "](<" + link + ">)" if link else tag + "（链接无效或缺失）"
        if status != "ok":
            prefix += "；沿用旧记录"
        prefix += "：" + item + "；发布 " + date_text(data.get("published_at"))
        prefix += "；最后成功 " + date_text(row.get("release_last_success_at"))
    elif status == "ok":
        prefix += "；发布记录缺失，不能判断版本"
    else:
        prefix += "；无可展示的历史成功记录"
    if status != "ok":
        prefix += "；本次检查 " + date_text(row.get("checked_at"))
    return prefix


def run_summary(state):
    run = state.get("last_run")
    if run is None:
        return "尚未运行 GitHub 元数据检查。"
    return ("最近一轮：" + date_text(run.get("checked_at")) + "；仓库数 " + str(run["repository_count"])
            + "，成功 " + str(run["ok_count"]) + "，错误 " + str(run["error_count"]) + "。单项结果和最后成功时间见下表。")


def render(library, manifest, state):
    validate_manifest(library, manifest)
    validate_state(state)
    entities = {item["id"]: item for item in library}
    mapping = {entity_id: row["full_name"] for row in manifest["repositories"] for entity_id in row["entity_ids"]}
    excluded = {row["entity_id"]: row["reason"] for row in manifest["excluded"]}
    observations = {key.casefold(): value for key, value in state["repositories"].items()}
    catalog = ["# 工具与知识目录", "", "共 " + str(len(library)) + " 条资料。按类型浏览，点击名称阅读完整卡片。", "",
               "“已阅读第一方来源”仅表示内容来源审核，不表示安装、安全、兼容性或大陆连通性测试通过。仅参考目录线索的条目，即使 GitHub 请求成功，项目身份仍未核验。", "",
               "GitHub 列仅展示自动检查保存的元数据；未归档不等于正在维护，Release 不等于兼容版本。没有状态文件时显示尚未检查，不采用历史来源快照冒充当前数据。", "", run_summary(state), "",
               "[查看更新检查及覆盖范围](UPDATES.md)", ""]
    kinds = sorted({item["kind"] for item in library}, key=lambda kind: (list(KINDS).index(kind) if kind in KINDS else len(KINDS), kind))
    for kind in kinds:
        group = sorted((item for item in library if item["kind"] == kind), key=lambda item: (item["name"].casefold(), item["id"]))
        catalog.extend(["## " + cell(KINDS.get(kind, kind)) + "（" + str(len(group)) + "）", "",
                        "| 项目与完整卡片 | 平台 | 内容审核 | GitHub 仓库观察 | GitHub Release 观察 |",
                        "| --- | --- | --- | --- | --- |"])
        for entity in group:
            full_name = mapping.get(entity["id"])
            row = observations.get(full_name.casefold()) if full_name else None
            repo_text = repo_observation(row) if full_name else "未纳入监测：" + EXCLUSIONS[excluded[entity["id"]]]
            release_text = release_observation(row) if full_name else "不适用；未建立根仓库映射"
            platforms = "、".join(cell(p) for p in entity["platforms"]) or "未记录或不适用"
            review = cell(REVIEW.get(entity["verification"].get("status"), "审核状态未识别，需查看卡片"))
            catalog.append("| " + " | ".join([card_link(entity), platforms, review, repo_text, release_text]) + " |")
        catalog.append("")
    updates = ["# GitHub 元数据观察记录", "", run_summary(state), "", "## 覆盖范围", "",
               "- 资料总数：" + str(len(library)),
               "- 纳入监测：" + str(len(mapping)) + " 条资料，映射到 " + str(len(manifest["repositories"])) + " 个去重根仓库。",
               "- 未纳入监测：" + str(len(excluded)) + " 条资料；原因如下。", "",
               "| 未纳入原因 | 条目数 |", "| --- | --- |"]
    reason_counts = Counter(excluded.values())
    updates.extend("| " + label + " | " + str(reason_counts.get(reason, 0)) + " |" for reason, label in EXCLUSIONS.items())
    updates.extend(["", "## 观察边界", "",
                    "- 清单只读取原始条目的 repository 字段；仅接受 HTTPS GitHub 根仓库地址（允许末尾 / 或 .git），按仓库名忽略大小写去重。没有从官网、发现来源或历史版本链接推断归属。",
                    "- 自动结果仅包括仓库公开可访问性、返回的仓库地址、归档/禁用状态、最近推送时间，以及 GitHub 最新正式 Release（不含草稿和预发布）；这不是发行版安装或功能测试。",
                    "- 仓库不可用或请求失败不等于仓库已删除；没有 Release、未检查、获取失败分别展示。正式 Release 查询不包含 tags 或应用商店版本。",
                    "- 请求失败保留旧值时，明确标注沿用旧记录及最后成功时间；日期不是维护活跃度、教程更新或兼容性证明。",
                    "- 元数据检查不会提升原有内容审核等级，也不会确认参考目录条目的身份、路由器型号兼容性、安全性或大陆访问效果。",
                    "- 本页和目录由固定导出快照、映射清单与状态文件生成；没有改写旧卡片、JSON、JSONL 或 SQLite 快照。", "",
                    "## 根仓库检查结果", "", "| GitHub 根仓库 | 关联资料 | 仓库观察 | Release 观察 |", "| --- | --- | --- | --- |"])
    for repo in sorted(manifest["repositories"], key=lambda item: (item["full_name"].casefold(), item["full_name"])):
        name = repo["full_name"]
        row = observations.get(name.casefold())
        links = "、".join(card_link(entities[entity_id]) for entity_id in sorted(repo["entity_ids"]))
        repo_link = "[" + cell(name) + "](<https://github.com/" + name + ">)"
        updates.append("| " + " | ".join([repo_link, links, repo_observation(row, detailed=True), release_observation(row)]) + " |")
    updates.extend(["", "## 未纳入监测的资料", "", "| 资料 | 原因 |", "| --- | --- |"])
    for entity_id in sorted(excluded):
        updates.append("| " + card_link(entities[entity_id]) + " | " + EXCLUSIONS[excluded[entity_id]] + " |")
    return "\n".join(catalog).rstrip() + "\n", "\n".join(updates).rstrip() + "\n"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / "data/upstream.json")
    parser.add_argument("--catalog-output", type=Path, default=ROOT / "CATALOG.md")
    parser.add_argument("--updates-output", type=Path, default=ROOT / "UPDATES.md")
    parser.add_argument("--write-manifest", action="store_true", help="rebuild manifest strictly from entity.repository")
    args = parser.parse_args(argv)
    library = read_json(ROOT / LIBRARY_PATH)
    if args.write_manifest:
        manifest = make_manifest(library)
    else:
        manifest = read_json(ROOT / MANIFEST_PATH)
    state = read_json(args.state) if args.state.exists() else {"schema_version": 1, "last_run": None, "repositories": {}}
    catalog, updates = render(library, manifest, state)
    for entity in library:
        if not (ROOT / "export/cards" / (entity["id"] + CARD_SUFFIX)).is_file():
            raise ValueError("missing original card: " + entity["id"])
    if args.write_manifest:
        (ROOT / MANIFEST_PATH).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / MANIFEST_PATH).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    for path, content in ((args.catalog_output, catalog), (args.updates_output, updates)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print("Rendered %d entities; %d monitored repositories; %d exclusions." % (len(library), len(manifest["repositories"]), len(manifest["excluded"])))


if __name__ == "__main__":
    main()
