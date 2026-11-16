#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学习轨迹 / 提交记录专项验收：服务端历史 API、前端学习页、回放弹层。"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
CSS = (ROOT / "web" / "style.css").read_text(encoding="utf-8")
RPG_CSS = (ROOT / "web" / "rpg.css").read_text(encoding="utf-8")
BASE = "http://127.0.0.1:8765"


def api(path):
    req = urllib.request.Request(BASE + path, headers={"Cache-Control": "no-store"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    checks = [
        ("五视图切换",
         'data-view="stats"' in HTML and 'data-view="arena"' in HTML and 'data-view="grammar"' in HTML
         and "view === 'book' || view === 'stats' || view === 'arena' || view === 'grammar'" in JS),
        ("学习页骨架",
         'id="statsWorkspace"' in HTML and 'id="statsHeatmap"' in HTML and "function renderStats" in JS
         and ".stats-workspace" in CSS),
        ("活跃热力图",
         "function renderStatsHeatmap" in JS and "heat-cell" in CSS and "statsState.dateFilter" in JS),
        ("提交记录抽屉",
         'id="historyPanel"' in HTML and "function toggleProblemHistory" in JS
         and ".history-inline" in CSS and 'id="btnHistory"' in JS),
        ("提交详情 / 代码回放",
         'id="submissionBackdrop"' in HTML and "function openSubmission" in JS
         and "submissionLoadCode" in JS and ".submission-panel" in CSS),
        ("学习报告导出",
         'id="statsExport"' in HTML and "function exportStatsReport" in JS
         and "statsReportMarkdown" in JS),
        ("AI Markdown 列表渲染",
         "function mdToHtml" in JS and "let listStart = 0;" in JS
         and "function bookMdToHtml" in JS),
        ("代码编辑器高亮 / 补全 / 缩进",
         'id="codeHighlight"' in HTML and 'id="codeSuggest"' in HTML
         and "function highlightCpp" in JS and "function updateCodeSuggest" in JS
         and "function handleEditorEnter" in JS and ".code-highlight" in CSS),
        ("AI 出题工作台",
         'id="aiGenPanel"' in HTML and 'id="aiGenDifficulty"' in HTML
         and "function aiGenerateProblem" in JS and "function aiSaveGenerated" in JS
         and "/api/problems/generated" in JS and ".ai-gen-panel" in CSS),
        ("保存代码文件",
         'id="btnSaveCode"' in HTML and "function saveCodeFile" in JS
         and "showSaveFilePicker" in JS),
        ("冒险等级 / 经验 / 升级动画",
         'id="rpgHud"' in HTML and 'id="rpgProfile"' in HTML
         and 'id="rpgBackdrop"' in HTML and 'id="levelupBackdrop"' in HTML
         and 'href="/static/rpg.css' in HTML
         and "RPG_DIFF_XP" in JS and "function rpgAfterSubmit" in JS
         and "function rpgSyncFromProgress" in JS and "rpgAfterSubmit(p, res, wasAC)" in JS
         and ".rpg-hud" in RPG_CSS and ".levelup-card" in RPG_CSS),
        ("CE/WA 智能 Debug 建议",
         'id="aiDebugSuggest"' in HTML and 'id="aiDebugGo"' in HTML
         and "function showDebugSuggest" in JS and "function aiDebugStart" in JS
         and "maybeShowDebugSuggest('submit', res)" in JS
         and "showDebugSuggest('run', state.lastResult)" in JS
         and ".ai-debug-suggest" in CSS),
        ("学习数据与提交存储",
         "SUBMISSIONS_JSON" in (ROOT / "server.py").read_text(encoding="utf-8")
         and "add_submission" in (ROOT / "server.py").read_text(encoding="utf-8")
         and "submission_summary" in (ROOT / "server.py").read_text(encoding="utf-8")),
    ]

    problems = json.loads((ROOT / "data" / "problems.json").read_text(encoding="utf-8"))["problems"]
    judged = [p for p in problems if p.get("tests") and p.get("kind") != "ai"]
    checks.append(("题库难度数据可汇总",
                   len(judged) == 348 and len({p.get("difficulty") for p in judged}) == 5))

    try:
        data = api("/api/submissions?limit=20")
        checks.append(("提交历史 API",
                       isinstance(data.get("items"), list) and "total" in data
                       and all("code" not in x for x in data.get("items", []))))
        if data.get("items"):
            one = api("/api/submissions/" + str(data["items"][0]["id"]))
            checks.append(("提交详情 API 含代码与用例",
                           bool(one.get("code")) and isinstance(one.get("cases"), list)))
        try:
            api("/api/submissions/__missing__")
            missing_ok = False
        except urllib.error.HTTPError as e:
            missing_ok = e.code == 404
        checks.append(("不存在的提交返回 404", missing_ok))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        checks.append(("本机服务可访问", False))
        print("  服务不可访问：", e)

    ok = 0
    for name, passed in checks:
        print(f"  [{'通过' if passed else '失败'}] {name}")
        ok += 1 if passed else 0
    print(f"结果：通过 {ok}，失败 {len(checks) - ok}")
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
