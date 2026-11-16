#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给每道题做可解释的难度评估，并补齐提示。

四个维度：
  知识点（用到了什么算法/数据结构）
  思维（要不要转化、证明、构造）
  实现（参考答案的长度与结构）
  细节（数据规模、取模、边界）
总分 1～5，对应 入门 / 基础 / 提高 / 进阶 / 挑战。
"""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_JSON = os.path.join(BASE, "data", "problems.json")
SOL_DIR = os.path.join(BASE, "data", "solutions")

LABELS = {1: "入门", 2: "基础", 3: "提高", 4: "进阶", 5: "挑战"}

TAG_LEVEL = {
    "输入输出": 1, "循环": 1, "分支": 1, "计数": 1, "求和": 1,
    "枚举": 1, "模拟": 2, "日期": 2, "进制": 2, "坐标": 2,
    "排序": 2, "字符串": 2, "结构体": 2, "pair": 2, "vector": 2,
    "高精度": 2, "前缀和": 2, "前缀": 2, "双指针": 3, "滑动窗口": 3,
    "差分": 3, "二分": 3, "二分答案": 3, "贪心": 3, "递归": 3,
    "DFS": 3, "BFS": 3, "栈": 3, "队列": 3, "哈希": 3, "并查集": 3,
    "堆": 3, "背包": 3, "数论": 3, "质数": 3, "筛法": 3, "GCD": 3,
    "快速幂": 3, "逆元": 3, "分治": 3, "归并": 3, "逆序对": 3,
    "连通块": 3, "离散化": 3, "位运算": 3, "map": 3, "set": 3,
    "第 k 大": 3, "动态规划": 4, "DP": 4, "图": 4, "树": 4,
    "最短路": 4, "Dijkstra": 4, "Floyd": 4, "最小生成树": 4,
    "Kruskal": 4, "Prim": 4, "拓扑": 4, "拓扑排序": 4,
    "区间 DP": 4, "树形 DP": 4, "状压 DP": 4, "状压": 4,
    "LIS": 4, "LCS": 4, "TSP": 4, "字典树": 4, "KMP": 4,
    "ST 表": 4, "RMQ": 4, "LCA": 4, "tarjan": 4, "割点": 4,
    "二分图": 4, "倍增": 4, "差分约束": 4, "最短路计数": 4,
    "网格": 4, "直径": 4, "构造": 4, "博弈": 4, "概率": 4,
    "矩阵": 2, "组合": 4, "容斥": 4, "分块": 4, "扫描线": 5,
    "树状数组": 4, "线段树": 5, "单调栈": 5, "单调队列": 4,
    "网络流": 5, "最大流": 5, "费用流": 5, "2-SAT": 5,
    "LCT": 5, "后缀数组": 5, "莫队": 5, "可持久化": 5,
    "高斯": 5, "矩阵快速幂": 5, "欧拉": 4, "基环树": 4,
    "强连通": 4, "缩点": 4, "最近公共祖先": 4,
}

# 关键词 → 标签，用来给没有标签的例题补上知识点
KEYWORDS = [
    ("线段树", ["线段树"]), ("树状数组", ["树状数组"]), ("单调栈", ["单调栈"]),
    ("单调队列", ["单调队列"]), ("最短路计数", ["最短路计数", "最短路"]),
    ("Dijkstra", ["Dijkstra", "最短路"]), ("Floyd", ["Floyd", "最短路"]),
    ("Kruskal", ["Kruskal", "最小生成树"]), ("Prim", ["Prim", "最小生成树"]),
    ("最小生成树", ["最小生成树"]), ("拓扑排序", ["拓扑排序"]),
    ("并查集", ["并查集"]), ("01 背包", ["背包", "动态规划"]),
    ("完全背包", ["背包", "动态规划"]), ("多重背包", ["背包", "动态规划"]),
    ("最长上升子序列", ["LIS", "动态规划"]), ("LIS", ["LIS", "动态规划"]),
    ("最长公共子序列", ["LCS", "动态规划"]), ("LCS", ["LCS", "动态规划"]),
    ("编辑距离", ["动态规划"]), ("区间 DP", ["区间 DP"]), ("区间dp", ["区间 DP"]),
    ("树形 DP", ["树形 DP"]), ("状压", ["状压 DP"]), ("TSP", ["TSP"]),
    ("KMP", ["KMP"]), ("哈希", ["哈希"]), ("字典树", ["字典树"]),
    ("二分答案", ["二分答案", "二分"]), ("二分", ["二分"]),
    ("前缀和", ["前缀和"]), ("差分", ["差分"]), ("离散化", ["离散化"]),
    ("ST 表", ["ST 表"]), ("RMQ", ["RMQ"]), ("网络流", ["网络流"]),
    ("最大流", ["最大流"]), ("费用流", ["费用流"]), ("强连通", ["强连通"]),
    ("缩点", ["缩点"]), ("割点", ["割点"]),
    ("LCA", ["LCA"]), ("倍增", ["倍增"]), ("欧拉", ["欧拉"]),
    ("基环树", ["基环树"]), ("扫描线", ["扫描线"]), ("分块", ["分块"]),
    ("莫队", ["莫队"]), ("可持久化", ["可持久化"]), ("逆元", ["逆元"]),
    ("快速幂", ["快速幂"]), ("欧几里得", ["数论"]), ("质数", ["质数"]),
    ("筛法", ["筛法"]), ("组合数", ["组合"]), ("容斥", ["容斥"]),
    ("矩阵快速幂", ["矩阵快速幂"]), ("高斯消元", ["高斯"]), ("SG", ["博弈"]),
    ("构造题", ["构造"]), ("构造方案", ["构造"]), ("大模拟", ["模拟"]), ("高精度", ["高精度"]),
    ("双指针", ["双指针"]), ("滑动窗口", ["滑动窗口"]), ("位运算", ["位运算"]),
    ("贪心", ["贪心"]), ("分治", ["分治"]), ("归并", ["归并"]),
    ("逆序对", ["逆序对"]), ("优先队列", ["堆"]), ("堆", ["堆"]),
    ("栈", ["栈"]), ("队列", ["队列"]), ("BFS", ["BFS"]), ("DFS", ["DFS"]),
    ("回溯", ["回溯"]), ("递归", ["递归"]), ("枚举", ["枚举"]),
    ("模拟", ["模拟"]), ("排序", ["排序"]), ("字符串", ["字符串"]),
    ("日期", ["日期"]), ("进制", ["进制"]), ("最大公约数", ["GCD"]),
    ("gcd", ["GCD"]), ("图论", ["图"]), ("有向图", ["图"]),
    ("无向图", ["图"]), ("连通图", ["图"]), ("树的直径", ["直径"]),
    ("二叉树", ["树"]), ("子树", ["树"]), ("树链", ["树"]),
    ("求和", ["求和"]), ("总和", ["求和"]),
]

CODE_PATTERNS = [
    (r"segment|tree\[\w*4\w*\]|pushup|pushdown", ["线段树"]),
    (r"lowbit|bit\[", ["树状数组"]),
    (r"priority_queue", ["堆"]),
    (r"lower_bound|upper_bound", ["二分"]),
    (r"queue<", ["BFS"]),
    (r"stack<", ["栈"]),
    (r"dp\[", ["动态规划"]),
    (r"unordered_map|map<", ["哈希"]),
    (r"sort\(", ["排序"]),
    (r"gcd\(", ["GCD"]),
]


def infer_tags(p, code):
    tags = [t for t in p.get("tags", []) if t not in ("思考题", "基础", "提高", "挑战")]
    text = p.get("title", "") + "\n" + p.get("statement_md", "") + "\n" + p.get("input_md", "")
    for kw, ts in KEYWORDS:
        if kw.lower() in text.lower():
            for t in ts:
                if t not in tags:
                    tags.append(t)
    for pat, ts in CODE_PATTERNS:
        if re.search(pat, code, re.I):
            for t in ts:
                if t not in tags:
                    tags.append(t)
    if not tags:
        if p.get("kind") == "think":
            tags = ["阅读分析"]
        elif "输入" in p.get("statement_md", ""):
            tags = ["模拟"]
    return tags[:4]


def tag_level(tags):
    levels = [TAG_LEVEL.get(t, 2) for t in tags if t not in ("阅读分析",)]
    return max(levels) if levels else 2


def solution_code(pid):
    fn = os.path.join(SOL_DIR, pid + ".cpp")
    if not os.path.exists(fn):
        return ""
    try:
        with open(fn, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def code_lines(code):
    return len([ln for ln in code.split("\n") if ln.strip()])


def has_large_constraints(p):
    text = p.get("constraints_md", "") + p.get("input_md", "")
    if re.search(r"10\^7|10\^8|10\^9", text):
        return 4
    if re.search(r"10\^5|10\^6|2×10\^5|200000|100000", text):
        return 3
    return 2


def detail_level(p, code):
    text = (p.get("statement_md", "") + p.get("constraints_md", "") + p.get("input_md", "")).lower()
    lv = has_large_constraints(p)
    if any(w in text for w in ("取模", "mod", "10^9+7", "10^9 + 7")):
        lv = max(lv, 4)
    if any(w in text for w in ("边界", "负", "空", "前导零", "多组", "精度", "相等", "不能")):
        lv = max(lv, 3)
    if re.search(r"%\s*1000000007|%\s*1e9", code):
        lv = max(lv, 4)
    return min(5, lv)


def thinking_level(p, tags, k):
    text = p.get("statement_md", "") + p.get("output_md", "")
    t = k
    if any(w in text for w in ("证明", "构造反例", "为什么", "说明", "改错", "指出")):
        t = max(t, 3)
    if any(w in text for w in ("恰好", "至少", "字典序最小", "方案数", "计数", "输出路线")):
        t = max(t, 3)
    if p.get("kind") == "think":
        t = max(t, 3)
    if k >= 5:
        t = max(t, 4)
    return min(5, t)


def impl_level(lines, tags):
    if lines <= 0:
        return 1
    if lines <= 12:
        lv = 1
    elif lines <= 24:
        lv = 2
    elif lines <= 40:
        lv = 3
    elif lines <= 65:
        lv = 4
    else:
        lv = 5
    if any(t in tags for t in ("线段树", "树状数组", "网络流", "可持久化", "莫队", "LCT")):
        lv = max(lv, 4)
    return min(5, lv)


def thinking_note(t, tags):
    if any(x in tags for x in ("动态规划", "DP", "背包", "LIS", "LCS", "区间 DP", "树形 DP", "状压 DP")):
        return "关键是设计状态和转移方程，想清楚“阶段、状态、决策”"
    if any(x in tags for x in ("图", "BFS", "DFS", "最短路", "拓扑排序", "并查集", "连通块", "树")):
        return "关键是把生活场景抽象成图或网格，再确定搜索/合并的顺序"
    if any(x in tags for x in ("二分", "二分答案", "贪心", "双指针", "滑动窗口")):
        return "关键是找到单调性/贪心依据，并说明为什么这样选不会更差"
    if any(x in tags for x in ("线段树", "树状数组", "单调栈", "单调队列", "堆", "字典树", "哈希")):
        return "关键是选对数据结构，并把每次操作维护成 O(log n) 或 O(1)"
    if any(x in tags for x in ("数论", "质数", "GCD", "快速幂", "逆元", "组合", "容斥")):
        return "关键是把公式推对，注意取模与整数范围"
    if any(x in tags for x in ("字符串", "模拟", "排序", "枚举", "循环", "计数", "求和")):
        return "关键是把步骤按顺序理清，注意下标和边界"
    return "关键是先想清楚暴力怎么做，再决定要不要优化"


def note_for(k, t, i, d, tags, lines, p):
    tag_text = "、".join(tags[:3]) if tags else "基础语法"
    kin = {1: "只需按题意一步步处理", 2: "需要把题意翻译成一段稳定的流程",
           3: "要把问题转成一个熟悉的模型", 4: "需要自己发现模型并处理组合关系",
           5: "涉及较深的结构或转化，容易卡在正确性上"}[k]
    tin = thinking_note(t, tags)
    iin = {1: "代码很短", 2: "代码约二十行", 3: "代码中等", 4: "实现细节较多", 5: "实现量大"}[i]
    text = p.get("constraints_md") or p.get("input_md") or "数据规模见题面"
    text = re.sub(r"[`*]", "", text).replace("\n", "；")
    text = re.sub(r"[。；;、\s]+$", "", text)
    text = text[:70]
    din = {1: "边界很少", 2: "注意基本边界", 3: "要注意数据范围与相等情况",
           4: "大范围/取模等细节容易出错", 5: "边界与常数都需要小心"}[d]
    return ("主要考 %s。%s；%s。%s，参考答案约 %d 行非空代码。数据范围：%s，%s。"
            % (tag_text, kin, tin, iin, lines, text, din))


def make_hints(p, tags):
    existing = p.get("hints") or []
    if existing:
        return existing[:3]
    hm = (p.get("hint_md") or "").strip()
    if hm:
        parts = [x.strip(" -") for x in re.split(r"\n+|；", hm) if x.strip()]
        if len(parts) >= 2:
            return parts[:3]
        return [hm]
    tag_text = "、".join(tags[:3]) if tags else "基础语法"
    c = (p.get("constraints_md") or "").replace("\n", " ")
    c = re.sub(r"[`*]", "", c).strip().rstrip("。；; ")
    c = c[:80]
    return [
        "先看数据范围：%s。估计一下暴力做法的时间复杂度，能不能在规定时限内跑完。" % (c or "见题面"),
        "这道题的关键知识点是 %s。把要做的事情拆成「读入 → 维护什么状态 → 每步怎么更新 → 输出」。" % tag_text,
        "写完先拿样例手算一遍，再自己造一组最小数据和一组边界数据（空、1 个元素、相等、负数）测试。",
    ]


def enrich(problems):
    for p in problems:
        code = solution_code(p["id"])
        lines = code_lines(code)
        tags = infer_tags(p, code)
        p["tags"] = tags
        k = tag_level(tags)
        t = thinking_level(p, tags, k)
        i = impl_level(lines, tags)
        d = detail_level(p, code)
        # 以知识点为主轴，思维/实现只做一级修正，避免“数据范围大”把简单题抬成中高难度
        score = k
        if k <= 3 and (i >= 4 or t >= 4):
            score += 1
        if k == 1 and (i >= 3 or d >= 4):
            score = 2
        if k == 2 and i <= 2 and t <= 2 and d <= 3:
            score = 1
        score = max(1, min(5, int(score)))
        p["difficulty"] = score
        p["difficulty_label"] = LABELS[score]
        p["difficulty_note"] = note_for(k, t, i, d, tags, lines, p)
        p["difficulty_factors"] = [
            {"name": "知识点", "level": k, "note": "、".join(tags[:3]) if tags else "基础语法"},
            {"name": "思维", "level": t, "note": thinking_note(t, tags)},
            {"name": "实现", "level": i, "note": "约 %d 行非空代码" % lines if lines else "无参考代码"},
            {"name": "细节", "level": d, "note": ["边界很少", "注意基本边界", "注意范围与相等", "大范围/取模细节", "边界与常数都要小心"][d - 1]},
        ]
        p["hints"] = make_hints(p, tags)
        p["hint_md"] = "\n".join(p["hints"])
    return problems


def main():
    with open(PROBLEMS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    enrich(data["problems"])
    data["meta"]["difficulty_counts"] = {
        str(i): sum(1 for p in data["problems"] if p["difficulty"] == i) for i in range(1, 6)
    }
    with open(PROBLEMS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("已评估 %d 道题" % len(data["problems"]))
    print("难度分布：", data["meta"]["difficulty_counts"])


if __name__ == "__main__":
    main()
