#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把没有做成判题的章末习题整理成「思考题」页面，并挂上附录 E 的提示。"""
import json
import os
import re

BOOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CH_DIR = os.path.join(BOOK, "chapters")
APP_E = os.path.join(BOOK, "appendix", "E.md")
DATA = os.path.join(BOOK, "oj", "data")
OUT = os.path.join(DATA, "extra", "think_all.json")

TAG_DIFF = {"基础": 1, "提高": 2, "挑战": 3}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_items(body):
    parts = re.split(r"\n(?=\d+\.\s)", body)
    items = {}
    for part in parts:
        m = re.match(r"(\d+)\.\s+(.*)", part.strip(), re.S)
        if not m:
            continue
        num = int(m.group(1))
        items[num] = m.group(2).strip()
    return items


def parse_chapter_exercises():
    result = {}
    for i in range(1, 33):
        path = os.path.join(CH_DIR, "ch%02d.md" % i)
        if not os.path.exists(path):
            continue
        text = read(path)
        idx = text.find("## 习题")
        if idx < 0:
            continue
        body = text[idx + len("## 习题"):]
        nxt = body.find("\n## ")
        if nxt >= 0:
            body = body[:nxt]
        body = re.sub(r"^\s*\n", "", body)
        result[i] = parse_items(body)
    return result


def parse_appendix_e():
    text = read(APP_E)
    hints = {}
    secs = list(re.finditer(r"## E\.(\d+)\s+\S*第\s*(\d+)\s*章", text))
    for k, m in enumerate(secs):
        end = secs[k + 1].start() if k + 1 < len(secs) else len(text)
        body = text[m.end():end]
        ch = int(m.group(2))
        hints[ch] = parse_items(body)
    return hints


def make_title(text, num):
    body = re.split(r"[。；！？\n]", text)[0]
    body = re.sub(r"\*\*|`|>|「|」|“|”|\"", "", body)
    first = re.sub(r"（[^）]*）|\([^)]*\)", "", body).strip()
    first = re.sub(r"\s+", " ", first).strip(" ，、：")
    if len(first) > 22:
        first = first[:22] + "…"
    return first or "（思考题）"


def main():
    ch_ex = parse_chapter_exercises()
    hints = parse_appendix_e()
    total = sum(len(v) for v in ch_ex.values())
    print("书稿习题共 %d 道（%d 章）" % (total, len(ch_ex)))

    # 判题题目以 extra/*.json（不含 think_all.json）和 examples.json 为准，
    # 不读 problems.json，避免上一轮生成结果互相覆盖造成 ID 重复。
    judged = set()
    ex_path = os.path.join(DATA, "examples.json")
    if os.path.exists(ex_path):
        with open(ex_path, encoding="utf-8") as f:
            judged.update(p["id"] for p in json.load(f))
    extra_dir = os.path.join(DATA, "extra")
    for fn in sorted(os.listdir(extra_dir)):
        if not fn.endswith(".json") or fn == "think_all.json":
            continue
        with open(os.path.join(extra_dir, fn), encoding="utf-8") as f:
            judged.update(p["id"] for p in json.load(f)
                          if p.get("kind", "exercise") in ("exercise", "example", "appendix"))

    out = []
    thinking = 0
    covered = 0
    for ch, items in sorted(ch_ex.items()):
        for num, raw in sorted(items.items()):
            pid = "p-%02d-%02d" % (ch, num)
            if pid in judged:
                covered += 1
                continue
            tag = "基础"
            m = re.search(r"\[(基础|提高|挑战)\]", raw)
            if m:
                tag = m.group(1)
            text = re.sub(r"^\[(基础|提高|挑战)\]\s*", "", raw).strip()
            hint = hints.get(ch, {}).get(num, "")
            hint = re.sub(r"^提示[:：]\s*", "", hint).strip()
            out.append({
                "id": pid,
                "kind": "think",
                "chapter": ch,
                "label": "习题 %d-%d" % (ch, num),
                "title": make_title(text, num),
                "difficulty": TAG_DIFF.get(tag, 1),
                "statement_md": text,
                "input_md": "",
                "output_md": "",
                "constraints_md": "",
                "hint_md": hint,
                "tags": ["思考题", tag],
                "tests": [],
                "samples": [],
                "source": "《从语法到算法：C++ 算法设计与 ACM 竞赛入门》习题 %d-%d" % (ch, num),
            })
            thinking += 1

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("已做成判题：%d 道；生成思考题页面：%d 道；合计 %d 道" % (covered, thinking, covered + thinking))
    print("输出：", OUT)


if __name__ == "__main__":
    main()
