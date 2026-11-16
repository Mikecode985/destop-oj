#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把《从语法到算法》原书电子版打包进本地 OJ。

源目录：项目根/chapters、appendix、assets、preface.md、build/full5.pdf
输出：oj/web/book/（章节 Markdown、插图、PDF、manifest.json）

用法：python tools/build_book.py
"""
import json
import os
import re
import shutil

OJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(OJ)
OUT = os.path.join(OJ, "web", "book")
OUT_CHAPTERS = os.path.join(OUT, "chapters")
OUT_ASSETS = os.path.join(OUT, "assets")


def read_title(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return os.path.basename(path)


def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def main():
    os.makedirs(OUT_CHAPTERS, exist_ok=True)
    os.makedirs(OUT_ASSETS, exist_ok=True)

    sections = []

    preface = os.path.join(ROOT, "preface.md")
    if os.path.isfile(preface):
        copy_file(preface, os.path.join(OUT_CHAPTERS, "preface.md"))
        sections.append({
            "id": "preface", "kind": "preface", "num": 0,
            "title": "前言", "file": "chapters/preface.md",
        })

    for n in range(1, 33):
        name = "ch%02d.md" % n
        src = os.path.join(ROOT, "chapters", name)
        if not os.path.isfile(src):
            continue
        copy_file(src, os.path.join(OUT_CHAPTERS, name))
        title = read_title(src)
        short = re.sub(r"^第\s*\d+\s*章\s*", "", title).strip()
        sections.append({
            "id": "ch%02d" % n, "kind": "chapter", "num": n,
            "title": title, "short": short, "file": "chapters/" + name,
        })

    for letter in "ABCDEF":
        src = os.path.join(ROOT, "appendix", letter + ".md")
        if not os.path.isfile(src):
            continue
        name = "appendix-" + letter + ".md"
        copy_file(src, os.path.join(OUT_CHAPTERS, name))
        title = read_title(src)
        short = re.sub(r"^附录\s*" + letter + r"\s*", "", title).strip()
        sections.append({
            "id": "appendix-" + letter, "kind": "appendix", "letter": letter,
            "title": title, "short": short, "file": "chapters/" + name,
        })

    assets_src = os.path.join(ROOT, "assets")
    copied_assets = 0
    if os.path.isdir(assets_src):
        for name in os.listdir(assets_src):
            src = os.path.join(assets_src, name)
            if os.path.isfile(src):
                copy_file(src, os.path.join(OUT_ASSETS, name))
                copied_assets += 1

    pdf_src = os.path.join(ROOT, "build", "full5.pdf")
    if os.path.isfile(pdf_src):
        copy_file(pdf_src, os.path.join(OUT, "original.pdf"))

    manifest = {
        "title": "从语法到算法：C++ 算法设计与 ACM 竞赛入门",
        "subtitle": "原书电子版 · 阅读与题目联动",
        "sections": sections,
        "has_pdf": os.path.isfile(os.path.join(OUT, "original.pdf")),
    }
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("章节/附录：%d 节" % len(sections))
    print("插图：%d 张" % copied_assets)
    print("PDF：%s" % ("已导入" if manifest["has_pdf"] else "未找到"))
    print("输出：%s" % OUT)


if __name__ == "__main__":
    main()
