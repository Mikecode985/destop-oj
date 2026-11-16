# -*- coding: utf-8 -*-
"""把 tools/cpp/*.py 里的 C++ 参考答案写入 data/solutions/ 并逐题判题校验。

用法：
    python tools\\build_solutions.py            # 全部
    python tools\\build_solutions.py ch05_06    # 只处理文件名含该字串的模块
    python tools\\build_solutions.py --write-only  # 只写文件，不判题
"""
import glob
import importlib.util
import io
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import server  # noqa: E402

CPP_DIR = os.path.join(BASE, "tools", "cpp")
SOL_DIR = os.path.join(BASE, "data", "solutions")
HEADER = "#include <bits/stdc++.h>"


def load_modules(kw):
    out = {}
    for fn in sorted(glob.glob(os.path.join(CPP_DIR, "*.py"))):
        if kw and kw not in os.path.basename(fn):
            continue
        name = "cpp_" + os.path.basename(fn)[:-3]
        spec = importlib.util.spec_from_file_location(name, fn)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in getattr(mod, "SOL", {}).items():
            if k in out:
                print("重复定义：%s（%s 覆盖前一条）" % (k, os.path.basename(fn)))
            out[k] = v
    return out


def normalize(code):
    """统一头文件：去掉开头若干 #include 行，只保留一行 bits/stdc++.h。"""
    lines = code.replace("\r\n", "\n").split("\n")
    has_bits = any(l.strip() == HEADER for l in lines[:12])
    body = [l for l in lines if not l.strip().startswith("#include")]
    if has_bits:
        # 已经带 bits，去掉重复的标准头
        pass
    text = HEADER + "\n" + "\n".join(body).lstrip("\n")
    return text.rstrip() + "\n"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    kw = args[0] if args else ""
    write_only = "--write-only" in sys.argv
    sols = load_modules(kw)
    if not sols:
        print("没有找到任何 C++ 参考答案（关键词：%s）" % (kw or "全部"))
        return 1

    problems = {}
    with io.open(server.PROBLEMS_JSON, encoding="utf-8") as f:
        for p in json.load(f)["problems"]:
            problems[p["id"]] = p

    os.makedirs(SOL_DIR, exist_ok=True)
    missing = sorted(set(sols) - set(problems))
    if missing:
        print("警告：以下 ID 不在题库里：%s" % ", ".join(missing))

    for pid, code in sols.items():
        with open(os.path.join(SOL_DIR, pid + ".cpp"), "w", encoding="utf-8", newline="\n") as f:
            f.write(normalize(code))
    print("已写入 %d 份参考答案" % len(sols))
    if write_only:
        return 0

    fails = []
    for i, (pid, code) in enumerate(sorted(sols.items()), 1):
        p = problems.get(pid)
        if not p:
            continue
        if not p.get("tests"):
            print("[跳过] %s 没有测试数据" % pid)
            continue
        r = server.judge(p, normalize(code))
        ok = r["verdict"] == "AC"
        print("[%s] %s %s %s" % ("通过" if ok else "失败", pid,
                                 r["verdict"], "" if ok else
                                 "失败用例 " + str([c["index"] for c in r["cases"] if c["status"] != "AC"])))
        if not ok:
            fails.append((pid, r))
    print("\n共 %d 题，通过 %d，失败 %d" % (len(sols), len(sols) - len(fails), len(fails)))
    for pid, r in fails:
        print("\n--- %s" % pid)
        for c in r["cases"]:
            if c["status"] != "AC":
                print("用例 %s %s" % (c["index"], c["status"]))
                print("期望：%r" % (c.get("expected", "")[:200],))
                print("实际：%r" % (c.get("actual", "")[:200],))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
