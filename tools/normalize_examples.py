# -*- coding: utf-8 -*-
"""把例题（ex-*.cpp）的参考答案头文件统一为 #include <bits/stdc++.h> 并逐题复核 AC。

用法：
    python tools\\normalize_examples.py            # 归一化 + 判题复核
    python tools\\normalize_examples.py --check    # 只判题复核，不改文件
"""
import glob
import io
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import server  # noqa: E402

SOL_DIR = os.path.join(BASE, "data", "solutions")
HEADER = "#include <bits/stdc++.h>"


def normalize(code):
    lines = code.replace("\r\n", "\n").split("\n")
    body = [l for l in lines if not l.strip().startswith("#include")]
    text = HEADER + "\n" + "\n".join(body).lstrip("\n")
    return text.rstrip() + "\n"


def main():
    check_only = "--check" in sys.argv
    problems = {}
    with io.open(server.PROBLEMS_JSON, encoding="utf-8") as f:
        for p in json.load(f)["problems"]:
            problems[p["id"]] = p

    files = sorted(glob.glob(os.path.join(SOL_DIR, "ex-*.cpp")))
    if not files:
        print("没有找到例题参考答案")
        return 1

    if not check_only:
        for fn in files:
            with io.open(fn, encoding="utf-8") as f:
                code = f.read()
            with open(fn, "w", encoding="utf-8", newline="\n") as f:
                f.write(normalize(code))
        print("已统一 %d 份例题参考答案的头文件" % len(files))

    fails = []
    for fn in files:
        pid = os.path.basename(fn)[:-4]
        p = problems.get(pid)
        if not p:
            print("[跳过] %s 不在题库里" % pid)
            continue
        with io.open(fn, encoding="utf-8") as f:
            code = f.read()
        r = server.judge(p, code)
        ok = r["verdict"] == "AC"
        print("[%s] %s %s" % ("通过" if ok else "失败", pid, r["verdict"]))
        if not ok:
            fails.append((pid, r))
    print("\n共 %d 题，通过 %d，失败 %d" % (len(files), len(files) - len(fails), len(fails)))
    for pid, r in fails:
        print("\n--- %s" % pid)
        for c in r["cases"]:
            if c["status"] != "AC":
                print("用例 %s %s" % (c["index"], c["status"]))
                print("期望：%r" % (c.get("expected", "")[:300],))
                print("实际：%r" % (c.get("actual", "")[:300],))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
