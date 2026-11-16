#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地 OJ 服务：调用本机 g++ 编译、逐用例评测，自带 Web 界面。

启动：python server.py            （默认 http://127.0.0.1:8765）
      python server.py --open     （启动后自动打开浏览器）
      python server.py --port 9000
"""
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
WEB_DIR = os.path.join(BASE, "web")
PROBLEMS_JSON = os.path.join(DATA_DIR, "problems.json")
PROGRESS_JSON = os.path.join(DATA_DIR, "progress.json")
SUBMISSIONS_JSON = os.path.join(DATA_DIR, "submissions.json")
SOL_DIR = os.path.join(DATA_DIR, "solutions")
MAX_SUBMISSIONS = 800

GPP_CANDIDATES = [
    "g++.exe", "g++",
    r"C:\Program Files (x86)\Embarcadero\Dev-Cpp\TDM-GCC-64\bin\g++.exe",
    r"C:\Program Files\Embarcadero\Dev-Cpp\TDM-GCC-64\bin\g++.exe",
    r"C:\TDM-GCC-64\bin\g++.exe",
    r"C:\mingw64\bin\g++.exe",
    r"C:\Program Files\mingw-w64\mingw64\bin\g++.exe",
]

LOCK = threading.Lock()
STATE = {"problems": None, "by_id": None}


def find_gpp():
    for c in GPP_CANDIDATES:
        p = shutil.which(c) if not c.endswith(".exe") or os.path.isabs(c) else c
        if p and os.path.exists(p):
            return p
    return None


def load_problems():
    with open(PROBLEMS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    problems = data["problems"] if isinstance(data, dict) else data
    STATE["problems"] = problems
    STATE["by_id"] = {p["id"]: p for p in problems}
    return problems


def load_progress():
    if os.path.exists(PROGRESS_JSON):
        try:
            with open(PROGRESS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_progress(p):
    tmp = PROGRESS_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PROGRESS_JSON)


def load_submissions():
    if os.path.exists(SUBMISSIONS_JSON):
        try:
            with open(SUBMISSIONS_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []


def save_submissions(items):
    tmp = SUBMISSIONS_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items[:MAX_SUBMISSIONS], f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, SUBMISSIONS_JSON)


def save_problem_bank(meta, problems):
    tmp = PROBLEMS_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "problems": problems}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PROBLEMS_JSON)


def _as_text(value, limit=20000):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value or "").strip()[:limit]


def _as_tests(raw, limit=10):
    if not isinstance(raw, list):
        return []
    out = []
    for t in raw[:limit]:
        if not isinstance(t, dict):
            continue
        ti = _as_text(t.get("in"), 20000)
        to = _as_text(t.get("out"), 20000)
        if ti or to:
            out.append({"in": ti, "out": to})
    return out


def normalize_generated_problem(payload):
    """把 AI 返回的松散 JSON 收紧成题库 schema；返回 (problem, error)。"""
    if not isinstance(payload, dict):
        return None, "生成结果不是 JSON 对象"
    p = payload.get("problem") if isinstance(payload.get("problem"), dict) else payload
    title = _as_text(p.get("title"), 80)
    statement = _as_text(p.get("statement_md") or p.get("statement") or p.get("description"))
    input_md = _as_text(p.get("input_md") or p.get("input") or p.get("input_format"))
    output_md = _as_text(p.get("output_md") or p.get("output") or p.get("output_format"))
    constraints = _as_text(p.get("constraints_md") or p.get("constraints") or p.get("constraint"))
    if not title:
        return None, "题目缺少 title"
    if len(statement) < 10:
        return None, "题面过短，缺少完整描述"
    if not input_md:
        return None, "题目缺少 input_md"
    if not output_md:
        return None, "题目缺少 output_md"
    if not constraints:
        return None, "题目缺少 constraints_md"

    samples = _as_tests(p.get("samples") or p.get("sample"), 4)
    tests = _as_tests(p.get("tests") or p.get("testcases") or p.get("test_cases"), 10)
    if not samples:
        samples = tests[:1]
    if not tests:
        return None, "题目缺少 tests，无法判题"
    if len(tests) < 4:
        return None, "至少需要 4 组 tests（建议 4-6 组），请重新生成"
    # 样例必须能直接判；没有把样例并进 tests 时补进去。
    if samples and not any(x["in"] == samples[0]["in"] and x["out"] == samples[0]["out"] for x in tests):
        tests.insert(0, dict(samples[0]))

    solution = _as_text(p.get("solution") or p.get("reference_solution") or p.get("solution_code"))
    if not solution:
        return None, "题目缺少 C++17 参考答案 solution"
    if "bits/stdc++.h" not in solution:
        solution = "#include <bits/stdc++.h>\n" + solution

    difficulty = p.get("difficulty", payload.get("difficulty", 3))
    try:
        difficulty = int(difficulty)
    except Exception:
        difficulty = 3
    difficulty = max(1, min(5, difficulty))
    topic = _as_text(payload.get("topic") or p.get("topic"), 120)

    tags = p.get("tags")
    if not isinstance(tags, list):
        tags = []
    tags = [_as_text(x, 30) for x in tags if _as_text(x, 30)]
    if not tags:
        tags = [topic or "AI 原创"]
    tags = tags[:6]

    hints = p.get("hints")
    if isinstance(hints, list):
        hints = [_as_text(x, 2000) for x in hints if _as_text(x, 2000)]
    else:
        hints = []
    hint_md = _as_text(p.get("hint_md") or p.get("hint"))
    if not hints and hint_md:
        hints = [x.strip() for x in re.split(r"\n+", hint_md) if x.strip()]
    if not hints:
        hints = [
            "先读清输入输出和样例，再想需要维护什么状态。",
            "把步骤拆成：读入 → 维护状态 → 更新 → 输出。",
            "先测最小规模，再测边界和极端值。",
        ]
    hint_md = hint_md or "\n".join(hints)

    try:
        time_limit = float(p.get("time_limit", 1.0))
    except Exception:
        time_limit = 1.0
    time_limit = max(0.5, min(3.0, time_limit))

    return {
        "title": title,
        "difficulty": difficulty,
        "statement_md": statement,
        "input_md": input_md,
        "output_md": output_md,
        "constraints_md": constraints,
        "samples": samples,
        "tests": tests,
        "solution": solution,
        "hints": hints,
        "hint_md": hint_md,
        "tags": tags,
        "topic": topic,
        "time_limit": time_limit,
    }, None


def problem_summary(p):
    return {
        "id": p["id"], "kind": p["kind"], "chapter": p["chapter"],
        "chapter_title": p.get("chapter_title", ""), "label": p.get("label", ""),
        "title": p["title"], "difficulty": p.get("difficulty", 2),
        "difficulty_label": p.get("difficulty_label", ""),
        "tags": p.get("tags", []), "has_judge": bool(p.get("tests")),
        "ai_generated": bool(p.get("ai_generated")),
    }


def problem_detail(p):
    detail = {k: v for k, v in p.items() if k != "tests"}
    detail["test_count"] = len(p.get("tests") or [])
    detail["has_solution"] = os.path.isfile(os.path.join(SOL_DIR, p["id"] + ".cpp"))
    return detail


def submission_summary(rec):
    out = {k: v for k, v in rec.items() if k not in ("code", "cases")}
    out["case_count"] = len(rec.get("cases") or [])
    out["ac_cases"] = sum(1 for c in (rec.get("cases") or []) if c.get("status") == "AC")
    return out


def add_submission(pid, code, result):
    """记录一次正式提交；只留最近 MAX_SUBMISSIONS 条，代码用于回放。"""
    items = load_submissions()
    now = time.time()
    sid = str(int(now * 1000))
    while any(str(x.get("id")) == sid for x in items):
        sid = str(int(sid) + 1)
    cases = [{
        "index": c.get("index"),
        "status": c.get("status"),
        "time": c.get("time", 0),
    } for c in (result.get("cases") or [])]
    rec = {
        "id": sid,
        "problem_id": pid,
        "ts": now,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
        "verdict": result.get("verdict") or "CE",
        "time_ms": result.get("time", 0),
        "code_len": len(code),
        "code": code[:200000],
        "cases": cases,
        "compiler": "g++ -std=c++17 -O2",
    }
    items.insert(0, rec)
    save_submissions(items)
    return rec


AI_MAX_CHARS = 60000


def ai_chat(body):
    """OpenAI 兼容接口的本地代理。Key 只在本次请求里使用，不写日志、不落盘。"""
    key = str(body.get("api_key") or "").strip()
    base = str(body.get("base_url") or "").strip()
    model = str(body.get("model") or "").strip()
    messages = body.get("messages")
    try:
        max_tokens = int(body.get("max_tokens") or 1400)
    except Exception:
        max_tokens = 1400
    max_tokens = max(512, min(8192, max_tokens))
    try:
        temperature = float(body.get("temperature") if body.get("temperature") is not None else 0.3)
    except Exception:
        temperature = 0.3
    temperature = max(0.0, min(1.2, temperature))
    try:
        timeout_s = float(body.get("timeout") or 60)
    except Exception:
        timeout_s = 60.0
    timeout_s = max(30.0, min(180.0, timeout_s))
    if not key:
        return 400, {"error": "请先填写 API Key"}
    if not model:
        return 400, {"error": "请先填写模型名"}
    u = urlparse(base)
    if u.scheme not in ("http", "https") or not u.hostname:
        return 400, {"error": "接口地址必须是 http(s):// 开头的完整地址"}
    if u.username or u.password:
        return 400, {"error": "接口地址里不要包含用户名或密码"}
    if u.scheme == "http" and u.hostname not in ("127.0.0.1", "localhost", "::1"):
        return 400, {"error": "除本机服务外，接口地址必须使用 https"}
    if not isinstance(messages, list) or not messages:
        return 400, {"error": "对话内容为空"}
    clean = []
    total = 0
    for m in messages[-16:]:
        if not isinstance(m, dict):
            continue
        role = m.get("role")
        content = m.get("content")
        if role not in ("system", "user", "assistant") or not isinstance(content, str):
            continue
        content = content[:20000]
        total += len(content)
        if total > AI_MAX_CHARS:
            break
        clean.append({"role": role, "content": content})
    if not clean:
        return 400, {"error": "对话内容格式不正确"}

    if u.path.rstrip("/").endswith("/chat/completions"):
        url = base
    else:
        url = base.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": clean,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
            "User-Agent": "LocalOJ/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8", "replace")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        msg = raw[:500]
        try:
            obj = json.loads(raw)
            err = obj.get("error")
            if isinstance(err, dict):
                msg = err.get("message") or msg
            elif isinstance(err, str):
                msg = err
        except Exception:
            pass
        code = e.code if e.code in (400, 401, 403, 404, 429) else 502
        return code, {"error": "AI 接口返回错误：%s" % (msg or e.reason)}
    except urllib.error.URLError as e:
        return 502, {"error": "连不上 AI 接口：%s" % (e.reason,)}
    except TimeoutError:
        return 504, {"error": "AI 接口超时，请稍后重试"}
    except Exception as e:
        return 502, {"error": "AI 请求失败：%s" % (e,)}

    try:
        choice = (data.get("choices") or [])[0]
        msg = choice.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            content = "".join(str(x.get("text", "")) if isinstance(x, dict) else str(x)
                              for x in content)
        if not content:
            content = msg.get("reasoning_content") or ""
    except Exception:
        return 502, {"error": "AI 返回格式无法识别"}
    if not content:
        return 502, {"error": "AI 没有返回文本内容"}
    return 200, {
        "content": content,
        "model": data.get("model") or model,
        "usage": data.get("usage") or {},
    }


def norm_out(text):
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip(" \t") for ln in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def squash(text):
    return re.sub(r"\s+", "", text or "")


def kill_tree(proc):
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            proc.kill()
    except Exception:
        pass


def _dbg(msg):
    if not os.environ.get("OJ_DEBUG"):
        return
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge_debug.log")
        with open(path, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (time.strftime("%H:%M:%S"), msg))
    except Exception:
        pass


def decode_output(raw):
    """g++ 在 Windows 上常按 GBK 输出，先按 UTF-8 试，失败再按 GB18030。"""
    if isinstance(raw, str):
        return raw
    for enc in ("utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def compile_cpp(src_path, exe_path):
    gpp = find_gpp()
    if not gpp:
        return False, "未找到 g++。请确认已安装 MinGW/TDM-GCC，并把 g++ 加入 PATH。"
    cmd = [gpp, "-std=c++17", "-O2", "-pipe", "-o", exe_path, src_path]
    try:
        cp = subprocess.run(cmd, capture_output=True, text=False, timeout=30,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired:
        return False, "编译超时（30 秒）。"
    if cp.returncode != 0:
        msg = (decode_output(cp.stderr) or decode_output(cp.stdout) or "").strip()
        msg = msg.replace(src_path, "main.cpp").replace(os.path.dirname(src_path), ".")
        return False, msg or "编译失败。"
    return True, ""


def run_one(exe, input_text, time_limit, cwd):
    started = time.perf_counter()
    _dbg("spawn %s tl=%.2f" % (exe, time_limit))
    proc = subprocess.Popen([exe], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding="utf-8",
                            errors="replace", cwd=cwd,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    _dbg("pid=%s started" % proc.pid)
    try:
        out, err = proc.communicate(input_text, timeout=time_limit)
        elapsed = time.perf_counter() - started
        _dbg("communicate ok rc=%s elapsed=%.2fs" % (proc.returncode, elapsed))
    except subprocess.TimeoutExpired:
        _dbg("timeout, killing pid=%s" % proc.pid)
        kill_tree(proc)
        _dbg("killed, second communicate")
        try:
            out, err = proc.communicate(timeout=2)
            _dbg("second communicate ok rc=%s" % proc.returncode)
        except Exception as e:
            _dbg("second communicate failed: %r" % e)
            out, err = "", ""
        return {"status": "TLE", "time": time_limit * 1000, "out": out or "", "err": err or ""}
    elapsed_ms = int(elapsed * 1000)
    if proc.returncode != 0:
        return {"status": "RE", "time": elapsed_ms, "out": out or "", "err": err or "",
                "code": proc.returncode}
    return {"status": "OK", "time": elapsed_ms, "out": out or "", "err": err or ""}


def judge(problem, code, self_input=None):
    tmp = tempfile.mkdtemp(prefix="oj_")
    try:
        src = os.path.join(tmp, "main.cpp")
        exe = os.path.join(tmp, "main.exe" if os.name == "nt" else "main")
        with open(src, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
        ok, msg = compile_cpp(src, exe)
        if not ok:
            return {"verdict": "CE", "message": msg, "cases": [], "time": 0}
        tl = float(problem.get("time_limit", 1.0))

        if self_input is not None:
            r = run_one(exe, self_input, max(tl, 1.0), tmp)
            status = r["status"]
            return {"verdict": status if status != "OK" else "OK", "cases": [{
                "index": 0, "status": status, "time": r["time"],
                "input": self_input, "expected": None, "actual": r["out"], "stderr": r["err"]}],
                "message": "", "time": r["time"]}

        tests = problem.get("tests") or []
        if not tests:
            return {"verdict": "NO_TEST", "message": "本题没有配置测试数据。", "cases": [], "time": 0}
        cases = []
        worst = "AC"
        total_ms = 0
        for i, t in enumerate(tests, 1):
            inp = t.get("in", "")
            if inp and not inp.endswith("\n"):
                inp += "\n"
            r = run_one(exe, inp, tl, tmp)
            total_ms += r["time"]
            actual = r["out"]
            exp = t.get("out", "")
            if r["status"] == "TLE":
                st = "TLE"
            elif r["status"] == "RE":
                st = "RE"
            elif norm_out(actual) == norm_out(exp):
                st = "AC"
            elif squash(actual) == squash(exp):
                st = "PE"
            else:
                st = "WA"
            case = {"index": i, "status": st, "time": r["time"], "expected": exp,
                    "actual": actual, "stderr": (r.get("err") or "")[:400]}
            if st != "AC":
                case["input"] = inp.rstrip("\n")
                cases.append(case)
            else:
                cases.append(case)
            rank = {"AC": 0, "PE": 1, "WA": 2, "TLE": 3, "RE": 4}
            if rank[st] > rank[worst]:
                worst = st
        return {"verdict": worst, "message": "", "cases": cases, "time": total_ms}

    finally:
        shutil.rmtree(tmp, ignore_errors=True)


class Handler(BaseHTTPRequestHandler):
    server_version = "LocalOJ/1.0"

    def log_message(self, fmt, *args):
        if os.environ.get("OJ_VERBOSE"):
            super().log_message(fmt, *args)

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send(code, body, "application/json; charset=utf-8")

    def _file(self, path, ctype):
        size = os.path.getsize(path)
        range_header = self.headers.get("Range")
        start, end, status = 0, size - 1, 200
        if range_header:
            m = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
            if not m:
                self.send_response(416)
                self.send_header("Content-Range", "bytes */%d" % size)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            a, b = m.group(1), m.group(2)
            if a:
                start = int(a)
                end = int(b) if b else size - 1
            elif b:
                start = max(0, size - int(b))
                end = size - 1
            else:
                start, end = 0, size - 1
            if start >= size or start > end:
                self.send_response(416)
                self.send_header("Content-Range", "bytes */%d" % size)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            end = min(end, size - 1)
            status = 206
        length = max(0, end - start + 1)
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        if status == 206:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.end_headers()
        if self.command == "HEAD":
            return
        with open(path, "rb") as f:
            f.seek(start)
            remain = length
            while remain > 0:
                chunk = f.read(min(262144, remain))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remain -= len(chunk)


    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/problems":
            plist = STATE["problems"] or load_problems()
            out = [problem_summary(p) for p in plist]
            return self._json({"problems": out})
        if path == "/api/progress":
            return self._json(load_progress())
        if path == "/api/submissions":
            qs = parse_qs(parsed.query)
            pid = (qs.get("problem") or [None])[0]
            try:
                limit = max(1, min(300, int((qs.get("limit") or ["60"])[0])))
            except Exception:
                limit = 60
            items = load_submissions()
            if pid:
                items = [x for x in items if x.get("problem_id") == pid]
            return self._json({
                "items": [submission_summary(x) for x in items[:limit]],
                "total": len(items),
                "problem": pid or "",
            })
        if path.startswith("/api/submissions/"):
            sid = unquote(path[len("/api/submissions/"):]).strip()
            for rec in load_submissions():
                if str(rec.get("id")) == sid:
                    return self._json(rec)
            return self._json({"error": "提交记录不存在"}, 404)
        if path.startswith("/api/problem/"):
            pid = path.rsplit("/", 1)[-1]
            p = STATE["by_id"].get(pid) if STATE["by_id"] else None
            if not p:
                return self._json({"error": "题目不存在"}, 404)
            return self._json(problem_detail(p))
        if path.startswith("/api/solution/"):
            pid = path.rsplit("/", 1)[-1].replace("/", "")
            for p in (STATE["problems"] or load_problems()):
                if p["id"] == pid:
                    break
            else:
                return self._json({"error": "题目不存在"}, 404)
            fn = os.path.join(SOL_DIR, pid + ".cpp")
            if not os.path.isfile(fn):
                return self._json({"error": "本题暂无参考答案"}, 404)
            with open(fn, encoding="utf-8") as f:
                code = f.read()
            return self._json({"id": pid, "lang": "cpp", "code": code})
        if path.startswith("/book/"):
            name = unquote(path[len("/book/"):])
            book_root = os.path.realpath(os.path.join(WEB_DIR, "book"))
            full = os.path.realpath(os.path.join(book_root, name))
            if full.startswith(book_root + os.sep) and os.path.isfile(full):
                ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
                if full.endswith(".md"):
                    ctype = "text/markdown; charset=utf-8"
                elif full.endswith((".json", ".txt")):
                    ctype += "; charset=utf-8"
                return self._file(full, ctype)
        if path == "/" or path == "":
            return self._file(os.path.join(WEB_DIR, "index.html"), "text/html; charset=utf-8")
        if path.startswith("/static/"):
            name = path[len("/static/"):]
            full = os.path.join(WEB_DIR, name)
            if os.path.exists(full) and os.path.isfile(full):
                ctype = "text/plain"
                if name.endswith(".css"):
                    ctype = "text/css; charset=utf-8"
                elif name.endswith(".js"):
                    ctype = "application/javascript; charset=utf-8"
                elif name.endswith(".svg"):
                    ctype = "image/svg+xml"
                elif name.endswith(".png"):
                    ctype = "image/png"
                elif name.endswith(".ico"):
                    ctype = "image/x-icon"
                elif name.endswith((".jpg", ".jpeg")):
                    ctype = "image/jpeg"
                elif name.endswith(".webp"):
                    ctype = "image/webp"
                return self._file(full, ctype)
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        if length > 2_000_000:
            return self._json({"error": "请求体过大"}, 413)
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        except Exception:
            return self._json({"error": "请求体不是合法 JSON"}, 400)

        if parsed.path == "/api/submit":
            pid = body.get("id")
            code = body.get("code", "")
            p = STATE["by_id"].get(pid)
            if not p:
                return self._json({"error": "题目不存在"}, 404)
            if not code.strip():
                return self._json({"error": "代码为空"}, 400)
            with LOCK:
                result = judge(p, code)
            progress = load_progress()
            rec = progress.get(pid, {"attempts": 0})
            rec["attempts"] = rec.get("attempts", 0) + 1
            rec["last"] = result["verdict"]
            if result["verdict"] == "AC" and rec.get("status") != "AC":
                rec["status"] = "AC"
                rec["ac_time"] = time.strftime("%Y-%m-%d %H:%M")
            elif rec.get("status") != "AC":
                rec["status"] = result["verdict"]
            progress[pid] = rec
            save_progress(progress)
            try:
                history = add_submission(pid, code, result)
                result["submission_id"] = history["id"]
            except Exception:
                result["submission_id"] = ""
            return self._json(result)

        if parsed.path == "/api/selfrun":
            pid = body.get("id")
            code = body.get("code", "")
            inp = body.get("input", "")
            p = STATE["by_id"].get(pid) or {"time_limit": 1.0}
            if not code.strip():
                return self._json({"error": "代码为空"}, 400)
            with LOCK:
                result = judge(p, code, self_input=inp)
            return self._json(result)

        if parsed.path == "/api/problems/generated":
            normalized, err = normalize_generated_problem(body)
            if err:
                return self._json({"error": err}, 400)
            requested = body.get("difficulty")
            if requested is not None:
                try:
                    requested = int(requested)
                    normalized["difficulty"] = max(1, min(5, requested))
                except Exception:
                    pass

            with LOCK:
                try:
                    with open(PROBLEMS_JSON, "r", encoding="utf-8") as f:
                        bank = json.load(f)
                    problems = bank["problems"] if isinstance(bank, dict) else bank
                    meta = bank.get("meta", {}) if isinstance(bank, dict) else {}
                except Exception as e:
                    return self._json({"error": "题库读取失败：%s" % e}, 500)

                title_key = normalized["title"].casefold()
                stmt_key = re.sub(r"\s+", "", normalized["statement_md"]).casefold()
                for p in problems:
                    if str(p.get("title", "")).strip().casefold() == title_key:
                        return self._json({"error": "题库里已有一道同名题，请换一个标题重新生成"}, 409)
                    if re.sub(r"\s+", "", str(p.get("statement_md", ""))).casefold() == stmt_key:
                        return self._json({"error": "题库里已有题面相同的题目，请换一个场景重新生成"}, 409)

                ai_count = sum(1 for p in problems if p.get("kind") == "ai") + 1
                stamp = time.strftime("%Y%m%d%H%M%S")
                pid = "ai-%s-%03d" % (stamp, int(time.time_ns() % 1000))
                while any(p.get("id") == pid for p in problems):
                    pid += "x"

                diff = normalized["difficulty"]
                diff_label = {1: "入门", 2: "基础", 3: "提高", 4: "进阶", 5: "挑战"}[diff]
                test_problem = {
                    "id": pid,
                    "kind": "ai",
                    "chapter": 33,
                    "chapter_title": "AI 原创题",
                    "label": "AI 出题 %02d" % ai_count,
                    "title": normalized["title"],
                    "difficulty": diff,
                    "statement_md": normalized["statement_md"],
                    "input_md": normalized["input_md"],
                    "output_md": normalized["output_md"],
                    "constraints_md": normalized["constraints_md"],
                    "samples": normalized["samples"],
                    "tests": normalized["tests"],
                    "time_limit": normalized["time_limit"],
                }
                result = judge(test_problem, normalized["solution"])
                if result.get("verdict") != "AC":
                    bad = next((c for c in result.get("cases", []) if c.get("status") != "AC"), {})
                    msg = result.get("message") or "参考答案没有通过全部测试用例"
                    if bad:
                        msg += "；首个失败用例：%s（第 %s 组）" % (bad.get("status"), bad.get("index"))
                    return self._json({
                        "error": "这道题还不能判：参考答案未通过自测。请重新生成或修改题目后再保存。",
                        "detail": msg,
                        "verdict": result.get("verdict"),
                        "cases": result.get("cases", [])[:2],
                    }, 422)

                if body.get("dry_run"):
                    return self._json({
                        "ok": True, "validated": True,
                        "verdict": result.get("verdict"),
                        "test_count": len(normalized["tests"]),
                        "reference_lines": len([x for x in normalized["solution"].splitlines() if x.strip()]),
                    })

                full = dict(normalized)
                full.update({
                    "id": pid,
                    "kind": "ai",
                    "chapter": 33,
                    "chapter_title": "AI 原创题",
                    "label": "AI 出题 %02d" % ai_count,
                    "difficulty_label": diff_label,
                    "difficulty_note": "AI 助教按你设定的难度生成；参考答案已通过全部测试用例。",
                    "difficulty_factors": [
                        {"name": "知识点", "level": diff, "note": "、".join(normalized["tags"])},
                        {"name": "思维", "level": diff, "note": "由 AI 按目标难度控制"},
                        {"name": "实现", "level": diff, "note": "参考答案 %d 行" % len([x for x in normalized["solution"].splitlines() if x.strip()])},
                        {"name": "细节", "level": diff, "note": "边界与数据范围见题面"},
                    ],
                    "code_files": [],
                    "source": "AI 助教原创" + (" · " + normalized["topic"] if normalized["topic"] else ""),
                    "solution": "solutions/%s.cpp" % pid,
                    "solution_name": pid + ".cpp",
                    "ai_generated": True,
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                })
                # tests 已保留在题库；参考答案写入 solutions/，题目里只存路径。
                full.pop("topic", None)

                try:
                    os.makedirs(SOL_DIR, exist_ok=True)
                    with open(os.path.join(SOL_DIR, pid + ".cpp"), "w", encoding="utf-8", newline="\n") as f:
                        f.write(normalized["solution"].rstrip() + "\n")
                    problems.append(full)
                    meta["count"] = len(problems)
                    counts = meta.setdefault("counts", {})
                    counts["ai"] = ai_count
                    diff_counts = meta.setdefault("difficulty_counts", {})
                    diff_counts[str(diff)] = int(diff_counts.get(str(diff), 0)) + 1
                    chapters = meta.setdefault("chapters", [])
                    if 33 not in chapters:
                        chapters.append(33)
                    save_problem_bank(meta, problems)
                    STATE["problems"] = problems
                    STATE["by_id"] = {p["id"]: p for p in problems}
                except Exception as e:
                    return self._json({"error": "保存题库失败：%s" % e}, 500)

            return self._json({
                "ok": True,
                "id": pid,
                "problem": problem_summary(full),
                "detail": problem_detail(full),
                "test_count": len(full["tests"]),
            })

        if parsed.path == "/api/progress/reset":
            save_progress({})
            return self._json({"ok": True})

        if parsed.path == "/api/ai":
            code, obj = ai_chat(body)
            return self._json(obj, code)

        return self._json({"error": "not found"}, 404)


def main():
    port = 8765
    open_browser = False
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
        if a == "--open":
            open_browser = True
    load_problems()
    url = "http://127.0.0.1:%d/" % port
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError:
        print("端口 %d 已被占用，可能 OJ 已经在运行：%s" % (port, url))
        if open_browser:
            webbrowser.open(url)
        return
    print("本地 OJ 已启动：%s" % url)
    print("g++：%s" % (find_gpp() or "未找到！"))
    print("按 Ctrl+C 停止。")
    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
