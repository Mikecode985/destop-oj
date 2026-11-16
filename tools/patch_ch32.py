#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把第 32 章三道例题改写成标准题面（保持原有测试数据与参考程序）。"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

PATCH = {
    "ex-32-01": {
        "title": "最大子段和（三次提交）",
        "difficulty": 2,
        "statement_md": (
            "给 n 个整数（可能全是负数），求**连续子段和的最大值**（子段不能为空）。\n\n"
            "本题对应书上例题 32-1 的「三次提交」：第一次把答案初始值设成 0，全负数时输出 0（WA）；"
            "第二次用 `int` 存 dp，中间结果溢出（WA）；第三次把初始值改成 `a[1]`、用 `long long`（AC）。"
            "提交时不妨先故意用前两版试试，看看 OJ 会给出什么结果。"
        ),
        "input_md": "第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 a[i]（|a[i]| ≤ 10^9）。",
        "output_md": "一行一个整数，表示最大子段和。",
        "constraints_md": "1 ≤ n ≤ 10^5，|a[i]| ≤ 10^9。答案可达 10^14 量级，**必须用 `long long`**。",
        "tags": ["DP", "最大子段和"],
    },
    "ex-32-02": {
        "title": "多组数据：读到文件结尾",
        "difficulty": 1,
        "statement_md": (
            "题面里关于输入常见三种说法：单组、第一行一个 T、多组数据读到文件结尾（EOF）。"
            "本题是第三种：不告诉你几组，一直读到读不出来为止。\n\n"
            "每组数据：第一行一个整数 n，第二行 n 个整数，输出这 n 个数的和。"
            "`while (cin >> n)` 就是「读到 EOF 就停」的写法；每组内部的累加器必须在循环里重新清零。"
        ),
        "input_md": "多组数据，读到文件结尾（EOF）。每组第一行一个整数 n（0 ≤ n ≤ 10^5），第二行 n 个整数（|a[i]| ≤ 10^9）。",
        "output_md": "每组输出一行，表示该组数据的总和。",
        "constraints_md": "总数据量不超过 10^6 个整数；n 可能为 0（此时该组输出 0）。",
        "tags": ["模拟", "多组数据"],
    },
    "ex-32-03": {
        "title": "最大子段和（暴力对拍版）",
        "difficulty": 1,
        "statement_md": (
            "本题就是例题 32-1 的暴力版本：两层循环枚举所有区间，O(n²)，n 很小的时候完全够用。\n\n"
            "它的用途是**对拍**：写一个随机数据生成器，让这个「慢但绝对正确」的程序和你那个「快但心里没底」的程序"
            "跑同样的输入，比较输出；连续几百组都一样，你的快程序大概率是对的。"
            "书上附录 A.8 给了一份现成的 Windows 批处理对拍脚本。"
        ),
        "input_md": "第一行一个整数 n（1 ≤ n ≤ 1000）。\n第二行 n 个整数 a[i]（|a[i]| ≤ 10^9）。",
        "output_md": "一行一个整数，表示最大子段和。",
        "constraints_md": "1 ≤ n ≤ 1000，|a[i]| ≤ 10^9；O(n²) 可以通过。",
        "tags": ["对拍", "暴力"],
    },
}


def main():
    path = os.path.join(DATA, "examples.json")
    with open(path, encoding="utf-8") as f:
        problems = json.load(f)
    n = 0
    for p in problems:
        if p["id"] in PATCH:
            p.update(PATCH[p["id"]])
            p["samples"] = p["tests"][:1]
            n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=1)
    print("已改写例题 %d 道（32-1 / 32-2 / 32-3）" % n)


if __name__ == "__main__":
    main()
