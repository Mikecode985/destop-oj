#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核对题库与原书阅读版的锚点覆盖率（纯离线，不启动服务）。

运行：python tools\\check_book_mapping.py
"""
import json
import os
import re

OJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(OJ, "data", "problems.json")
BOOK = os.path.join(OJ, "web", "book")


def norm(s):
    return re.sub(r"\s+", "", s or "")


def main():
    problems = json.load(open(DATA, encoding="utf-8"))["problems"]
    missing = []
    checked = 0
    for p in problems:
        if p.get("kind") in ("local", "ai"):
            continue
        label = p.get("label") or ""
        if p.get("kind") == "appendix":
            letter = label.split("-")[0].upper() if "-" in label else "C"
            section = os.path.join(BOOK, "chapters", "appendix-%s.md" % letter)
        else:
            ch = int(p.get("chapter") or 0)
            section = os.path.join(BOOK, "chapters", "ch%02d.md" % ch)
        if not os.path.exists(section):
            missing.append((p["id"], label, "章节文件不存在"))
            continue
        text = open(section, encoding="utf-8").read()
        heads = [l.lstrip("#").strip() for l in text.splitlines() if l.startswith("#")]
        checked += 1
        if label.startswith("例题"):
            if any(norm(label) in norm(h) for h in heads):
                continue
            missing.append((p["id"], label, "例题标题未找到"))
            continue
        if label.startswith("C-"):
            if any(norm(label) in norm(h) for h in heads):
                continue
            missing.append((p["id"], label, "附录标题未找到"))
            continue
        if label.startswith("习题"):
            m = re.match(r"习题\s*\d+\s*-\s*(\d+)", label)
            if not m:
                missing.append((p["id"], label, "题号格式无法解析"))
                continue
            if any(norm(label) in norm(h) for h in heads):
                continue
            # 找到「## 习题」后的有序列表，按第几项定位。
            lines = text.splitlines()
            ex_line = next((i for i, l in enumerate(lines) if re.match(r"^##\s*习题\s*$", l.strip())), None)
            if ex_line is None:
                missing.append((p["id"], label, "本章没有「## 习题」"))
                continue
            items = []
            for l in lines[ex_line + 1:]:
                if re.match(r"^##\s+", l):
                    break
                if re.match(r"^\d+\.\s+", l):
                    items.append(l)
            idx = int(m.group(1))
            if idx <= len(items):
                continue
            missing.append((p["id"], label, "习题列表只有 %d 项" % len(items)))
            continue
        missing.append((p["id"], label, "未知标签前缀"))

    print("已检查非原创题：%d 道" % checked)
    print("未定位：%d 道" % len(missing))
    for mid, label, why in missing[:40]:
        print("  %s %s -> %s" % (mid, label, why))
    return 0 if not missing else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
