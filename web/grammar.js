/* ============================================================
   语法加油站
   - 当前代码体检（本地规则，不把代码发到任何地方）
   - 编译 / 运行 / 逻辑错误的急救卡
   - C++ 语法货架、原书章节联动
   - 5 分钟小练习，记录保存在本机
   ============================================================ */
'use strict';

const GRAMMAR_KEY = 'oj.grammar.v1';

const GRAMMAR_SYMPTOMS = [
  {
    key: 'ce',
    tag: 'CE',
    label: '编译错误',
    short: '红色报错',
    title: '先让编译器把话说完',
    lead: '编译错误通常只看第一条。后面的报错常常是第一处错误的连锁反应。',
    checks: [
      '从上往下读第一条 error，先不管它下面的 note',
      '检查中文分号 `；`、中文括号和全角空格',
      '检查括号、引号、分号是否成对闭合',
      '对照报错行号，先看上一行是否漏了分号',
    ],
    bad: 'for (int i = 0; i < n; i++) {\n    cout << a[i]；\n}',
    good: 'for (int i = 0; i < n; i++) {\n    cout << a[i];\n}',
    book: 'ch02',
    bookLabel: 'C++ 基础补课',
    ask: '请按编译器第一条报错，帮我定位最可能的语法错误，不要直接重写整份代码。',
  },
  {
    key: 'wa',
    tag: 'WA',
    label: '答案错误',
    short: '样例过了',
    title: '样例是路标，不是终点',
    lead: '样例通过只说明最小路径正确。WA 要先怀疑边界、初始化和下标。',
    checks: [
      '用 n = 1、空输入、全相同值各跑一遍',
      '检查循环是否从 0 到 n - 1，而不是到 n',
      '检查变量是否在每组数据前重新初始化',
      '检查答案是否可能为负、溢出或需要取模',
    ],
    bad: 'int sum = 0;\nfor (int i = 0; i <= n; i++)\n    sum += a[i];',
    good: 'int sum = 0;\nfor (int i = 0; i < n; i++)\n    sum += a[i];',
    book: 'ch04',
    bookLabel: '复杂度与边界',
    ask: '我的代码样例通过但答案错误。请只检查边界、下标和初始化，指出最可能的 1 个原因。',
  },
  {
    key: 're',
    tag: 'RE',
    label: '运行错误',
    short: '程序崩了',
    title: '先找越界和除零',
    lead: 'RE 不是“结果不对”，而是程序在某个用例上没有办法继续运行。',
    checks: [
      '检查数组下标是否可能等于 n，或访问空 vector',
      '检查除数是否可能为 0，取模是否可能除以 0',
      '检查递归深度是否超过栈空间',
      '检查是否把局部大数组开在函数内部',
    ],
    bad: 'int a[10];\ncout << a[10] << endl;',
    good: 'vector<int> a(10);\ncout << a[9] << endl;',
    book: 'ch03',
    bookLabel: 'STL 与容器',
    ask: '程序出现运行错误。请优先检查数组越界、空容器、除零和递归深度，不要先改算法。',
  },
  {
    key: 'tle',
    tag: 'TLE',
    label: '超时',
    short: '跑得太慢',
    title: '先数复杂度，再优化常数',
    lead: 'TLE 先看循环层数和数据范围，再考虑 `endl`、频繁拷贝这类常数开销。',
    checks: [
      '把数据范围代进最大循环次数，估一下是不是 10^8 以上',
      '检查是否有 while 循环没有推进变量',
      '把 `endl` 换成 `\\n`，把同步流关闭',
      '能用前缀和、二分、排序或记忆化，就不要重复扫描',
    ],
    bad: 'for (int i = 0; i < n; i++)\n    for (int j = 0; j < n; j++)\n        // n = 1e5 时这里会跑 1e10 次',
    good: '// 先用前缀和 / 二分 / 排序把重复扫描降下来\n// 1e5 的数据通常要接近 O(n log n) 或 O(n)',
    book: 'ch04',
    bookLabel: '复杂度：为什么会超时',
    ask: '我遇到了超时。请根据数据范围估算复杂度，指出最该先改掉的一层循环或常数开销。',
  },
  {
    key: 'io',
    tag: 'I/O',
    label: '输入输出',
    short: '读不进来',
    title: '空格、换行和多组数据',
    lead: '`cin >>` 会跳过空格和换行，`getline` 不会；两者混用时最容易读错。',
    checks: [
      '读完整行前，先用 `cin.ignore()` 吃掉上一行换行',
      '多组数据用 `while (cin >> n)`，不要只读一组',
      '输出末尾空格通常没关系，但不要多输出一行解释',
      '本地自测时，把输入框里的换行也当作真实输入',
    ],
    bad: 'int n;\nstring s;\ncin >> n;\ngetline(cin, s); // 可能读到空串',
    good: 'int n;\nstring s;\ncin >> n;\ncin.ignore();\ngetline(cin, s);',
    book: 'ch02',
    bookLabel: 'C++ 基础补课',
    ask: '请检查我的输入读取方式，特别是 cin、getline、getchar 混用和多组数据的部分。',
  },
  {
    key: 'overflow',
    tag: 'LL',
    label: '整数溢出',
    short: '答案变负',
    title: '先转 long long，再相乘',
    lead: '两个 int 相乘会在 int 里先算完，再赋给 long long 已经来不及了。',
    checks: [
      '乘法前先写 `1LL * a * b`',
      '累加和可能超过 2 × 10^9 时用 long long',
      '输出 long long 用 `%lld` 或 `cout`',
      '取模时每一步都保持数值在范围内',
    ],
    bad: 'int a = 100000, b = 100000;\nlong long c = a * b;',
    good: 'int a = 100000, b = 100000;\nlong long c = 1LL * a * b;',
    book: 'ch04',
    bookLabel: '复杂度与数值范围',
    ask: '请检查我的整数溢出风险，重点看乘法、累加、取模和输出格式。',
  },
];

const GRAMMAR_CARDS = [
  {
    id: 'starter',
    tag: 'BASIC · 01',
    title: '一屏起手式',
    summary: '头文件、快读、main 一次写齐，开新题直接从这里开始。',
    code: `#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    return 0;
}`,
    book: 'ch02',
    bookLabel: '第 2 章 · C++ 基础补课',
    tip: '本机使用 g++ 17，`bits/stdc++.h` 可以直接用；不要忘了 `return 0;`。',
  },
  {
    id: 'input',
    tag: 'READ · 02',
    title: '多组输入',
    summary: '读到文件结束为止；比固定读一组更耐造。',
    code: `int n;
while (cin >> n) {
    // 处理这一组数据
    cout << n << '\\n';
}`,
    book: 'ch02',
    bookLabel: '第 2 章 · 输入与循环',
    tip: '题目说“多组数据”时，不要只读一组；while 的条件本身就是读取动作。',
  },
  {
    id: 'vector',
    tag: 'STL · 03',
    title: 'vector 先开好空间',
    summary: '下标访问前，先确认容器里真的有这个位置。',
    code: `int n;
cin >> n;
vector<int> a(n);
for (int i = 0; i < n; i++) {
    cin >> a[i];
}

// 追加元素用 push_back
vector<int> b;
b.push_back(10);`,
    book: 'ch03',
    bookLabel: '第 3 章 · STL 速成',
    tip: '`vector<int> a(n)` 已经有 n 个元素；空 vector 不能直接 `a[0]`。',
  },
  {
    id: 'sort',
    tag: 'STL · 04',
    title: '排序与 lambda',
    summary: '默认升序；自定义顺序时，比较器必须严格。',
    code: `sort(a.begin(), a.end());              // 升序
sort(a.begin(), a.end(), [](int x, int y) {
    return x > y;                       // 降序
});`,
    book: 'ch07',
    bookLabel: '第 7 章 · 排序与二分',
    tip: '比较器不要写 `<=` 或 `>=`；相等时返回 true 会破坏排序规则。',
  },
  {
    id: 'string',
    tag: 'STRING · 05',
    title: '读一整行字符串',
    summary: '`cin >>` 只读一个词，包含空格的整行要用 getline。',
    code: `int n;
string s;
cin >> n;
cin.ignore(numeric_limits<streamsize>::max(), '\\n');
getline(cin, s);`,
    book: 'ch28',
    bookLabel: '第 28 章 · 字符串算法',
    tip: '`cin >> n` 后面的换行还在缓冲区里；先 ignore 再 getline。',
  },
  {
    id: 'number',
    tag: 'NUMBER · 06',
    title: 'long long 防溢出',
    summary: '乘法前先转 1LL；大和也要用 long long 接。',
    code: `int a = 100000, b = 100000;
long long product = 1LL * a * b;

long long sum = 0;
for (int x : a) sum += x;
cout << sum << '\\n';`,
    book: 'ch04',
    bookLabel: '第 4 章 · 复杂度与数值范围',
    tip: '`1LL * a * b` 会先把 a 提升为 long long，再乘 b。',
  },
  {
    id: 'struct',
    tag: 'STRUCT · 07',
    title: '结构体排序',
    summary: '多关键字排序：先比较第一关键字，再比较第二关键字。',
    code: `struct Node { int x, y; };

sort(v.begin(), v.end(), [](const Node &a, const Node &b) {
    if (a.x != b.x) return a.x < b.x;
    return a.y < b.y;
});`,
    book: 'ch03',
    bookLabel: '第 3 章 · 结构体与 STL',
    tip: '先写清楚“谁在前”的规则，再写 lambda；相等时不要返回 true。',
  },
  {
    id: 'debug',
    tag: 'DEBUG · 08',
    title: '用 cerr 照亮路径',
    summary: '调试输出写 stderr，不污染 stdout，也不会影响判题输出。',
    code: `int mid = (l + r) / 2;
cerr << "l=" << l << " r=" << r
     << " mid=" << mid << '\\n';`,
    book: 'ch02',
    bookLabel: '第 2 章 · 本地调试',
    tip: '提交前把 cerr 全部删掉；它不会进入标准输出，但会拖慢程序。',
  },
];

const GRAMMAR_QUIZ = [
  {
    q: '#include <bits/stdc++.h> 在竞赛代码里通常意味着什么？',
    code: `#include <bits/stdc++.h>
using namespace std;`,
    options: [
      '只包含 cin / cout',
      '把 C++ 标准库的大部分头文件一次性引入',
      '自动开启 -O2 优化',
      '把所有 int 自动变成 long long',
    ],
    answer: 1,
    why: '它是竞赛常用的“万能头”，方便但会拉长编译时间；本地 g++ 17 可以直接使用。',
  },
  {
    q: '下面代码读取 `3\\nhello\\n`，变量 s 最可能是什么？',
    code: `int n;
string s;
cin >> n;
getline(cin, s);`,
    options: ['"hello"', '空字符串', '"3hello"', '"\\nhello"'],
    answer: 1,
    why: '`cin >> n` 把换行留在了缓冲区；`getline` 先读到了这个换行，所以 s 是空串。读整行前要 `cin.ignore()`。',
  },
  {
    q: '这段代码最可能发生什么？',
    code: `vector<int> v;
v[0] = 7;`,
    options: ['正常写入', '越界访问，v 还没有元素', '自动扩容到 1', '编译错误'],
    answer: 1,
    why: '空的 vector 没有 `v[0]`；要写入先用 `push_back` 或 `resize` / 构造时给大小。',
  },
  {
    q: '变量 c 的结果为什么可能是错的？',
    code: `int a = 100000, b = 100000;
long long c = a * b;`,
    options: [
      'long long 不能存 1e10',
      'a * b 先按 int 计算，溢出后才赋给 c',
      'int 和 long long 不能相乘',
      '没有加 using namespace std',
    ],
    answer: 1,
    why: '乘法表达式先按 int 求值，再隐式转换成 long long。写成 `1LL * a * b` 才能先提升类型。',
  },
  {
    q: '`if (a = 3)` 和 `if (a == 3)` 的区别是？',
    code: `int a = 1;
if (a = 3) {
    cout << "yes";
}`,
    options: [
      '完全一样',
      '前者是赋值，条件永远为真',
      '前者是相等比较，后者是赋值',
      '编译一定失败',
    ],
    answer: 1,
    why: '`=` 是赋值，赋值表达式的值就是 3（非零，视为真）。比较要用 `==`。',
  },
  {
    q: 'C++ 中 `cout << (-7 % 3)` 的结果通常是？',
    code: `cout << (-7 % 3) << '\\n';`,
    options: ['2', '-1', '1', '0'],
    answer: 1,
    why: 'C++11 起整数除法向零截断，余数与被除数同号，所以 `-7 % 3` 是 -1；需要非负余数时要额外调整。',
  },
  {
    q: '这个比较器最大的问题是？',
    code: `sort(v.begin(), v.end(), [](int a, int b) {
    return a <= b;
});`,
    options: [
      '不能使用 lambda',
      '`<=` 把相等元素也当作“小于”，不满足严格弱序',
      '必须写 a > b',
      'sort 只能排字符串',
    ],
    answer: 1,
    why: '比较器要对相等元素返回 false。用 `<` 或 `>`，不要在比较器里写 `<=` / `>=`。',
  },
  {
    q: '`while (cin >> n)` 通常在什么情况下结束？',
    code: `int n;
while (cin >> n) {
    cout << n << '\\n';
}`,
    options: [
      'n 等于 0 时',
      '读到文件结束或输入流进入失败状态',
      '只循环一次',
      'n 为负数时',
    ],
    answer: 1,
    why: '`cin >> n` 返回流对象，读取失败（例如 EOF 或类型不匹配）会让条件为 false；不是靠 n == 0 停。',
  },
];

let grammar = null;
let grammarState = {
  symptom: 'ce',
  card: 'starter',
  quiz: null,
  quizIndex: 0,
  quizSelected: -1,
  quizDone: false,
  quizResult: [],
  setCounted: false,
  scannedCode: null,
  diagnostics: [],
  focusLine: null,
};

/* ---------------- 基础工具 ---------------- */

function grammarEsc(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function grammarToday() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

function grammarLoad() {
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(GRAMMAR_KEY) || 'null'); } catch (e) { }
  const base = {
    v: 1,
    visits: 0,
    scans: 0,
    copies: 0,
    drills: { answered: 0, correct: 0, sets: 0, best: 0, streak: 0, lastDate: '' },
    daily: { date: '', answered: 0, correct: 0 },
  };
  if (!saved || typeof saved !== 'object') return base;
  const result = Object.assign(base, saved);
  result.drills = Object.assign(base.drills, saved.drills || {});
  result.daily = Object.assign(base.daily, saved.daily || {});
  return result;
}

function grammarSave() {
  if (!grammar) return;
  try { localStorage.setItem(GRAMMAR_KEY, JSON.stringify(grammar)); } catch (e) { }
}

function grammarTodayStats() {
  if (!grammar || grammar.daily.date !== grammarToday()) {
    return { date: grammarToday(), answered: 0, correct: 0 };
  }
  return grammar.daily;
}

function grammarRecordAnswer(correct) {
  if (!grammar) return;
  const today = grammarToday();
  if (grammar.daily.date !== today) grammar.daily = { date: today, answered: 0, correct: 0 };
  grammar.drills.answered += 1;
  grammar.drills.correct += correct ? 1 : 0;
  grammar.drills.streak = correct ? (grammar.drills.streak || 0) + 1 : 0;
  grammar.drills.lastDate = today;
  grammar.daily.answered += 1;
  grammar.daily.correct += correct ? 1 : 0;
  grammarSave();
}

function grammarCurrentCode() {
  const editor = document.getElementById('code');
  return editor ? editor.value : '';
}

function grammarCurrentProblem() {
  try { return state && state.current ? state.current : null; } catch (e) { return null; }
}

function grammarIssueLine(code, index) {
  if (index == null || index < 0) return null;
  return code.slice(0, index).split('\n').length;
}

function grammarIssue(severity, title, message, fix, line) {
  return { severity, title, message, fix, line: line || null };
}

/* ---------------- 本地代码体检 ---------------- */

function grammarDiagnose(code) {
  const issues = [];
  if (!code || !code.trim()) return issues;
  const hasBits = /#include\s*<\s*bits\/stdc\+\+\.h\s*>/.test(code);
  const hasIostream = /#include\s*<\s*iostream\s*>/.test(code);
  const hasUsing = /using\s+namespace\s+std\s*;/.test(code);
  const hasStandardCall = /(?:cin|cout|vector|string|map|set|sort|pair|queue|priority_queue)\b/.test(code);
  const hasMain = /int\s+main\s*\(/.test(code);
  const hasReturn = /return\s+0\s*;/.test(code);
  const hasIos = /ios\s*::\s*sync_with_stdio/.test(code);
  const hasCin = /cin\s*>>/.test(code);
  const hasGetline = /getline\s*\(/.test(code);
  const hasIgnore = /cin\s*\.\s*ignore\s*\(/.test(code);
  const hasEndl = /endl/.test(code);
  const hasLoop = /(?:for|while)\s*\(/.test(code);

  if (!hasBits) {
    issues.push(grammarIssue(
      'tip', '还没有使用万能头',
      hasIostream ? '当前用的是 <iostream>，本机 g++17 支持更省事的 <bits/stdc++.h>。' : '代码里没有找到标准库头文件。',
      '#include <bits/stdc++.h>',
      null
    ));
  }
  if (hasStandardCall && !hasUsing && !/\bstd\s*::/.test(code)) {
    const idx = code.search(/(?:cin|cout|vector|string|map|set|sort|pair)\b/);
    issues.push(grammarIssue(
      'warn', '标准库名字没有来源',
      '用了 cin / cout / vector 等名字，但没有 `using namespace std;`，也没有写 `std::`。',
      '加一行 `using namespace std;`，或写成 `std::cin` / `std::vector`。',
      grammarIssueLine(code, idx)
    ));
  }
  if (!hasMain) {
    issues.push(grammarIssue(
      'error', '没有找到 main 函数',
      '判题程序需要从 `int main()` 开始执行；检查是否只写了函数或注释。',
      'int main() { ... return 0; }',
      null
    ));
  }
  if (hasMain && !hasReturn) {
    const idx = code.search(/int\s+main\s*\(/);
    issues.push(grammarIssue(
      'warn', 'main 没有 return 0',
      '本机 g++ 通常能容忍，但标准写法应在 main 末尾 `return 0;`。',
      '在 main 的最后一个 `}` 前补 `return 0;`。',
      grammarIssueLine(code, idx)
    ));
  }
  if (hasCin && !hasIos) {
    const idx = code.search(/cin\s*>>/);
    issues.push(grammarIssue(
      'tip', '可以关掉同步流',
      '数据量大时，`cin` 默认和 stdio 同步，可能拖慢输入。',
      '在 main 开头加 `ios::sync_with_stdio(false); cin.tie(nullptr);`。',
      grammarIssueLine(code, idx)
    ));
  }
  if (hasGetline && hasCin && !hasIgnore) {
    const idx = code.search(/getline\s*\(/);
    issues.push(grammarIssue(
      'warn', 'getline 前可能吃不到换行',
      '如果前面刚用 `cin >>` 读了数字，缓冲区里可能还有一个换行，getline 会先读到它。',
      '在 `getline` 前加 `cin.ignore();`，或统一使用一种读入方式。',
      grammarIssueLine(code, idx)
    ));
  }
  if (hasEndl && hasLoop) {
    const idx = code.search(/endl/);
    issues.push(grammarIssue(
      'tip', '循环里的 endl 会拖慢输出',
      '`endl` 每次都会刷新流；大量输出时通常只需换行 `\\n`。',
      '把循环里的 `endl` 换成 `\\n`。',
      grammarIssueLine(code, idx)
    ));
  }

  // 中文标点：排除 // 行注释和字符串中的内容，尽量少误报。
  const chineseMarks = /[；，（）｛｝【】“”]/g;
  let m;
  while ((m = chineseMarks.exec(code)) !== null) {
    const lineStart = code.lastIndexOf('\n', m.index - 1) + 1;
    const lineEnd = code.indexOf('\n', m.index);
    const lineText = code.slice(lineStart, lineEnd < 0 ? code.length : lineEnd);
    const commentAt = lineText.indexOf('//');
    if (commentAt >= 0 && commentAt < m.index - lineStart) continue;
    const quoteCount = (lineText.slice(0, m.index - lineStart).match(/"/g) || []).length;
    if (quoteCount % 2 === 1) continue;
    issues.push(grammarIssue(
      'error', '代码里出现了中文标点',
      '编译器会把中文全角标点当成未知字符，常见于复制题面或输入法未切回英文时。',
      '把中文标点改成英文半角 `; , ( ) { }`。',
      grammarIssueLine(code, m.index)
    ));
    break;
  }

  const emptyLoop = /for\s*\([^)]*\)\s*;/.exec(code);
  if (emptyLoop) {
    issues.push(grammarIssue(
      'warn', '循环体只有一个分号',
      '`for (...);` 表示循环体为空，后面的代码可能并不是循环的一部分。',
      '去掉分号，补上 `{ ... }` 循环体。',
      grammarIssueLine(code, emptyLoop.index)
    ));
  }

  const assignmentIf = /if\s*\([^)]*(?<![=!<>])=(?!=)[^)]*\)/.exec(code);
  if (assignmentIf) {
    issues.push(grammarIssue(
      'warn', 'if 条件里像是赋值',
      '`if (a = b)` 是赋值，不是比较；条件值会变成 b 的值。',
      '如果本意是比较，改成 `if (a == b)`。',
      grammarIssueLine(code, assignmentIf.index)
    ));
  }

  const largeArray = /\b(?:int|long\s+long|char|double)\s+\w+\s*\[\s*(\d{7,})\s*\]/.exec(code);
  if (largeArray) {
    issues.push(grammarIssue(
      'warn', '局部大数组可能爆栈',
      '函数内部的数组放在栈上， `' + largeArray[1] + '` 个元素可能超过栈空间。',
      '把大数组移到全局变量，或用 `vector` 动态分配。',
      grammarIssueLine(code, largeArray.index)
    ));
  }

  const intMul = /\bint\s+\w+\s*=\s*\w+\s*\*\s*\w+\s*;/.exec(code);
  if (intMul && !/1LL\s*\*/.test(code)) {
    issues.push(grammarIssue(
      'tip', '乘法前确认类型',
      '如果两个乘数都是 int，乘积会先按 int 计算，再赋给别的类型。',
      '需要大数时写成 `1LL * a * b`。',
      grammarIssueLine(code, intMul.index)
    ));
  }

  issues.sort((a, b) => {
    const order = { error: 0, warn: 1, tip: 2 };
    if (a.line == null && b.line != null) return 1;
    if (b.line == null && a.line != null) return -1;
    return (order[a.severity] - order[b.severity]) || ((a.line || 0) - (b.line || 0));
  });
  return issues.slice(0, 9);
}

function grammarScan() {
  const code = grammarCurrentCode();
  grammarState.scannedCode = code;
  grammarState.diagnostics = grammarDiagnose(code);
  grammarState.focusLine = null;
  if (grammar) {
    grammar.scans = (grammar.scans || 0) + 1;
    grammarSave();
  }
  grammarRender();
}

/* ---------------- 渲染 ---------------- */

function grammarCodePreview(code, diagnostics) {
  if (!code || !code.trim()) {
    return `<div class="grammar-code-empty"><b>waiting for code</b>编辑器里还没有代码。<br>先插入起手式，或写几行再回来体检。</div>`;
  }
  const lines = code.split('\n');
  const flags = new Set(diagnostics.map((d) => d.line).filter(Boolean));
  const show = lines.slice(0, 20);
  const rows = show.map((line, i) => {
    const no = i + 1;
    const flag = flags.has(no) ? ' flag' : '';
    return `<div class="grammar-code-line${flag}"><span class="num">${no}</span><span class="txt">${grammarEsc(line || ' ')}</span></div>`;
  }).join('');
  const more = lines.length > 20 ? `<div class="grammar-code-more">+ ${lines.length - 20} 行 · 在编辑器中查看完整代码</div>` : '';
  return `<div class="grammar-code-lines">${rows}${more}</div>`;
}

function grammarDiagnosticsHtml(diagnostics) {
  if (!diagnostics.length) {
    return `<div class="grammar-diag-empty"><b>体检通过</b>没有发现明显的语法风险。<br>继续写核心逻辑，赛后再回来体检一次。</div>`;
  }
  const sevLabel = { error: '错误', warn: '注意', tip: '提示' };
  const sevMark = { error: '!', warn: '!', tip: 'i' };
  return diagnostics.map((d, i) => `
    <button class="grammar-diagnostic ${d.severity}" type="button" data-g-line="${d.line || ''}" title="在编辑器中定位">
      <span class="grammar-diag-mark">${sevMark[d.severity] || 'i'}</span>
      <span class="grammar-diag-main">
        <span class="grammar-diag-title">${grammarEsc(d.title)}${d.line ? `<b>L${d.line}</b>` : ''}</span>
        <span class="grammar-diag-msg">${grammarEsc(d.message)}</span>
        <span class="grammar-diag-fix">→ ${grammarEsc(d.fix)}</span>
      </span>
    </button>`).join('') + `<div class="grammar-diags-foot"><span class="grammar-scan-status ${diagnostics.some((d) => d.severity === 'error') ? 'error' : 'warn'}">${sevLabel[diagnostics[0].severity] || '提示'}级问题 · ${diagnostics.length} 条</span></div>`;
}

function grammarHeroHtml() {
  const problem = grammarCurrentProblem();
  const stats = grammar || grammarLoad();
  const today = grammarTodayStats();
  const todayCount = today.answered || 0;
  const meter = Math.min(100, Math.round((todayCount / 3) * 100));
  const meterText = todayCount ? todayCount + '/3' : '0/3';
  return `
    <section class="grammar-hero">
      <div class="grammar-hero-copy">
        <div class="grammar-kicker">SYNTAX SERVICE STATION · 98# · C++17</div>
        <h1>语法<em>加油站</em></h1>
        <p>把卡住你的语法，拆成可以马上用的一块知识。先体检代码，再对症下药；不用离开题库。</p>
        <div class="grammar-hero-actions">
          <button class="grammar-btn primary" type="button" data-g-scan>体检当前代码</button>
          <button class="grammar-btn ghost" type="button" data-g-scroll-cards>翻开语法货架</button>
          <button class="grammar-btn" type="button" data-g-new-quiz>5 分钟小练习</button>
        </div>
        <div class="grammar-current-pill">
          <span>CURRENT PROBLEM</span>
          <b>${problem ? grammarEsc((problem.label ? problem.label + ' · ' : '') + (problem.title || problem.id)) : '自由练习 · 还没有选题'}</b>
          ${problem ? '<button type="button" data-g-open-problem>回到题目</button>' : ''}
        </div>
        <div class="grammar-hero-meta">
          <span><b>${stats.scans || 0}</b> 次体检</span>
          <span><b>${stats.drills.answered || 0}</b> 题已练</span>
          <span><b>${stats.drills.correct || 0}</b> 题答对</span>
          <span><b>${stats.copies || 0}</b> 个片段复制</span>
        </div>
      </div>
      <aside class="grammar-pass" aria-label="今日加注">
        <div class="grammar-pass-top">
          <span class="grammar-pass-label">DAILY FUEL · 今日加注</span>
          <span class="grammar-pass-mark">+</span>
        </div>
        <div class="grammar-meter" style="--meter:${meter}%">
          <div class="grammar-meter-inner"><b>${meterText}</b><small>语法值</small></div>
        </div>
        <div class="grammar-pass-foot">
          <div class="grammar-pass-stat"><span>连续答题</span><b>${stats.drills.streak || 0} DAY</b></div>
          <div class="grammar-pass-stat"><span>最佳小练</span><b>${stats.drills.best || 0} / 5</b></div>
        </div>
      </aside>
    </section>`;
}

function grammarScanHtml() {
  const code = grammarCurrentCode();
  const diagnostics = grammarState.diagnostics;
  const codeHash = code;
  if (grammarState.scannedCode !== codeHash) {
    grammarState.scannedCode = codeHash;
    grammarState.diagnostics = grammarDiagnose(code);
  }
  const issueCount = grammarState.diagnostics.length;
  const errorCount = grammarState.diagnostics.filter((d) => d.severity === 'error').length;
  const statusClass = !code.trim() ? '' : (errorCount ? 'error' : (issueCount ? 'warn' : ''));
  const statusText = !code.trim() ? '待检测' : (errorCount ? `${errorCount} 个错误` : (issueCount ? `${issueCount} 条提示` : '通过'));
  return `
    <section class="grammar-scan" id="grammarScanner">
      <header class="grammar-scan-head">
        <div class="grammar-scan-title"><i></i>CAR CHECK · 当前代码体检</div>
        <span class="grammar-scan-status ${statusClass}">${statusText}</span>
        <button class="grammar-btn subtle" type="button" data-g-scan>重新扫描</button>
      </header>
      <div class="grammar-scan-grid">
        <div class="grammar-codebox" aria-label="当前编辑器代码">${grammarCodePreview(code, grammarState.diagnostics)}</div>
        <div class="grammar-diags">
          <div class="grammar-diags-head"><span>LOCAL HEURISTICS</span><b>${issueCount ? issueCount + ' 条结果' : '0 条结果'}</b></div>
          ${grammarDiagnosticsHtml(grammarState.diagnostics)}
          ${code.trim() ? `<div class="grammar-diags-foot"><button class="grammar-btn subtle" type="button" data-g-ask>把体检结果交给 AI</button></div>` : ''}
        </div>
      </div>
    </section>`;
}

function grammarSymptomHtml() {
  const selected = grammarState.symptom;
  const symptom = GRAMMAR_SYMPTOMS.find((s) => s.key === selected);
  return `
    <section class="grammar-panel">
      <div class="grammar-panel-head"><div><span class="grammar-section-num">01 · TRIAGE</span><h3>对症下药</h3></div><span class="grammar-label">6 EMERGENCY CARDS</span></div>
      <div class="grammar-symptom-grid">
        ${GRAMMAR_SYMPTOMS.map((s) => `<button class="grammar-symptom ${selected === s.key ? 'on' : ''}" type="button" data-g-symptom="${s.key}"><span>${s.tag}</span><b>${grammarEsc(s.label)}</b><small>${grammarEsc(s.short)}</small></button>`).join('')}
      </div>
      ${symptom ? `
        <div class="grammar-triage-detail">
          <div class="grammar-triage-title"><span>${symptom.tag}</span>${grammarEsc(symptom.title)}</div>
          <p class="grammar-triage-lead">${grammarEsc(symptom.lead)}</p>
          <ul class="grammar-check-list">${symptom.checks.map((x) => `<li>${grammarEsc(x)}</li>`).join('')}</ul>
          <div class="grammar-triage-demo">
            <div class="grammar-demo bad"><span>坑 / BEFORE</span><pre>${grammarEsc(symptom.bad)}</pre></div>
            <div class="grammar-demo good"><span>修 / AFTER</span><pre>${grammarEsc(symptom.good)}</pre></div>
          </div>
          <div class="grammar-triage-actions">
            <button class="grammar-card-book" type="button" data-g-book="${symptom.book}" data-g-book-label="${grammarEsc(symptom.bookLabel)}">去原书 · ${grammarEsc(symptom.bookLabel)}</button>
            <button class="grammar-btn subtle" type="button" data-g-copy-symptom="${symptom.key}">复制修法</button>
            <button class="grammar-btn subtle" type="button" data-g-ask-symptom="${symptom.key}">请教 AI</button>
          </div>
        </div>` : ''}
    </section>`;
}

function grammarCardsHtml() {
  const selected = GRAMMAR_CARDS.find((c) => c.id === grammarState.card) || GRAMMAR_CARDS[0];
  return `
    <section class="grammar-panel" id="grammarCards">
      <div class="grammar-panel-head"><div><span class="grammar-section-num">02 · SHELF</span><h3>语法货架</h3></div><span class="grammar-label">8 QUICK CARDS</span></div>
      <div class="grammar-card-grid">
        ${GRAMMAR_CARDS.map((c) => `<button class="grammar-card ${selected.id === c.id ? 'on' : ''}" type="button" data-g-card="${c.id}"><span class="grammar-card-top"><span class="grammar-card-tag">${c.tag}</span><span class="grammar-card-icon">↗</span></span><b>${grammarEsc(c.title)}</b><small>${grammarEsc(c.summary)}</small></button>`).join('')}
      </div>
      ${selected ? `
        <div class="grammar-card-pre"><span>${selected.tag} · SNIPPET</span><pre>${grammarEsc(selected.code)}</pre></div>
        <p class="grammar-triage-lead">${grammarEsc(selected.tip)}</p>
        <div class="grammar-card-actions">
          <button class="grammar-card-book" type="button" data-g-book="${selected.book}" data-g-book-label="${grammarEsc(selected.bookLabel)}">去原书 · ${grammarEsc(selected.bookLabel)}</button>
          <button class="grammar-btn subtle" type="button" data-g-copy-card="${selected.id}">复制片段</button>
          <button class="grammar-btn subtle" type="button" data-g-ask-card="${selected.id}">请 AI 讲这张卡</button>
        </div>` : ''}
    </section>`;
}

function grammarQuizHtml() {
  if (!grammarState.quiz) grammarNewQuiz();
  const quiz = grammarState.quiz || [];
  const index = grammarState.quizIndex || 0;
  const q = quiz[index];
  const selected = grammarState.quizSelected;
  const done = grammarState.quizDone;
  const result = grammarState.quizResult || [];
  const correctCount = result.filter(Boolean).length;
  const dots = quiz.map((_, i) => {
    const answered = i < result.length;
    return `<i class="${answered ? 'on' : ''} ${i === index && !done ? 'now' : ''}"></i>`;
  }).join('');
  let body = '';
  if (done) {
    const message = correctCount >= 5 ? '语法值拉满，今天可以下班。' : (correctCount >= 4 ? '很稳，只差一个边角。' : (correctCount >= 3 ? '基础在线，错题值得再看一眼。' : '别急，把这几张卡翻回来看一遍。'));
    body = `<div class="grammar-quiz-complete"><div class="grammar-quiz-complete-mark">${correctCount >= 4 ? '✦' : '◷'}</div><h4>${correctCount} / ${quiz.length} 答对</h4><p>${message}<br>本轮记录已留在本机，下一组会换题。</p><button class="grammar-btn primary" type="button" data-g-new-quiz>再来一组</button><button class="grammar-btn ghost" type="button" data-g-scroll-cards>翻语法货架</button></div>`;
  } else if (q) {
    const feedback = selected >= 0 ? `<div class="grammar-quiz-feedback ${selected === q.answer ? '' : 'wrong'}"><b>${selected === q.answer ? '✓ 正确' : '× 再看一眼'}</b><span>${grammarEsc(q.why)}</span></div>` : '';
    body = `
      <div class="grammar-quiz-kicker">QUESTION <b>${String(index + 1).padStart(2, '0')}</b> / ${String(quiz.length).padStart(2, '0')} · 本地题库</div>
      <div class="grammar-quiz-q">${grammarEsc(q.q)}</div>
      ${q.code ? `<pre class="grammar-quiz-code">${grammarEsc(q.code)}</pre>` : ''}
      <div class="grammar-options">
        ${q.options.map((opt, i) => {
          let cls = '';
          if (selected >= 0) {
            if (i === q.answer) cls = 'correct';
            else if (i === selected) cls = 'wrong';
          }
          return `<button class="grammar-option ${cls}" type="button" data-g-answer="${i}" ${selected >= 0 ? 'disabled' : ''}><b>${String.fromCharCode(65 + i)}</b><span>${grammarEsc(opt)}</span></button>`;
        }).join('')}
      </div>
      ${feedback}
      <div class="grammar-quiz-foot"><span class="grammar-quiz-hint">${selected >= 0 ? '看完解析再进入下一题' : '选一个答案，答错也会告诉你为什么'}</span><button class="grammar-btn primary" type="button" data-g-next ${selected < 0 ? 'disabled' : ''}>${index >= quiz.length - 1 ? '看本轮结果' : '下一题'} →</button></div>`;
  }
  return `
    <section class="grammar-drill" id="grammarDrill">
      <aside class="grammar-drill-side"><span class="grammar-label">5 MIN DRILL</span><h3>小练习</h3><p>不用等一整道题。<br>一次只修一个语法点。</p><div class="grammar-drill-score"><b>${correctCount}</b><span>/ ${quiz.length || 5}</span></div><div class="grammar-progress-dots">${dots}</div></aside>
      <div class="grammar-drill-main">${body}</div>
    </section>`;
}

function grammarRender() {
  const ws = document.getElementById('grammarWorkspace');
  if (!ws) return;
  if (!grammar) grammar = grammarLoad();
  if (!grammarState.quiz) grammarNewQuiz();
  const keep = ws.scrollTop;
  ws.innerHTML = `<div class="grammar-shell">
    ${grammarHeroHtml()}
    <div class="grammar-section-head"><div class="grammar-section-head-copy"><span class="grammar-section-num">00 · DIAGNOSTIC BAY</span><h2>先给代码做个体检</h2><p>只在本机做静态检查，不会上传代码；点结果可直接跳回编辑器对应行。</p></div><span class="grammar-head-note">LOCAL ONLY · NO API KEY NEEDED</span></div>
    ${grammarScanHtml()}
    <div class="grammar-columns">${grammarSymptomHtml()}${grammarCardsHtml()}</div>
    ${grammarQuizHtml()}
    <div class="grammar-footnote"><span>本地 OJ · 从语法到算法</span><i class="dot"></i><span>语法加油站不生成新题、不修改题库</span><i class="dot"></i><span>记录保存在 <b>localStorage['oj.grammar.v1']</b></span></div>
  </div>`;
  ws.scrollTop = keep;
}

/* ---------------- 小练习 ---------------- */

function grammarNewQuiz() {
  const pool = GRAMMAR_QUIZ.slice().sort(() => Math.random() - 0.5).slice(0, 5);
  grammarState.quiz = pool;
  grammarState.quizIndex = 0;
  grammarState.quizSelected = -1;
  grammarState.quizDone = false;
  grammarState.quizResult = [];
  grammarState.setCounted = false;
}

function grammarAnswer(option) {
  if (!grammarState.quiz || grammarState.quizSelected >= 0 || grammarState.quizDone) return;
  const q = grammarState.quiz[grammarState.quizIndex];
  if (!q) return;
  grammarState.quizSelected = option;
  const correct = option === q.answer;
  grammarState.quizResult.push(correct);
  grammarRecordAnswer(correct);
  grammarRender();
}

function grammarNext() {
  if (!grammarState.quiz || grammarState.quizSelected < 0) return;
  if (grammarState.quizIndex >= grammarState.quiz.length - 1) {
    grammarState.quizDone = true;
    if (grammar && !grammarState.setCounted) {
      grammar.drills.sets = (grammar.drills.sets || 0) + 1;
      const correct = grammarState.quizResult.filter(Boolean).length;
      grammar.drills.best = Math.max(grammar.drills.best || 0, correct);
      grammarSave();
      grammarState.setCounted = true;
    }
  } else {
    grammarState.quizIndex += 1;
    grammarState.quizSelected = -1;
  }
  grammarRender();
}

/* ---------------- 操作 / AI / 原书 ---------------- */

function grammarToast(message) {
  if (typeof toast === 'function') toast(message);
}

function grammarCopy(text, label) {
  const done = () => {
    if (grammar) { grammar.copies = (grammar.copies || 0) + 1; grammarSave(); }
    grammarToast((label || '片段') + '已复制');
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => grammarCopyFallback(text, done));
  } else {
    grammarCopyFallback(text, done);
  }
}

function grammarCopyFallback(text, done) {
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    const copied = document.execCommand('copy');
    ta.remove();
    if (copied) done();
    else grammarToast('当前浏览器不允许复制，请手动选中代码');
  } catch (e) {
    grammarToast('当前浏览器不允许复制，请手动选中代码');
  }
}

function grammarScrollTo(selector) {
  setTimeout(() => {
    const target = document.querySelector(selector);
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 30);
}

function grammarOpenProblem() {
  const p = grammarCurrentProblem();
  if (!p) { grammarToast('还没有选中题目'); return; }
  if (typeof setView === 'function') setView('oj');
  if (typeof selectProblem === 'function') selectProblem(p.id, false);
}

function grammarJumpLine(line) {
  if (!line) return;
  const ed = document.getElementById('code');
  if (!ed) return;
  const lines = ed.value.split('\n');
  const target = Math.max(0, Math.min(lines.length - 1, line - 1) );
  let pos = 0;
  for (let i = 0; i < target; i++) pos += lines[i].length + 1;
  const end = pos + (lines[target] || '').length;
  if (typeof editorSetValue === 'function') editorSetValue(ed.value, pos, end);
  if (typeof setView === 'function') setView('oj');
  setTimeout(() => { ed.focus(); ed.setSelectionRange(pos, end); }, 30);
  grammarToast('已在编辑器定位到 L' + line);
}

function grammarOpenBook(section, label) {
  if (!section) return;
  if (typeof openBook !== 'function') { grammarToast('原书阅读器还没准备好'); return; }
  grammarToast('正在打开原书 · ' + (label || section));
  openBook(section, label || '').catch(() => grammarToast('没有找到对应章节'));
}

function grammarPromptForScan() {
  const p = grammarCurrentProblem();
  const code = grammarCurrentCode();
  const diags = grammarState.diagnostics.length ? grammarState.diagnostics.map((d, i) => `${i + 1}. ${d.title}${d.line ? '（L' + d.line + '）' : ''}：${d.message} 建议：${d.fix}`).join('\n') : '本地体检未发现明显问题。';
  return `你是我的 C++ 语法教练。先不要重写整份代码，请只按下面这份本地体检结果，帮我判断哪些是真正需要改的，并给出最小修改。\n\n题目：${p ? (p.label ? p.label + ' · ' : '') + p.title : '未选题'}\n\n本地体检结果：\n${diags}\n\n当前代码：\n\`\`\`cpp\n${code}\n\`\`\`\n\n输出：优先讲最严重的 1～2 条；每条给出原因、具体改哪一行、改完怎么验证。`;
}

function grammarAskAI(prompt) {
  if (typeof aiSetMode === 'function') aiSetMode('debug');
  if (typeof aiOpen === 'function') aiOpen();
  const input = document.getElementById('aiInput');
  if (input) {
    input.value = prompt;
    input.focus();
  }
  grammarToast('问题已放进 AI 助手，点发送即可');
}

function grammarAskScan() {
  grammarAskAI(grammarPromptForScan());
}

function grammarAskSymptom(key) {
  const s = GRAMMAR_SYMPTOMS.find((x) => x.key === key);
  if (!s) return;
  grammarAskAI(`你是我的 C++ 语法教练。请只针对「${s.label}」这个症状帮我排查当前题目和代码，不要先给完整答案。\n\n题目：${grammarCurrentProblem() ? grammarCurrentProblem().title : '未选题'}\n\n症状：${s.lead}\n\n当前代码：\n\`\`\`cpp\n${grammarCurrentCode() || '（编辑器还没有代码）'}\n\`\`\`\n\n请按“先检查什么 → 最容易错在哪里 → 最小验证方法”的顺序回答。`);
}

function grammarAskCard(id) {
  const c = GRAMMAR_CARDS.find((x) => x.id === id);
  if (!c) return;
  grammarAskAI(`请用最少的例子，给我讲清楚这张 C++ 语法卡：「${c.title}」。\n\n卡片说明：${c.summary}\n\n示例代码：\n\`\`\`cpp\n${c.code}\n\`\`\`\n\n请先讲它解决的问题，再讲一个最容易踩的坑，最后给一个 2 分钟能做的练习。不要重写我当前的题目代码。`);
}

/* ---------------- 事件绑定 ---------------- */

function grammarBind() {
  const ws = document.getElementById('grammarWorkspace');
  if (!ws || ws.dataset.bound === '1') return;
  ws.dataset.bound = '1';
  ws.addEventListener('click', (e) => {
    const target = e.target.closest('[data-g-scan],[data-g-symptom],[data-g-card],[data-g-copy-card],[data-g-copy-symptom],[data-g-ask],[data-g-ask-symptom],[data-g-ask-card],[data-g-book],[data-g-open-problem],[data-g-answer],[data-g-next],[data-g-new-quiz],[data-g-scroll-cards],[data-g-line]');
    if (!target) return;
    if (target.dataset.gScan !== undefined) { grammarScan(); return; }
    if (target.dataset.gSymptom) { grammarState.symptom = target.dataset.gSymptom; grammarRender(); return; }
    if (target.dataset.gCard) { grammarState.card = target.dataset.gCard; grammarRender(); return; }
    if (target.dataset.gCopyCard) {
      const c = GRAMMAR_CARDS.find((x) => x.id === target.dataset.gCopyCard);
      if (c) grammarCopy(c.code, '语法卡');
      return;
    }
    if (target.dataset.gCopySymptom) {
      const s = GRAMMAR_SYMPTOMS.find((x) => x.key === target.dataset.gCopySymptom);
      if (s) grammarCopy(s.good, '修法');
      return;
    }
    if (target.dataset.gAsk !== undefined) { grammarAskScan(); return; }
    if (target.dataset.gAskSymptom) { grammarAskSymptom(target.dataset.gAskSymptom); return; }
    if (target.dataset.gAskCard) { grammarAskCard(target.dataset.gAskCard); return; }
    if (target.dataset.gLine) { grammarJumpLine(Number(target.dataset.gLine)); return; }
    if (target.dataset.gBook) { grammarOpenBook(target.dataset.gBook, target.dataset.gBookLabel || ''); return; }
    if (target.dataset.gOpenProblem !== undefined) { grammarOpenProblem(); return; }
    if (target.dataset.gAnswer !== undefined) { grammarAnswer(Number(target.dataset.gAnswer)); return; }
    if (target.dataset.gNext !== undefined) { grammarNext(); return; }
    if (target.dataset.gNewQuiz !== undefined) { grammarNewQuiz(); grammarRender(); grammarScrollTo('#grammarDrill'); return; }
    if (target.dataset.gScrollCards !== undefined) {
      const cards = document.getElementById('grammarCards');
      if (cards) cards.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
  });
}

function grammarBoot() {
  grammar = grammarLoad();
  grammar.visits = (grammar.visits || 0) + 1;
  if (!grammar.daily || grammar.daily.date !== grammarToday()) {
    grammar.daily = { date: grammarToday(), answered: 0, correct: 0 };
  }
  grammarSave();
  if (!grammarState.quiz) grammarNewQuiz();
  grammarBind();
  grammarRender();
}

function grammarAfterData() {
  if (!grammar) grammar = grammarLoad();
  if (typeof currentView !== 'undefined' && currentView === 'grammar') grammarRender();
}

grammarBoot();

/* app.js 的题库加载可能晚于本文件；数据到位后再补一次上下文。 */
setTimeout(() => {
  if (typeof state !== 'undefined' && state.problems && state.problems.length) grammarAfterData();
}, 1200);
