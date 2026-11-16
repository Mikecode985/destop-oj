#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 tools/gen/*.py 里的题目定义编译成 data/extra/*.json：
逐个跑参考解生成期望输出，检查空输出/超时，并写出样例。
"""
import importlib.util
import json
import os
import random
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(BASE, "tools", "gen")
OUT = os.path.join(BASE, "data", "extra")


def load_mod(path):
    name = "gen_" + os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(s):
    s = str(s).replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(ln.rstrip() for ln in s.split("\n")).strip("\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(f for f in os.listdir(GEN) if f.endswith(".py") and f != "common.py")
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    total = 0
    problems_all = []
    errors = []
    for fn in files:
        if only and not any(o in fn for o in only):
            continue
        mod = load_mod(os.path.join(GEN, fn))
        probs = []
        for p in mod.PROBLEMS:
            pid = p["id"]
            cases = p["cases"]
            outs = []
            slowest = 0
            for i, c in enumerate(cases):
                t0 = time.perf_counter()
                try:
                    o = p["solve"](c)
                except Exception as e:
                    errors.append("%s 用例 %d 参考解异常：%r" % (pid, i + 1, e))
                    o = ""
                dt = time.perf_counter() - t0
                slowest = max(slowest, dt)
                o = norm(o)
                if not o:
                    errors.append("%s 用例 %d 输出为空（输入 %r）" % (pid, i + 1, c[:80]))
                outs.append(o)
            if slowest > 2.0:
                errors.append("%s 参考解最慢用例 %.1f 秒，生成偏慢" % (pid, slowest))

            if p.get("brute") and p.get("random_case"):
                for _ in range(40):
                    c = p["random_case"]()
                    a = norm(p["solve"](c))
                    b = norm(p["brute"](c))
                    if a != b:
                        errors.append("%s 对拍不一致：输入 %r 解 %r 暴力 %r" % (pid, c, a, b))
                        break

            sn = min(p.get("sample_n", 2), len(cases))
            cases_n = [norm(c) for c in cases]
            probs.append({
                "id": pid, "kind": p.get("kind", "exercise"),
                "chapter": p.get("chapter", 0), "chapter_title": p.get("chapter_title", ""),
                "label": p.get("label", pid), "title": p["title"],
                "difficulty": p.get("difficulty", 2),
                "time_limit": p.get("time_limit", 2.0),
                "statement_md": p["statement_md"], "input_md": p["input_md"],
                "output_md": p["output_md"], "constraints_md": p.get("constraints_md", ""),
                "hint_md": p.get("hint_md", ""), "note_md": p.get("note_md", ""),
                "hints": p.get("hints", []),
                "difficulty_label": p.get("difficulty_label", ""),
                "difficulty_note": p.get("difficulty_note", ""),
                "difficulty_factors": p.get("difficulty_factors", []),
                "tags": p.get("tags", []),
                "source": p.get("source", "《从语法到算法：C++ 算法设计与 ACM 竞赛入门》"),
                "samples": [{"in": cases_n[i], "out": outs[i]} for i in range(sn)],
                "tests": [{"in": cases_n[i], "out": outs[i]} for i in range(len(cases))],
            })
        out_path = os.path.join(OUT, os.path.splitext(fn)[0] + ".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(probs, f, ensure_ascii=False, indent=1)
        total += len(probs)
        problems_all.extend(probs)
        print("%-18s %3d 题" % (fn, len(probs)))

    print("\n合计 %d 题" % total)
    if errors:
        print("发现问题 %d 条：" % len(errors))
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("校验：参考解全部跑通，无空输出。")


if __name__ == "__main__":
    main()
