#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端验收：题库完整性、判题（AC/WA/TLE/CE/PE）、自测、进度。"""
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8765"
OJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(OJ, "data")

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


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def post(path, payload):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def post_status(path, payload):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            obj = json.loads(e.read().decode("utf-8"))
        except Exception:
            obj = {"error": ""}
        return e.code, obj


def solution_text(filename):
    with open(os.path.join(DATA, "solutions", filename), encoding="utf-8") as f:
        return f.read()


C_C01 = r"""
#include <iostream>
using namespace std;
int main() {
    int n; cin >> n;
    long long sum = 0, best = -1; int idx = 1;
    for (int i = 1; i <= n; i++) {
        long long x; cin >> x;
        sum += x;
        if (x > best) { best = x; idx = i; }
    }
    cout << sum << "\n" << idx << "\n";
    return 0;
}
"""

C_C02 = r"""
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
int main() {
    int n; cin >> n;
    vector<pair<long long, string>> v(n);
    for (int i = 0; i < n; i++) cin >> v[i].second >> v[i].first;
    sort(v.begin(), v.end());
    for (auto &p : v) cout << p.second << " " << p.first << "\n";
    return 0;
}
"""

C_P1801 = r"""
#include <iostream>
using namespace std;
long long t[100005]; int n;
void add(int i, long long v){ for(;i<=n;i+=i&-i) t[i]+=v; }
long long qry(int i){ long long s=0; for(;i>0;i-=i&-i) s+=t[i]; return s; }
int main(){ int q; cin>>n>>q; while(q--){ int op; cin>>op;
  if(op==1){int x;long long k;cin>>x>>k;add(x,k);}
  else {int l,r;cin>>l>>r;cout<<qry(r)-qry(l-1)<<"\n";} } return 0; }
"""

C_P2501 = r"""
#include <iostream>
#include <algorithm>
using namespace std;
long long a[305], pre[305], f[305][305];
int main(){ int n; cin>>n; for(int i=1;i<=n;i++){cin>>a[i]; pre[i]=pre[i-1]+a[i];}
 for(int len=2;len<=n;len++) for(int i=1;i+len-1<=n;i++){ int j=i+len-1;
   f[i][j]=1LL<<60; for(int k=i;k<j;k++) f[i][j]=min(f[i][j], f[i][k]+f[k+1][j]);
   f[i][j]+=pre[j]-pre[i-1]; }
 cout<<f[1][n]<<"\n"; return 0; }
"""

C_P2605 = r"""
#include <iostream>
#include <algorithm>
using namespace std;
int d[16][16]; long long dp[1<<15][15];
int main(){ int n; cin>>n; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cin>>d[i][j];
 const long long INF=1LL<<60; for(int m=0;m<(1<<n);m++) for(int i=0;i<n;i++) dp[m][i]=INF;
 dp[1][0]=0;
 for(int m=1;m<(1<<n);m++) for(int i=0;i<n;i++){ if(dp[m][i]>=INF||!(m>>i&1)) continue;
   for(int j=0;j<n;j++) if(!(m>>j&1)) dp[m|1<<j][j]=min(dp[m|1<<j][j], dp[m][i]+d[i][j]); }
 long long ans=INF; for(int i=0;i<n;i++) ans=min(ans, dp[(1<<n)-1][i]+d[i][0]);
 cout<<ans<<"\n"; return 0; }
"""

C_P3005 = r"""
#include <iostream>
using namespace std;
const long long MOD=1000000007;
int main(){ int n; cin>>n; if(n==0){cout<<1<<"\n";return 0;} if(n==1){cout<<0<<"\n";return 0;}
 long long a=0,b=1; for(int i=3;i<=n;i++){ long long c=(i-1)%MOD*((a+b)%MOD)%MOD; a=b; b=c; }
 cout<<b%MOD<<"\n"; return 0; }
"""


def main():
    print("== 1. 题库完整性 ==")
    data = get("/api/problems")
    plist = data["problems"]
    kinds = {}
    for p in plist:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    check("题目总数 399", len(plist) == 399, "实际 %d" % len(plist))
    check("例题 94", kinds.get("example") == 94, str(kinds))
    check("可判题习题 118", kinds.get("exercise") == 118)
    check("思考题 51", kinds.get("think") == 51)
    check("附录 C 36", kinds.get("appendix") == 36)
    check("贵阳原创 100", kinds.get("local") == 100)
    judged = [p for p in plist if p["has_judge"]]
    check("可判题全部有测试数据", len(judged) == 348, "%d 道可判题" % len(judged))
    check("列表带难度标签", all(p.get("difficulty_label") for p in plist), "字段 difficulty_label")

    print("== 2. 详情接口 ==")
    d1 = get("/api/problem/c-01")
    check("详情不含测试数据", "tests" not in d1)
    check("详情带测试点数量", d1.get("test_count", 0) > 0, "test_count=%s" % d1.get("test_count"))
    th = get("/api/problem/p-01-01")
    check("思考题无测试数据", th.get("test_count") == 0)
    check("思考题有提示", bool(th.get("hint_md")), th.get("hint_md", "")[:40])
    g1 = get("/api/problem/gy-050")
    check("贵阳题有分层提示", len(g1.get("hints") or []) >= 2, "%d 层" % len(g1.get("hints") or []))
    check("贵阳题有难度解释", bool(g1.get("difficulty_note")) and len(g1.get("difficulty_factors") or []) == 4,
          "%d 个维度" % len(g1.get("difficulty_factors") or []))
    check("参考答案为 bits/stdc++.h", "#include <bits/stdc++.h>" in solution_text("gy-050.cpp"))

    print("== 3. 例题参考解判题（AC） ==")
    for pid, sol in [("ex-01-01", "ex-01-01.cpp"), ("ex-19-01", "ex-19-01.cpp"),
                     ("ex-24-03", "ex-24-03.cpp"), ("ex-32-01", "ex-32-01.cpp"),
                     ("ex-32-02", "ex-32-02.cpp")]:
        if not os.path.exists(os.path.join(DATA, "solutions", sol)):
            check(pid, False, "找不到参考程序 %s" % sol)
            continue
        res = post("/api/submit", {"id": pid, "code": solution_text(sol)})
        check(pid + " 提交", res.get("verdict") == "AC",
              "%s（%d 个测试点）" % (res.get("verdict"), len(res.get("cases", []))))

    print("== 4. 习题 / 附录 C 自写解法判题（AC） ==")
    for pid, code in [("c-01", C_C01), ("c-02", C_C02), ("p-18-01", C_P1801),
                      ("p-25-01", C_P2501), ("gy-050", solution_text("gy-050.cpp")),
                      ("p-30-05", C_P3005)]:
        res = post("/api/submit", {"id": pid, "code": code})
        bad = [c["index"] for c in res.get("cases", []) if c["status"] != "AC"]
        check(pid + " 提交", res.get("verdict") == "AC",
              "%s（%d 个测试点，失败点 %s）" % (res.get("verdict"), len(res.get("cases", [])), bad))

    print("== 5. 异常判题 ==")
    wa = post("/api/submit", {"id": "c-01", "code": "#include <iostream>\nint main(){std::cout<<\"0\\n1\\n\";}"})
    check("WA", wa.get("verdict") == "WA", wa.get("verdict"))
    ce = post("/api/submit", {"id": "c-01", "code": "int main(){ this is not c++ }"})
    check("CE", ce.get("verdict") == "CE", (ce.get("message") or "")[:40])
    tle = post("/api/submit", {"id": "c-01", "code":
               "#include <iostream>\nint main(){volatile long long x=0; while(1) x++;}"})
    check("TLE", tle.get("verdict") == "TLE",
          "%s（用例 %s）" % (tle.get("verdict"), [c.get("status") for c in tle.get("cases", [])]))
    pe = post("/api/submit", {"id": "c-01", "code":
               "#include <iostream>\nusing namespace std;\nint main(){int n;cin>>n;long long s=0,b=-1;int k=1;"
               "for(int i=1;i<=n;i++){long long x;cin>>x;s+=x;if(x>b){b=x;k=i;}}cout<<\" \"<<s<<\"\\n  \"<<k<<\"\\n\";}"})
    check("PE", pe.get("verdict") == "PE", pe.get("verdict"))

    print("== 6. 自测 ==")
    sr = post("/api/selfrun", {"id": "c-01", "code": C_C01, "input": "3\n1 2 3"})
    out = (sr.get("cases") or [{}])[0].get("actual", "")
    check("自测输出正确", out.strip().replace("\r", "") == "6\n3", repr(out))
    sr2 = post("/api/selfrun", {"id": "c-01", "code": C_C01, "input": "4\n0 0 7 7"})
    out2 = (sr2.get("cases") or [{}])[0].get("actual", "")
    check("自测并列最大值取小编号", out2.strip().replace("\r", "") == "14\n3", repr(out2))

    print("== 7. 进度 ==")
    prog = get("/api/progress")
    check("进度已记录", len(prog) >= 10, "%d 条记录" % len(prog))
    check("AC 记录存在", any(v.get("status") == "AC" for v in prog.values()))
    reset = post("/api/progress/reset", {})
    check("重置进度", reset.get("ok") is True)
    check("重置后为空", len(get("/api/progress")) == 0)

    print("== 8. 静态资源 ==")
    with urllib.request.urlopen(BASE + "/", timeout=10) as r:
        html = r.read().decode("utf-8")
    check("首页可访问", "本地 OJ" in html or "OJ" in html, "%d 字节" % len(html))
    check("首页有本地文件提交入口", 'id="btnImport"' in html and 'id="fileInput"' in html)
    check("本地文件提交限制代码文件类型", '.cpp' in html and 'accept=".cpp,.cc,.cxx,.c,.h,.hpp,.txt"' in html)
    check("首页有 AI 助教入口", 'id="btnAI"' in html and 'id="aiKey"' in html and 'id="aiProvider"' in html)

    print("== 9. AI 助教接口 ==")
    code, obj = post_status("/api/ai", {
        "api_key": "",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "hi"}],
    })
    check("未填 API Key 被拒绝", code == 400 and "API Key" in obj.get("error", ""), "%s %s" % (code, obj.get("error")))
    code2, obj2 = post_status("/api/ai", {
        "api_key": "test",
        "base_url": "http://example.com/v1",
        "model": "m",
        "messages": [{"role": "user", "content": "hi"}],
    })
    check("非本机明文接口被拒绝", code2 == 400 and "https" in obj2.get("error", ""), "%s %s" % (code2, obj2.get("error")))

    print("\n结果：通过 %d，失败 %d" % (passed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
