#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""刷题工作台专项验收：收藏、错题、每日/随机、本章题目联动。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
CSS = (ROOT / "web" / "style.css").read_text(encoding="utf-8")


def main() -> int:
    checks = [
        ("收藏 / 错题筛选",
         'data-filter="star"' in HTML and 'data-filter="wrong"' in HTML
         and "function toggleStar" in JS and "oj.stars" in JS),
        ("每日一题",
         'id="btnDaily"' in HTML and "function openDailyProblem" in JS and "function localDayKey" in JS),
        ("随机一题",
         'id="btnRandom"' in HTML and "function openRandomProblem" in JS and "notAC" in JS),
        ("本章题目反向联动",
         'id="bookRelated"' in HTML and "function renderBookRelated" in JS and ".book-related" in CSS),
    ]
    ok = 0
    for name, passed in checks:
        print(f"  [{'通过' if passed else '失败'}] {name}")
        ok += 1 if passed else 0
    print(f"结果：通过 {ok}，失败 {len(checks) - ok}")
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
