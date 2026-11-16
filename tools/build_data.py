#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把例题、习题、附录 C 合并成 data/problems.json，并做一致性检查。"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
EXAMPLES = os.path.join(DATA, "examples.json")
EXTRA_DIR = os.path.join(DATA, "extra")
OUT = os.path.join(DATA, "problems.json")
DUP_JSON = os.path.join(DATA, "duplicates.json")
NOTES_JSON = os.path.join(DATA, "merge_notes.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(p):
    p.setdefault("kind", "exercise")
    p.setdefault("chapter", 0)
    p.setdefault("chapter_title", "")
    p.setdefault("difficulty", 2)
    p.setdefault("time_limit", 1.0)
    p.setdefault("samples", [])
    p.setdefault("tests", [])
    p.setdefault("tags", [])
    p.setdefault("hint_md", "")
    p.setdefault("source", "")
    if p["kind"] == "appendix":
        p["chapter"] = 0
        p["chapter_title"] = "贵阳主题练习"
        p.setdefault("label", "C-" + p["id"].split("-")[-1])
    if p["kind"] == "local":
        p["chapter"] = 0
        p["chapter_title"] = "贵阳生活 100 题"
        p.setdefault("label", p["id"].upper())
    return p


def load_optional(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def main():
    deprecated = load_optional(DUP_JSON, {"duplicates": []})
    drop = {d["id"]: d for d in deprecated.get("duplicates", [])}
    notes = load_optional(NOTES_JSON, {})
    problems = []
    if os.path.exists(EXAMPLES):
        for p in load_json(EXAMPLES):
            p["difficulty"] = p.get("difficulty", 2)
            problems.append(normalize(p))
    if os.path.isdir(EXTRA_DIR):
        for fn in sorted(os.listdir(EXTRA_DIR)):
            if fn.endswith(".json"):
                for p in load_json(os.path.join(EXTRA_DIR, fn)):
                    problems.append(normalize(p))

    # 去重：按 data/duplicates.json 的结论剔除重复题，并把被删题的补充说明并回保留题
    kept = []
    removed = []
    for p in problems:
        if p["id"] in drop:
            removed.append(p["id"])
            continue
        if p["id"] in notes:
            extra = notes[p["id"]].strip()
            if extra:
                p["note_md"] = (p.get("note_md") or "").strip()
                p["note_md"] = (p["note_md"] + "\n\n" + extra).strip()
        kept.append(p)
    problems = kept
    if removed:
        print("去重：移除 %d 道重复题 %s" % (len(removed), ", ".join(sorted(removed))))

    # 去重
    seen = {}
    for p in problems:
        if p["id"] in seen:
            print("重复题目 ID：", p["id"], "（后一条覆盖前一条）")
        seen[p["id"]] = p
    problems = list(seen.values())

    kind_order = {"example": 0, "exercise": 1, "think": 2, "reading": 3, "appendix": 4, "local": 5}
    problems.sort(key=lambda p: (p["chapter"] if p["chapter"] else 99,
                                 kind_order.get(p["kind"], 9), p["id"]))

    # 检查
    errs = []
    for p in problems:
        for key in ("id", "title", "statement_md"):
            if not p.get(key):
                errs.append("%s 缺少 %s" % (p.get("id"), key))
        if p["kind"] in ("example", "exercise", "appendix", "local") and not p["tests"]:
            errs.append("%s 没有测试数据" % p["id"])
        for t in p["tests"]:
            if "in" not in t or "out" not in t:
                errs.append("%s 用例字段不全" % p["id"])
        if len(p["tests"]) > 0 and not p["samples"]:
            errs.append("%s 缺少样例" % p["id"])

    # 可解释难度评估 + 提示补全
    try:
        from evaluate_difficulty import enrich
        enrich(problems)
    except Exception as e:
        print("难度评估跳过：%r" % (e,))

    meta = {
        "book": "《从语法到算法：C++ 算法设计与 ACM 竞赛入门》",
        "count": len(problems),
        "counts": {
            "example": sum(1 for p in problems if p["kind"] == "example"),
            "exercise": sum(1 for p in problems if p["kind"] == "exercise"),
            "think": sum(1 for p in problems if p["kind"] == "think"),
            "reading": sum(1 for p in problems if p["kind"] == "reading"),
            "appendix": sum(1 for p in problems if p["kind"] == "appendix"),
            "local": sum(1 for p in problems if p["kind"] == "local"),
        },
        "deduplicated": sorted(drop.keys()),
        "difficulty_counts": {
            str(i): sum(1 for p in problems if p.get("difficulty") == i) for i in range(1, 6)
        },
        "chapters": sorted({p["chapter"] for p in problems if p["chapter"]}),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "problems": problems}, f, ensure_ascii=False, indent=1)

    print("总题目：%d" % len(problems))
    print("分类：", meta["counts"])
    if errs:
        print("检查问题：")
        for e in errs:
            print(" -", e)
    else:
        print("检查：全部通过")


if __name__ == "__main__":
    main()
