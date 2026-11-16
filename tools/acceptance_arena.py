#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""算法竞技场专项验收：赛制、竞速积分、赛后总结、战绩卡与本地赛季接线。"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
ARENA_JS = (ROOT / "web" / "arena.js").read_text(encoding="utf-8")
ARENA_CSS = (ROOT / "web" / "arena.css").read_text(encoding="utf-8")
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

    checks = [
        ("五视图含竞技场入口",
         'data-view="arena"' in HTML and 'data-view="grammar"' in HTML
         and 'id="arenaWorkspace"' in HTML and 'id="viewSwitch"' in HTML),
        ("比赛中页头与侧栏",
         'id="arenaHeadLive"' in HTML and 'id="arenaSide"' in HTML
         and 'arena-live' in ARENA_CSS),
        ("赛后总结与交卷确认",
         'id="arenaRecap"' in HTML and 'id="arenaConfirm"' in HTML
         and 'arenaShowRecap' in ARENA_JS and 'arenaAskFinish' in ARENA_JS),
        ("三种赛制与题量",
         len(re.findall(r"key: '(sprint|standard|expedition)'", ARENA_JS)) == 3
         and "count: 2" in ARENA_JS and "count: 3" in ARENA_JS and "count: 4" in ARENA_JS),
        ("竞速积分与罚时",
         "ARENA_BASE" in ARENA_JS and "speedFactor" in ARENA_JS
         and "attempts * 5" in ARENA_JS and "penalty" in ARENA_JS),
        ("提交即时结算接线",
         "arenaOnSubmit(p, res)" in JS and "function arenaOnSubmit" in ARENA_JS
         and "function arenaFinish" in ARENA_JS),
        ("全部解出自提交",
         "allSolved" in ARENA_JS and "arenaFinish(true" in ARENA_JS
         and "自动交卷" in ARENA_JS),
        ("本地赛季持久化",
         "oj.arena.v1" in ARENA_JS and "localStorage" in ARENA_JS
         and "arenaAfterData" in ARENA_JS and "arenaGrade" in ARENA_JS),
        ("赛后 AI 复盘与战绩卡",
         "arenaReviewRecord" in ARENA_JS and "aiSetMode('review')" in ARENA_JS
         and "arenaSaveCard" in ARENA_JS and "canvas.toBlob" in ARENA_JS),
        ("视觉样式与窄屏适配",
         ".arena-hero" in ARENA_CSS and ".arena-prob" in ARENA_CSS
         and ".arena-recap-grade" in ARENA_CSS and "@media (max-width: 900px)" in ARENA_CSS),
        ("题库可判与难度覆盖",
         len(judged) >= 300 and difficulties >= {1, 2, 3, 4, 5}),
        ("页面 ID 不重复",
         not duplicate_ids),
    ]

    ok = 0
    for name, passed in checks:
        print(f"  [{'通过' if passed else '失败'}] {name}")
        ok += 1 if passed else 0
    print(f"题库：{len(PROBLEMS)} 道，可判 {len(judged)} 道，难度覆盖 {sorted(difficulties)}")
    if duplicate_ids:
        print("重复 ID：", duplicate_ids)
    print(f"结果：通过 {ok}，失败 {len(checks) - ok}")
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
