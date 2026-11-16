#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""原书阅读功能专项验收：不重置做题进度，可随时重复运行。

前置：server.py 已在 127.0.0.1:8765 运行。
运行：python tools\\acceptance_book.py
"""
import json
import os
import sys
import urllib.request

BASE = "http://127.0.0.1:8765"
OJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

passed = 0
failed = 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print("  [通过] %s %s" % (name, detail))
    else:
        failed += 1
        print("  [失败] %s %s" % (name, detail))


def fetch(path, headers=None):
    req = urllib.request.Request(BASE + path, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.headers, r.read()


def main():
    print("== 原书阅读专项验收 ==")
    print("== 1. 目录与章节 ==")
    st, hd, body = fetch("/book/manifest.json")
    manifest = json.loads(body.decode("utf-8"))
    sections = manifest.get("sections", [])
    check("manifest 可访问", st == 200 and isinstance(sections, list), "%d 节" % len(sections))
    check("目录为 39 节", len(sections) == 39, "实际 %d" % len(sections))
    check("目录包含 PDF 标记", manifest.get("has_pdf") is True)
    ids = [s.get("id") for s in sections]
    check("章节 id 完整", ids.count("preface") == 1 and all(("ch%02d" % i) in ids for i in range(1, 33))
          and all(("appendix-" + c) in ids for c in "ABCDEF"))

    st, hd, body = fetch("/book/chapters/ch01.md")
    text = body.decode("utf-8")
    check("第 1 章可读", st == 200 and "例题 1-1" in text and "求和会不会溢出" in text,
          "%d 字节" % len(text))
    st, hd, body = fetch("/book/chapters/appendix-C.md")
    textc = body.decode("utf-8")
    check("附录 C 可读", st == 200 and "C-01" in textc and "贵阳地铁一号线" in textc,
          "%d 字节" % len(textc))

    print("== 2. 插图与 PDF ==")
    st, hd, body = fetch("/book/assets/fig-01-roadmap.png")
    check("插图可读", st == 200 and len(body) > 10000 and hd.get("Content-Type") == "image/png",
          "%d 字节" % len(body))
    st, hd, body = fetch("/book/original.pdf", {"Range": "bytes=0-99"})
    check("PDF Range 分片", st == 206 and len(body) == 100
          and hd.get("Content-Range", "").endswith("/7328925"),
          "%s %s" % (hd.get("Content-Range"), hd.get("Content-Type")))

    print("== 3. 前端入口 ==")
    st, hd, body = fetch("/")
    html = body.decode("utf-8")
    check("做题/原书切换", 'id="viewSwitch"' in html and 'data-view="book"' in html)
    check("原书工作区与目录", 'id="bookWorkspace"' in html and 'id="bookToc"' in html
          and 'id="bookContent"' in html)
    check("每章导学卡入口", 'id="bookGuide"' in html and 'class="book-guide"' in html)
    check("划词工具条", 'id="bookSelBar"' in html and 'data-book-ask="explain"' in html
          and 'id="bookAskRelate"' in html)
    check("原书侧栏入口", 'id="bookCurrentOpen"' in html and 'id="bookPdf"' in html)

    print("== 4. 前端实现 ==")
    st, hd, body = fetch("/static/app.js")
    js = body.decode("utf-8")
    check("原书渲染器", "function bookMdToHtml" in js and "bookAssetUrl" in js)
    check("题面联动入口", 'id="btnBookLink"' in js and "openBookForCurrent" in js)
    check("每章思维导图", "function bookGuideModel" in js and "function bookGuideHtml" in js
          and "function drawBookMindmap" in js)
    check("题目映射", "function bookSectionForProblem" in js and "appendix-" in js)
    check("选段问 AI", "aiBookQuote" in js and "function askBookSelection" in js)
    st, hd, body = fetch("/static/style.css")
    css = body.decode("utf-8")
    check("原书阅读样式", ".book-paper" in css and ".book-code" in css and ".book-selbar" in css)
    check("导学卡样式", ".book-guide" in css and ".book-mindmap" in css and ".mm-lines" in css)

    print("\n结果：通过 %d，失败 %d" % (passed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
