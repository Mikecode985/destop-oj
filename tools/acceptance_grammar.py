#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""语法加油站专项验收：第五视图、体检规则、急救卡、语法卡、小练习、联动与本地存储。"""
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
GRAMMAR_JS = (ROOT / "web" / "grammar.js").read_text(encoding="utf-8")
GRAMMAR_CSS = (ROOT / "web" / "grammar.css").read_text(encoding="utf-8")
PROBLEMS = json.loads((ROOT / "data" / "problems.json").read_text(encoding="utf-8"))
PROBLEMS = PROBLEMS.get("problems", PROBLEMS) if isinstance(PROBLEMS, dict) else PROBLEMS


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == "id" and value:
                self.ids.append(value)


def main() -> int:
    ids = IdCollector()
    ids.feed(HTML)
    duplicate_ids = sorted({x for x in ids.ids if ids.ids.count(x) > 1})
    judged = [p for p in PROBLEMS if p.get("tests")]
    difficulties = {p.get("difficulty") for p in judged}
    symptom_count = len(re.findall(r"key: '(ce|wa|re|tle|io|overflow)'", GRAMMAR_JS))
    card_count = len(re.findall(r"id: '(starter|input|vector|sort|string|number|struct|debug)'", GRAMMAR_JS))
    quiz_count = len(re.findall(r"answer: \d", GRAMMAR_JS))

    try:
        node_check = subprocess.run(
            ["node", "--check", str(ROOT / "web" / "grammar.js")],
            capture_output=True, text=True, timeout=20,
        )
        node_ok = node_check.returncode == 0
    except Exception:
        node_ok = False

    checks = [
        ("第五视图入口",
         'data-view="grammar"' in HTML and 'id="grammarWorkspace"' in HTML
         and 'grammar.css' in HTML and 'grammar.js' in HTML
         and 'grammar-tab' in HTML),
        ("app.js 五视图接线",
         "view === 'grammar'" in JS and "currentView === 'grammar'" in JS
         and "grammarRender()" in JS and "grammarAfterData()" in JS
         and "grammar-mode" in JS),
        ("Hero 与今日加油表",
         'grammarHeroHtml' in GRAMMAR_JS and 'grammar-meter' in GRAMMAR_JS
         and 'DAILY FUEL' in GRAMMAR_JS and 'todayCount' in GRAMMAR_JS
         and 'CURRENT PROBLEM' in GRAMMAR_JS),
        ("当前代码体检规则",
         'function grammarDiagnose' in GRAMMAR_JS
         and 'bits/stdc' in GRAMMAR_JS and 'int main' in GRAMMAR_JS
         and 'using namespace std' in GRAMMAR_JS and 'return 0' in GRAMMAR_JS
         and 'sync_with_stdio' in GRAMMAR_JS),
        ("启发式错误覆盖",
         all(x in GRAMMAR_JS for x in [
             "中文标点", "循环体只有一个分号", "if 条件里像是赋值",
             "局部大数组可能爆栈", "getline 前可能吃不到换行",
             "循环里的 endl 会拖慢输出", "乘法前确认类型",
         ])),
        ("诊断严重程度与定位",
         "severity" in GRAMMAR_JS and "grammarIssueLine" in GRAMMAR_JS
         and "data-g-line" in GRAMMAR_JS and "grammarJumpLine" in GRAMMAR_JS
         and "editorSetValue" in GRAMMAR_JS),
        ("错误急救六卡",
         symptom_count == 6 and 'GRAMMAR_SYMPTOMS' in GRAMMAR_JS
         and 'grammar-triage' in GRAMMAR_CSS and 'grammar-symptom' in GRAMMAR_CSS),
        ("语法货架八卡",
         card_count == 8 and 'GRAMMAR_CARDS' in GRAMMAR_JS
         and 'grammar-card' in GRAMMAR_CSS and 'grammar-card-grid' in GRAMMAR_JS),
        ("5 分钟小练习",
         quiz_count == 8 and 'GRAMMAR_QUIZ' in GRAMMAR_JS
         and 'slice(0, 5)' in GRAMMAR_JS and 'grammarAnswer' in GRAMMAR_JS
         and 'grammarNext' in GRAMMAR_JS and 'grammarNewQuiz' in GRAMMAR_JS
         and 'grammar-quiz' in GRAMMAR_CSS),
        ("本地存储与统计",
         "GRAMMAR_KEY = 'oj.grammar.v1'" in GRAMMAR_JS
         and all(x in GRAMMAR_JS for x in ["visits", "scans", "copies", "answered", "correct", "sets", "best"])),
        ("AI 助教联动",
         "grammarAskAI" in GRAMMAR_JS and "aiSetMode('debug')" in GRAMMAR_JS
         and "aiOpen()" in GRAMMAR_JS and "aiInput" in GRAMMAR_JS
         and "不要先给完整答案" in GRAMMAR_JS),
        ("原书章节联动",
         "grammarOpenBook" in GRAMMAR_JS and "openBook(section" in GRAMMAR_JS
         and "ch02" in GRAMMAR_JS and "ch28" in GRAMMAR_JS),
        ("复制与降级兜底",
         "navigator.clipboard" in GRAMMAR_JS and "execCommand('copy')" in GRAMMAR_JS
         and "grammarCopyFallback" in GRAMMAR_JS),
        ("视觉与响应式",
         ".grammar-workspace" in GRAMMAR_CSS and ".grammar-hero" in GRAMMAR_CSS
         and ".grammar-pass" in GRAMMAR_CSS and ".grammar-scan" in GRAMMAR_CSS
         and ".grammar-drill" in GRAMMAR_CSS
         and "@media (max-width: 980px)" in GRAMMAR_CSS
         and "@media (max-width: 700px)" in GRAMMAR_CSS),
        ("语法模式隐藏旧视图",
         "body.grammar-mode" in GRAMMAR_CSS and ".grammar-mode .layout" in GRAMMAR_CSS
         and ".grammar-mode .book-workspace" in GRAMMAR_CSS
         and ".grammar-mode .arena-workspace" in GRAMMAR_CSS),
        ("脚本语法可解析",
         node_ok),
        ("题库基线未受影响",
         len(PROBLEMS) >= 390 and len(judged) >= 300 and difficulties >= {1, 2, 3, 4, 5}),
        ("页面 ID 不重复",
         not duplicate_ids),
    ]

    ok = 0
    for name, passed in checks:
        print(f"  [{'通过' if passed else '失败'}] {name}")
        ok += 1 if passed else 0
    print(f"语法模块：急救 {symptom_count} 张，语法卡 {card_count} 张，小练习 {quiz_count} 题")
    print(f"题库：{len(PROBLEMS)} 道，可判 {len(judged)} 道，难度覆盖 {sorted(difficulties)}")
    if duplicate_ids:
        print("重复 ID：", duplicate_ids)
    print(f"结果：通过 {ok}，失败 {len(checks) - ok}")
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
