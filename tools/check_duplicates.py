#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查题库里的重复题，输出 data/duplicates_report.json。

判定：
  1. 标题归一化后完全相同；
  2. 题面归一化后完全相同；
  3. 测试数据集合逐字相同（且不是空测试的思考题）；
  4. 标题/题面相似度 ≥ 0.85，作为人工复核线索。
"""
import difflib
import hashlib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
PROBLEMS = os.path.join(DATA, "problems.json")
DUP = os.path.join(DATA, "duplicates.json")
OUT = os.path.join(DATA, "duplicates_report.json")


def norm(s):
    s = re.sub(r"\s+", "", s or "")
    s = re.sub(r"[，。、；：！？“”‘’（）()《》<>【】\[\],.;:!?\"']", "", s)
    s = re.sub(r"本题是第.*?章习题.*?。", "", s)
    return s


def main():
    with open(PROBLEMS, encoding="utf-8") as f:
        problems = json.load(f)["problems"]
    with open(DUP, encoding="utf-8") as f:
        dup = json.load(f)
    removed = {d["id"]: d for d in dup.get("duplicates", [])}
    kept = {}
    for v in dup.get("kept_variants", []):
        ids = v.get("ids") or []
        if len(ids) >= 2:
            kept[tuple(sorted(ids))] = v.get("reason", "")

    groups = {"same_title": [], "same_statement": [], "same_tests": [], "kept_same_tests": [], "near": []}
    by_title, by_stmt, by_tests = {}, {}, {}
    for p in problems:
        by_title.setdefault(norm(p["title"]), []).append(p["id"])
        by_stmt.setdefault(norm(p.get("statement_md", "")), []).append(p["id"])
        tests = p.get("tests") or []
        if tests:
            h = hashlib.md5(json.dumps(tests, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            by_tests.setdefault(h, []).append(p["id"])

    for k, ids in by_title.items():
        if len(ids) > 1:
            groups["same_title"].append({"title": k, "ids": ids})
    for k, ids in by_stmt.items():
        if len(ids) > 1:
            groups["same_statement"].append({"ids": ids})
    for k, ids in by_tests.items():
        if len(ids) > 1:
            if tuple(sorted(ids)) in kept:
                groups["kept_same_tests"].append({"ids": ids, "reason": kept[tuple(sorted(ids))]})
            else:
                groups["same_tests"].append({"ids": ids})

    for i in range(len(problems)):
        for j in range(i + 1, len(problems)):
            a, b = problems[i], problems[j]
            t = difflib.SequenceMatcher(None, norm(a["title"]), norm(b["title"])).ratio()
            s = difflib.SequenceMatcher(None, norm(a.get("statement_md", "")),
                                        norm(b.get("statement_md", ""))).ratio()
            if t >= 0.9 or s >= 0.85:
                item = {"ids": [a["id"], b["id"]], "title_ratio": round(t, 3),
                        "statement_ratio": round(s, 3)}
                pair = tuple(sorted([a["id"], b["id"]]))
                if pair in kept:
                    item["kept_reason"] = kept[pair]
                elif a["id"].startswith("gy-") and b["id"].startswith("gy-"):
                    item["note"] = "同一题型模板下的不同贵阳生活场景，输入数据与答案不同"
                groups["near"].append(item)

    report = {
        "checked": len(problems),
        "duplicates_removed": len(removed),
        "removed": list(removed.values()),
        "kept_variants": dup.get("kept_variants", []),
        "groups": {k: v for k, v in groups.items()},
        "note": "same_tests 只列未获保留的同测试题；kept_same_tests 是已在 duplicates.json 说明的同题多解/不同模型；near 只作复核线索，不自动删除。",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print("检查 %d 题；已按结论移除 %d 道重复题。" % (len(problems), len(removed)))
    print("同标题 %d 组，同题面 %d 组，同测试数据 %d 组，保留 variant 同测试 %d 对，相似待复核 %d 组。"
          % (len(groups["same_title"]), len(groups["same_statement"]),
             len(groups["same_tests"]), len(groups["kept_same_tests"]), len(groups["near"])))
    for g in groups["same_tests"]:
        print("  同测试：", g["ids"])
    for g in groups["same_title"]:
        print("  同标题：", g["title"], g["ids"])
    print("报告：", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
