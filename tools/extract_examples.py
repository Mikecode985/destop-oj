#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 chapters/chNN.md 抽取全部例题：题面、样例、书中测试用例、参考代码。

输出：
  data/examples.json           例题结构化数据
  data/solutions/<id>.cpp      参考代码（书中完整程序）
并可选地对全部例题做一次编译 + 跑用例校验（--verify）。
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OJ = os.path.join(ROOT, "oj")
CH_DIR = os.path.join(ROOT, "chapters")
DATA = os.path.join(OJ, "data")
SOL = os.path.join(DATA, "solutions")

CHAPTER_RE = re.compile(r"^# 第 (\d+) 章\s*(.*)$", re.M)
EX_RE = re.compile(r"^### 例题 (\d+)-(\d+)\s*(.*)$", re.M)
CPP_RE = re.compile(r"^```cpp:([^\s`]+)\n(.*?)^```$", re.M | re.S)
TEST_RE = re.compile(r"<<<TEST\n(.*?)TEST>>>", re.S)
SAMPLE_RE = re.compile(
    r"\*\*样例[^*]*\*\*\s*\n+\s*输入[：:]\s*\n+```\s*\n(.*?)^```\s*\n+\s*输出[：:]\s*\n+```\s*\n(.*?)^```",
    re.M | re.S,
)


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_tests(block):
    """把 <<<TEST ... TEST>>> 里的 IN/OUT 段落切成 (input, output) 列表。"""
    cases = []
    cur = None
    buf = []
    mode = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if line == "IN":
            if cur is not None:
                cur["out"] = "\n".join(buf)
                cases.append(cur)
            cur = {"in": ""}
            buf = []
            mode = "in"
            continue
        if line == "OUT":
            if cur is None:
                cur = {"in": ""}
            cur["in"] = "\n".join(buf)
            buf = []
            mode = "out"
            continue
        if mode:
            buf.append(line)
    if cur is not None:
        cur["out"] = "\n".join(buf)
        cases.append(cur)
    out = []
    for c in cases:
        out.append((c["in"].strip("\n"), c["out"].strip("\n")))
    return out


def clean_statement(text):
    """去掉代码块、样例块、思路/代码/易错点小节，保留题目说明部分。"""
    # 截断到 思路/代码/易错点/为什么 等分析小节之前
    cut = len(text)
    for marker in ("**思路**", "**代码**", "**易错点**", "**为什么", "**复杂度**", "**验证**", "**实现**", "**数据范围**"):
        pos = text.find(marker)
        if pos != -1:
            cut = min(cut, pos)
    text = text[:cut]
    text = SAMPLE_RE.sub("", text)
    text = re.sub(r"^```.*?^```\s*$", "", text, flags=re.M | re.S)
    text = re.sub(r"<<<TEST.*?TEST>>>", "", text, flags=re.S)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def field(text, name):
    m = re.search(r"\*\*%s\*\*[：:]\s*(.+?)(?=\n\s*\n|\n\*\*)" % name, text, re.S)
    return m.group(1).strip() if m else ""


def main():
    os.makedirs(SOL, exist_ok=True)
    problems = []
    for fn in sorted(os.listdir(CH_DIR)):
        if not re.match(r"ch\d+\.md$", fn):
            continue
        content = read(os.path.join(CH_DIR, fn))
        chm = CHAPTER_RE.search(content)
        if not chm:
            continue
        ch_no = int(chm.group(1))
        ch_title = chm.group(2).strip()
        matches = list(EX_RE.finditer(content))
        for idx, m in enumerate(matches):
            start = m.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
            # 例题块到下一个小节标题为止，避免把后面的正文吞进来
            nxt = re.search(r"^## ", content[start:end], re.M)
            block = content[start:end]
            if nxt:
                block = block[: nxt.start()]
            pid = "ex-%02d-%02d" % (ch_no, int(m.group(2)))
            title = m.group(3).strip()
            code_blocks = CPP_RE.findall(block)
            tests = []
            for tb in TEST_RE.findall(block):
                tests.extend(split_tests(tb))
            samples = SAMPLE_RE.findall(block)
            body = clean_statement(block)
            statement = field(block, "题目") or re.sub(r"^\*\*(题目|题意)\*\*[：:]\s*", "", body)
            statement = re.sub(r"^\*\*(题目|题意)\*\*[：:]\s*", "", statement).strip()
            constraints = field(block, "数据范围")
            if not samples and tests:
                samples = [(tests[0][0], tests[0][1])]
            problems.append({
                "id": pid,
                "kind": "example",
                "chapter": ch_no,
                "chapter_title": ch_title,
                "label": "例题 %d-%d" % (ch_no, int(m.group(2))),
                "title": title,
                "difficulty": 2,
                "statement_md": statement,
                "input_md": field(block, "输入格式"),
                "output_md": field(block, "输出格式"),
                "constraints_md": constraints,
                "samples": [{"in": i.strip("\n"), "out": o.strip("\n")} for i, o in samples],
                "tests": [{"in": i, "out": o} for i, o in tests],
                "code_files": [{"name": n, "code": c} for n, c in code_blocks],
                "source": "《从语法到算法：C++ 算法设计与 ACM 竞赛入门》%s" % ("例题 %d-%d" % (ch_no, int(m.group(2)))),
            })

    # 保存参考代码（每道例题取第一个完整程序；多程序的另存）
    for p in problems:
        p["solution"] = None
        if p["code_files"]:
            main_code = p["code_files"][0]
            fname = p["id"] + ".cpp"
            with open(os.path.join(SOL, fname), "w", encoding="utf-8", newline="\n") as f:
                f.write(main_code["code"].rstrip() + "\n")
            p["solution"] = "solutions/" + fname
            p["solution_name"] = main_code["name"]
            for extra in p["code_files"][1:]:
                base = os.path.splitext(extra["name"])[0]
                extra_name = "%s.%s.cpp" % (p["id"], re.sub(r"\W+", "_", base))
                with open(os.path.join(SOL, extra_name), "w", encoding="utf-8", newline="\n") as f:
                    f.write(extra["code"].rstrip() + "\n")

    out = os.path.join(DATA, "examples.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=1)

    print("例题总数:", len(problems))
    no_test = [p["id"] for p in problems if not p["tests"]]
    no_code = [p["id"] for p in problems if not p["solution"]]
    no_sample = [p["id"] for p in problems if not p["samples"]]
    print("无用例:", no_test)
    print("无完整程序:", no_code)
    print("无样例:", no_sample)

    if "--verify" in sys.argv:
        verify(problems)


def norm(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def verify(problems):
    tmp = tempfile.mkdtemp(prefix="ojverify_")
    ok = fail = skip = 0
    report = []
    for p in problems:
        if not p["solution"] or not p["tests"]:
            skip += 1
            continue
        src = os.path.join(DATA, p["solution"])
        exe = os.path.join(tmp, p["id"] + ".exe")
        cp = subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-o", exe, src],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if cp.returncode != 0:
            fail += 1
            report.append((p["id"], "CE", cp.stderr[-400:]))
            continue
        bad = None
        for n, t in enumerate(p["tests"], 1):
            try:
                rn = subprocess.run([exe], input=t["in"] + ("\n" if t["in"] else ""),
                                    capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", timeout=3, cwd=tmp)
            except subprocess.TimeoutExpired:
                bad = ("TLE", "case %d" % n)
                break
            if rn.returncode != 0:
                bad = ("RE", "case %d rc=%d %s" % (n, rn.returncode, rn.stderr[-300:]))
                break
            if norm(rn.stdout) != norm(t["out"]):
                bad = ("WA", "case %d\nEXPECTED:\n%s\nGOT:\n%s" % (n, t["out"][:300], rn.stdout[:300]))
                break
        if bad:
            fail += 1
            report.append((p["id"], bad[0], bad[1]))
        else:
            ok += 1
            if cp.stderr.strip():
                report.append((p["id"], "WARN", cp.stderr[-300:]))
    print("校验：AC=%d FAIL=%d SKIP=%d" % (ok, fail, skip))
    for item in report:
        print("-", item[0], item[1])
        print(item[2])


if __name__ == "__main__":
    main()
