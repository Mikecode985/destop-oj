#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查每一节原书是否都能生成导学卡的知识块（离线校验）。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "web" / "book"
SKIP = {"本章小结", "小结", "习题"}


def plain(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_~]", "", text)
    return text.strip()


def main() -> int:
    manifest = json.loads((BOOK / "manifest.json").read_text(encoding="utf-8"))
    rows = []
    failed = []
    for section in manifest.get("sections", []):
        path = BOOK / section["file"]
        if not path.exists():
            failed.append((section["id"], "章节文件不存在"))
            continue
        text = plain(path.read_text(encoding="utf-8"))
        blocks = []
        for line in text.splitlines():
            m = re.match(r"^##\s+(.*)$", line.strip())
            if not m:
                continue
            title = m.group(1).strip()
            if title in SKIP:
                continue
            blocks.append(title)
        if not blocks:
            failed.append((section["id"], "没有可用的 ## 知识块"))
        rows.append((section["id"], len(blocks)))

    for sid, n in rows:
        print(f"{sid:12s} {n} 个知识块")
    print(f"已检查 {len(rows)} 节；最少 {min((n for _, n in rows), default=0)} 个知识块")
    if failed:
        for sid, reason in failed:
            print(f"  [失败] {sid}：{reason}")
        print(f"结果：失败 {len(failed)} 节")
        return 1
    print("结果：全部通过，0 节缺少导学知识块")
    return 0


if __name__ == "__main__":
    sys.exit(main())
