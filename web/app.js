'use strict';

const TEMPLATE = `#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 在这里写你的代码

    return 0;
}
`;

const state = {
  problems: [],
  byId: {},
  progress: {},
  filter: 'all',
  q: '',
  sort: 'chapter',
  current: null,
  open: {},
  busy: false,
  lastResult: null,
  stars: new Set(),
};

const $ = (id) => document.getElementById(id);

let currentView = 'oj';
let bookSelText = '';
let aiBookQuote = null;
const bookState = { manifest: null, section: null, cache: {}, loading: null };
const statsState = { items: [], loading: false, loaded: false, filter: 'all', dateFilter: '' };
const submissionState = { current: null };
const historyState = { pid: '', items: [] };

/* ---- 冒险等级：本地持久化，首次 AC 得经验，不因重复提交刷经验 ---- */
const RPG_KEY = 'oj.rpg.v1';
const RPG_MAX_LEVEL = 40;
const RPG_DIFF_XP = { 1: 20, 2: 35, 3: 55, 4: 85, 5: 130 };
const RPG_RANKS = [
  { level: 1, title: '初入算法谷', subtitle: '从第一道 AC 开始，沿着书页往前走。' },
  { level: 5, title: '代码学徒', subtitle: '开始把书上的语法变成自己的解法。' },
  { level: 10, title: '数据结构行者', subtitle: '数组、栈、队列、树，你能看见它们的形状。' },
  { level: 15, title: '算法骑士', subtitle: '贪心、二分、DP，开始组合招式。' },
  { level: 20, title: '竞赛游侠', subtitle: '面对陌生题面，也能自己搭出模型。' },
  { level: 25, title: '算法大师', subtitle: '能讲清楚为什么，而不只是写出答案。' },
  { level: 30, title: '传奇选手', subtitle: '题库里留下了一条属于你的轨迹。' },
  { level: 40, title: '算法传说', subtitle: '等级已满，但算法之路没有终点。' },
];
let rpg = null;

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ---- 轻量 LaTeX：题面和 AI 回复里的 $...$ 不再原样露出反斜杠 ---- */
const TEX_SYMBOLS = {
  le: '≤', ge: '≥', lt: '&lt;', gt: '&gt;', ne: '≠', neq: '≠', equiv: '≡',
  approx: '≈', sim: '∼', propto: '∝', in: '∈', notin: '∉', ni: '∋',
  subset: '⊂', subseteq: '⊆', supset: '⊃', supseteq: '⊇',
  cup: '∪', cap: '∩', setminus: '∖', emptyset: '∅', varnothing: '∅',
  times: '×', div: '÷', cdot: '·', pm: '±', mp: '∓', ast: '∗',
  to: '→', rightarrow: '→', leftarrow: '←', Rightarrow: '⇒', Leftarrow: '⇐',
  leftrightarrow: '↔', iff: '⇔', therefore: '∴', because: '∵',
  dots: '…', ldots: '…', cdots: '⋯', vdots: '⋮', ddots: '⋱', infty: '∞',
  forall: '∀', exists: '∃', nexists: '∄', neg: '¬', land: '∧', lor: '∨',
  sum: '∑', prod: '∏', int: '∫', oint: '∮', partial: '∂', nabla: '∇',
  lceil: '⌈', rceil: '⌉', lfloor: '⌊', rfloor: '⌋', langle: '⟨', rangle: '⟩',
  mid: '|', vert: '|', Vert: '‖', backslash: '\\', percent: '%',
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε', varepsilon: 'ε',
  zeta: 'ζ', eta: 'η', theta: 'θ', vartheta: 'ϑ', iota: 'ι', kappa: 'κ',
  lambda: 'λ', mu: 'μ', nu: 'ν', xi: 'ξ', pi: 'π', varpi: 'ϖ', rho: 'ρ',
  sigma: 'σ', varsigma: 'ς', tau: 'τ', upsilon: 'υ', phi: 'φ', varphi: 'ϕ',
  chi: 'χ', psi: 'ψ', omega: 'ω',
  Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ', Xi: 'Ξ', Pi: 'Π',
  Sigma: 'Σ', Upsilon: 'Υ', Phi: 'Φ', Psi: 'Ψ', Omega: 'Ω',
  quad: ' ', qquad: ' ', space: ' ', nbsp: ' ',
};

function texGroup(src, start) {
  if (src[start] !== '{') return null;
  let depth = 0;
  for (let i = start; i < src.length; i++) {
    if (src[i] === '{' && (i === 0 || src[i - 1] !== '\\')) depth += 1;
    else if (src[i] === '}' && (i === 0 || src[i - 1] !== '\\')) {
      depth -= 1;
      if (depth === 0) return { inner: src.slice(start + 1, i), next: i + 1 };
    }
  }
  return { inner: src.slice(start + 1), next: src.length };
}

function texReadAtom(src, start) {
  if (src[start] === '{') {
    const g = texGroup(src, start);
    return g ? { html: texToHtml(g.inner), next: g.next } : { html: '', next: start + 1 };
  }
  if (src[start] === '\\') {
    const m = /^\\([A-Za-z]+|.)/.exec(src.slice(start));
    if (m) {
      const name = m[1];
      if (TEX_SYMBOLS[name]) return { html: TEX_SYMBOLS[name], next: start + m[0].length };
      if (name === ' ') return { html: '&nbsp;', next: start + 2 };
      return { html: name, next: start + m[0].length };
    }
  }
  return { html: src[start] || '', next: start + 1 };
}

function texToHtml(src) {
  let out = '';
  let i = 0;
  while (i < src.length) {
    const ch = src[i];
    if (ch === '\\') {
      const m = /^\\([A-Za-z]+|.)/.exec(src.slice(i));
      if (!m) { out += '\\'; i += 1; continue; }
      const name = m[1];
      let next = i + m[0].length;
      if (name === 'frac' || name === 'dfrac' || name === 'tfrac') {
        const a = texGroup(src, next);
        if (a) {
          const b = texGroup(src, a.next);
          if (b) {
            out += `<span class="math-frac"><span class="math-num">${texToHtml(a.inner)}</span><span class="math-den">${texToHtml(b.inner)}</span></span>`;
            i = b.next;
            continue;
          }
        }
      }
      if (name === 'sqrt') {
        let rootAt = next;
        let rootIndex = '';
        if (src[rootAt] === '[') {
          const close = src.indexOf(']', rootAt + 1);
          if (close > rootAt) {
            rootIndex = src.slice(rootAt + 1, close);
            rootAt = close + 1;
          }
        }
        const g = texGroup(src, rootAt);
        if (g) {
          const prefix = rootIndex ? `<sup>${texToHtml(rootIndex)}</sup>` : '';
          out += `<span class="math-sqrt">${prefix}√<span class="math-rad">${texToHtml(g.inner)}</span></span>`;
          i = g.next;
          continue;
        }
      }
      if (['text', 'textrm', 'mathrm', 'mathbf', 'mathit', 'operatorname', 'mbox'].includes(name)) {
        const g = texGroup(src, next);
        if (g) { out += `<span class="math-text">${g.inner}</span>`; i = g.next; continue; }
      }
      if (name === 'left' || name === 'right') {
        // \left( / \right) 只保留后面的括号本身
        i = next;
        continue;
      }
      if (name === 'begin' || name === 'end') {
        const g = texGroup(src, next);
        if (g) { i = g.next; continue; }
      }
      if (name === '\\' || name === 'newline' || name === 'cr') {
        out += '<br>'; i = next; continue;
      }
      if (name === 'overline') {
        const g = texGroup(src, next);
        if (g) { out += `<span class="math-overline">${texToHtml(g.inner)}</span>`; i = g.next; continue; }
      }
      if (TEX_SYMBOLS[name]) { out += TEX_SYMBOLS[name]; i = next; continue; }
      if (name === ' ' || name === 'quad' || name === 'qquad') { out += ' '; i = next; continue; }
      // 未知命令去掉反斜杠，至少不把 \foo 原样露给读者
      out += /^[A-Za-z]+$/.test(name) ? name : name;
      i = next;
      continue;
    }
    if (ch === '^' || ch === '_') {
      const atom = texReadAtom(src, i + 1);
      out += `<${ch === '^' ? 'sup' : 'sub'}>${atom.html}</${ch === '^' ? 'sup' : 'sub'}>`;
      i = atom.next;
      continue;
    }
    if (ch === '{') {
      const g = texGroup(src, i);
      if (g) { out += texToHtml(g.inner); i = g.next; continue; }
    }
    if (ch === '}') { i += 1; continue; }
    out += ch;
    i += 1;
  }
  return out;
}

function mathifyHtml(html) {
  // 先处理 $$...$$，再处理行内 $...$、\(...\)、\[...\]。
  let t = String(html || '');
  t = t.replace(/\$\$([\s\S]*?)\$\$/g, (m, x) => `<div class="math-block">${texToHtml(x)}</div>`);
  t = t.replace(/\\\[([\s\S]*?)\\\]/g, (m, x) => `<div class="math-block">${texToHtml(x)}</div>`);
  t = t.replace(/\\\(([\s\S]*?)\\\)/g, (m, x) => `<span class="math-inline">${texToHtml(x)}</span>`);
  t = t.replace(/\$([^$\n]+)\$/g, (m, x) => `<span class="math-inline">${texToHtml(x)}</span>`);
  return t;
}

function inlineFmt(s) {
  let t = esc(s);
  const codes = [];
  // 先保护行内代码，避免代码里的 $ 被当公式。
  t = t.replace(/`([^`]+)`/g, (m, code) => {
    const token = `\u0001C${codes.length}\u0001`;
    codes.push(code);
    return token;
  });
  t = mathifyHtml(t);
  t = t.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
  t = t.replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  t = t.replace(/\u0001C(\d+)\u0001/g, (m, i) => `<code class="inline">${codes[Number(i)] || ''}</code>`);
  return t;
}

/* 极简 Markdown 渲染：够用于本书题面（段落、列表、代码块、粗体、行内代码、表格、引用） */
function mdToHtml(md) {
  const lines = String(md || '').replace(/\r/g, '').split('\n');
  let html = '';
  let i = 0;
  let list = null;
  let listStart = 0;

  const closeList = () => { if (list) { html += `</${list}>`; list = null; listStart = 0; } };

  while (i < lines.length) {
    let line = lines[i];

    if (/^```/.test(line)) {
      closeList();
      const lang = (line.match(/^```([A-Za-z0-9_+-]*)/) || [])[1] || '';
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++;
      html += `<pre data-lang="${esc(lang)}">${esc(buf.join('\n'))}</pre>`;
      continue;
    }

    if (!line.trim()) { closeList(); i++; continue; }

    const mathLine = line.trim();
    const blockMath = mathLine.match(/^\$\$([\s\S]+)\$\$$/) || mathLine.match(/^\\\[([\s\S]+)\\\]$/);
    if (blockMath) {
      closeList();
      html += `<div class="math-block">${texToHtml(esc(blockMath[1].trim()))}</div>`;
      i++;
      continue;
    }

    const hm = line.match(/^(#{2,4})\s+(.*)$/);
    if (hm) {
      closeList();
      const lv = hm[1].length >= 4 ? 4 : 3;
      html += `<h${lv}>${inlineFmt(hm[2])}</h${lv}>`;
      i++;
      continue;
    }

    if (/^>\s?/.test(line)) {
      closeList();
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^>\s?/, ''));
        i++;
      }
      html += `<blockquote>${inlineFmt(buf.join(' '))}</blockquote>`;
      continue;
    }

    // 表格
    if (/^\|/.test(line) && i + 1 < lines.length && /^\|[\s:|-]+\|$/.test(lines[i + 1].trim())) {
      closeList();
      const head = line.split('|').slice(1, -1).map((x) => inlineFmt(x.trim()));
      i += 2;
      const rows = [];
      while (i < lines.length && /^\|/.test(lines[i])) {
        rows.push(lines[i].split('|').slice(1, -1).map((x) => inlineFmt(x.trim())));
        i++;
      }
      html += `<table><thead><tr>${head.map((x) => `<th>${x}</th>`).join('')}</tr></thead><tbody>`;
      html += rows.map((r) => `<tr>${r.map((x) => `<td>${x}</td>`).join('')}</tr>`).join('');
      html += '</tbody></table>';
      continue;
    }

    if (/^(\s*)([-*]|\d+\.)\s+/.test(line)) {
      const ordered = /^\s*\d+\./.test(line);
      const tag = ordered ? 'ol' : 'ul';
      const num = ordered ? Number((line.match(/^\s*(\d+)\./) || [0, 1])[1]) : 0;
      if (list !== tag) {
        closeList();
        html += `<${tag} class="book-list"${ordered && num !== 1 ? ` start="${num}"` : ''}>`;
        list = tag;
        listStart = num;
      }
      html += `<li${ordered ? ` data-num="${num}"` : ''}>${inlineFmt(line.replace(/^(\s*)([-*]|\d+\.)\s+/, ''))}</li>`;
      if (ordered) listStart = num + 1;
      i++;
      continue;
    }

    closeList();
    const buf = [line];
    i++;
    while (i < lines.length && lines[i].trim() && !/^\s*```|^#{1,4}\s|^>\s?|^\|/.test(lines[i])
      && !/^(\s*)([-*]|\d+\.)\s+/.test(lines[i])) {
      buf.push(lines[i]);
      i++;
    }
    html += `<p>${inlineFmt(buf.join('\n')).replace(/\n/g, '<br>')}</p>`;
  }
  closeList();
  return html;
}

/* 原书阅读器专用 Markdown：保留章节层级、代码文件名、插图和表格 */
function bookAssetUrl(src) {
  const s = String(src || '').trim();
  if (/^(https?:|data:|#)/.test(s)) return s;
  if (s.startsWith('assets/')) return '/book/' + s;
  return '/book/assets/' + s.replace(/^\.?\//, '');
}

function bookInline(s) {
  let t = esc(s);
  const codes = [];
  t = t.replace(/`([^`]+)`/g, (m, code) => {
    const token = `\u0001B${codes.length}\u0001`;
    codes.push(code);
    return token;
  });
  t = mathifyHtml(t);
  t = t.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
  t = t.replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  t = t.replace(/\*([^*]+)\*/g, '<i>$1</i>');
  t = t.replace(/\u0001B(\d+)\u0001/g, (m, i) => `<code class="inline">${codes[Number(i)] || ''}</code>`);
  return t;
}

function bookMdToHtml(md) {
  const lines = String(md || '').replace(/\r/g, '').split('\n');
  let html = '';
  let i = 0;
  let list = null;
  let listStart = 0;
  let headingIndex = 0;

  const closeList = () => { if (list) { html += `</${list}>`; list = null; listStart = 0; } };

  while (i < lines.length) {
    let line = lines[i];

    if (/^\s*```/.test(line)) {
      closeList();
      const info = line.trim().slice(3).trim();
      const colon = info.indexOf(':');
      const lang = colon >= 0 ? info.slice(0, colon) : info;
      const title = colon >= 0 ? info.slice(colon + 1).trim() : '';
      const buf = [];
      i++;
      while (i < lines.length && !/^\s*```\s*$/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++;
      const indents = buf.filter((x) => x.trim()).map((x) => (x.match(/^(\s*)/) || ['', ''])[1].length);
      const cut = indents.length ? Math.min(...indents) : 0;
      const code = buf.map((x) => x.slice(cut)).join('\n');
      html += '<div class="book-code">' +
        '<div class="book-code-head"><span class="book-code-dot"></span><span class="book-code-title">' +
        esc(title || (lang ? lang.toUpperCase() : 'CODE')) +
        '</span><button class="book-code-copy" type="button">复制</button></div>' +
        `<pre data-lang="${esc(lang)}">${esc(code)}</pre></div>`;
      continue;
    }

    if (/^!\[/.test(line.trim())) {
      closeList();
      const m = line.trim().match(/^!\[([^\]]*)\]\(([^)]+)\)/);
      if (m) {
        html += `<figure class="book-figure"><img src="${esc(bookAssetUrl(m[2]))}" alt="${esc(m[1])}" loading="lazy">` +
          `<figcaption>${esc(m[1])}</figcaption></figure>`;
        i++;
        continue;
      }
    }

    if (!line.trim()) { closeList(); i++; continue; }

    const bookMathLine = line.trim();
    const bookBlockMath = bookMathLine.match(/^\$\$([\s\S]+)\$\$$/) || bookMathLine.match(/^\\\[([\s\S]+)\\\]$/);
    if (bookBlockMath) {
      closeList();
      html += `<div class="math-block">${texToHtml(esc(bookBlockMath[1].trim()))}</div>`;
      i++;
      continue;
    }

    const hm = line.match(/^(#{1,4})\s+(.*)$/);
    if (hm) {
      closeList();
      headingIndex++;
      const lv = hm[1].length;
      html += `<h${lv} id="book-h-${headingIndex}" class="book-h book-h${lv}">${bookInline(hm[2])}</h${lv}>`;
      i++;
      continue;
    }

    if (/^>\s?/.test(line)) {
      closeList();
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^>\s?/, ''));
        i++;
      }
      html += `<blockquote class="book-quote">${bookInline(buf.join('\n')).replace(/\n/g, '<br>')}</blockquote>`;
      continue;
    }

    if (/^\|/.test(line) && i + 1 < lines.length && /^\|[\s:|-]+\|$/.test(lines[i + 1].trim())) {
      closeList();
      const head = line.split('|').slice(1, -1).map((x) => bookInline(x.trim()));
      i += 2;
      const rows = [];
      while (i < lines.length && /^\|/.test(lines[i])) {
        rows.push(lines[i].split('|').slice(1, -1).map((x) => bookInline(x.trim())));
        i++;
      }
      html += `<div class="book-table-wrap"><table><thead><tr>${head.map((x) => `<th>${x}</th>`).join('')}</tr></thead><tbody>` +
        rows.map((r) => `<tr>${r.map((x) => `<td>${x}</td>`).join('')}</tr>`).join('') +
        '</tbody></table></div>';
      continue;
    }

    if (/^(\s*)([-*]|\d+\.)\s+/.test(line)) {
      const ordered = /^\s*\d+\./.test(line);
      const tag = ordered ? 'ol' : 'ul';
      const num = ordered ? Number((line.match(/^\s*(\d+)\./) || [0, 1])[1]) : 0;
      if (list !== tag) {
        closeList();
        html += `<${tag} class="book-list"${ordered && num !== 1 ? ` start="${num}"` : ''}>`;
        list = tag;
        listStart = num;
      }
      html += `<li${ordered ? ` data-num="${num}"` : ''}>${bookInline(line.replace(/^(\s*)([-*]|\d+\.)\s+/, ''))}</li>`;
      if (ordered) listStart = num + 1;
      i++;
      continue;
    }

    if (/^---+$/.test(line.trim())) { closeList(); html += '<div class="book-rule"></div>'; i++; continue; }

    closeList();
    const buf = [line];
    i++;
    while (i < lines.length && lines[i].trim() && !/^\s*```|^#{1,4}\s|^>\s?|^\|/.test(lines[i])
      && !/^!\[/.test(lines[i].trim())
      && !/^(\s*)([-*]|\d+\.)\s+/.test(lines[i])) {
      buf.push(lines[i]);
      i++;
    }
    html += `<p>${bookInline(buf.join('\n')).replace(/\n/g, '<br>')}</p>`;
  }
  closeList();
  return html;
}

function bindBookCodeCopy() {
  document.querySelectorAll('#bookContent .book-code-copy').forEach((btn) => {
    btn.onclick = () => {
      const pre = btn.closest('.book-code').querySelector('pre');
      aiCopyText(pre.textContent, '代码已复制');
    };
  });
}

/* ================= 每章 HTML 导学卡 / 思维导图 ================= */
function bookPlain(s) {
  return String(s || '')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/[*_~]/g, '')
    .replace(/<[^>]+>/g, '')
    .replace(/^[>\-*|]+\s*/, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function bookClip(s, n) {
  const t = String(s || '').replace(/\s+/g, ' ').trim();
  return t.length > n ? t.slice(0, Math.max(1, n - 1)) + '…' : t;
}

function bookGuideModel(md) {
  const lines = String(md || '').replace(/\r/g, '').split('\n');
  const sections = [];
  const traps = [];
  const trapSeen = new Set();
  const trapWord = /易错|陷阱|坑|注意|别把|不要|WA|RE|TLE|溢出|越界|边界|取模|初始化|long long/;
  let inCode = false;
  let cur = null;
  let intro = '';

  for (const raw of lines) {
    const line = raw.trim();
    if (/^\s*```/.test(line)) { inCode = !inCode; continue; }
    if (inCode) continue;
    const h2 = line.match(/^##\s+(.*)$/);
    const h3 = line.match(/^###\s+(.*)$/);
    if (h2) {
      const title = bookPlain(h2[1]);
      if (/^(本章小结|小结|习题)$/.test(title)) { cur = null; continue; }
      cur = { title, subs: [], summary: '' };
      sections.push(cur);
      continue;
    }
    if (h3) {
      if (cur) cur.subs.push(bookPlain(h3[1]));
      continue;
    }
    if (!line) continue;
    const plain = bookPlain(line.replace(/^[-*]\s+/, ''));
    if (!plain) continue;
    if (!intro && !cur) intro = plain;
    if (cur && !cur.summary && !/^\|/.test(line) && !/^\d+\.\s/.test(line)) cur.summary = plain;

    if (plain.length >= 16) {
      for (const part of plain.split(/[。；]/)) {
        const s = part.trim();
        if (s.length < 16 || s.length > 110 || !trapWord.test(s) || trapSeen.has(s)) continue;
        trapSeen.add(s);
        traps.push({ text: s, score: /易错|陷阱|坑|溢出|越界|WA|RE|TLE/.test(s) ? 2 : 1 });
      }
    }
  }

  const picked = traps.sort((a, b) => b.score - a.score).slice(0, 6).map((x) => x.text);
  if (!sections.length) {
    sections.push({ title: '本章速览', subs: [], summary: intro || '打开正文开始阅读。' });
  }
  const cleanSections = sections.map((s) => ({
    ...s,
    summary: s.summary ? bookClip(s.summary, 150) : '',
  }));
  return {
    intro: intro ? bookClip(intro, 120) : (cleanSections[0].summary || ''),
    sections: cleanSections,
    traps: picked,
  };
}

function bookGuideHtml(section, model) {
  const colors = ['#0071e3', '#7a5af8', '#0aa06e', '#df8a00', '#df4f72', '#4f6ef7', '#0a9aa8', '#b45ad6'];
  const branches = model.sections.slice(0, 8);
  const extra = model.sections.length - branches.length;
  const subCount = branches.reduce((n, s) => n + s.subs.length, 0);
  const intro = model.intro || '这一章先看导图，再进入正文。';
  const branchHtml = branches.map((s, i) => {
    const kids = s.subs.slice(0, 4);
    return `<div class="mm-branch" style="--c:${colors[i % colors.length]}" data-goto="${esc(s.title)}">
      <div class="mm-branch-head"><span class="mm-index">${String(i + 1).padStart(2, '0')}</span>
      <span class="mm-title">${esc(bookClip(s.title, 27))}</span></div>
      <div class="mm-subs">${kids.length
        ? kids.map((x) => `<button type="button" data-goto="${esc(x)}">${esc(bookClip(x, 18))}</button>`).join('')
        : `<span class="mm-empty">${esc(bookClip(s.summary || '看正文这一节', 28))}</span>`}</div>
    </div>`;
  }).join('') + (extra > 0 ? `<div class="mm-branch mm-more"><div class="mm-branch-head"><span class="mm-index">+</span>
      <span class="mm-title">还有 ${extra} 节</span></div><span class="mm-empty">用左侧目录继续展开</span></div>` : '');

  const route = branches.map((s, i) => `<details class="guide-route-item"${i === 0 ? ' open' : ''}>
    <summary><span class="guide-route-num">${String(i + 1).padStart(2, '0')}</span><b>${esc(bookClip(s.title, 42))}</b></summary>
    <p>${esc(s.summary || '这一节从正文开始读，遇到例题先自己推一遍。')}</p>
    <button type="button" data-goto="${esc(s.title)}">跳到这一节 →</button>
  </details>`).join('');

  const traps = model.traps.length
    ? model.traps.map((t, i) => `<details class="guide-trap"${i < 2 ? ' open' : ''}>
        <summary><span>!</span>易错提醒 ${String(i + 1).padStart(2, '0')}</summary>
        <p>${esc(t)}</p></details>`).join('')
    : `<div class="guide-empty">本章没有提取到明确的易错句。读例题时重点检查边界、数据范围和初始化。</div>`;

  return `<div class="book-guide-head">
    <div class="guide-mark">✦</div>
    <div class="guide-title"><span>INTERACTIVE STUDY MAP</span><h2>本章导学</h2></div>
    <div class="guide-meta">${branches.length} 个知识块 · ${subCount} 个细分节点</div>
    <button class="guide-toggle" id="bookGuideToggle" type="button">收起</button>
  </div>
  <div class="book-guide-body">
    <div class="guide-intro"><b>一句话读懂本章</b><span>${esc(intro)}</span></div>
    <div class="guide-tabs" role="tablist">
      <button class="guide-tab on" type="button" data-guide-tab="map">思维导图</button>
      <button class="guide-tab" type="button" data-guide-tab="route">学习路线</button>
      <button class="guide-tab" type="button" data-guide-tab="traps">易错提醒</button>
    </div>
    <div class="guide-panes">
      <div class="guide-pane" data-guide-pane="map">
        <div class="book-mindmap" id="bookMindmap">
          <svg class="mm-lines" id="bookMindLines" aria-hidden="true"></svg>
          <div class="mm-root"><small>${esc(section.kind === 'chapter' ? 'CHAPTER ' + bookSectionNumber(section) : (section.kind === 'appendix' ? 'APPENDIX ' + (section.letter || '') : 'PREFACE'))}</small><b>${esc(bookClip(section.short || section.title, 22))}</b><em>${branches.length} 个分支</em></div>
          <div class="mm-grid">${branchHtml}</div>
        </div>
        <div class="guide-hint">点击任意节点或小标签，直接跳到正文对应位置</div>
      </div>
      <div class="guide-pane hide" data-guide-pane="route">
        <div class="guide-route">${route}</div>
      </div>
      <div class="guide-pane hide" data-guide-pane="traps">
        <div class="guide-traps">${traps}</div>
      </div>
    </div>
  </div>`;
}

function drawBookMindmap() {
  const wrap = $('bookMindmap');
  const svg = $('bookMindLines');
  if (!wrap || !svg || !wrap.offsetParent) return;
  const rect = wrap.getBoundingClientRect();
  if (rect.width < 20 || rect.height < 20) return;
  const root = wrap.querySelector('.mm-root');
  if (!root) return;
  const rr = root.getBoundingClientRect();
  const x1 = rr.left + rr.width / 2 - rect.left;
  const y1 = rr.bottom - rect.top;
  let paths = '';
  wrap.querySelectorAll('.mm-branch').forEach((b) => {
    const br = b.getBoundingClientRect();
    const x2 = br.left + br.width / 2 - rect.left;
    const y2 = br.top - rect.top;
    const mid = (y1 + y2) / 2;
    const color = b.style.getPropertyValue('--c') || '#0071e3';
    paths += `<path d="M ${x1.toFixed(1)} ${y1.toFixed(1)} C ${x1.toFixed(1)} ${mid.toFixed(1)}, ${x2.toFixed(1)} ${mid.toFixed(1)}, ${x2.toFixed(1)} ${y2.toFixed(1)}" stroke="${color}" stroke-width="1.6" fill="none" opacity=".4"/>`;
  });
  svg.setAttribute('viewBox', `0 0 ${Math.round(rect.width)} ${Math.round(rect.height)}`);
  svg.innerHTML = paths;
}

function bindBookGuide() {
  const guide = $('bookGuide');
  if (!guide) return;
  guide.classList.toggle('collapsed', !!bookState.guideCollapsed);
  const toggle = guide.querySelector('#bookGuideToggle');
  if (toggle) {
    toggle.textContent = bookState.guideCollapsed ? '展开' : '收起';
    toggle.onclick = () => {
      bookState.guideCollapsed = !bookState.guideCollapsed;
      guide.classList.toggle('collapsed', bookState.guideCollapsed);
      toggle.textContent = bookState.guideCollapsed ? '展开' : '收起';
      if (!bookState.guideCollapsed) setTimeout(drawBookMindmap, 60);
    };
  }
  guide.querySelectorAll('[data-guide-tab]').forEach((btn) => {
    btn.onclick = () => {
      guide.querySelectorAll('[data-guide-tab]').forEach((b) => b.classList.toggle('on', b === btn));
      guide.querySelectorAll('[data-guide-pane]').forEach((p) => p.classList.toggle('hide', p.dataset.guidePane !== btn.dataset.guideTab));
      if (btn.dataset.guideTab === 'map') setTimeout(drawBookMindmap, 30);
    };
  });
  guide.querySelectorAll('[data-goto]').forEach((el) => {
    el.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      bookScrollToLabel(el.dataset.goto);
    };
  });
  if (!bookState.guideCollapsed) setTimeout(drawBookMindmap, 80);
}


function stars(n) {
  const v = Math.max(1, Math.min(5, n || 2));
  let s = '';
  for (let i = 1; i <= 5; i++) s += i <= v ? '★' : '<span class="off">★</span>';
  return `<span class="stars" title="难度 ${v}/5">${s}</span>`;
}

const KIND_TEXT = { example: '例题', exercise: '习题', appendix: '附录 C', local: '贵阳原创', ai: 'AI 原创', think: '思考题', reading: '阅读' };

function kindClass(k) {
  if (k === 'example') return 'example';
  if (k === 'appendix') return 'appendix';
  if (k === 'local') return 'local';
  if (k === 'ai') return 'ai';
  if (k === 'think' || k === 'reading') return 'reading';
  return 'exercise';
}

function toast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove('show'), 1800);
}

/* ---------------- 收藏 / 每日一题 / 随机一题 ---------------- */
function loadStars() {
  try {
    const raw = JSON.parse(localStorage.getItem('oj.stars') || '[]');
    state.stars = new Set(Array.isArray(raw) ? raw.filter((x) => typeof x === 'string') : []);
  } catch (e) {
    state.stars = new Set();
  }
}

function saveStars() {
  try { localStorage.setItem('oj.stars', JSON.stringify([...state.stars])); } catch (e) { }
}

function toggleStar(id) {
  if (!id) return;
  if (state.stars.has(id)) state.stars.delete(id);
  else state.stars.add(id);
  saveStars();
  const p = state.byId[id];
  if (p && state.current && state.current.id === id) {
    const btn = $('btnStar');
    if (btn) {
      const on = state.stars.has(id);
      btn.classList.toggle('on', on);
      btn.innerHTML = `<span class="ico">${on ? '★' : '☆'}</span> ${on ? '已收藏' : '收藏'}`;
    }
  }
  renderSidebar();
  toast(state.stars.has(id) ? '已收藏，可在「收藏」里找到' : '已取消收藏');
}

function clearProblemFilters() {
  state.filter = 'all';
  state.q = '';
  if ($('searchInput')) $('searchInput').value = '';
  if ($('clearSearch')) $('clearSearch').style.display = 'none';
  document.querySelectorAll('#filterChips .chip').forEach((c) => c.classList.toggle('on', c.dataset.filter === 'all'));
}

function hashText(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function localDayKey() {
  const d = new Date();
  return String(d.getFullYear()) + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

function dailyProblem() {
  const pool = state.problems.filter((p) => p.has_judge && p.kind !== 'think' && p.kind !== 'reading');
  if (!pool.length) return null;
  const key = localDayKey();
  const idx = hashText('daily:' + key) % pool.length;
  return pool.slice().sort((a, b) => String(a.id).localeCompare(String(b.id)))[idx];
}

function openDailyProblem() {
  setView('oj');
  const p = dailyProblem();
  if (!p) { toast('题库还没有可判题'); return; }
  clearProblemFilters();
  selectProblem(p.id);
  try { localStorage.setItem('oj.daily', JSON.stringify({ date: localDayKey(), id: p.id })); } catch (e) { }
  let done = false;
  try {
    const saved = JSON.parse(localStorage.getItem('oj.daily') || 'null');
    done = !!(saved && saved.date === localDayKey() && state.progress[saved.id] && state.progress[saved.id].status === 'AC');
  } catch (e) { }
  toast('今日一题：' + (p.label || '') + ' ' + p.title + (done ? '（今天已完成，可再刷一遍）' : ''));
}

function openRandomProblem() {
  setView('oj');
  const pool = state.problems.filter((p) => p.has_judge && p.kind !== 'think' && p.kind !== 'reading');
  if (!pool.length) { toast('题库还没有可判题'); return; }
  const notAC = pool.filter((p) => !(state.progress[p.id] && state.progress[p.id].status === 'AC'));
  const list = notAC.length ? notAC : pool;
  const p = list.find((x) => x.id !== (state.current && state.current.id)) || list[0];
  clearProblemFilters();
  selectProblem(p.id);
  toast('随机一题：' + (p.label || '') + ' ' + p.title);
}


function filtersActive() {
  return state.filter !== 'all' || state.q.trim() !== '';
}

function matches(p) {
  if (state.filter === 'ac' && !(state.progress[p.id] && state.progress[p.id].status === 'AC')) return false;
  if (state.filter === 'todo' && state.progress[p.id] && state.progress[p.id].status === 'AC') return false;
  if (state.filter === 'wrong') {
    const pr = state.progress[p.id] || {};
    if (!pr.attempts || pr.status === 'AC') return false;
  }
  if (state.filter === 'star' && !state.stars.has(p.id)) return false;
  if (state.filter === 'ai') {
    if (p.kind !== 'ai') return false;
  } else if (state.filter === 'guiyang') {
    if (!(p.kind === 'appendix' || p.kind === 'local')) return false;
  } else if (['example', 'exercise', 'think'].includes(state.filter)) {
    if (state.filter === 'think') {
      if (!(p.kind === 'think' || p.kind === 'reading')) return false;
    } else if (p.kind !== state.filter) return false;
  }
  const q = state.q.trim().toLowerCase();
  if (!q) return true;
  const hay = [p.id, p.label, p.title, '第' + p.chapter + '章', p.chapter_title || '',
    p.difficulty_label || '', (p.tags || []).join(' ')].join(' ').toLowerCase();
  return hay.includes(q);
}

const DIFF_LABELS = { 1: '入门', 2: '基础', 3: '提高', 4: '进阶', 5: '挑战' };

function groupKeyOf(p) {
  if (p.kind === 'ai') return 'ai';
  if (state.sort === 'chapter') {
    if (p.kind === 'local') return 'gy';
    if (p.kind === 'appendix') return 'ap';
    return 'ch:' + p.chapter;
  }
  return 'lv:' + (p.difficulty || 2);
}

function groupRank(k) {
  if (k === 'gy') return -2;
  if (k === 'ap') return -1;
  if (k === 'ai') return 33;
  const [t, n] = k.split(':');
  return Number(n);
}

function groupMeta(key, ps) {
  if (key === 'gy') return { idx: 'GY', name: '贵阳生活 100 题', sub: '原创' };
  if (key === 'ap') return { idx: 'C', name: '附录 C · 贵阳主题练习', sub: '' };
  if (key === 'ai') return { idx: 'AI', name: 'AI 助教原创题', sub: '可判题' };
  const [t, n] = key.split(':');
  if (t === 'lv') {
    return { idx: '★' + n, name: `难度 ${n} · ${DIFF_LABELS[+n] || ''}`, sub: '' };
  }
  return { idx: String(n).padStart(2, '0'), name: `第 ${n} 章　${ps[0].chapter_title || ''}`, sub: '' };
}

function renderSidebar() {
  const wrap = $('sideList');
  const list = state.problems.filter(matches);
  if (!list.length) {
    wrap.innerHTML = '<div class="side-empty">没有匹配的题目</div>';
    return;
  }
  const groups = new Map();
  for (const p of list) {
    const key = groupKeyOf(p);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(p);
  }
  const keys = [...groups.keys()].sort((a, b) => {
    if (state.sort === 'desc') return groupRank(b) - groupRank(a);
    return groupRank(a) - groupRank(b);
  });
  let html = '';
  for (const key of keys) {
    const ps = groups.get(key);
    const meta = groupMeta(key, ps);
    const judged = ps.filter((p) => p.has_judge);
    const ac = judged.filter((p) => state.progress[p.id] && state.progress[p.id].status === 'AC').length;
    const hasCurrent = state.current && ps.some((p) => p.id === state.current.id);
    const isOpen = filtersActive() || hasCurrent || (state.open[key] !== undefined ? state.open[key]
      : (state.sort !== 'chapter' || key === 'ch:1'));
    html += `<div class="chapter-group ${isOpen ? 'open' : ''}" data-group="${key}">
      <div class="chapter-head">
        <span class="idx ${key === 'gy' ? 'gy' : ''}${key === 'ai' ? 'ai' : ''}">${meta.idx}</span>
        <span class="name" title="${esc(meta.name)}">${esc(meta.name)}</span>
        <span class="cnt" title="可判题 ${judged.length} 道">${ac}/${judged.length}</span>
        <span class="arrow">›</span>
      </div>
      <div class="chapter-items">`;
    for (const p of ps) {
      const pr = state.progress[p.id] || {};
      let dot = '';
      if (pr.status === 'AC') dot = 'ac';
      else if (pr.attempts) dot = pr.last === 'WA' || pr.last === 'PE' ? 'bad' : 'try';
      const tag = p.kind === 'example' ? '<span class="tag ex">例</span>'
        : p.kind === 'local' ? '<span class="tag gy">贵</span>'
          : p.kind === 'ai' ? '<span class="tag ai">AI</span>'
            : p.kind === 'appendix' ? '<span class="tag">C</span>'
              : (p.kind === 'think' || p.kind === 'reading') ? '<span class="tag">思</span>' : '<span class="tag">习</span>';
      const active = state.current && state.current.id === p.id ? 'active' : '';
      const lv = p.difficulty || 2;
      const star = state.stars.has(p.id) ? '<span class="star-mark" title="已收藏">★</span>' : '';
      html += `<div class="problem-item ${active}" data-id="${p.id}" title="${esc(p.label + ' ' + p.title)} · 难度 ${lv}/5">
        <span class="dot ${dot}"></span><span class="lv lv${lv}">${lv}</span>
        <span class="t">${esc(p.title)}</span>${star}${tag}</div>`;
    }
    html += '</div></div>';
  }
  wrap.innerHTML = html;

  wrap.querySelectorAll('.chapter-head').forEach((el) => {
    el.onclick = () => {
      if (filtersActive()) return;
      const g = el.parentElement;
      const key = g.dataset.group;
      g.classList.toggle('open');
      state.open[key] = g.classList.contains('open');
    };
  });
  wrap.querySelectorAll('.problem-item').forEach((el) => {
    el.onclick = () => selectProblem(el.dataset.id);
  });
  const active = wrap.querySelector('.problem-item.active');
  if (active) requestAnimationFrame(() => active.scrollIntoView({ block: 'nearest' }));
}

function updateProgressBar() {
  const total = state.problems.filter((p) => p.kind !== 'think' && p.kind !== 'reading').length;
  const ac = state.problems.filter((p) => state.progress[p.id] && state.progress[p.id].status === 'AC').length;
  $('acCount').textContent = ac;
  $('totalCount').textContent = total;
  $('progressFill').style.width = total ? (ac / total * 100).toFixed(1) + '%' : '0';
  rpgRenderHud();
}

/* ================= 冒险等级 ================= */
function rpgDefault() {
  return { v: 1, xp: 0, awarded: {}, daily: { date: '', first: false } };
}

function rpgLoad() {
  try {
    const raw = JSON.parse(localStorage.getItem(RPG_KEY) || 'null');
    if (raw && typeof raw === 'object') {
      const xp = Number(raw.xp);
      return {
        v: 1,
        xp: Number.isFinite(xp) && xp >= 0 ? Math.floor(xp) : 0,
        awarded: raw.awarded && typeof raw.awarded === 'object' ? raw.awarded : {},
        daily: raw.daily && typeof raw.daily === 'object' ? raw.daily : { date: '', first: false },
      };
    }
  } catch (e) { /* 本地经验数据损坏时重新开始 */ }
  return rpgDefault();
}

function rpgSave() {
  try { localStorage.setItem(RPG_KEY, JSON.stringify(rpg)); } catch (e) { }
}

function rpgNeed(level) {
  return Math.round(80 + Math.max(0, level - 1) * 34 + Math.pow(Math.max(1, level), 1.32) * 4);
}

function rpgRank(level) {
  let rank = RPG_RANKS[0];
  for (const r of RPG_RANKS) if (r.level <= level) rank = r;
  return rank;
}

function rpgInfo(xp) {
  const total = xp === undefined ? rpg.xp : xp;
  let level = 1;
  let levelStart = 0;
  while (level < RPG_MAX_LEVEL && total >= levelStart + rpgNeed(level)) {
    levelStart += rpgNeed(level);
    level++;
  }
  const need = level >= RPG_MAX_LEVEL ? 0 : rpgNeed(level);
  const into = Math.max(0, total - levelStart);
  const pct = need ? Math.min(100, into / need * 100) : 100;
  const nextRank = RPG_RANKS.find((r) => r.level > level) || null;
  return {
    level, xp: total, levelStart, into, need, pct,
    rank: rpgRank(level), nextRank,
    isMax: level >= RPG_MAX_LEVEL,
  };
}

function rpgSolvedProblems() {
  return state.problems.filter((p) => state.progress[p.id] && state.progress[p.id].status === 'AC');
}

function rpgDailyDone() {
  return !!(rpg && rpg.daily && rpg.daily.date === localDayKey() && rpg.daily.first);
}

function rpgBaseXp(p) {
  const diff = Math.max(1, Math.min(5, Number(p && p.difficulty) || 2));
  return RPG_DIFF_XP[diff] || 35;
}

function rpgAwardProblem(p, opts) {
  opts = opts || {};
  if (!p || !p.id || !rpg) return null;
  if (rpg.awarded[p.id]) return { gain: 0, base: 0, dailyBonus: 0, oldInfo: rpgInfo(), newInfo: rpgInfo() };
  const base = rpgBaseXp(p);
  let dailyBonus = 0;
  if (!opts.silent && !opts.noDaily) {
    const today = localDayKey();
    if (!rpg.daily || rpg.daily.date !== today) rpg.daily = { date: today, first: false };
    if (!rpg.daily.first) {
      dailyBonus = 10;
      rpg.daily.first = true;
    }
  }
  const oldInfo = rpgInfo();
  const gain = base + dailyBonus;
  rpg.xp += gain;
  rpg.awarded[p.id] = { date: localDayKey(), xp: gain };
  rpgSave();
  const newInfo = rpgInfo();
  return { gain, base, dailyBonus, oldInfo, newInfo, problem: p };
}

function rpgSyncFromProgress(opts) {
  opts = opts || {};
  if (!state.problems.length || !rpg) return;
  let gained = 0;
  let count = 0;
  for (const p of state.problems) {
    if (!(state.progress[p.id] && state.progress[p.id].status === 'AC')) continue;
    if (rpg.awarded[p.id]) continue;
    const award = rpgAwardProblem(p, { silent: true, noDaily: true });
    if (award && award.gain) {
      gained += award.gain;
      count++;
    }
  }
  const oneToday = state.problems.find((p) => {
    const rec = state.progress[p.id];
    return rec && rec.status === 'AC' && String(rec.ac_time || '').slice(0, 10) === localDayKey();
  });
  if (oneToday && (!rpg.daily || rpg.daily.date !== localDayKey() || !rpg.daily.first)) {
    rpg.daily = { date: localDayKey(), first: true };
    rpg.xp += 10;
    gained += 10;
    if (rpg.awarded[oneToday.id]) {
      const rec = rpg.awarded[oneToday.id];
      rpg.awarded[oneToday.id] = { date: rec.date || localDayKey(), xp: (Number(rec.xp) || 0) + 10 };
    }
  }
  if (gained) rpgSave();
  rpgRenderHud();
  if (gained && opts.announce) {
    const info = rpgInfo();
    const levelText = info.level > 1 ? ' · 当前 Lv.' + info.level : '';
    toast('历史战绩已结算 +' + gained + ' XP' + levelText);
  }
  return { gained, count };
}

function rpgRenderHud() {
  if (!rpg) rpg = rpgLoad();
  const info = rpgInfo();
  const solved = rpgSolvedProblems();
  const hud = $('rpgHud');
  if (!hud) return;
  if ($('rpgLevelNo')) $('rpgLevelNo').textContent = info.level;
  if ($('rpgTitle')) $('rpgTitle').textContent = info.rank.title;
  if ($('rpgXpText')) $('rpgXpText').textContent = info.isMax ? 'MAX · 满级' : info.into + ' / ' + info.need + ' XP';
  if ($('rpgFill')) $('rpgFill').style.width = info.pct.toFixed(1) + '%';
  if ($('rpgSolved')) $('rpgSolved').textContent = solved.length + ' 题已通过';
  if ($('rpgDaily')) {
    $('rpgDaily').textContent = rpgDailyDone() ? '今日首胜已完成' : '今日首胜 +10 XP';
    $('rpgDaily').classList.toggle('done', rpgDailyDone());
  }
  hud.classList.toggle('max', info.isMax);
  hud.dataset.level = String(info.level);
  if ($('rpgProfile')) rpgRenderProfile();
}

function rpgXpBurst(gain) {
  const hud = $('rpgHud');
  if (!hud || !gain) return;
  const pop = document.createElement('span');
  pop.className = 'rpg-xp-pop';
  pop.textContent = '+' + gain + ' XP';
  hud.appendChild(pop);
  setTimeout(() => pop.remove(), 1400);
}

function rpgBadges() {
  const solved = rpgSolvedProblems();
  const tags = new Set();
  for (const p of solved) for (const t of (p.tags || [])) tags.add(t);
  return [
    { icon: '✦', title: '初出茅庐', desc: '通过第 1 道题', ok: solved.length >= 1 },
    { icon: '◆', title: '五题斩', desc: '累计通过 5 道题', ok: solved.length >= 5 },
    { icon: '✧', title: '十题勇者', desc: '累计通过 10 道题', ok: solved.length >= 10 },
    { icon: '⬢', title: '知识收集者', desc: '通过题目覆盖 5 个知识点', ok: tags.size >= 5 },
    { icon: '★', title: '挑战者', desc: '通过一道 5 级题', ok: solved.some((p) => Number(p.difficulty) === 5) },
    { icon: '◈', title: 'AI 先锋', desc: '通过一道 AI 原创题', ok: solved.some((p) => p.kind === 'ai') },
  ];
}

function rpgBadgeHtml(badges, compact) {
  return badges.map((b) => `<div class="rpg-badge${b.ok ? ' on' : ''}${compact ? ' compact' : ''}" title="${esc(b.desc)}">
    <span class="rpg-badge-icon">${b.ok ? b.icon : '·'}</span>
    <span><b>${esc(b.title)}</b><small>${esc(b.desc)}</small></span>
  </div>`).join('');
}

function rpgProfileHtml() {
  const info = rpgInfo();
  const solved = rpgSolvedProblems();
  const badges = rpgBadges();
  return `<div class="rpg-profile-hero">
      <div class="rpg-profile-medal"><small>LEVEL</small><b>${info.level}</b></div>
      <div class="rpg-profile-copy">
        <div class="rpg-profile-kicker">ADVENTURER · 本机进度</div>
        <h2>${esc(info.rank.title)}<span>${info.isMax ? '已达等级上限' : '距离下一级 ' + (info.need - info.into) + ' XP'}</span></h2>
        <p>${esc(info.rank.subtitle)}</p>
      </div>
      <button class="rpg-profile-more" type="button" data-rpg-open>打开冒险者档案 →</button>
    </div>
    <div class="rpg-profile-main">
      <div class="rpg-profile-xp">
        <div class="rpg-profile-xp-head"><span>等级经验</span><b>${info.xp} XP</b></div>
        <div class="rpg-profile-bar"><i style="width:${info.pct.toFixed(1)}%"></i></div>
        <div class="rpg-profile-xp-foot"><span>Lv.${info.level} · ${info.into} / ${info.need} XP</span><span>${solved.length} 题通过 · ${rpgDailyDone() ? '今日首胜已完成' : '今日首胜待领取'}</span></div>
      </div>
      <div class="rpg-profile-stats">
        <div><span>已通过</span><b>${solved.length}</b><small>题</small></div>
        <div><span>当前称号</span><b>${esc(info.rank.title)}</b></div>
        <div><span>下一称号</span><b>${info.nextRank ? esc(info.nextRank.title) : '已满级'}</b></div>
      </div>
    </div>
    <div class="rpg-profile-badges">${rpgBadgeHtml(badges, true)}</div>`;
}

function rpgRenderProfile() {
  const root = $('rpgProfile');
  if (root) root.innerHTML = rpgProfileHtml();
}

function rpgRenderModal() {
  const body = $('rpgModalBody');
  if (!body) return;
  const info = rpgInfo();
  const solved = rpgSolvedProblems();
  const badges = rpgBadges();
  const daily = rpgDailyDone();
  body.innerHTML = `
    <div class="rpg-modal-hero">
      <div class="rpg-modal-medal"><small>LEVEL</small><b>${info.level}</b></div>
      <div class="rpg-modal-title">
        <span class="rpg-modal-kicker">${esc(info.rank.title)}</span>
        <h3>${esc(info.rank.subtitle)}</h3>
        <div class="rpg-modal-bar"><i style="width:${info.pct.toFixed(1)}%"></i></div>
        <div class="rpg-modal-xp"><span>${info.isMax ? 'MAX' : '还需 ' + (info.need - info.into) + ' XP 升级'}</span><b>${info.xp} XP</b></div>
      </div>
    </div>
    <div class="rpg-modal-stats">
      <div><span>已通过</span><b>${solved.length}</b><small>道题</small></div>
      <div><span>今日首胜</span><b>${daily ? '已完成' : '待完成'}</b><small>${daily ? '+10 XP 已入账' : '通过任意题 +10 XP'}</small></div>
      <div><span>下一称号</span><b>${info.nextRank ? esc(info.nextRank.title) : '已满级'}</b><small>${info.nextRank ? 'Lv.' + info.nextRank.level : '保持输出'}</small></div>
    </div>
    <div class="rpg-modal-section"><span class="rpg-modal-label">ACHIEVEMENTS · 勋章</span><div class="rpg-badges-grid">${rpgBadgeHtml(badges, false)}</div></div>
    <div class="rpg-modal-section rpg-modal-note">
      <span class="rpg-modal-label">HOW XP WORKS</span>
      <p>首次通过一道题获得经验：难度 1～5 分别为 <b>20 / 35 / 55 / 85 / 130 XP</b>；每天第一次 AC 额外 <b>+10 XP</b>。重复提交同一道题不会刷经验，等级与经验只保存在本机。</p>
    </div>
    <div class="rpg-modal-foot"><button class="rpg-modal-close" id="rpgModalClose" type="button">回到题目</button></div>`;
  const close = $('rpgModalClose');
  if (close) close.onclick = rpgClose;
}

function rpgOpen() {
  rpgRenderModal();
  const back = $('rpgBackdrop');
  if (back) back.classList.remove('hide');
  document.body.classList.add('rpg-open');
}

function rpgClose() {
  const back = $('rpgBackdrop');
  if (back) back.classList.add('hide');
  document.body.classList.remove('rpg-open');
}

function rpgLevelUp(info) {
  const back = $('levelupBackdrop');
  if (!back || !info) return;
  if ($('levelupNo')) $('levelupNo').textContent = info.level;
  if ($('levelupTitle')) $('levelupTitle').textContent = info.rank.title;
  if ($('levelupSub')) $('levelupSub').textContent = info.rank.subtitle;
  if ($('levelupUnlock')) {
    $('levelupUnlock').textContent = info.nextRank
      ? '下一个称号：' + info.nextRank.title + ' · Lv.' + info.nextRank.level
      : '已抵达当前最高等级，继续把题库点亮。';
  }
  const confetti = $('levelupConfetti');
  if (confetti) {
    const colors = ['#40a9ff', '#7d7cff', '#ffd166', '#54d68a', '#ff7b9c'];
    confetti.innerHTML = Array.from({ length: 20 }, (_, i) => {
      const x = 8 + (i * 37) % 86;
      const rot = (i * 43) % 360;
      const delay = (i % 7) * 0.05;
      return '<i style="left:' + x + '%;--r:' + rot + 'deg;--d:' + delay + 's;background:' + colors[i % colors.length] + '"></i>';
    }).join('');
  }
  back.classList.remove('hide');
  document.body.classList.add('levelup-open');
}

function rpgCloseLevelUp() {
  const back = $('levelupBackdrop');
  if (back) back.classList.add('hide');
  document.body.classList.remove('levelup-open');
}

function rpgAfterSubmit(p, result, wasAC) {
  if (!result || result.verdict !== 'AC' || wasAC) return;
  const award = rpgAwardProblem(p, {});
  if (!award || !award.gain) return;
  rpgRenderHud();
  rpgXpBurst(award.gain);
  if (award.newInfo.level > award.oldInfo.level) {
    setTimeout(() => rpgLevelUp(award.newInfo), 180);
  }
  toast('+' + award.gain + ' XP · ' + (award.dailyBonus ? '今日首胜已领取' : '首次通过'));
}

function rpgBind() {
  if ($('rpgHud')) $('rpgHud').onclick = rpgOpen;
  if ($('rpgClose')) $('rpgClose').onclick = rpgClose;
  if ($('rpgBackdrop')) {
    $('rpgBackdrop').addEventListener('click', (e) => {
      if (e.target === $('rpgBackdrop')) rpgClose();
    });
  }
  if ($('levelupClose')) $('levelupClose').onclick = rpgCloseLevelUp;
  if ($('levelupBackdrop')) {
    $('levelupBackdrop').addEventListener('click', (e) => {
      if (e.target === $('levelupBackdrop')) rpgCloseLevelUp();
    });
  }
  document.addEventListener('click', (e) => {
    if (e.target.closest('[data-rpg-open]')) rpgOpen();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    if ($('levelupBackdrop') && !$('levelupBackdrop').classList.contains('hide')) rpgCloseLevelUp();
    else if ($('rpgBackdrop') && !$('rpgBackdrop').classList.contains('hide')) rpgClose();
  });
}

function sampleHtml(p) {
  const samples = p.samples || [];
  if (!samples.length) return '';
  return samples.map((s, idx) => {
    const tag = samples.length > 1 ? `样例 ${idx + 1}` : '样例';
    return `<div class="io-block">
      <h3>${tag}</h3>
      <div class="io-grid">
        <div class="sample"><div class="cap"><span>输入</span><button data-copy="${esc(s.in)}">复制</button></div><pre>${esc(s.in)}</pre></div>
        <div class="sample"><div class="cap"><span>输出</span><button data-copy="${esc(s.out)}">复制</button></div><pre>${esc(s.out)}</pre></div>
      </div>
    </div>`;
  }).join('');
}

function hintPanelHtml(p) {
  let hints = Array.isArray(p.hints) ? p.hints.slice() : [];
  if (!hints.length && p.hint_md) hints = String(p.hint_md).split('\n');
  hints = hints.map((x) => String(x).trim()).filter(Boolean);
  if (!hints.length) hints = ['先按题意把输入输出和样例对一遍，再想需要维护什么状态。'];
  return `<div class="hint-panel" id="hintPanel" hidden>
    <div class="panel-head"><span>提示</span><span class="panel-sub">一层一层看，先自己想 3 分钟</span></div>
    <ol class="hint-list">${hints.map((h, i) => `<li class="hint-step ${i ? 'more' : ''}" data-step="${i + 1}">${mdToHtml(h)}</li>`).join('')}</ol>
    ${hints.length > 1 ? '<button class="panel-more" id="btnHintMore">再看一层</button>' : ''}
  </div>`;
}

function diffPanelHtml(p) {
  const d = p.difficulty || 2;
  const factors = Array.isArray(p.difficulty_factors) ? p.difficulty_factors : [];
  const rows = factors.map((f) => {
    const lv = Math.max(1, Math.min(5, f.level || 1));
    let dots = '';
    for (let i = 1; i <= 5; i++) dots += `<i class="${i <= lv ? 'on' : ''}"></i>`;
    return `<div class="factor-row">
      <span class="factor-name">${esc(f.name)}</span>
      <span class="factor-dots">${dots}</span>
      <span class="factor-note">${esc(f.note || '')}</span>
    </div>`;
  }).join('');
  return `<div class="diff-panel" id="diffPanel" hidden>
    <div class="panel-head"><span>难度评估</span><span class="panel-score lv${d}">${d}/5 · ${esc(p.difficulty_label || DIFF_LABELS[d])}</span></div>
    ${p.difficulty_note ? `<p class="diff-note">${esc(p.difficulty_note)}</p>` : ''}
    <div class="factor-grid">${rows}</div>
    <div class="diff-legend">1 入门 · 2 基础 · 3 提高 · 4 进阶 · 5 挑战</div>
  </div>`;
}

function renderProblem(p) {
  $('welcome').style.display = 'none';
  const head = $('problemHead');
  const body = $('statement');
  head.style.display = 'block';
  body.style.display = 'block';

  const kind = p.kind || 'exercise';
  const diff = p.difficulty || 2;
  const pr = state.progress[p.id] || {};
  head.innerHTML = `
    <div class="meta-row">
      <span class="pill ${kindClass(kind)}">${KIND_TEXT[kind] || '题目'}</span>
      <span>${esc(p.label || '')}</span>
      ${p.chapter ? `<span>·</span><span>第 ${p.chapter} 章 ${esc(p.chapter_title || '')}</span>` : ''}
      <span class="pill diff lv${diff}">${p.difficulty_label || DIFF_LABELS[diff]} ${diff}/5</span>
      ${pr.status === 'AC' ? '<span class="pill ac">已通过</span>' : ''}
    </div>
    <h2>${esc(p.title)}</h2>
    <div class="sub">
      <span>${p.test_count ? `${p.test_count} 组测试数据` : '无判题数据'}</span>
      <span>时间限制 ${p.time_limit || 1} 秒</span>
      <span>${esc(p.source || '')}</span>
    </div>
    <div class="problem-actions">
      <button class="action-btn" id="btnHint"><span class="ico">◐</span> 提示</button>
      <button class="action-btn" id="btnDiff"><span class="ico">▤</span> 难度评估</button>
      <button class="action-btn star-btn ${state.stars.has(p.id) ? 'on' : ''}" id="btnStar"><span class="ico">${state.stars.has(p.id) ? '★' : '☆'}</span> ${state.stars.has(p.id) ? '已收藏' : '收藏'}</button>
      <button class="action-btn" id="btnHistory"><span class="ico">◷</span> 提交记录</button>
      ${p.kind !== 'local' && p.kind !== 'ai' ? '<button class="action-btn book-link" id="btnBookLink"><span class="ico">▤</span> 对应原书</button>' : ''}
      <span class="action-note">${stars(diff)} <span class="diff-text">${esc(p.difficulty_label || '')}</span></span>
    </div>`;

  let html = mdToHtml(p.statement_md || '');
  if (p.input_md) html += `<h3>输入格式</h3>${mdToHtml(p.input_md)}`;
  if (p.output_md) html += `<h3>输出格式</h3>${mdToHtml(p.output_md)}`;
  if (p.constraints_md) html += `<h3>数据范围</h3>${mdToHtml(p.constraints_md)}`;
  if (p.io_note) html += `<h3>输入输出说明</h3>${mdToHtml(p.io_note)}`;
  html += hintPanelHtml(p);
  html += diffPanelHtml(p);
  html += sampleHtml(p);
  if (p.note_md) html += `<div class="hint-box"><b>说明</b><br>${mdToHtml(p.note_md)}</div>`;
  if (p.has_solution) html += `
    <div class="answer-box">
      <div class="answer-head">
        <b>参考答案</b>
        <span class="answer-tip">C++17 · 头文件 <code>#include&lt;bits/stdc++.h&gt;</code></span>
        <button class="btn ghost" id="btnAnswer">查看参考答案</button>
        <button class="btn ghost" id="btnAnswerCopy" style="display:none">复制</button>
      </div>
      <pre class="code answer-code" id="answerCode" style="display:none"></pre>
    </div>`;
  body.innerHTML = html;
  body.scrollTop = 0;

  const hintPanel = document.getElementById('hintPanel');
  const diffPanel = document.getElementById('diffPanel');
  document.getElementById('btnHint').onclick = () => {
    const willOpen = hintPanel.hasAttribute('hidden');
    if (willOpen) { hintPanel.removeAttribute('hidden'); hintPanel.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
    else hintPanel.setAttribute('hidden', '');
  };
  document.getElementById('btnDiff').onclick = () => {
    const willOpen = diffPanel.hasAttribute('hidden');
    if (willOpen) { diffPanel.removeAttribute('hidden'); diffPanel.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
    else diffPanel.setAttribute('hidden', '');
  };
  const btnBookLink = document.getElementById('btnBookLink');
  if (btnBookLink) btnBookLink.onclick = () => openBookForCurrent();
  const btnStar = document.getElementById('btnStar');
  if (btnStar) btnStar.onclick = () => toggleStar(p.id);
  const btnHistory = document.getElementById('btnHistory');
  if (btnHistory) btnHistory.onclick = () => toggleProblemHistory(p.id);
  const btnHintMore = document.getElementById('btnHintMore');
  if (btnHintMore) {
    let shown = 1;
    btnHintMore.onclick = () => {
      const next = hintPanel.querySelector('.hint-step.more');
      if (!next) { btnHintMore.style.display = 'none'; return; }
      next.classList.remove('more');
      shown++;
      if (!hintPanel.querySelector('.hint-step.more')) btnHintMore.textContent = '已经全部看完';
    };
  }

  body.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.onclick = async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        toast('已复制');
      } catch (e) {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
        toast('已复制');
      }
    };
  });

  if (p.has_solution) {
    const btnA = document.getElementById('btnAnswer');
    const preA = document.getElementById('answerCode');
    const btnCopy = document.getElementById('btnAnswerCopy');
    const copy = async (text) => {
      try {
        await navigator.clipboard.writeText(text);
        toast('已复制参考答案');
      } catch (e) {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
        toast('已复制参考答案');
      }
    };
    btnA.onclick = async () => {
      btnA.disabled = true;
      btnA.textContent = '加载中…';
      try {
        const r = await fetch('/api/solution/' + encodeURIComponent(p.id));
        const j = await r.json();
        if (!r.ok) throw new Error(j.error || '加载失败');
        preA.textContent = j.code;
        preA.style.display = 'block';
        btnA.style.display = 'none';
        btnCopy.style.display = '';
        btnCopy.onclick = () => copy(j.code);
      } catch (e) {
        toast('参考答案加载失败');
        btnA.disabled = false;
        btnA.textContent = '查看参考答案';
      }
    };
  }
}

function templateFor(p) {
  return TEMPLATE;
}

function setCode(text) {
  const code = $('code');
  code.value = text;
  refreshCodeEditor();
  saveCode();
}

function updateGutter() {
  const code = $('code');
  const n = code.value.split('\n').length;
  let s = '';
  for (let i = 1; i <= n; i++) s += i + '\n';
  $('gutter').textContent = s;
  $('gutter').scrollTop = code.scrollTop;
}

/* ================= 代码编辑器：高亮 / 补全 / 自动缩进 ================= */
const CPP_EDITOR_LINE = 20;
const CPP_EDITOR_PAD = 13;

const CPP_EDITOR_CONTROL = new Set([
  'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default', 'break',
  'continue', 'return', 'goto', 'try', 'catch', 'throw',
]);
const CPP_EDITOR_TYPES = new Set([
  'bool', 'char', 'char8_t', 'char16_t', 'char32_t', 'double', 'float', 'int',
  'long', 'short', 'signed', 'unsigned', 'void', 'wchar_t', 'size_t', 'ssize_t',
  'int8_t', 'int16_t', 'int32_t', 'int64_t', 'uint8_t', 'uint16_t', 'uint32_t',
  'uint64_t', 'string', 'vector', 'map', 'set', 'multiset', 'unordered_map',
  'unordered_set', 'queue', 'priority_queue', 'stack', 'deque', 'pair', 'tuple',
  'array', 'list', 'bitset', 'complex',
]);
const CPP_EDITOR_KEYWORDS = new Set([
  'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor',
  'class', 'compl', 'const', 'constexpr', 'const_cast', 'decltype', 'delete',
  'dynamic_cast', 'enum', 'explicit', 'export', 'extern', 'false', 'friend',
  'inline', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr',
  'operator', 'or', 'or_eq', 'private', 'protected', 'public', 'register',
  'reinterpret_cast', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct',
  'template', 'this', 'thread_local', 'true', 'typedef', 'typeid', 'typename',
  'union', 'using', 'virtual', 'volatile', 'xor', 'xor_eq', 'include', 'define',
  'ifndef', 'endif', 'pragma',
]);
const CPP_EDITOR_BUILTINS = new Set([
  'std', 'cin', 'cout', 'cerr', 'clog', 'endl', 'ios', 'sync_with_stdio', 'tie',
  'printf', 'scanf', 'puts', 'gets', 'memset', 'memcpy', 'strlen', 'strcmp',
  'sort', 'stable_sort', 'reverse', 'unique', 'max', 'min', 'abs', 'swap',
  'lower_bound', 'upper_bound', 'binary_search', 'gcd', 'lcm', 'to_string',
  'stoi', 'stoll', 'substr', 'find', 'insert', 'erase', 'push_back', 'pop_back',
  'size', 'empty', 'front', 'back', 'top', 'begin', 'end', 'rbegin', 'rend',
]);

const CPP_EDITOR_CALLS = new Set([
  'if', 'for', 'while', 'switch', 'catch', 'main', 'sort', 'max', 'min', 'abs',
  'swap', 'memset', 'printf', 'scanf', 'strlen', 'push_back', 'insert', 'erase',
  'find', 'substr', 'lower_bound', 'upper_bound', 'gcd', 'lcm', 'to_string',
  'stoi', 'size', 'empty', 'sync_with_stdio',
]);

const CPP_EDITOR_SUGGEST_BASE = (() => {
  const map = new Map();
  const add = (label, kind, detail, insert, cursorOffset) => {
    if (!label || map.has(label)) return;
    map.set(label, {
      label, kind, detail,
      insert: insert == null ? label : insert,
      cursorOffset: cursorOffset == null ? null : cursorOffset,
    });
  };
  ['if', 'for', 'while', 'switch', 'catch'].forEach((label) => {
    add(label, 'kw', '控制语句', label + ' ()', label.length + 2);
  });
  CPP_EDITOR_CONTROL.forEach((label) => {
    if (!['if', 'for', 'while', 'switch', 'catch'].includes(label)) add(label, 'kw', '控制语句');
  });
  CPP_EDITOR_TYPES.forEach((label) => add(label, 'ty', '类型 / 容器'));
  CPP_EDITOR_KEYWORDS.forEach((label) => {
    if (!CPP_EDITOR_TYPES.has(label) && !CPP_EDITOR_CONTROL.has(label)) add(label, 'kw', '关键字');
  });
  CPP_EDITOR_BUILTINS.forEach((label) => {
    if (!CPP_EDITOR_TYPES.has(label)) add(label, 'bi', '标准库');
  });
  ['main', 'sort', 'max', 'min', 'abs', 'swap', 'memset', 'printf', 'scanf',
    'strlen', 'push_back', 'insert', 'erase', 'find', 'substr', 'lower_bound',
    'upper_bound', 'gcd', 'lcm', 'to_string', 'stoi', 'size', 'empty',
    'sync_with_stdio'].forEach((label) => {
    map.delete(label);
    const call = label + '()';
    add(label, 'fn', '函数', call, label.length + 1);
  });
  CPP_EDITOR_CALLS.forEach((label) => {
    if (!map.has(label)) add(label, 'fn', '函数', label + '()', label.length + 1);
  });
  ['std::cin', 'std::cout', 'std::cerr', 'std::endl', 'std::ios', 'std::string',
    'std::vector', 'std::map', 'std::set', 'std::queue', 'std::stack',
    'std::priority_queue', 'std::unordered_map', 'std::unordered_set',
    'std::pair', 'std::size_t', 'std::tie'].forEach((label) => add(label, 'bi', 'std 命名空间'));
  ['std::sort', 'std::max', 'std::min', 'std::abs', 'std::swap',
    'std::lower_bound', 'std::upper_bound', 'std::to_string', 'std::stoi'].forEach((label) => {
    add(label, 'fn', 'std 函数', label + '()', label.length + 1);
  });
  add('std::sync_with_stdio', 'fn', 'std 函数', 'std::sync_with_stdio(false)');
  return [...map.values()];
})();

const editorUI = {
  ready: false,
  suggestTimer: 0,
  suggest: { open: false, items: [], index: 0, wordStart: 0, prefix: '' },
};

function tokenSpan(cls, text) {
  return '<span class="tok-' + cls + '">' + esc(text) + '</span>';
}

function highlightCpp(source) {
  const s = String(source || '');
  let out = '';
  let i = 0;
  while (i < s.length) {
    const c = s[i];

    if (c === '/' && s[i + 1] === '/') {
      let j = s.indexOf('\n', i);
      if (j < 0) j = s.length;
      out += tokenSpan('comment', s.slice(i, j));
      i = j;
      continue;
    }
    if (c === '/' && s[i + 1] === '*') {
      let j = s.indexOf('*/', i + 2);
      j = j < 0 ? s.length : j + 2;
      out += tokenSpan('comment', s.slice(i, j));
      i = j;
      continue;
    }
    if (c === '#') {
      const lineStart = s.lastIndexOf('\n', i - 1) + 1;
      if (!s.slice(lineStart, i).trim()) {
        let j = s.indexOf('\n', i);
        if (j < 0) j = s.length;
        out += tokenSpan('pre', s.slice(i, j));
        i = j;
        continue;
      }
    }
    if (c === '"' || c === "'") {
      const quote = c;
      let j = i + 1;
      while (j < s.length) {
        if (s[j] === '\\') { j += 2; continue; }
        if (s[j] === quote) { j++; break; }
        if (s[j] === '\n') break;
        j++;
      }
      out += tokenSpan('str', s.slice(i, j));
      i = j;
      continue;
    }
    if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(s[i + 1]))) {
      let j = i + 1;
      while (j < s.length && /[0-9a-fA-FxXbBoO._']/.test(s[j])) j++;
      out += tokenSpan('num', s.slice(i, j));
      i = j;
      continue;
    }
    if (/[A-Za-z_]/.test(c)) {
      let j = i + 1;
      while (j < s.length && /[A-Za-z0-9_]/.test(s[j])) j++;
      const word = s.slice(i, j);
      let k = j;
      while (k < s.length && (s[k] === ' ' || s[k] === '\t')) k++;
      let cls = 'var';
      if (CPP_EDITOR_CONTROL.has(word)) cls = 'control';
      else if (CPP_EDITOR_TYPES.has(word)) cls = 'type';
      else if (CPP_EDITOR_KEYWORDS.has(word)) cls = 'key';
      else if (CPP_EDITOR_BUILTINS.has(word)) cls = 'builtin';
      else if (s[k] === '(') cls = 'fn';
      out += tokenSpan(cls, word);
      i = j;
      continue;
    }

    const op = s.slice(i).match(/^(::|->\*|->|<<=|>>=|<=>|==|!=|<=|>=|&&|\|\||\+\+|--|<<|>>|\+=|-=|\*=|\/=|%=|&=|\|=|^=|\.\.\.)/);
    if (op) {
      out += tokenSpan('op', op[0]);
      i += op[0].length;
      continue;
    }
    if (/\s/.test(c)) {
      let j = i;
      while (j < s.length && /\s/.test(s[j])) j++;
      out += esc(s.slice(i, j));
      i = j;
      continue;
    }
    if ('{}()[];,.:?+-*/%&|^!~=<>'.includes(c)) {
      out += tokenSpan('op', c);
      i++;
      continue;
    }
    out += esc(c);
    i++;
  }
  return out + (s.endsWith('\n') ? '\n' : '');
}

function refreshCodeEditor() {
  const code = $('code');
  const editor = $('codeEditor');
  const inner = $('codeHighlightInner');
  if (!code || !editor || !inner) return;
  updateGutter();
  inner.innerHTML = highlightCpp(code.value);
  editor.classList.add('syntax-ready');
  syncEditorScroll();
  updateEditorStatus();
}

function syncEditorScroll() {
  const code = $('code');
  if (!code) return;
  const gutter = $('gutter');
  const highlight = $('codeHighlight');
  if (gutter) gutter.scrollTop = code.scrollTop;
  if (highlight) {
    highlight.scrollTop = code.scrollTop;
    highlight.scrollLeft = code.scrollLeft;
  }
  updateEditorActiveLine();
}

function updateEditorStatus() {
  const code = $('code');
  if (!code) return;
  const start = code.selectionStart || 0;
  const end = code.selectionEnd || 0;
  const before = code.value.slice(0, start);
  const line = before.split('\n').length;
  const lineStart = before.lastIndexOf('\n') + 1;
  const col = start - lineStart + 1;
  const selected = end > start ? ' · 选中 ' + (end - start) : '';
  const pos = $('editorPos');
  const chars = $('editorChars');
  if (pos) pos.textContent = 'Ln ' + line + ', Col ' + col + selected;
  if (chars) chars.textContent = code.value.length + ' 字符 · ' + code.value.split('\n').length + ' 行';
}

function updateEditorActiveLine() {
  const code = $('code');
  const lineEl = $('codeActiveLine');
  if (!code || !lineEl) return;
  const before = code.value.slice(0, code.selectionStart || 0);
  const lineIndex = before.split('\n').length - 1;
  const top = CPP_EDITOR_PAD + lineIndex * CPP_EDITOR_LINE - code.scrollTop;
  if (top < -CPP_EDITOR_LINE || top > code.clientHeight) {
    lineEl.style.opacity = '0';
    return;
  }
  lineEl.style.top = Math.max(0, top) + 'px';
  lineEl.style.height = CPP_EDITOR_LINE + 'px';
  lineEl.style.opacity = '1';
}

function editorSetValue(value, start, end) {
  const code = $('code');
  code.value = value;
  code.selectionStart = start;
  code.selectionEnd = end;
  refreshCodeEditor();
  saveCode();
}

function currentCodeLine(pos) {
  const code = $('code');
  const lineStart = code.value.lastIndexOf('\n', Math.max(0, pos - 1)) + 1;
  let lineEnd = code.value.indexOf('\n', pos);
  if (lineEnd < 0) lineEnd = code.value.length;
  return { lineStart, lineEnd };
}

function handleEditorTab(outdent) {
  const code = $('code');
  const s = code.selectionStart;
  const e = code.selectionEnd;
  if (s === e && !outdent) {
    editorSetValue(code.value.slice(0, s) + '    ' + code.value.slice(e), s + 4, s + 4);
    return;
  }
  if (s === e && outdent) {
    const { lineStart } = currentCodeLine(s);
    const line = code.value.slice(lineStart, s);
    const spaces = line.match(/ *$/)[0].length;
    if (!spaces) return;
    const cut = Math.min(4, spaces);
    editorSetValue(code.value.slice(0, s - cut) + code.value.slice(s), s - cut, s - cut);
    return;
  }
  const start = code.value.lastIndexOf('\n', Math.max(0, s - 1)) + 1;
  const end = code.value.indexOf('\n', Math.max(s, e - 1));
  const blockEnd = end < 0 ? code.value.length : end;
  const lines = code.value.slice(start, blockEnd).split('\n');
  let removed = 0;
  let added = 0;
  const newLines = lines.map((line) => {
    if (outdent) {
      const match = line.match(/^(    |\t)/);
      if (match) { removed += match[0].length; return line.slice(match[0].length); }
      return line;
    }
    added += 4;
    return '    ' + line;
  });
  const newBlock = newLines.join('\n');
  const firstLineLen = lines[0] ? lines[0].length : 0;
  const newFirstLen = newLines[0] ? newLines[0].length : 0;
  const firstDelta = newFirstLen - firstLineLen;
  const delta = newBlock.length - (blockEnd - start);
  const newStart = Math.max(start, s + (outdent ? Math.min(0, firstDelta) : 4));
  const newEnd = Math.max(newStart, e + delta);
  editorSetValue(
    code.value.slice(0, start) + newBlock + code.value.slice(blockEnd),
    Math.min(newStart, start + newBlock.length),
    Math.min(newEnd, start + newBlock.length)
  );
}

function handleEditorEnter() {
  const code = $('code');
  const s = code.selectionStart;
  const e = code.selectionEnd;
  const { lineStart } = currentCodeLine(s);
  const before = code.value.slice(lineStart, s);
  const after = code.value.slice(e, code.value.indexOf('\n', e) < 0 ? code.value.length : code.value.indexOf('\n', e));
  const indent = before.match(/^[ \t]*/)[0];
  const trimmed = before.trim();
  const betweenBraces = trimmed.endsWith('{') && after.trimStart().startsWith('}');
  let insert = '';
  let caret = 0;
  if (betweenBraces) {
    insert = '\n' + indent + '    \n' + indent;
    caret = s + 1 + indent.length + 4;
  } else {
    const extra = trimmed.endsWith('{') || /^(case\s|default\s)/.test(trimmed) ? '    ' : '';
    insert = '\n' + indent + extra;
    caret = s + insert.length;
  }
  editorSetValue(code.value.slice(0, s) + insert + code.value.slice(e), caret, caret);
}

function handleEditorPair(key) {
  const code = $('code');
  const s = code.selectionStart;
  const e = code.selectionEnd;
  if (e > s) {
    const pairs = { '(': ')', '[': ']', '{': '}', '"': '"', "'": "'" };
    if (pairs[key]) {
      editorSetValue(code.value.slice(0, s) + key + code.value.slice(s, e) + pairs[key] + code.value.slice(e), s + 1, e + 1);
      return true;
    }
    return false;
  }
  const pairs = { '(': ')', '[': ']', '{': '}' };
  if (!pairs[key] || code.value[s] === pairs[key]) return false;
  editorSetValue(code.value.slice(0, s) + key + pairs[key] + code.value.slice(e), s + 1, s + 1);
  return true;
}

function handleEditorKeydown(e) {
  if (e.isComposing || e.keyCode === 229) return;
  const code = $('code');
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') return;
  if ((e.ctrlKey || e.metaKey) && (e.key === ' ' || e.code === 'Space')) {
    e.preventDefault();
    updateCodeSuggest(true);
    return;
  }
  if (editorUI.suggest.open) {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      moveCodeSuggest(e.key === 'ArrowDown' ? 1 : -1);
      return;
    }
    if (e.key === 'Enter' || e.key === 'Tab') {
      e.preventDefault();
      acceptCodeSuggest(editorUI.suggest.index);
      return;
    }
    if (e.key === 'Escape') {
      e.preventDefault();
      hideCodeSuggest();
      return;
    }
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') hideCodeSuggest();
  }
  if (e.key === 'Tab') {
    e.preventDefault();
    hideCodeSuggest();
    handleEditorTab(e.shiftKey);
    return;
  }
  if (e.key === 'Enter') {
    e.preventDefault();
    hideCodeSuggest();
    handleEditorEnter();
    return;
  }
  if (e.key === 'Backspace' && code.selectionStart === code.selectionEnd && code.selectionStart > 0) {
    const pos = code.selectionStart;
    const before = code.value[pos - 1];
    const after = code.value[pos];
    const pairs = { '(': ')', '[': ']', '{': '}', '"': '"', "'": "'" };
    if (pairs[before] === after) {
      e.preventDefault();
      editorSetValue(code.value.slice(0, pos - 1) + code.value.slice(pos + 1), pos - 1, pos - 1);
      return;
    }
  }
  if ((e.key === '}' || e.key === ')' || e.key === ']' || e.key === "'" || e.key === '"') &&
      code.selectionStart === code.selectionEnd) {
    const pos = code.selectionStart;
    if (pos < code.value.length && code.value[pos] === e.key) {
      e.preventDefault();
      code.selectionStart = code.selectionEnd = pos + 1;
      updateEditorStatus();
      updateEditorActiveLine();
      return;
    }
    if (e.key === '}') {
      const { lineStart } = currentCodeLine(pos);
      const before = code.value.slice(lineStart, pos);
      if (!before.trim() && before.length >= 4) {
        e.preventDefault();
        const cut = Math.min(4, before.length);
        editorSetValue(code.value.slice(0, pos - cut) + '}' + code.value.slice(pos), pos - cut + 1, pos - cut + 1);
        return;
      }
    }
  }
  if (!e.ctrlKey && !e.metaKey && !e.altKey && { '(': 1, '[': 1, '{': 1 }[e.key]) {
    if (handleEditorPair(e.key)) e.preventDefault();
  }
}

function codeCaretInStringOrComment() {
  const code = $('code');
  const pos = code.selectionStart || 0;
  const before = code.value.slice(0, pos);
  const lineStart = before.lastIndexOf('\n') + 1;
  let line = before.slice(lineStart);
  if (line.includes('//')) return true;
  if (before.lastIndexOf('/*') > before.lastIndexOf('*/')) return true;
  let inString = false;
  let escaped = false;
  for (const ch of line) {
    if (escaped) { escaped = false; continue; }
    if (ch === '\\') { escaped = true; continue; }
    if (ch === '"') inString = !inString;
  }
  return inString;
}

function updateCodeSuggest(force) {
  const code = $('code');
  const suggestEl = $('codeSuggest');
  if (!code || !suggestEl) return;
  if (document.activeElement !== code) return hideCodeSuggest();
  if (code.selectionEnd !== code.selectionStart) return hideCodeSuggest();
  if (!force && codeCaretInStringOrComment()) return hideCodeSuggest();
  const pos = code.selectionStart;
  const lineStart = code.value.lastIndexOf('\n', Math.max(0, pos - 1)) + 1;
  const lineBefore = code.value.slice(lineStart, pos);
  const match = lineBefore.match(/[A-Za-z_][A-Za-z0-9_:]*$/);
  const prefix = match ? match[0] : '';
  if (!force && !prefix) return hideCodeSuggest();
  if (prefix.length > 28) return hideCodeSuggest();
  const lower = prefix.toLowerCase();
  const items = [];
  const seen = new Set();
  const push = (item) => {
    if (!item || seen.has(item.label)) return;
    if (lower && !item.label.toLowerCase().startsWith(lower)) return;
    seen.add(item.label);
    items.push(item);
  };
  if (prefix.includes('::')) {
    CPP_EDITOR_SUGGEST_BASE.filter((item) => item.label.includes('::')).forEach(push);
  } else {
    CPP_EDITOR_SUGGEST_BASE.filter((item) => !item.label.includes('::')).forEach(push);
  }
  const identifierRe = /\b[A-Za-z_][A-Za-z0-9_]*\b/g;
  const codeIds = new Map();
  let m;
  while ((m = identifierRe.exec(code.value)) !== null) {
    const word = m[0];
    if (word === prefix || CPP_EDITOR_KEYWORDS.has(word) || CPP_EDITOR_TYPES.has(word) ||
        CPP_EDITOR_CONTROL.has(word) || CPP_EDITOR_BUILTINS.has(word)) continue;
    codeIds.set(word, (codeIds.get(word) || 0) + 1);
  }
  [...codeIds.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).forEach(([word]) => {
    push({ label: word, kind: 'id', detail: '当前代码', insert: word, cursorOffset: null });
  });
  if (!items.length) return hideCodeSuggest();
  const weight = { kw: 0, ty: 1, bi: 2, fn: 3, id: 4 };
  items.sort((a, b) => {
    const ap = a.label.toLowerCase().startsWith(lower) ? 0 : 1;
    const bp = b.label.toLowerCase().startsWith(lower) ? 0 : 1;
    return ap - bp || (weight[a.kind] ?? 5) - (weight[b.kind] ?? 5) ||
      a.label.length - b.label.length || a.label.localeCompare(b.label);
  });
  editorUI.suggest.open = true;
  editorUI.suggest.items = items.slice(0, 10);
  editorUI.suggest.index = 0;
  editorUI.suggest.wordStart = pos - prefix.length;
  editorUI.suggest.prefix = prefix;
  renderCodeSuggest();
}

function renderCodeSuggest() {
  const el = $('codeSuggest');
  if (!el) return;
  const items = editorUI.suggest.items;
  const head = '<div class="code-suggest-head"><b>C++ 补全</b><span>↑↓ 选择 · Enter 插入</span></div>';
  el.innerHTML = head + items.map((item, i) =>
    '<div class="sug-item' + (i === editorUI.suggest.index ? ' active' : '') + '" data-index="' + i + '">' +
      '<span class="sug-kind ' + item.kind + '">' + (item.kind === 'id' ? 'V' : item.kind === 'fn' ? 'F' : item.kind === 'ty' ? 'T' : item.kind === 'bi' ? 'B' : 'K') + '</span>' +
      '<span class="sug-label">' + esc(item.label) + '</span>' +
      '<span class="sug-detail">' + esc(item.detail) + '</span>' +
    '</div>'
  ).join('');
  el.hidden = false;
  positionCodeSuggest();
}

function positionCodeSuggest() {
  const el = $('codeSuggest');
  const code = $('code');
  if (!el || !code || el.hidden) return;
  const rect = code.getBoundingClientRect();
  const pos = code.selectionStart || 0;
  const before = code.value.slice(0, pos);
  const lineStart = before.lastIndexOf('\n') + 1;
  const lineText = before.slice(lineStart);
  const probe = document.createElement('div');
  const cs = getComputedStyle(code);
  probe.style.cssText = 'position:fixed;left:-10000px;top:0;visibility:hidden;margin:0;border:0;padding:0;' +
    'white-space:pre;font-family:' + cs.fontFamily + ';font-size:' + cs.fontSize + ';font-weight:' + cs.fontWeight +
    ';letter-spacing:' + cs.letterSpacing + ';line-height:' + cs.lineHeight + ';tab-size:' + cs.tabSize;
  probe.textContent = lineText;
  const marker = document.createElement('span');
  marker.textContent = '|';
  probe.appendChild(marker);
  document.body.appendChild(probe);
  const leftInside = marker.getBoundingClientRect().left - probe.getBoundingClientRect().left;
  probe.remove();
  const lineIndex = before.split('\n').length - 1;
  let x = rect.left + 15 + leftInside - code.scrollLeft;
  let y = rect.top + 13 + lineIndex * CPP_EDITOR_LINE - code.scrollTop + CPP_EDITOR_LINE;
  const width = Math.min(286, window.innerWidth - 18);
  el.style.width = width + 'px';
  const height = el.offsetHeight;
  if (x + width > window.innerWidth - 9) x = window.innerWidth - width - 9;
  if (x < 9) x = 9;
  if (y + height > window.innerHeight - 9) y = rect.top + 13 + lineIndex * CPP_EDITOR_LINE - code.scrollTop - height - 4;
  if (y < 9) y = 9;
  el.style.left = Math.round(x) + 'px';
  el.style.top = Math.round(y) + 'px';
}

function moveCodeSuggest(direction) {
  if (!editorUI.suggest.open || !editorUI.suggest.items.length) return;
  const n = editorUI.suggest.items.length;
  editorUI.suggest.index = (editorUI.suggest.index + direction + n) % n;
  document.querySelectorAll('#codeSuggest .sug-item').forEach((el, i) => {
    el.classList.toggle('active', i === editorUI.suggest.index);
  });
  const active = document.querySelector('#codeSuggest .sug-item.active');
  if (active) active.scrollIntoView({ block: 'nearest' });
}

function acceptCodeSuggest(index) {
  const item = editorUI.suggest.items[index];
  if (!item) return;
  const code = $('code');
  const start = editorUI.suggest.wordStart;
  const end = code.selectionEnd;
  const next = code.value.slice(end).match(/^\s*(.)/);
  const nextChar = next ? next[1] : '';
  let insert = item.insert;
  if (item.cursorOffset != null && nextChar === '(' && insert.endsWith('()')) {
    insert = item.label;
  }
  const caret = start + (item.cursorOffset != null && insert !== item.label ? item.cursorOffset : insert.length);
  editorSetValue(code.value.slice(0, start) + insert + code.value.slice(end), caret, caret);
  hideCodeSuggest();
  code.focus();
}

function hideCodeSuggest() {
  const el = $('codeSuggest');
  if (el) el.hidden = true;
  editorUI.suggest.open = false;
  editorUI.suggest.items = [];
}

function setupCodeEditor() {
  const code = $('code');
  if (!code || editorUI.ready) return;
  editorUI.ready = true;
  const suggestEl = $('codeSuggest');
  if (suggestEl && suggestEl.parentElement !== document.body) document.body.appendChild(suggestEl);
  code.addEventListener('input', () => {
    refreshCodeEditor();
    saveCode();
    clearTimeout(editorUI.suggestTimer);
    editorUI.suggestTimer = setTimeout(() => updateCodeSuggest(false), 35);
  });
  code.addEventListener('scroll', () => {
    syncEditorScroll();
    hideCodeSuggest();
  });
  code.addEventListener('keydown', handleEditorKeydown);
  code.addEventListener('click', () => { updateEditorStatus(); updateEditorActiveLine(); hideCodeSuggest(); });
  code.addEventListener('keyup', () => { updateEditorStatus(); updateEditorActiveLine(); });
  code.addEventListener('blur', () => setTimeout(hideCodeSuggest, 120));
  if (suggestEl) {
    suggestEl.addEventListener('mousedown', (e) => {
      const item = e.target.closest('.sug-item');
      if (!item) return;
      e.preventDefault();
      acceptCodeSuggest(Number(item.dataset.index));
    });
  }
  window.addEventListener('resize', hideCodeSuggest);
  window.addEventListener('scroll', hideCodeSuggest, true);
  document.addEventListener('mousedown', (e) => {
    if (e.target === code || (suggestEl && suggestEl.contains(e.target))) return;
    hideCodeSuggest();
  });
  refreshCodeEditor();
}

function saveCode() {
  if (!state.current) return;
  try {
    localStorage.setItem('oj.code.' + state.current.id, $('code').value);
  } catch (e) { /* 忽略容量问题 */ }
}

const CODE_FILE_RE = /\.(cpp|cc|cxx|c|h|hpp|txt)$/i;

function importCodeFile(file, autoSubmit) {
  if (!file) return;
  if (!CODE_FILE_RE.test(file.name)) {
    toast('请选择 .cpp / .c / .h / .txt 代码文件');
    return;
  }
  if (file.size > 2 * 1024 * 1024) {
    toast('文件超过 2 MB，请检查是否选错了文件');
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    let text = '';
    const buf = reader.result;
    try {
      text = new TextDecoder('utf-8', { fatal: true }).decode(buf);
    } catch (e) {
      try {
        text = new TextDecoder('gb18030').decode(buf);
      } catch (e2) {
        toast('文件编码无法识别，请另存为 UTF-8 后重试');
        return;
      }
    }
    text = text.replace(/^\uFEFF/, '');
    if (!text.trim()) { toast('文件内容是空的'); return; }
    setCode(text);
    if (autoSubmit) {
      if (state.current && state.current.test_count > 0) {
        toast('已载入 ' + file.name + '，正在提交');
        submit();
      } else {
        toast('已载入 ' + file.name + '，请先选择一道可判题的题目');
      }
    } else {
      toast('已导入 ' + file.name + '，点「提交评测」即可判题');
    }
    $('code').focus();
  };
  reader.onerror = () => toast('读取文件失败，请换一个文件重试');
  reader.readAsArrayBuffer(file);
}

function codeFileBaseName() {
  const p = state.current;
  const raw = p
    ? ((p.id || '') + '_' + (p.title || ''))
    : 'local_oj_code';
  const safe = String(raw).replace(/[\\/:*?"<>|\r\n\t]+/g, '_').replace(/\s+/g, '_')
    .replace(/_+/g, '_').replace(/^_+|_+$/g, '');
  return (safe || 'local_oj_code').slice(0, 72);
}

async function saveCodeFile() {
  const code = $('code').value;
  if (!code.trim()) { toast('代码还是空的，先写一点再保存'); return; }
  const filename = codeFileBaseName() + '.cpp';
  // Chromium / Edge 支持真正的“另存为”位置选择；桌面端不支持时退回下载。
  if (window.showSaveFilePicker) {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: filename,
        types: [{ description: 'C++ 源文件', accept: { 'text/x-c++src': ['.cpp'] } }],
      });
      const writable = await handle.createWritable();
      await writable.write(code.endsWith('\n') ? code : code + '\n');
      await writable.close();
      toast('已保存到 ' + (handle.name || filename));
      return;
    } catch (e) {
      if (e && e.name === 'AbortError') return;
      // 其他异常（例如桌面端权限受限）继续走下载兜底。
    }
  }
  const blob = new Blob([code.endsWith('\n') ? code : code + '\n'], { type: 'text/x-c++src;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
  toast('已下载 ' + filename);
}

/* ================= AI 助教 ================= */
const AI_PRESETS = {
  deepseek: { base: 'https://api.deepseek.com/v1', model: 'deepseek-chat' },
  openai: { base: 'https://api.openai.com/v1', model: 'gpt-4o-mini' },
  siliconflow: { base: 'https://api.siliconflow.cn/v1', model: 'deepseek-ai/DeepSeek-V3' },
  custom: { base: '', model: '' },
};
const AI_SYSTEM = `你是本地 OJ 的 C++ 算法助教，面向正在准备蓝桥杯、计算机等级考试和算法入门的学生。
回答要求：
1. 用简体中文，先给结论，再分步骤解释；代码用 C++17。
2. 优先讲思路和关键不变量，不要一上来甩完整答案；用户明确要完整代码时可以给。
3. 找错时要引用用户当前代码里的具体行或写法，指出最可能的错误，并给最小修改。
4. 不要编造题目没有给出的数据范围、样例或测试结果。
5. 如果信息不足，明确说需要什么，不要猜。`;

const AI_MODES = {
  coach: {
    label: '教练',
    sub: '一步步提示，不直接代写',
    extra: '当前模式：教练。不要直接给完整代码；先给一个可执行的小提示，再等用户尝试。除非用户明确要求完整代码。',
    quick: [
      ['p1', '给我一个提示', '先不要给完整代码或完整做法。只给我一个能马上动手尝试的提示，指出应该先观察什么。'],
      ['p2', '我卡住了', '我卡住了。请判断我可能卡在哪一步，给一个更小的例子或一个反问，帮我往下走。'],
      ['p3', '下一步怎么想', '基于我当前的代码和思路，告诉我下一步只需要想清楚什么，不要一次讲完整道题。'],
      ['p4', '检查边界', '只检查边界和特殊情况：空输入、最小规模、最大值、重复值、负数或取模，指出我可能漏掉哪一个。'],
    ],
  },
  debug: {
    label: '诊断',
    sub: '对着代码和判题结果找错',
    extra: '当前模式：诊断。重点检查当前代码的具体错误；引用变量名、循环边界或状态转移。先给最可能的 1 个原因，再给最小修改，不要重写整份代码。',
    quick: [
      ['p1', '为什么没通过', '结合最近判题结果，指出当前代码最可能错在哪里，并解释为什么会错。'],
      ['p2', '检查循环边界', '专门检查循环、下标、边界和初始化，列出你怀疑的具体位置。'],
      ['p3', '解释这组数据', '用最近失败的输入，手算一遍程序应该怎么走，指出在哪一步偏离了期望输出。'],
      ['p4', '给最小修改', '不要重写整份代码，只给最少需要改的行，并说明修改理由。'],
    ],
  },
  data: {
    label: '造数据',
    sub: '生成边界/随机输入，一键自测',
    extra: '当前模式：造数据。只输出 2 到 3 组测试输入，每组放在一个 ```input 代码块里；不要解释，不要输出答案。覆盖边界、最小规模、重复值或极端值。',
    quick: [
      ['p1', '造边界数据', '为这道题生成 3 组最容易暴露错误的边界输入，放在 input 代码块里。'],
      ['p2', '造最小数据', '生成最小规模、空输入或只有 1 个元素的测试输入。'],
      ['p3', '造随机数据', '生成一组中等规模随机输入，数值范围覆盖题目允许的范围。'],
      ['p4', '对拍思路', '告诉我怎么用暴力程序对拍，并给一组适合对拍的小输入。'],
    ],
  },
  code: {
    label: '代码',
    sub: '给可提交代码，一键插入编辑器',
    extra: '当前模式：代码。给出完整可提交的 C++17 代码，放在 ```cpp 代码块里；代码要包含 #include <bits/stdc++.h>，并简要说明复杂度。',
    quick: [
      ['p1', '给完整代码', '请给出完整可提交的 C++17 代码，放在 cpp 代码块里，并说明复杂度。'],
      ['p2', '换一种写法', '在能通过的前提下换一种更直观或更稳的写法，仍给完整 cpp 代码。'],
      ['p3', '逐行解释', '逐行解释你给出的关键代码，重点讲不变量和边界。'],
      ['p4', '压缩代码', '在不影响可读性的前提下压缩代码，并说明哪些部分不能省。'],
    ],
  },
  review: {
    label: '复盘',
    sub: '沉淀题解、模板和易错点',
    extra: '当前模式：复盘。输出结构化题解笔记：题目模型、关键思路、复杂度、易错点、可复用模板。用 Markdown 小标题，不要写空话。',
    quick: [
      ['p1', '总结这道题', '把这道题总结成一段可复习的题解笔记，包含模型、思路、复杂度和易错点。'],
      ['p2', '提炼模板', '提炼这道题可复用的代码模板，指出哪些变量和边界需要按题目修改。'],
      ['p3', '和相似题对比', '根据题目标签，指出它和哪些题型容易混淆，并说明区分方法。'],
      ['p4', '写复盘清单', '给我一份 5 条以内的复盘清单，方便下次遇到同类题快速检查。'],
    ],
  },
  gen: {
    label: '出题',
    sub: '按难度和内容生成可判题',
    extra: '当前模式：出题。你正在协助用户生成一道可判题的新题。只输出符合 JSON schema 的题目对象，不要输出解释。',
    quick: [
      ['p1', '生成一道新题', '请用当前设置生成一道可判题的新题。'],
      ['p2', '提高一个难度', '把目标难度提高一档，重新生成一道题。'],
      ['p3', '换一个场景', '保留知识点，但换一个完全不同的生活场景重新出题。'],
      ['p4', '再补边界用例', '检查并补充最小、最大和极端边界测试用例。'],
    ],
  },
};

const AI_GEN_DIFFICULTY = {
  1: { label: '入门', guide: '单一条件/循环/输入输出，10–20 行可完成；不引入复杂数据结构。' },
  2: { label: '基础', guide: '模拟、排序、前缀和、简单贪心或基础容器，15–30 行；有一个小转化。' },
  3: { label: '提高', guide: '二分、DP、图搜索、并查集等常见算法，需要建模；25–45 行。' },
  4: { label: '进阶', guide: '两个以上知识点组合、复杂状态设计或明显思维拐点；40–70 行。' },
  5: { label: '挑战', guide: '竞赛级综合题，约束紧、需要优化或较难的观察；70 行以上。' },
};

const AI_GEN_SPEC = `你是一名严谨的算法竞赛出题助教。你的任务不是讲解，而是生成一道可以直接放进本地 OJ、能被 g++ 判题的新题。

【唯一输出格式】
只输出一个 JSON 对象，不要 Markdown 围栏，不要前后解释。字段如下：
{
  "title": "简洁独特的中文标题，不超过 24 个汉字",
  "statement_md": "完整题面，可用 Markdown，必须自包含",
  "input_md": "输入格式",
  "output_md": "输出格式",
  "constraints_md": "数据范围与特殊约定",
  "samples": [{"in": "样例输入（真实换行用 \\n）", "out": "样例输出"}],
  "tests": [{"in": "测试输入", "out": "唯一正确输出"}, ...],
  "solution": "#include <bits/stdc++.h>\\n...完整 C++17 参考代码...",
  "hint_md": "一段渐进式提示，不直接给答案",
  "hints": ["第一层提示", "第二层提示", "第三层提示"],
  "tags": ["2-4 个知识点标签"]
}

【硬性规范】
1. 题面完整：背景、输入、输出、数据范围、至少 1 组样例；禁止“见原题”“同上”之类。
2. 可判题：tests 必须有 4–6 组，且一定包含 sample；覆盖最小规模、边界/重复/负数、最大或极端情况。每组的 in/out 必须是确定、精确的字符串，不能有解释或代码围栏。
3. 参考答案：C++17，第一行必须是 #include <bits/stdc++.h>；代码必须能在 1 秒内通过全部 tests，输出与 tests 完全一致。不要依赖随机、时间、文件或交互。
4. 数据规模要适合本地评测：建议 n ≤ 2×10^5，答案在 64 位整数范围内；如使用取模，必须在题面写清楚。
5. 难度必须与目标一致；难度越高，建模、算法或细节要求越高，不能只把数据范围改大。
6. 原创：先在心里比较至少两个不同的题目机制，选最不像常见模板题的一个。不要与已有题目同名，不要只给旧题换情景/换地名/换角色，不要把原书段落照抄进题面。若提供原书选段，只提炼其中的知识点、方法或易错点，再设计新的故事、数据和问题。
7. 自检：输出前逐个对照 samples[0] 与 tests[0]，核对所有 tests 的 out 确实由 solution 产生；检查 tests 覆盖最小、边界、极端；检查 solution 第一行确实是 #include <bits/stdc++.h>。
8. 提示只给方向，不泄露完整做法；不要输出答案或测试数据的解释。
9. 标题和题面要能被学生直接读懂；专有名词先解释再使用。
10. 数学公式：题面可以用 $...$ 包裹 LaTeX；但 JSON 字符串里的反斜杠要按 JSON 规则双写（例如 \\dots、\\le），或者优先直接使用 Unicode（…、≤、∈）。不要把 \\dots 这类反斜杠裸写进 JSON，否则会解析失败。公式保持短小，只用基本符号、上下标、分数和根号，不要使用复杂宏包或 \\begin{...}。
11. 先在心里写出参考答案，再根据参考答案的实际行为生成 tests；tests 必须正好 4～6 组，宁可少写题面，也不要把 JSON 截断。`;

let aiConfig = null;
let aiHistory = [];
let aiProblemId = null;
let aiBusy = false;
let aiMode = 'coach';
let aiTranscript = [];
let aiGenBusy = false;
let aiDebugPending = null;

function loadAIConfig() {
  const fallback = { provider: 'deepseek', ...AI_PRESETS.deepseek, key: '' };
  try {
    const raw = JSON.parse(localStorage.getItem('oj.ai.config') || 'null');
    if (raw && typeof raw === 'object') {
      return {
        provider: AI_PRESETS[raw.provider] ? raw.provider : 'custom',
        base: String(raw.base || fallback.base),
        model: String(raw.model || fallback.model),
        key: String(raw.key || ''),
      };
    }
  } catch (e) { /* 配置损坏时用默认值 */ }
  return fallback;
}

function persistAIConfig() {
  try { localStorage.setItem('oj.ai.config', JSON.stringify(aiConfig)); } catch (e) { }
}

function aiRenderConfigState() {
  const el = $('aiConfigState');
  if (!el) return;
  const has = aiConfig && aiConfig.key;
  el.textContent = has ? ('已配置 · ' + (aiConfig.model || '未填模型')) : '未配置 API Key';
  el.classList.toggle('ok', !!has);
  $('aiConfig').classList.toggle('hide', !!has);
}

function aiApplyProvider(p) {
  const preset = AI_PRESETS[p];
  $('aiProvider').value = p;
  if (p !== 'custom' && preset) {
    $('aiBase').value = preset.base;
    $('aiModel').value = preset.model;
  }
}

function aiResetForProblem(pid) {
  if (aiProblemId === pid) return;
  aiProblemId = pid;
  aiHistory = [];
  aiTranscript = [];
  aiBookQuote = null;
  const box = $('aiMessages');
  if (box) box.innerHTML = '';
  const welcome = $('aiWelcome');
  if (welcome) welcome.style.display = '';
  aiRenderGenQuote();
  aiUpdateContext();
}

function aiUpdateContext() {
  const el = $('aiContext');
  if (!el) return;
  const p = state.current;
  if (!p) {
    el.textContent = aiBookQuote ? '原书选段 · 未选题' : (aiMode === 'gen' ? 'AI 出题 · 自由出题' : (currentView === 'book' ? '原书阅读 · 未选题' : '当前未选题'));
    return;
  }
  const verdict = state.lastResult && state.lastResult.verdict ? verdictText(state.lastResult.verdict) : '未提交';
  let text = (p.label || p.id) + ' · ' + (p.title || '') + ' · ' + verdict;
  if (aiBookQuote) text += ' · 原书选段';
  el.textContent = text;
}

function aiSetMode(mode) {
  if (!AI_MODES[mode]) return;
  aiMode = mode;
  document.querySelectorAll('#aiModes .ai-mode').forEach((b) => {
    b.classList.toggle('on', b.dataset.aiMode === mode);
  });
  const conf = AI_MODES[mode];
  $('aiSub').textContent = conf.sub;
  const isGen = mode === 'gen';
  if ($('aiGenPanel')) $('aiGenPanel').classList.toggle('hide', !isGen);
  if (isGen) aiGenSetCollapsed(false);
  if ($('aiQuick')) $('aiQuick').classList.toggle('hide', isGen);
  const quick = $('aiQuick');
  if (quick && !isGen) {
    quick.querySelectorAll('button').forEach((b, i) => {
      const item = conf.quick[i];
      if (!item) return;
      b.dataset.aiPrompt = item[2];
      b.textContent = item[1];
    });
  }
  if (isGen) aiRenderGenQuote();
  $('aiInput').placeholder = isGen
    ? '也可以直接写下出题要求，Enter 生成题目'
    : '用「' + conf.label + '」模式提问，Enter 发送，Shift+Enter 换行';
  aiUpdateContext();
}

function aiCopyText(text, tip) {
  const done = () => toast(tip || '已复制');
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => aiCopyTextFallback(text, done));
  } else {
    aiCopyTextFallback(text, done);
  }
}

function aiCopyTextFallback(text, done) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); done(); } catch (e) { toast('复制失败'); }
  ta.remove();
}

function aiActionButton(label, cls, fn) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'ai-code-action ' + (cls || '');
  b.textContent = label;
  b.onclick = fn;
  return b;
}

function aiEnhanceAnswer(el, rawText) {
  const text = String(rawText || '');
  el.querySelectorAll('pre').forEach((pre) => {
    const lang = String(pre.dataset.lang || '').toLowerCase();
    const code = pre.textContent || '';
    const isCpp = ['cpp', 'c++', 'cc', 'cxx', 'c'].includes(lang) || /#include\s*</.test(code);
    const isInput = ['input', 'test', 'stdin', 'sample', 'in'].includes(lang);
    if (!code.trim()) return;
    const bar = document.createElement('div');
    bar.className = 'ai-code-actions';
    if (isCpp) {
      bar.appendChild(aiActionButton('插入编辑器', 'strong', () => {
        setCode(code.replace(/\s+$/, '') + '\n');
        toast('已插入编辑器');
      }));
    }
    if (isInput) {
      bar.appendChild(aiActionButton('填入自测输入', 'strong', () => {
        $('selfInput').value = code.replace(/\s+$/, '') + '\n';
        showConsole(true);
        updateInputLines();
        toast('已填入控制台，点“运行”自测');
      }));
    }
    bar.appendChild(aiActionButton('复制', '', () => aiCopyText(code, '代码已复制')));
    pre.parentNode.insertBefore(bar, pre.nextSibling);
  });
  if (text.trim()) {
    const foot = document.createElement('div');
    foot.className = 'ai-msg-foot';
    foot.appendChild(aiActionButton('复制回答', '', () => aiCopyText(text, '回答已复制')));
    el.appendChild(foot);
  }
}

function aiExport() {
  if (!state.current) { toast('先选一道题'); return; }
  const p = state.current;
  const items = aiTranscript.map((m) => {
    return '### ' + (m.role === 'user' ? '我' : 'AI 助教') + '\n\n' + String(m.text || '').trim();
  });
  const md = '# ' + (p.label || p.id) + ' ' + (p.title || '') + '\n\n' +
    '> 由本地 OJ AI 助教导出 · ' + new Date().toLocaleString('zh-CN') + '\n\n' +
    (items.join('\n\n') || '（还没有对话）') + '\n';
  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'AI助教-' + (p.label || p.id) + '.md';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  toast('对话已导出');
}

function aiOpen() {
  hideAiDebugSuggest();
  const noContext = !state.current && !aiBookQuote && currentView !== 'book';
  if (noContext && aiMode !== 'gen') aiSetMode('gen');
  aiUpdateContext();
  aiRenderGenQuote();
  $('aiBackdrop').classList.remove('hide');
  aiRenderConfigState();
  if (!aiConfig.key) {
    $('aiConfig').classList.remove('hide');
    setTimeout(() => $('aiKey').focus(), 80);
  } else if (aiMode === 'gen') {
    setTimeout(() => $('aiGenTopic').focus(), 80);
  } else {
    setTimeout(() => $('aiInput').focus(), 80);
  }
}

function aiClose() {
  $('aiBackdrop').classList.add('hide');
}

/* ---- CE / WA 后的 AI debug 建议 ---- */
function hideAiDebugSuggest() {
  aiDebugPending = null;
  const el = $('aiDebugSuggest');
  if (el) el.classList.add('hide');
}

function debugSnippet(res, source) {
  if (source === 'run' || res.verdict === 'CE') {
    const msg = String(res.message || '').trim();
    return msg.split('\n').slice(0, 7).join('\n');
  }
  const bad = (res.cases || []).find((c) => c.status !== 'AC');
  if (!bad) return String(res.message || '').trim();
  const clip = (v) => String(v == null ? '' : v).slice(0, 420);
  return '输入\n' + clip(bad.input) + '\n期望输出\n' + clip(bad.expected) + '\n你的输出\n' + clip(bad.actual);
}

function showDebugSuggest(source, res) {
  if (!state.current || !res || (res.verdict !== 'CE' && res.verdict !== 'WA')) {
    hideAiDebugSuggest();
    return;
  }
  aiDebugPending = { source, res, problemId: state.current.id, verdict: res.verdict };
  const isRun = source === 'run';
  const kicker = $('aiDebugKicker');
  const title = $('aiDebugTitle');
  const body = $('aiDebugBody');
  const snippet = $('aiDebugSnippet');
  if (kicker) kicker.textContent = isRun ? 'AI DEBUG · 运行编译失败' : 'AI DEBUG · 提交 WA';
  if (title) title.textContent = isRun ? '编译器先拦住了' : '这组测试没通过';
  if (body) body.textContent = isRun
    ? '要请 AI 助教看编译器报错，并指出最小修改吗？'
    : '要请 AI 助教对着失败输入、期望输出和当前代码找错吗？';
  if (snippet) {
    const text = debugSnippet(res, source);
    snippet.textContent = text;
    snippet.hidden = !text;
  }
  const el = $('aiDebugSuggest');
  if (el) el.classList.remove('hide');
}

function maybeShowDebugSuggest(source, res) {
  if (res && (res.verdict === 'CE' || res.verdict === 'WA')) showDebugSuggest(source, res);
  else hideAiDebugSuggest();
}

function aiDebugPrompt() {
  const p = state.current;
  const pending = aiDebugPending;
  if (!p || !pending) return '';
  const verdict = pending.res && pending.res.verdict === 'CE' ? '编译错误 CE' : '答案错误 WA';
  return '请帮我 debug：这道题「' + (p.label || p.id) + ' ' + (p.title || '') + '」刚才' +
    (pending.source === 'run' ? '运行自测' : '提交') + '的结果是 ' + verdict +
    '。请进入诊断模式：先用一句话指出最可能的错误，引用具体代码、变量或边界；再给最小修改，不要重写整份代码；如果有失败用例，请说明怎样用这组输入复现。';
}

function aiDebugStart() {
  const prompt = aiDebugPrompt();
  if (!prompt) { hideAiDebugSuggest(); return; }
  hideAiDebugSuggest();
  aiSetMode('debug');
  aiOpen();
  if ($('aiInput')) $('aiInput').value = prompt;
  aiUpdateContext();
  if (aiConfig && aiConfig.key) {
    toast('已把错误上下文交给 AI 助教');
    setTimeout(() => aiSend(prompt), 120);
  } else {
    toast('填入 API Key 后即可发送诊断问题');
    setTimeout(() => { if ($('aiKey')) $('aiKey').focus(); }, 80);
  }
}

function aiDebugBind() {
  const el = $('aiDebugSuggest');
  if (!el) return;
  if ($('aiDebugClose')) $('aiDebugClose').onclick = hideAiDebugSuggest;
  if ($('aiDebugLater')) $('aiDebugLater').onclick = () => { hideAiDebugSuggest(); toast('可以先看失败用例和编译器信息'); };
  if ($('aiDebugGo')) $('aiDebugGo').onclick = aiDebugStart;
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !el.classList.contains('hide')) hideAiDebugSuggest();
  });
}

function aiScrollBottom() {
  const s = $('aiScroll');
  if (s) s.scrollTop = s.scrollHeight;
}

function aiAddMessage(role, text, pending) {
  const box = $('aiMessages');
  const div = document.createElement('div');
  div.className = 'ai-msg ' + role + (pending ? ' pending' : '');
  if (role === 'assistant' && pending) {
    div.innerHTML = '<div class="ai-thinking"><i></i><i></i><i></i><span>正在思考</span></div>';
  } else if (role === 'assistant') {
    div.innerHTML = mdToHtml(text);
    aiEnhanceAnswer(div, text);
  } else {
    div.textContent = text;
  }
  box.appendChild(div);
  $('aiWelcome').style.display = 'none';
  aiScrollBottom();
  return div;
}

function aiProblemContext() {
  const p = state.current;
  if (!p) return '当前没有选中题目。';
  const parts = [
    '题号：' + (p.label || p.id) + ' ' + (p.title || ''),
    '题面：' + (p.statement_md || ''),
    '输入格式：' + (p.input_md || ''),
    '输出格式：' + (p.output_md || ''),
    '数据范围：' + (p.constraints_md || ''),
  ];
  const code = $('code').value.trim();
  parts.push('当前代码：\n```cpp\n' + (code ? code.slice(0, 12000) : '（还没写代码）') + '\n```');
  const r = state.lastResult;
  if (r && r.verdict) {
    let s = '最近一次判题：' + verdictText(r.verdict) + '，通过 ' +
      (r.cases || []).filter((c) => c.status === 'AC').length + ' / ' + (r.cases || []).length + '。';
    const bad = (r.cases || []).find((c) => c.status !== 'AC');
    if (bad) {
      s += '\n失败用例：输入\n```\n' + String(bad.input || '').slice(0, 1000) +
        '\n```\n期望输出\n```\n' + String(bad.expected || '').slice(0, 1000) +
        '\n```\n实际输出\n```\n' + String(bad.actual || '').slice(0, 1000) + '\n```';
    }
    if (r.message) s += '\n编译器信息：\n```\n' + String(r.message).slice(0, 1800) + '\n```';
    parts.push(s);
  } else {
    parts.push('最近一次判题：尚未提交。');
  }
  if (aiBookQuote) {
    parts.push('用户刚在原书《' + aiBookQuote.chapter + '》中选中的内容：\n\n> ' +
      String(aiBookQuote.text || '').slice(0, 2400).replace(/\n/g, '\n> '));
  }
  return parts.join('\n\n');
}

async function aiRequest(messages, opts) {
  const options = opts || {};
  const r = await fetch('/api/ai', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: aiConfig.key,
      base_url: aiConfig.base,
      model: aiConfig.model,
      messages,
      max_tokens: options.max_tokens,
      temperature: options.temperature,
      timeout: options.timeout,
    }),
  });
  let data = null;
  try { data = await r.json(); } catch (e) { }
  if (!r.ok) throw new Error((data && data.error) || ('AI 接口请求失败：HTTP ' + r.status));
  if (!data || !data.content) throw new Error('AI 没有返回内容');
  return data;
}

/* ---- AI 出题工作台 ---- */
function aiGenDiff() {
  const el = $('aiGenDifficulty');
  const value = Math.max(1, Math.min(5, Number(el && el.value) || 3));
  const info = AI_GEN_DIFFICULTY[value] || AI_GEN_DIFFICULTY[3];
  if ($('aiGenDiffName')) $('aiGenDiffName').textContent = value + ' · ' + info.label;
  if (el) {
    const pct = ((value - 1) / 4) * 100;
    el.style.setProperty('--gen-fill', pct + '%');
    el.setAttribute('aria-valuetext', value + ' ' + info.label);
  }
  return { value, label: info.label, guide: info.guide };
}

function aiGenSetCollapsed(on) {
  const panel = $('aiGenPanel');
  const btn = $('aiGenToggle');
  if (!panel) return;
  panel.classList.toggle('collapsed', !!on);
  if (btn) btn.textContent = on ? '展开' : '收起';
}

function aiRenderGenQuote() {
  const box = $('aiGenQuote');
  const txt = $('aiGenQuoteText');
  if (!box || !txt) return;
  if (!aiBookQuote) {
    box.classList.add('hide');
    txt.textContent = '';
    return;
  }
  const content = String(aiBookQuote.text || '').replace(/\s+/g, ' ').trim();
  txt.textContent = (aiBookQuote.chapter || '原书') + ' · “' + content.slice(0, 92) + (content.length > 92 ? '…' : '') + '”';
  txt.title = content.slice(0, 1600);
  box.classList.remove('hide');
}

function aiGenPrompt(topic, diff) {
  const p = state.current;
  const parts = [];
  parts.push('【本次出题】');
  parts.push('目标难度：' + diff.value + '（' + diff.label + '）。难度要求：' + diff.guide);
  parts.push(topic
    ? '出题内容 / 要求：' + topic.slice(0, 1400)
    : '出题内容：未指定。请从原书选段或当前题目中提炼一个相邻知识点，或自选一个适合算法入门的原创知识点。');
  if (aiBookQuote) {
    parts.push('用户在原书《' + (aiBookQuote.chapter || '原书') + '》中勾画了以下内容：\n' +
      String(aiBookQuote.text || '').slice(0, 2600).replace(/\n/g, '\n> '));
    parts.push('请只把它当作知识点/方法线索，重新设计故事、数据与问题，不要照抄原文，也不要与当前题库常见题同质化。');
  }
  if (p) {
    parts.push('当前正在做的题（仅供参考，不要照抄题面或直接改数）：\n' +
      (p.label || p.id) + ' ' + (p.title || '') + '\n' +
      String(p.statement_md || '').slice(0, 1400) + '\n数据范围：' + String(p.constraints_md || '').slice(0, 800));
  }
  parts.push('原创性要求：先想一个与常见模板不同的机制，再动笔；不要用“换一个地名/角色但算法和输入输出完全一样”的方式造题。');
  parts.push('请确保题面、样例、tests 和参考答案相互一致；参考答案必须真的能通过全部 tests。');
  parts.push('现在只输出题目 JSON。');
  return parts.join('\n\n');
}

function aiRepairJsonText(source) {
  // 模型经常把 LaTeX 的 \dots、\le 直接塞进 JSON 字符串，导致 JSON.parse
  // 把这些反斜杠当成非法转义。逐字符修复字符串内部的反斜杠与裸换行。
  let s = String(source || '');
  let out = '';
  let inString = false;
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (!inString) {
      out += ch;
      if (ch === '"') inString = true;
      continue;
    }
    if (ch === '"') { inString = false; out += ch; continue; }
    if (ch === '\\') {
      const n = s[i + 1];
      if (!n) { out += '\\\\'; continue; }
      if (n === 'u') {
        const hex = s.slice(i + 2, i + 6);
        if (/^[0-9a-fA-F]{4}$/.test(hex)) { out += '\\u' + hex; i += 5; }
        else out += '\\\\';
        continue;
      }
      if ('"\\/bfnrt'.includes(n)) { out += '\\' + n; i += 1; continue; }
      // 非法 JSON 转义：补一个反斜杠，让 \dots 变成 JSON 里的 \\dots。
      out += '\\\\';
      continue;
    }
    if (ch === '\n') { out += '\\n'; continue; }
    if (ch === '\r') { out += '\\r'; continue; }
    if (ch === '\t') { out += '\\t'; continue; }
    if (ch.charCodeAt(0) < 0x20) {
      out += '\\u' + String(ch.charCodeAt(0)).padStart(4, '0');
      continue;
    }
    out += ch;
  }
  return out;
}

function aiParseGenerated(raw) {
  let s = String(raw || '').trim().replace(/^\uFEFF/, '');
  const fence = s.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fence) s = fence[1].trim();
  const first = s.indexOf('{');
  const last = s.lastIndexOf('}');
  if (first < 0 || last <= first) {
    throw new Error('AI 返回的 JSON 不完整（可能被截断），请重新生成');
  }
  s = s.slice(first, last + 1);
  const candidates = [s, aiRepairJsonText(s)];
  for (const candidate of candidates) {
    for (const text of [candidate, candidate.replace(/,\s*([}\]])/g, '$1')]) {
      try {
        return JSON.parse(text);
      } catch (e) { /* 尝试下一种修复 */ }
    }
  }
  throw new Error('AI 返回的 JSON 无法解析（可能被截断，或公式里的反斜杠未转义），请重新生成');
}

function aiTextValue(...values) {
  const v = values.find((x) => x !== undefined && x !== null && String(x).trim() !== '');
  return v === undefined ? '' : String(v).trim();
}

function aiNormalizeTest(t) {
  if (!t || typeof t !== 'object') return null;
  const input = aiTextValue(t.in, t.input, t.stdin, t.sample_in);
  const output = aiTextValue(t.out, t.output, t.expected, t.stdout, t.sample_out);
  if (!input && !output) return null;
  return { in: input, out: output };
}

function aiNormalizeGenerated(raw, diff) {
  const source = raw && typeof raw === 'object' && raw.problem && typeof raw.problem === 'object'
    ? raw.problem : raw;
  if (!source || typeof source !== 'object') throw new Error('AI 没有返回题目对象');
  const title = aiTextValue(source.title);
  const statement = aiTextValue(source.statement_md, source.statement, source.description);
  const input = aiTextValue(source.input_md, source.input_format, source.input);
  const output = aiTextValue(source.output_md, source.output_format, source.output);
  const constraints = aiTextValue(source.constraints_md, source.constraints, source.constraint);
  const rawSamples = Array.isArray(source.samples) ? source.samples : (Array.isArray(source.sample) ? source.sample : []);
  const rawTests = Array.isArray(source.tests) ? source.tests
    : (Array.isArray(source.testcases) ? source.testcases : (Array.isArray(source.test_cases) ? source.test_cases : []));
  let samples = rawSamples.map(aiNormalizeTest).filter(Boolean);
  let tests = rawTests.map(aiNormalizeTest).filter(Boolean);
  if (!samples.length) samples = tests.slice(0, 1);
  if (!tests.length) tests = samples.slice();
  if (!title || title.length < 2) throw new Error('生成题缺少有效标题');
  if (statement.length < 10) throw new Error('生成题题面过短');
  if (!input || !output || !constraints) throw new Error('生成题缺少输入/输出/数据范围');
  if (!samples.length) throw new Error('生成题缺少样例');
  if (tests.length < 4) throw new Error('AI 只返回了 ' + tests.length + ' 组测试；本地判题至少需要 4 组，请重新生成');
  if (tests.length > 8) tests = tests.slice(0, 8);

  let solution = aiTextValue(source.solution, source.reference_solution, source.solution_code);
  solution = solution.replace(/^```(?:cpp|c\+\+|c)?\s*\n?/i, '').replace(/```\s*$/i, '').trim();
  if (!solution) throw new Error('生成题缺少 C++ 参考答案');
  if (solution.length < 30) throw new Error('生成题参考答案过短');
  if (!/bits\/stdc\+\+\.h/.test(solution)) solution = '#include <bits/stdc++.h>\n' + solution;

  let hints = Array.isArray(source.hints) ? source.hints.map((x) => String(x).trim()).filter(Boolean) : [];
  const hintMd = aiTextValue(source.hint_md, source.hint);
  if (!hints.length && hintMd) hints = hintMd.split('\n').map((x) => x.trim()).filter(Boolean);
  if (!hints.length) hints = ['先读清输入输出和样例，再想需要维护什么状态。', '把步骤拆成读入、更新和输出。', '先测最小规模，再测边界。'];
  const tags = (Array.isArray(source.tags) ? source.tags : String(source.tags || '').split(/[，,、]/))
    .map((x) => String(x).trim()).filter(Boolean).slice(0, 6);
  if (!tags.length) tags.push('AI 原创');

  return {
    title,
    difficulty: diff.value,
    statement_md: statement,
    input_md: input,
    output_md: output,
    constraints_md: constraints,
    samples,
    tests,
    solution,
    hint_md: hintMd || hints.join('\n'),
    hints,
    tags,
    topic: aiTextValue(source.topic, raw && raw.topic, aiGenTopicValue()),
  };
}

function aiGenTopicValue() {
  return $('aiGenTopic') ? String($('aiGenTopic').value || '').trim() : '';
}

function aiGeneratedTestsHtml(gen) {
  const samples = gen.samples.map((t, i) =>
    `<div class="gen-case"><b>样例 ${i + 1}</b><div class="gen-io"><span>in</span><pre>${esc(t.in)}</pre></div><div class="gen-io"><span>out</span><pre>${esc(t.out)}</pre></div></div>`
  ).join('');
  const tests = gen.tests.map((t, i) =>
    `<div class="gen-case"><b>#${i + 1}</b><div class="gen-io"><span>in</span><pre>${esc(t.in)}</pre></div><div class="gen-io"><span>out</span><pre>${esc(t.out)}</pre></div></div>`
  ).join('');
  return `<div class="gen-cases"><h4>样例</h4>${samples}<h4>判题测试 · ${gen.tests.length} 组</h4>${tests}</div>`;
}

function aiShowGenerated(gen) {
  const box = document.createElement('div');
  box.className = 'ai-msg assistant ai-gen-result';
  box.innerHTML = `
    <div class="gen-preview">
      <div class="gen-preview-head">
        <span class="gen-preview-kicker">AI 原创题 · 难度 ${gen.difficulty} · ${gen.tests.length} 组测试</span>
        <h3>${esc(gen.title)}</h3>
        <div class="gen-preview-tags">${gen.tags.map((t) => `<span>${esc(t)}</span>`).join('')}</div>
      </div>
      <div class="gen-preview-statement">${mdToHtml(gen.statement_md)}</div>
      <div class="gen-preview-format">
        <div><b>输入</b>${mdToHtml(gen.input_md)}</div>
        <div><b>输出</b>${mdToHtml(gen.output_md)}</div>
        <div><b>数据范围</b>${mdToHtml(gen.constraints_md)}</div>
      </div>
      <details class="gen-preview-details">
        <summary>展开样例、全部测试与 C++17 参考答案</summary>
        ${aiGeneratedTestsHtml(gen)}
        <h4>参考答案 · 保存时由本机 g++ 校验</h4>
        <pre class="gen-solution">${esc(gen.solution)}</pre>
      </details>
      <div class="gen-preview-error hide"></div>
      <div class="gen-preview-actions">
        <button class="gen-btn gen-save-open" type="button">保存并做题</button>
        <button class="gen-btn gen-save-only" type="button">仅保存到题库</button>
        <button class="gen-btn ghost gen-retry" type="button">重新生成</button>
      </div>
      <div class="gen-preview-state">保存时会把参考答案和全部 tests 交给本机 g++ 预校验；校验通过才会入库。</div>
    </div>`;
  $('aiMessages').appendChild(box);
  $('aiWelcome').style.display = 'none';
  aiGenSetCollapsed(true);
  box.querySelector('.gen-save-open').onclick = () => aiSaveGenerated(gen, true, box);
  box.querySelector('.gen-save-only').onclick = () => aiSaveGenerated(gen, false, box);
  box.querySelector('.gen-retry').onclick = () => aiGenerateProblem();
  aiScrollBottom();
}

async function aiRefreshProblemIndex() {
  const r = await fetch('/api/problems');
  if (!r.ok) throw new Error('题库刷新失败');
  const pr = await r.json();
  state.problems = pr.problems || [];
  state.byId = Object.fromEntries(state.problems.map((p) => [p.id, p]));
  state.open = state.open || {};
  state.open['ai'] = true;
  renderSidebar();
  updateProgressBar();
}

async function aiSaveGenerated(gen, openAfter, card) {
  if (card.dataset.saving === '1') return;
  card.dataset.saving = '1';
  const buttons = [...card.querySelectorAll('.gen-btn')];
  buttons.forEach((b) => { b.disabled = true; });
  const saveOpen = card.querySelector('.gen-save-open');
  const saveOnly = card.querySelector('.gen-save-only');
  const oldLabels = [saveOpen.textContent, saveOnly.textContent];
  saveOpen.textContent = '校验中…';
  saveOnly.textContent = '校验中…';
  const errBox = card.querySelector('.gen-preview-error');
  errBox.classList.add('hide');
  errBox.textContent = '';
  try {
    const r = await fetch('/api/problems/generated', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem: gen, difficulty: gen.difficulty }),
    });
    let data = null;
    try { data = await r.json(); } catch (e) { }
    if (!r.ok) {
      let msg = (data && data.error) || '保存失败：HTTP ' + r.status;
      if (data && data.detail) msg += '\n' + data.detail;
      throw new Error(msg);
    }
    await aiRefreshProblemIndex();
    state.cache = state.cache || {};
    if (data.detail) state.cache[data.id] = data.detail;
    card.dataset.saving = '0';
    card.querySelector('.gen-preview-state').innerHTML =
      '已通过 g++ 校验并入库：<b>' + esc(data.id) + '</b> · ' + (data.test_count || gen.tests.length) + ' 组测试 · 参考答案可查看';
    saveOpen.disabled = true;
    saveOnly.disabled = true;
    saveOpen.textContent = '已保存';
    saveOnly.textContent = '已保存';
    if (openAfter) {
      aiClose();
      setView('oj');
      await selectProblem(data.id, false);
      toast('已保存并载入「' + gen.title + '」，写完代码即可提交评测');
    } else {
      toast('已保存到题库 · AI 题：' + gen.title);
    }
  } catch (e) {
    card.dataset.saving = '0';
    let message = e.message;
    if (message && !message.includes('\n')) message += '\n可以点「重新生成」换一组样例与测试。';
    errBox.textContent = message;
    errBox.classList.remove('hide');
    buttons.forEach((b) => { b.disabled = false; });
    saveOpen.textContent = oldLabels[0];
    saveOnly.textContent = oldLabels[1];
  }
}

async function aiGenerateProblem(overrideTopic) {
  if (aiGenBusy) return;
  if (!aiConfig.key) {
    $('aiConfig').classList.remove('hide');
    $('aiKey').focus();
    toast('先填 API Key 才能让助教出题');
    return;
  }
  if (!aiConfig.base || !aiConfig.model) {
    $('aiConfig').classList.remove('hide');
    toast('接口地址和模型名不能为空');
    return;
  }
  if (overrideTopic !== undefined && $('aiGenTopic')) $('aiGenTopic').value = String(overrideTopic || '').trim();
  aiGenSetCollapsed(false);
  const diff = aiGenDiff();
  const topic = aiGenTopicValue();
  const seedText = topic || (aiBookQuote ? '按原书选段' : (state.current ? '仿照当前知识点' : '自由原创'));
  aiGenBusy = true;
  const go = $('aiGenGo');
  if (go) { go.disabled = true; go.textContent = '生成中…'; }
  aiAddMessage('user', '出题：' + seedText + ' · 难度 ' + diff.value + ' · ' + diff.label);
  const pending = aiAddMessage('assistant', '', true);
  const thinking = pending.querySelector('.ai-thinking span');
  if (thinking) thinking.textContent = '正在写题、配样例和参考代码…';
  try {
    const messages = [
      { role: 'system', content: AI_SYSTEM + '\n\n' + AI_GEN_SPEC },
      { role: 'user', content: aiGenPrompt(topic, diff) },
    ];
    const data = await aiRequest(messages, { max_tokens: 8000, temperature: 0.4, timeout: 150 });
    pending.remove();
    const raw = aiParseGenerated(data.content);
    const gen = aiNormalizeGenerated(raw, diff);
    aiShowGenerated(gen);
  } catch (e) {
    pending.remove();
    const err = aiAddMessage('assistant', '出题失败：' + e.message);
    err.classList.add('error');
    aiScrollBottom();
  } finally {
    aiGenBusy = false;
    if (go) { go.disabled = false; go.textContent = '生成题目'; }
  }
}

async function aiTestConnection() {
  const btn = $('aiSave');
  const old = btn.textContent;
  btn.disabled = true;
  btn.textContent = '测试中…';
  try {
    await aiRequest([
      { role: 'system', content: '你是 API 连通性测试助手，只回复 OK。' },
      { role: 'user', content: '只回复 OK' },
    ]);
    toast('API 连接成功');
    aiRenderConfigState();
    $('aiConfig').classList.add('hide');
    return true;
  } catch (e) {
    toast('连接失败：' + e.message);
    $('aiConfig').classList.remove('hide');
    return false;
  } finally {
    btn.disabled = false;
    btn.textContent = old;
  }
}

async function aiSend(userText) {
  const text = String(userText || '').trim();
  if (!text || aiBusy) return;
  if (aiMode === 'gen') {
    if (aiGenBusy) return;
    $('aiInput').value = '';
    aiGenerateProblem(text);
    return;
  }
  if (!state.current && !aiBookQuote) { toast('先选一道题，或从原书选一段内容'); return; }
  if (!aiConfig.key) {
    $('aiConfig').classList.remove('hide');
    $('aiKey').focus();
    toast('先填 API Key 才能使用 AI 助教');
    return;
  }
  if (!aiConfig.base || !aiConfig.model) {
    $('aiConfig').classList.remove('hide');
    toast('接口地址和模型名不能为空');
    return;
  }
  aiBusy = true;
  $('aiSend').disabled = true;
  document.querySelectorAll('#aiQuick button').forEach((b) => { b.disabled = true; });
  $('aiInput').value = '';
  aiAddMessage('user', text);
  aiTranscript.push({ role: 'user', text });
  const pending = aiAddMessage('assistant', '正在思考', true);
  try {
    const messages = [
      { role: 'system', content: AI_SYSTEM + '\n\n' + AI_MODES[aiMode].extra + '\n\n当前上下文：\n' + aiProblemContext() },
      ...aiHistory.slice(-8),
      { role: 'user', content: text },
    ];
    const data = await aiRequest(messages);
    pending.classList.remove('pending');
    pending.innerHTML = mdToHtml(data.content);
    aiEnhanceAnswer(pending, data.content);
    aiTranscript.push({ role: 'assistant', text: data.content });
    aiHistory.push({ role: 'user', content: text });
    aiHistory.push({ role: 'assistant', content: String(data.content).slice(0, 8000) });
    if (aiHistory.length > 12) aiHistory = aiHistory.slice(-12);
    aiScrollBottom();
  } catch (e) {
    pending.classList.remove('pending');
    pending.classList.add('error');
    pending.textContent = '出错了：' + e.message;
    aiScrollBottom();
  } finally {
    aiBusy = false;
    $('aiSend').disabled = false;
    document.querySelectorAll('#aiQuick button').forEach((b) => { b.disabled = false; });
  }
}

function aiBind() {
  aiConfig = loadAIConfig();
  $('aiProvider').value = aiConfig.provider;
  $('aiBase').value = aiConfig.base;
  $('aiModel').value = aiConfig.model;
  $('aiKey').value = aiConfig.key;
  aiRenderConfigState();
  aiSetMode(aiMode);
  aiGenDiff();
  if ($('aiGenDifficulty')) $('aiGenDifficulty').addEventListener('input', aiGenDiff);
  if ($('aiGenGo')) $('aiGenGo').onclick = () => aiGenerateProblem();
  if ($('aiGenToggle')) $('aiGenToggle').onclick = () => {
    const panel = $('aiGenPanel');
    if (panel) aiGenSetCollapsed(!panel.classList.contains('collapsed'));
  };
  if ($('aiGenQuoteClear')) $('aiGenQuoteClear').onclick = () => {
    aiBookQuote = null;
    aiRenderGenQuote();
    aiUpdateContext();
    toast('已取消使用原书选段');
  };
  if ($('aiGenTopic')) {
    $('aiGenTopic').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        aiGenerateProblem();
      }
    });
  }

  $('btnAI').onclick = aiOpen;
  $('aiClose').onclick = aiClose;
  $('aiExport').onclick = aiExport;
  $('aiBackdrop').addEventListener('click', (e) => {
    if (e.target === $('aiBackdrop')) aiClose();
  });
  $('aiConfigToggle').onclick = () => {
    $('aiConfig').classList.toggle('hide');
  };
  $('aiProvider').onchange = () => aiApplyProvider($('aiProvider').value);
  $('aiSave').onclick = async () => {
    const key = $('aiKey').value.trim();
    const base = $('aiBase').value.trim();
    const model = $('aiModel').value.trim();
    if (!key) { toast('请先填入 API Key'); $('aiKey').focus(); return; }
    if (!base || !model) { toast('接口地址和模型名不能为空'); return; }
    aiConfig = { provider: $('aiProvider').value, base, model, key };
    persistAIConfig();
    aiRenderConfigState();
    await aiTestConnection();
  };
  $('aiSend').onclick = () => aiSend($('aiInput').value);
  $('aiInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      aiSend($('aiInput').value);
    }
  });
  document.querySelectorAll('#aiModes .ai-mode').forEach((b) => {
    b.onclick = () => aiSetMode(b.dataset.aiMode);
  });
  document.querySelectorAll('#aiQuick button').forEach((b) => {
    b.onclick = () => aiSend(b.dataset.aiPrompt || b.textContent);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !$('aiBackdrop').classList.contains('hide')) aiClose();
  });
}

/* ================= 原书阅读 / 题目联动 ================= */
function bookPad2(n) {
  return String(n).padStart(2, '0');
}

function bookSectionForProblem(p) {
  if (!p || p.kind === 'local' || p.kind === 'ai') return null;
  if (p.kind === 'appendix') {
    const prefix = String(p.label || '').split('-')[0].toUpperCase();
    return { sectionId: 'appendix-' + prefix, label: p.label || '' };
  }
  if (p.chapter) return { sectionId: 'ch' + bookPad2(p.chapter), label: p.label || '' };
  return null;
}

function bookFindSection(id) {
  return (bookState.manifest && bookState.manifest.sections || []).find((s) => s.id === id) || null;
}

function bookProblemsForSection(section) {
  if (!section || !state.problems.length) return [];
  return state.problems.filter((p) => {
    const map = bookSectionForProblem(p);
    return map && map.sectionId === section.id;
  }).sort((a, b) => String(a.label || a.id).localeCompare(String(b.label || b.id), 'zh-CN', { numeric: true }));
}

function renderBookRelated(section) {
  const box = $('bookRelated');
  if (!box || !section) return;
  const list = bookProblemsForSection(section);
  if (!list.length) {
    box.innerHTML = '<div class="book-related-head"><span>本章题目</span><b>0</b></div><div class="book-related-empty">本章暂时没有收录题目</div>';
    return;
  }
  const ac = list.filter((p) => state.progress[p.id] && state.progress[p.id].status === 'AC').length;
  const items = list.map((p) => {
    const pr = state.progress[p.id] || {};
    const dot = pr.status === 'AC' ? 'ac' : (pr.attempts ? 'bad' : '');
    return `<button type="button" class="book-related-item" data-id="${esc(p.id)}" title="${esc(p.label + ' ' + p.title)}">
      <i class="br-dot ${dot}"></i><span class="br-label">${esc(p.label || '')}</span>
      <span class="br-title">${esc(p.title)}</span><span class="br-lv">${p.difficulty || 2}</span>
    </button>`;
  }).join('');
  box.innerHTML = `<div class="book-related-head"><span>本章题目</span><b>${ac}/${list.length}</b>
    <button type="button" id="bookRelatedGo">去刷题</button></div>
    <div class="book-related-list">${items}</div>`;
  box.querySelectorAll('.book-related-item').forEach((btn) => {
    btn.onclick = () => {
      clearProblemFilters();
      setView('oj');
      selectProblem(btn.dataset.id);
    };
  });
  const go = document.getElementById('bookRelatedGo');
  if (go) go.onclick = () => {
    const first = list.find((p) => !(state.progress[p.id] && state.progress[p.id].status === 'AC')) || list[0];
    clearProblemFilters();
    setView('oj');
    selectProblem(first.id);
  };
}

function bookSectionNumber(section) {
  if (!section) return '00';
  if (section.kind === 'chapter') return bookPad2(section.num);
  if (section.kind === 'appendix') return section.letter || 'A';
  return '序';
}

async function bookLoadManifest() {
  if (bookState.manifest) return bookState.manifest;
  const r = await fetch('/book/manifest.json', { cache: 'no-store' });
  if (!r.ok) throw new Error('原书目录读取失败');
  bookState.manifest = await r.json();
  renderBookToc($('bookSearch') ? $('bookSearch').value : '');
  updateBookCurrent();
  return bookState.manifest;
}

function renderBookToc(query) {
  const nav = $('bookToc');
  if (!nav || !bookState.manifest) return;
  const q = String(query || '').trim().toLowerCase();
  const sections = bookState.manifest.sections || [];
  const match = (s) => !q || ((s.title || '') + ' ' + (s.short || '')).toLowerCase().includes(q);
  const chapters = sections.filter((s) => s.kind === 'chapter' && match(s));
  const appendices = sections.filter((s) => s.kind === 'appendix' && match(s));
  const preface = sections.filter((s) => s.kind === 'preface' && match(s));
  let html = '';
  if (preface.length) {
    html += '<div class="book-toc-label">卷首</div>';
    html += preface.map(bookTocItem).join('');
  }
  if (chapters.length) {
    html += '<div class="book-toc-label">正文 <span>' + chapters.length + '</span></div>';
    html += chapters.map(bookTocItem).join('');
  }
  if (appendices.length) {
    html += '<div class="book-toc-label">附录 <span>' + appendices.length + '</span></div>';
    html += appendices.map(bookTocItem).join('');
  }
  if (!html) html = '<div class="book-toc-empty">没有匹配的章节</div>';
  nav.innerHTML = html;
  nav.querySelectorAll('.book-toc-item').forEach((btn) => {
    btn.onclick = () => openBook(btn.dataset.sec);
  });
  const active = nav.querySelector('.book-toc-item.active');
  if (active) active.scrollIntoView({ block: 'nearest' });
}

function bookTocItem(section) {
  const num = bookSectionNumber(section);
  const name = section.short || section.title || '';
  return `<button class="book-toc-item ${bookState.section && bookState.section.id === section.id ? 'active' : ''}" data-sec="${esc(section.id)}">
    <span class="book-toc-num ${section.kind}">${esc(num)}</span>
    <span class="book-toc-name">${esc(name)}</span>
    <span class="book-toc-arrow">›</span>
  </button>`;
}

function setView(view) {
  currentView = (view === 'book' || view === 'stats' || view === 'arena' || view === 'grammar') ? view : 'oj';
  document.body.classList.toggle('book-mode', currentView === 'book');
  document.body.classList.toggle('stats-mode', currentView === 'stats');
  document.body.classList.toggle('arena-mode', currentView === 'arena');
  document.body.classList.toggle('grammar-mode', currentView === 'grammar');
  $('bookWorkspace').classList.toggle('hide', currentView !== 'book');
  $('statsWorkspace').classList.toggle('hide', currentView !== 'stats');
  const arenaWorkspace = $('arenaWorkspace');
  if (arenaWorkspace) arenaWorkspace.classList.toggle('hide', currentView !== 'arena');
  const grammarWorkspace = $('grammarWorkspace');
  if (grammarWorkspace) grammarWorkspace.classList.toggle('hide', currentView !== 'grammar');
  document.querySelectorAll('#viewSwitch .view-tab').forEach((b) => {
    b.classList.toggle('on', b.dataset.view === currentView);
  });
  if (currentView !== 'book') hideBookSelection();
  if (currentView === 'book') {
    $('bookScroll').focus({ preventScroll: true });
  }
  if (currentView === 'stats') {
    const stats = $('statsWorkspace');
    if (stats) stats.scrollTop = 0;
    loadStats(true);
  }
  if (currentView === 'arena' && typeof arenaRender === 'function') arenaRender();
  if (currentView === 'grammar' && typeof grammarRender === 'function') grammarRender();
  aiUpdateContext();
}

async function openBookView() {
  await bookLoadManifest();
  const map = bookSectionForProblem(state.current);
  const target = (map && bookFindSection(map.sectionId)) || bookState.section || bookFindSection('ch01') || bookState.manifest.sections[0];
  if (target) await openBook(target.id, map && map.sectionId === target.id ? map.label : '');
}

async function openBookForCurrent() {
  const map = bookSectionForProblem(state.current);
  if (!map) { toast('这道贵阳原创题没有对应的原书章节'); return; }
  const section = await bookLoadManifest().then(() => bookFindSection(map.sectionId));
  if (!section) { toast('没有找到对应的原书章节'); return; }
  await openBook(section.id, map.label);
}

async function openBook(sectionId, anchorLabel) {
  await bookLoadManifest();
  const section = bookFindSection(sectionId);
  if (!section) return;
  setView('book');
  updateBookCurrent();
  if (bookState.cache[sectionId] !== undefined && bookState.section && bookState.section.id === sectionId) {
    renderBookToc($('bookSearch') ? $('bookSearch').value : '');
    bookState.section = section;
    if (anchorLabel) bookScrollToLabel(anchorLabel);
    return;
  }
  $('bookContent').innerHTML = '<div class="book-loading"><i></i><i></i><i></i><span>正在翻开原书…</span></div>';
  $('bookCrumb').textContent = section.title;
  try {
    let md = bookState.cache[sectionId];
    if (md === undefined) {
      const r = await fetch('/book/' + section.file, { cache: 'no-store' });
      if (!r.ok) throw new Error('章节读取失败');
      md = await r.text();
      bookState.cache[sectionId] = md;
    }
    renderBookSection(section, md, anchorLabel);
  } catch (e) {
    $('bookContent').innerHTML = '<div class="book-load-error">原书章节读取失败：' + esc(e.message) + '</div>';
  }
}

function renderBookSection(section, md, anchorLabel) {
  bookState.section = section;
  $('bookHeroNum').textContent = bookSectionNumber(section);
  $('bookHeroKicker').textContent = section.kind === 'chapter' ? 'CHAPTER' : (section.kind === 'appendix' ? 'APPENDIX' : 'PREFACE');
  $('bookHeroTitle').textContent = section.title || '';
  $('bookHeroSub').textContent = section.kind === 'chapter'
    ? '《从语法到算法》· 原书阅读'
    : (section.kind === 'appendix' ? '附录 · 原书阅读' : '卷首 · 原书阅读');
  $('bookCrumb').textContent = section.title || '原书阅读';
  let body = String(md || '').replace(/^#\s+.*\r?\n?/, '');
  const guideModel = bookGuideModel(body);
  $('bookGuide').innerHTML = bookGuideHtml(section, guideModel);
  $('bookContent').innerHTML = bookMdToHtml(body);
  bindBookCodeCopy();
  bindBookGuide();
  const idx = bookState.manifest ? bookState.manifest.sections.findIndex((s) => s.id === section.id) : -1;
  const prev = idx > 0 ? bookState.manifest.sections[idx - 1] : null;
  const next = idx >= 0 && idx < bookState.manifest.sections.length - 1 ? bookState.manifest.sections[idx + 1] : null;
  $('bookPrev').disabled = !prev;
  $('bookNext').disabled = !next;
  $('bookPrev').dataset.sec = prev ? prev.id : '';
  $('bookNext').dataset.sec = next ? next.id : '';
  $('bookPageHint').textContent = section.kind === 'chapter'
    ? '第 ' + section.num + ' 章 / 共 ' + (bookState.manifest.sections.filter((s) => s.kind === 'chapter').length) + ' 章'
    : (section.kind === 'appendix' ? '附录 ' + (section.letter || '') : '卷首');
  $('bookScroll').scrollTop = 0;
  renderBookToc($('bookSearch') ? $('bookSearch').value : '');
  renderBookRelated(section);
  updateBookProgress();
  if (anchorLabel) setTimeout(() => bookScrollToLabel(anchorLabel), 90);
}

function bookScrollToLabel(label) {
  const box = $('bookContent');
  if (!box || !label) return;
  const labels = String(label).replace(/\s+/g, '');
  const headings = [...box.querySelectorAll('.book-h')];
  let target = headings.find((h) => h.textContent.replace(/\s+/g, '').includes(labels));

  // 很多章的习题是「## 习题」下面的有序列表，而不是「### 习题 X-Y」标题。
  if (!target) {
    const m = labels.match(/^习题(\d+)-(\d+)$/);
    if (m) {
      const exHead = headings.find((h) => /^习题$/.test(h.textContent.trim()));
      if (exHead) {
        let node = exHead.nextElementSibling;
        const items = [];
        while (node && !node.classList.contains('book-h')) {
          if (node.matches && node.matches('ol.book-list, ul.book-list')) {
            items.push(...node.querySelectorAll(':scope > li[data-num]'));
          }
          node = node.nextElementSibling;
        }
        target = items.find((li) => li.dataset.num === m[2]) || items[Number(m[2]) - 1] || null;
      }
    }
  }

  if (!target) {
    const norm = labels.replace(/第/g, '').replace(/题/g, '').slice(0, 5);
    target = headings.find((h) => norm.length > 1 && h.textContent.replace(/\s+/g, '').includes(norm));
  }
  if (!target) return;
  const top = target.getBoundingClientRect().top - $('bookScroll').getBoundingClientRect().top - 18;
  $('bookScroll').scrollTo({ top: Math.max(0, $('bookScroll').scrollTop + top), behavior: 'smooth' });
  target.classList.add('book-hit');
  setTimeout(() => target.classList.remove('book-hit'), 1800);
}

function updateBookCurrent() {
  const title = $('bookCurrentTitle');
  if (!title) return;
  const p = state.current;
  const open = $('bookCurrentOpen');
  if (!p) {
    title.textContent = '未选题';
    open.textContent = '打开对应章节';
    open.disabled = true;
    return;
  }
  const map = bookSectionForProblem(p);
  title.textContent = (p.label || p.id) + ' · ' + (p.title || '');
  if (map) {
    open.textContent = '打开对应章节';
    open.disabled = false;
    open.dataset.sec = map.sectionId;
    open.dataset.label = map.label;
  } else {
    open.textContent = '本题无原书章节';
    open.disabled = true;
    open.dataset.sec = '';
  }
}

function updateBookProgress() {
  const box = $('bookScroll');
  if (!box) return;
  const max = box.scrollHeight - box.clientHeight;
  const pct = max > 0 ? Math.min(100, Math.max(0, Math.round(box.scrollTop / max * 100))) : 0;
  $('bookPercent').textContent = pct + '%';
  $('bookProgressFill').style.width = pct + '%';
}

function hideBookSelection() {
  const bar = $('bookSelBar');
  if (bar) bar.classList.add('hide');
  bookSelText = '';
}

function captureBookSelection() {
  if (currentView !== 'book') return;
  const sel = window.getSelection();
  if (!sel || !sel.rangeCount || sel.isCollapsed) { hideBookSelection(); return; }
  const text = String(sel.toString() || '').replace(/\s+/g, ' ').trim();
  if (text.length < 2) { hideBookSelection(); return; }
  const range = sel.getRangeAt(0);
  const anchor = range.startContainer.nodeType === 1 ? range.startContainer : range.startContainer.parentElement;
  const focus = range.endContainer.nodeType === 1 ? range.endContainer : range.endContainer.parentElement;
  if (!anchor || !focus || !$('bookContent').contains(anchor) || !$('bookContent').contains(focus)) return;
  const rect = range.getBoundingClientRect();
  if (!rect || rect.width < 1) return;
  bookSelText = text.slice(0, 2400);
  const bar = $('bookSelBar');
  $('bookSelPreview').textContent = '“' + text.slice(0, 36) + (text.length > 36 ? '…' : '') + '”';
  $('bookAskRelate').style.display = state.current ? '' : 'none';
  bar.classList.remove('hide');
  const bw = 360;
  const bh = 46;
  bar.style.left = Math.round(Math.min(Math.max(12, rect.left), window.innerWidth - bw - 12)) + 'px';
  bar.style.top = Math.round(Math.min(Math.max(66, rect.bottom + 8), window.innerHeight - bh - 12)) + 'px';
}

function askBookSelection(kind) {
  const text = bookSelText;
  if (!text) return;
  const p = state.current;
  const chapter = bookState.section ? bookState.section.title : '原书';
  aiBookQuote = { chapter, text };
  if (kind === 'generate') {
    hideBookSelection();
    window.getSelection().removeAllRanges();
    aiOpen();
    aiSetMode('gen');
    aiRenderGenQuote();
    if (aiConfig && aiConfig.key) {
      setTimeout(() => $('aiGenTopic').focus(), 120);
      toast('已带入原书选段，设置难度后点「生成题目」');
    } else {
      $('aiConfig').classList.remove('hide');
      $('aiKey').focus();
      toast('填好 API Key 后即可用这段内容出题');
    }
    return;
  }
  const quote = '我在原书《' + chapter + '》里选中了：\n\n> ' + text.replace(/\n/g, '\n> ') + '\n\n';
  const prompt = kind === 'relate' && p
    ? quote + '请结合当前题目「' + (p.label || p.id) + ' ' + (p.title || '') + '」解释：这段话对应题目的哪个知识点？它对我解题有什么提示？不要直接给完整代码。'
    : quote + '请用中文解释这段话；如果它和当前题目有关，再说明关系。';
  hideBookSelection();
  window.getSelection().removeAllRanges();
  aiOpen();
  aiSetMode('coach');
  $('aiInput').value = prompt;
  if (aiConfig && aiConfig.key) aiSend(prompt);
  else {
    $('aiConfig').classList.remove('hide');
    $('aiKey').focus();
    toast('填好 API Key 后按发送，选段已为你留在输入框');
  }
}

function bookBind() {
  document.querySelectorAll('#viewSwitch .view-tab').forEach((b) => {
    b.onclick = () => {
      if (b.dataset.view === 'book') openBookView();
      else if (b.dataset.view === 'stats') setView('stats');
      else if (b.dataset.view === 'arena') setView('arena');
      else if (b.dataset.view === 'grammar') setView('grammar');
      else setView('oj');
    };
  });
  $('bookBack').onclick = () => setView('oj');
  $('bookCurrentBack').onclick = () => setView('oj');
  $('bookCurrentOpen').onclick = () => {
    const sec = $('bookCurrentOpen').dataset.sec;
    $('bookSearch').value = '';
    if (sec) openBook(sec, $('bookCurrentOpen').dataset.label || '');
  };
  $('bookSearch').addEventListener('input', (e) => renderBookToc(e.target.value));
  $('bookPrev').onclick = () => {
    if (!$('bookPrev').dataset.sec) return;
    $('bookSearch').value = '';
    openBook($('bookPrev').dataset.sec);
  };
  $('bookNext').onclick = () => {
    if (!$('bookNext').dataset.sec) return;
    $('bookSearch').value = '';
    openBook($('bookNext').dataset.sec);
  };
  $('bookPdf').onclick = () => window.open('/book/original.pdf', '_blank', 'noopener');
  $('bookScroll').addEventListener('scroll', () => {
    updateBookProgress();
    if (!$('bookSelBar').classList.contains('hide')) hideBookSelection();
  }, { passive: true });
  document.addEventListener('mouseup', (e) => {
    if (currentView !== 'book' || e.target.closest('#bookSelBar')) return;
    setTimeout(captureBookSelection, 0);
  });
  document.addEventListener('keyup', (e) => {
    if (currentView !== 'book') return;
    if (e.shiftKey || ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
      setTimeout(captureBookSelection, 0);
    }
  });
  document.addEventListener('mousedown', (e) => {
    if (currentView === 'book' && !e.target.closest('#bookSelBar') && !e.target.closest('#bookContent')) hideBookSelection();
  });
  document.querySelectorAll('#bookSelBar [data-book-ask]').forEach((b) => {
    b.onclick = () => askBookSelection(b.dataset.bookAsk);
  });
  $('bookSelCopy').onclick = () => {
    aiCopyText(bookSelText, '原书内容已复制');
    hideBookSelection();
  };
  window.addEventListener('resize', () => { updateBookProgress(); drawBookMindmap(); });
}

/* ================= 学习轨迹 / 提交记录 ================= */
function dateKeyOf(d) {
  return String(d.getFullYear()) + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

function dayStart(d) {
  const x = new Date(d);
  x.setHours(0, 0, 0, 0);
  return x;
}

function statsDayCounts(items) {
  const counts = {};
  for (const rec of items) {
    if (!rec.ts) continue;
    const key = dateKeyOf(new Date(rec.ts * 1000));
    counts[key] = (counts[key] || 0) + 1;
  }
  return counts;
}

function statsStreak(counts) {
  let day = dayStart(new Date());
  let streak = 0;
  if (!counts[dateKeyOf(day)]) day.setDate(day.getDate() - 1);
  while (counts[dateKeyOf(day)]) {
    streak++;
    day.setDate(day.getDate() - 1);
  }
  return streak;
}

async function loadStats(force = false) {
  if (statsState.loading) return;
  if (statsState.loaded && !force) { renderStats(); return; }
  statsState.loading = true;
  const root = $('statsMetrics');
  if (root) root.innerHTML = '<div class="stats-loading"><i></i> 正在汇总本机提交…</div>';
  try {
    await refreshProgress();
    const r = await fetch('/api/submissions?limit=300', { cache: 'no-store' });
    if (!r.ok) throw new Error('提交记录读取失败');
    const data = await r.json();
    statsState.items = data.items || [];
    statsState.loaded = true;
    renderStats();
  } catch (e) {
    if (root) root.innerHTML = '<div class="stats-empty">读取失败，请确认本机服务正在运行。</div>';
    toast('学习数据读取失败');
  } finally {
    statsState.loading = false;
  }
}

function renderStats() {
  if (!statsState.items) statsState.items = [];
  rpgRenderProfile();
  renderStatsMetrics();
  renderStatsHeatmap();
  renderStatsDiff();
  renderStatsWeak();
  renderStatsHistory();
}

function renderStatsMetrics() {
  const root = $('statsMetrics');
  if (!root) return;
  const items = statsState.items;
  const acs = items.filter((x) => x.verdict === 'AC').length;
  const rate = items.length ? Math.round(acs / items.length * 100) : 0;
  const counts = statsDayCounts(items);
  const activeDays = Object.keys(counts).filter((k) => counts[k] > 0).length;
  const streak = statsStreak(counts);
  const solvedIds = new Set();
  for (const p of state.problems) {
    if (state.progress[p.id] && state.progress[p.id].status === 'AC') solvedIds.add(p.id);
  }
  for (const rec of items) if (rec.verdict === 'AC') solvedIds.add(rec.problem_id);
  const solved = solvedIds.size;
  root.innerHTML = `
    <div class="stats-metric"><span>已通过题目</span><b>${solved}</b><small>本机累计</small></div>
    <div class="stats-metric"><span>正式提交</span><b>${items.length}</b><small>最近 300 条</small></div>
    <div class="stats-metric"><span>AC 提交</span><b>${acs}</b><small>AC 率 ${rate}%</small></div>
    <div class="stats-metric"><span>活跃天数</span><b>${activeDays}</b><small>有提交的日子</small></div>
    <div class="stats-metric"><span>连续提交</span><b>${streak}</b><small>天</small></div>`;
}

function renderStatsHeatmap() {
  const root = $('statsHeatmap');
  if (!root) return;
  const today = dayStart(new Date());
  const monday = new Date(today);
  monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
  const start = new Date(monday);
  start.setDate(monday.getDate() - 15 * 7);
  const counts = statsDayCounts(statsState.items);
  let html = '';
  for (let i = 0; i < 112; i++) {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    const key = dateKeyOf(d);
    const n = counts[key] || 0;
    const level = n === 0 ? 0 : n < 2 ? 1 : n < 4 ? 2 : n < 8 ? 3 : 4;
    html += `<i class="heat-cell lv${level}${statsState.dateFilter === key ? ' on' : ''}" title="${key} · ${n} 次提交" data-date="${key}"></i>`;
  }
  root.innerHTML = html;
  root.querySelectorAll('.heat-cell').forEach((cell) => {
    cell.onclick = () => {
      statsState.dateFilter = statsState.dateFilter === cell.dataset.date ? '' : cell.dataset.date;
      renderStatsHeatmap();
      renderStatsHistory();
    };
  });
  $('statsHeatRange').textContent = '最近 16 周 · ' + (statsState.items.length ? '共 ' + statsState.items.length + ' 次' : '暂无提交');
}

function renderStatsDiff() {
  const root = $('statsDiff');
  if (!root) return;
  const rows = [1, 2, 3, 4, 5].map((lv) => {
    const all = state.problems.filter((p) => Number(p.difficulty || 2) === lv && (p.has_judge || (Array.isArray(p.tests) && p.tests.length > 0)));
    const ac = all.filter((p) => state.progress[p.id] && state.progress[p.id].status === 'AC').length;
    return { lv, all: all.length, ac, pct: all.length ? Math.round(ac / all.length * 100) : 0 };
  });
  root.innerHTML = rows.map((r) => `<div class="stats-diff-row">
    <span class="stats-diff-lv lv${r.lv}">${r.lv}</span>
    <div class="stats-diff-main"><div class="stats-diff-top"><b>${DIFF_LABELS[r.lv]}</b><span>${r.ac}/${r.all} 通过</span></div>
      <div class="stats-bar"><i style="width:${r.pct}%"></i></div></div>
  </div>`).join('');
}

function statsWeakRows() {
  const tagCounts = {};
  let failed = 0;
  for (const rec of statsState.items) {
    if (rec.verdict === 'AC') continue;
    failed++;
    const p = state.byId[rec.problem_id];
    if (!p) continue;
    for (const tag of (p.tags || [])) tagCounts[tag] = (tagCounts[tag] || 0) + 1;
  }
  if (!failed) {
    for (const p of state.problems) {
      const pr = state.progress[p.id] || {};
      if (!pr.attempts || pr.status === 'AC') continue;
      for (const tag of (p.tags || [])) tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    }
  }
  return Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 6);
}

function renderStatsWeak() {
  const root = $('statsWeak');
  if (!root) return;
  const rows = statsWeakRows();
  if (!rows.length) {
    root.innerHTML = '<div class="stats-empty">还没有失败提交。提交错误后，这里会按知识点自动归类。</div>';
    return;
  }
  const max = rows[0][1] || 1;
  root.innerHTML = rows.map(([tag, n], i) => `<div class="stats-weak-row">
    <span class="stats-weak-index">${String(i + 1).padStart(2, '0')}</span>
    <div class="stats-weak-main"><div class="stats-weak-top"><b>${esc(tag)}</b><span>${n} 次</span></div>
      <div class="stats-bar weak"><i style="width:${Math.round(n / max * 100)}%"></i></div></div>
  </div>`).join('');
}

function statsHistoryRow(rec) {
  const p = state.byId[rec.problem_id] || {};
  const cases = rec.case_count ? `${rec.ac_cases}/${rec.case_count}` : '—';
  return `<button class="stats-history-row" type="button" data-sub="${esc(rec.id)}">
    <span class="verdict ${esc(rec.verdict)}">${esc(rec.verdict)}</span>
    <span class="shr-title"><b>${esc(p.label || rec.problem_id)}</b>${esc(p.title || '')}</span>
    <span class="shr-cases">${cases}</span>
    <span class="shr-time">${esc((rec.created_at || '').slice(5, 16))}</span>
  </button>`;
}

function renderStatsHistory() {
  const root = $('statsHistory');
  if (!root) return;
  const all = statsState.dateFilter
    ? statsState.items.filter((rec) => rec.ts && dateKeyOf(new Date(rec.ts * 1000)) === statsState.dateFilter)
    : statsState.items;
  const items = all.slice(0, 12);
  if (!items.length) {
    root.innerHTML = statsState.dateFilter
      ? `<div class="stats-empty">${esc(statsState.dateFilter)} 没有提交记录。再点一次热力格取消筛选。</div>`
      : '<div class="stats-empty">还没有正式提交。去做一道题，提交后这里会出现记录。</div>';
    $('statsHistoryTotal').textContent = statsState.dateFilter ? statsState.dateFilter + ' · 0 条' : '';
    return;
  }
  $('statsHistoryTotal').textContent = statsState.dateFilter
    ? statsState.dateFilter + ' · 共 ' + all.length + ' 条'
    : `最近 ${items.length} 条`;
  root.innerHTML = items.map(statsHistoryRow).join('');
  root.querySelectorAll('[data-sub]').forEach((btn) => {
    btn.onclick = () => openSubmission(btn.dataset.sub);
  });
}

async function openSubmission(id) {
  if (!id) return;
  try {
    const r = await fetch('/api/submissions/' + encodeURIComponent(id), { cache: 'no-store' });
    const rec = await r.json();
    if (!r.ok) throw new Error(rec.error || '提交不存在');
    submissionState.current = rec;
    const p = state.byId[rec.problem_id] || {};
    $('submissionKicker').textContent = 'SUBMISSION #' + rec.id;
    $('submissionTitle').textContent = (p.label || rec.problem_id) + ' · ' + (p.title || '');
    const v = $('submissionVerdict');
    v.className = 'verdict ' + rec.verdict;
    v.textContent = rec.verdict;
    $('submissionMeta').textContent = `${rec.created_at || ''} · 用时 ${rec.time_ms || 0} ms · 代码 ${rec.code_len || 0} 字节 · ${rec.compiler || 'C++17'}`;
    $('submissionCode').textContent = rec.code || '';
    const cases = rec.cases || [];
    $('submissionCases').innerHTML = cases.length
      ? cases.map((c) => `<span class="case-pill ${esc(c.status)}"><span class="cd"></span>#${c.index} ${esc(c.status)} · ${c.time || 0}ms</span>`).join('')
      : '<span class="stats-empty">无测试用例（编译错误或本题无数据）。</span>';
    $('submissionBackdrop').classList.remove('hide');
  } catch (e) {
    toast('提交记录读取失败');
  }
}

function closeSubmission() {
  $('submissionBackdrop').classList.add('hide');
  submissionState.current = null;
}

async function toggleProblemHistory(pid) {
  const panel = $('historyPanel');
  if (!panel) return;
  if (!panel.classList.contains('hide') && historyState.pid === pid) {
    panel.classList.add('hide');
    return;
  }
  historyState.pid = pid;
  panel.classList.remove('hide');
  $('historyPanelCount').textContent = '读取中…';
  $('historyInlineList').innerHTML = '<div class="history-empty">正在读取提交记录…</div>';
  try {
    const r = await fetch('/api/submissions?problem=' + encodeURIComponent(pid) + '&limit=60', { cache: 'no-store' });
    const data = await r.json();
    historyState.items = data.items || [];
    $('historyPanelCount').textContent = `${data.total || 0} 次`;
    const list = $('historyInlineList');
    if (!historyState.items.length) {
      list.innerHTML = '<div class="history-empty">这道题还没有正式提交记录。</div>';
      return;
    }
    list.innerHTML = historyState.items.map((rec) => {
      const time = (rec.created_at || '').slice(5, 16);
      return `<button class="history-row" type="button" data-sub="${esc(rec.id)}">
        <span class="verdict ${esc(rec.verdict)}">${esc(rec.verdict)}</span>
        <span class="history-time">${esc(time)}</span>
        <span class="history-cases">${rec.ac_cases}/${rec.case_count} 用例</span>
        <span class="history-len">${rec.code_len} 字节</span>
        <span class="history-arrow">›</span>
      </button>`;
    }).join('');
    list.querySelectorAll('[data-sub]').forEach((btn) => {
      btn.onclick = () => openSubmission(btn.dataset.sub);
    });
  } catch (e) {
    $('historyPanelCount').textContent = '读取失败';
    $('historyInlineList').innerHTML = '<div class="history-empty">提交记录读取失败。</div>';
  }
}

function statsReportMarkdown() {
  const items = statsState.items;
  const acs = items.filter((x) => x.verdict === 'AC').length;
  const rate = items.length ? Math.round(acs / items.length * 100) : 0;
  const counts = statsDayCounts(items);
  const activeDays = Object.keys(counts).filter((k) => counts[k] > 0).length;
  const streak = statsStreak(counts);
  const solvedIds = new Set();
  for (const p of state.problems) {
    if (state.progress[p.id] && state.progress[p.id].status === 'AC') solvedIds.add(p.id);
  }
  for (const rec of items) if (rec.verdict === 'AC') solvedIds.add(rec.problem_id);
  const lines = [
    '# 本地 OJ 学习报告',
    '',
    '> 生成时间：' + new Date().toLocaleString('zh-CN') + ' · 数据来自本机 `data/submissions.json`',
    '',
    '## 总览',
    '',
    '| 指标 | 数值 |',
    '| --- | --- |',
    '| 已通过题目 | ' + solvedIds.size + ' / 348 |',
    '| 正式提交 | ' + items.length + ' 次 |',
    '| AC 提交 | ' + acs + ' 次 |',
    '| AC 率 | ' + rate + '% |',
    '| 活跃天数 | ' + activeDays + ' 天 |',
    '| 连续提交 | ' + streak + ' 天 |',
    '',
    '## 难度分布',
    '',
    '| 难度 | 已通过 / 可判题 |',
    '| --- | --- |',
  ];
  for (const lv of [1, 2, 3, 4, 5]) {
    const all = state.problems.filter((p) => Number(p.difficulty || 2) === lv && (p.has_judge || (Array.isArray(p.tests) && p.tests.length > 0)));
    const ac = all.filter((p) => state.progress[p.id] && state.progress[p.id].status === 'AC').length;
    lines.push(`| ${lv} ${DIFF_LABELS[lv]} | ${ac} / ${all.length} |`);
  }
  lines.push('', '## 薄弱知识点', '');
  const weak = statsWeakRows();
  if (weak.length) {
    lines.push('| 知识点 | 错误次数 |', '| --- | --- |');
    for (const [tag, n] of weak) lines.push(`| ${tag} | ${n} |`);
  } else {
    lines.push('暂无失败提交记录。');
  }
  lines.push('', '## 最近提交', '');
  if (items.length) {
    lines.push('| 时间 | 题号 | 结果 | 用例 |', '| --- | --- | --- | --- |');
    for (const rec of items.slice(0, 20)) {
      const p = state.byId[rec.problem_id] || {};
      lines.push(`| ${rec.created_at || ''} | ${p.label || rec.problem_id} ${p.title || ''} | ${rec.verdict} | ${rec.ac_cases || 0}/${rec.case_count || 0} |`);
    }
  } else {
    lines.push('还没有正式提交记录。');
  }
  lines.push('', '---', '', '由本地 OJ「学习」页导出。');
  return lines.join('\n');
}

function exportStatsReport() {
  try {
    const md = statsReportMarkdown();
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '本地OJ学习报告-' + dateKeyOf(new Date()) + '.md';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
    toast('学习报告已导出');
  } catch (e) {
    toast('学习报告导出失败');
  }
}

function bindStats() {
  const refresh = $('statsRefresh');
  if (refresh) refresh.onclick = () => { statsState.loaded = false; loadStats(true); };
  const exp = $('statsExport');
  if (exp) exp.onclick = exportStatsReport;
  const close = $('submissionClose');
  if (close) close.onclick = closeSubmission;
  if ($('submissionBackdrop')) $('submissionBackdrop').onclick = (e) => {
    if (e.target === $('submissionBackdrop')) closeSubmission();
  };
  if ($('submissionOpenProblem')) $('submissionOpenProblem').onclick = () => {
    const rec = submissionState.current;
    if (!rec) return;
    closeSubmission();
    setView('oj');
    selectProblem(rec.problem_id);
  };
  if ($('submissionLoadCode')) $('submissionLoadCode').onclick = async () => {
    const rec = submissionState.current;
    if (!rec) return;
    closeSubmission();
    setView('oj');
    await selectProblem(rec.problem_id);
    setCode(rec.code || '');
    toast('已载入这次提交的代码');
  };
  if ($('submissionCopy')) $('submissionCopy').onclick = () => {
    const rec = submissionState.current;
    if (rec) aiCopyText(rec.code || '', '提交代码已复制');
  };
  if ($('submissionAskAI')) $('submissionAskAI').onclick = async () => {
    const rec = submissionState.current;
    if (!rec) return;
    closeSubmission();
    setView('oj');
    await selectProblem(rec.problem_id);
    setCode(rec.code || '');
    aiSetMode('review');
    aiOpen();
    const p = state.byId[rec.problem_id] || {};
    $('aiInput').value = `请复盘我在「${p.label || rec.problem_id} ${p.title || ''}」的这次提交：${rec.created_at} 提交，结果是 ${rec.verdict}，用时 ${rec.time_ms || 0} ms。请按复盘模式分析这次代码的亮点、风险、下次遇到同类题应该先想什么。`;
    $('aiInput').focus();
    toast('已把这次提交放进 AI 复盘');
  };
  if ($('historyPanelClose')) $('historyPanelClose').onclick = () => $('historyPanel').classList.add('hide');
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !$('submissionBackdrop').classList.contains('hide')) closeSubmission();
  });
}

async function selectProblem(id, push = true) {
  const meta = state.byId[id];
  if (!meta) return;
  let detail = state.cache && state.cache[id];
  if (!detail) {
    const r = await fetch('/api/problem/' + encodeURIComponent(id));
    if (!r.ok) { toast('题目读取失败'); return; }
    detail = await r.json();
    state.cache = state.cache || {};
    state.cache[id] = detail;
  }
  state.current = detail;
  aiResetForProblem(detail.id);
  updateBookCurrent();
  if (push && location.hash !== '#p=' + id) history.replaceState(null, '', '#p=' + id);
  renderProblem(detail);
  if (!filtersActive()) {
    const gk = groupKeyOf(detail);
    if (!state.open[gk]) { state.open[gk] = true; }
  }
  renderSidebar();

  let saved = null;
  try { saved = localStorage.getItem('oj.code.' + id); } catch (e) { }
  setCode(saved != null ? saved : templateFor(detail));

  $('selfInput').value = (detail.samples && detail.samples[0]) ? detail.samples[0].in : '';
  resetConsole();
  resetResult();
  historyState.pid = '';
  historyState.items = [];
  if ($('historyPanel')) $('historyPanel').classList.add('hide');
  const hasJudge = (detail.test_count || 0) > 0;
  $('btnSubmit').disabled = !hasJudge;
  const readonly = detail.kind === 'reading' || detail.kind === 'think';
  $('btnSubmit').style.opacity = readonly ? .45 : 1;
  $('editorHint').textContent = readonly ? '本题为阅读/思考题，无判题数据'
    : (hasJudge ? 'Ctrl+Enter 提交' : '本题暂无判题数据');
}

function setConsoleOut(text, cls) {
  const el = $('consoleOut');
  el.textContent = text;
  el.className = 'console-out' + (cls ? ' ' + cls : '');
}

function setConsoleStatus(text) {
  $('consoleStatus').textContent = text;
}

function updateInputLines() {
  const v = $('selfInput').value;
  const n = v ? v.split('\n').length : 0;
  $('inputLines').textContent = n + ' 行';
}

function showConsole(on) {
  $('consoleBox').classList.toggle('hide', !on);
  $('btnSelf').textContent = on ? '收起控制台' : '控制台';
}

function resetConsole() {
  const inp = $('selfInput');
  inp.value = inp.value || '';
  updateInputLines();
  setConsoleStatus('未运行');
  setConsoleOut('点「运行自测」后，程序输出会显示在这里', 'muted');
}

function resetResult() {  state.lastResult = null;
  hideAiDebugSuggest();
  aiUpdateContext();
  $('verdict').textContent = state.current && (state.current.kind === 'reading' || state.current.kind === 'think') ? '阅读题' : '等待提交';
  $('verdict').className = 'verdict none';
  $('resultSum').textContent = '';
  $('resultBody').innerHTML = '';
  $('resultPanel').classList.remove('expanded');
  $('resultToggle').textContent = '展开';
}

function verdictClass(v) {
  return ['AC', 'WA', 'TLE', 'RE', 'CE', 'PE'].includes(v) ? v : 'none';
}

function verdictText(v) {
  return {
    AC: 'AC 通过', WA: 'WA 答案错误', TLE: 'TLE 超时', RE: 'RE 运行错误',
    CE: 'CE 编译错误', PE: 'PE 格式错误', OK: '运行完成', NO_TEST: '无测试数据', none: '等待提交',
  }[v] || v;
}

function showResult(res, kind) {
  state.lastResult = res;
  aiUpdateContext();
  const v = res.verdict || 'none';
  $('verdict').textContent = verdictText(v);
  $('verdict').className = 'verdict ' + verdictClass(v);

  if (kind === 'self') {
    $('resultSum').innerHTML = `运行完成 · 用时 <b>${res.time || 0}</b> ms`;
    const c = (res.cases && res.cases[0]) || {};
    $('resultBody').innerHTML = `
      <div class="detail">
        <div class="row"><h5>输出</h5><pre>${esc(c.actual || '')}</pre></div>
        ${c.stderr ? `<div class="row"><h5>stderr</h5><pre class="err">${esc(c.stderr)}</pre></div>` : ''}
      </div>`;
    expandResult(true);
    return;
  }

  if (v === 'CE') {
    $('resultSum').innerHTML = '编译未通过';
    $('resultBody').innerHTML = `<div class="detail"><div class="row"><h5>编译器信息</h5><pre class="err">${esc(res.message || '')}</pre></div></div>`;
    expandResult(true);
    return;
  }

  const cases = res.cases || [];
  const acn = cases.filter((c) => c.status === 'AC').length;
  $('resultSum').innerHTML = `通过 <b>${acn}</b> / <b>${cases.length}</b> · 总用时 <b>${res.time || 0}</b> ms`;
  let html = `<div class="case-strip">`;
  for (const c of cases) {
    html += `<div class="case-pill ${c.status}" data-case="${c.index}"><span class="cd"></span>#${c.index} ${c.status} <span style="color:#98a39d">${c.time}ms</span></div>`;
  }
  html += '</div><div id="caseDetail"></div>';
  $('resultBody').innerHTML = html;

  const pills = $('resultBody').querySelectorAll('.case-pill');
  const showCase = (idx) => {
    const c = cases.find((x) => x.index === idx);
    if (!c) return;
    pills.forEach((el) => el.classList.toggle('on', el.dataset.case === String(idx)));
    let d = '';
    if (c.input !== undefined) d += `<div class="row"><h5>输入</h5><pre>${esc(c.input)}</pre></div>`;
    if (c.expected !== undefined && c.expected !== null) d += `<div class="row"><h5>期望输出</h5><pre>${esc(c.expected)}</pre></div>`;
    if (c.actual !== undefined) d += `<div class="row"><h5>你的输出</h5><pre>${esc(c.actual)}</pre></div>`;
    if (c.stderr) d += `<div class="row"><h5>stderr</h5><pre class="err">${esc(c.stderr)}</pre></div>`;
    if (!d) d = '<div class="row"><h5>说明</h5><pre>该用例已通过。</pre></div>';
    $('caseDetail').innerHTML = `<div class="detail">${d}</div>`;
  };
  pills.forEach((el) => { el.onclick = () => showCase(Number(el.dataset.case)); });
  const firstBad = cases.find((c) => c.status !== 'AC');
  if (firstBad) showCase(firstBad.index);
  else if (cases.length) showCase(cases[0].index);
  expandResult(v !== 'AC');
}

function expandResult(on) {
  $('resultPanel').classList.toggle('expanded', !!on);
  $('resultToggle').textContent = on ? '收起' : '展开';
}

async function submit() {
  if (state.busy || !state.current) return;
  const p = state.current;
  if (!(p.test_count > 0)) { toast(p.kind === 'reading' || p.kind === 'think' ? '本题为阅读/思考题，无需提交' : '本题暂无判题数据'); return; }
  const code = $('code').value;
  if (!code.trim()) { toast('代码是空的'); return; }
  const wasAC = !!(state.progress[p.id] && state.progress[p.id].status === 'AC');
  state.busy = true;
  hideAiDebugSuggest();
  $('btnSubmit').disabled = true;
  $('verdict').textContent = '评测中…';
  $('verdict').className = 'verdict none';
  $('resultSum').textContent = '正在调用本机 g++ 编译并运行全部用例';
  $('resultBody').innerHTML = '<div style="padding:8px 0;color:#8a958f;font-size:12.5px">编译 → 逐用例运行 → 比对输出，请稍候…</div>';
  expandResult(true);
  try {
    const r = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: p.id, code }),
    });
    const res = await r.json();
    if (res.error) { toast(res.error); resetResult(); return; }
    showResult(res, 'submit');
    statsState.loaded = false;
    if ($('historyPanel') && !$('historyPanel').classList.contains('hide')) {
      historyState.pid = '';
      toggleProblemHistory(p.id);
    }
    await refreshProgress();
    rpgAfterSubmit(p, res, wasAC);
    if (typeof arenaOnSubmit === 'function') arenaOnSubmit(p, res);
    maybeShowDebugSuggest('submit', res);
  } catch (e) {
    toast('请求失败：' + e.message);
  } finally {
    state.busy = false;
    $('btnSubmit').disabled = false;
  }
}

async function selfRun() {
  if (state.busy || !state.current) return;
  const p = state.current;
  const code = $('code').value;
  if (!code.trim()) { toast('代码是空的'); return; }
  const input = $('selfInput').value;
  showConsole(true);
  state.busy = true;
  hideAiDebugSuggest();
  $('btnRun').disabled = true;
  $('btnRun').textContent = '运行中…';
  setConsoleStatus('编译并运行中…');
  setConsoleOut('正在调用本机 g++ 编译，然后用左边的输入跑一遍…', 'muted');
  try {
    const r = await fetch('/api/selfrun', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: p.id, code, input }),
    });
    const res = await r.json();
    if (res.error) {
      setConsoleStatus('运行失败');
      setConsoleOut(res.error, 'err');
      toast(res.error);
      hideAiDebugSuggest();
      return;
    }
    if (res.verdict === 'CE') {
      setConsoleStatus('编译错误');
      setConsoleOut(res.message || '编译失败', 'err');
      state.lastResult = { verdict: 'CE', message: res.message || '编译失败', cases: [] };
      aiUpdateContext();
      showDebugSuggest('run', state.lastResult);
      return;
    }
    hideAiDebugSuggest();
    const c = (res.cases && res.cases[0]) || {};
    const st = c.status || res.verdict;
    const text = {
      OK: `运行完成 · ${c.time || 0} ms`,
      RE: '运行错误 RE',
      TLE: '超时 TLE',
    }[st] || ('运行结束 ' + st);
    setConsoleStatus(text);
    let out = c.actual || '';
    if (!out) out = '(程序没有输出)';
    if (c.stderr) out += '\n\n[stderr]\n' + c.stderr;
    setConsoleOut(out, st === 'OK' ? '' : 'err');
    state.lastResult = res;
    aiUpdateContext();
  } catch (e) {
    setConsoleStatus('请求失败');
    setConsoleOut('请求失败：' + e.message, 'err');
  } finally {
    state.busy = false;
    $('btnRun').disabled = false;
    $('btnRun').textContent = '运行自测';
  }
}

async function refreshProgress() {
  try {
    const r = await fetch('/api/progress');
    state.progress = await r.json();
  } catch (e) { }
  updateProgressBar();
  renderSidebar();
  if (bookState.section) renderBookRelated(bookState.section);
}

function bind() {
  $('searchInput').addEventListener('input', (e) => {
    state.q = e.target.value;
    $('clearSearch').style.display = state.q ? 'block' : 'none';
    renderSidebar();
  });
  $('clearSearch').onclick = () => {
    $('searchInput').value = '';
    state.q = '';
    $('clearSearch').style.display = 'none';
    renderSidebar();
  };
  $('filterChips').addEventListener('click', (e) => {
    const b = e.target.closest('.chip');
    if (!b) return;
    state.filter = b.dataset.filter;
    document.querySelectorAll('#filterChips .chip').forEach((c) => c.classList.toggle('on', c === b));
    renderSidebar();
  });
  $('sortSeg').addEventListener('click', (e) => {
    const b = e.target.closest('.seg-btn');
    if (!b) return;
    state.sort = b.dataset.sort;
    document.querySelectorAll('#sortSeg .seg-btn').forEach((x) => x.classList.toggle('on', x === b));
    renderSidebar();
  });
  if ($('btnDaily')) $('btnDaily').onclick = openDailyProblem;
  if ($('btnRandom')) $('btnRandom').onclick = openRandomProblem;

  setupCodeEditor();

  $('btnSubmit').onclick = submit;
  $('btnRun').onclick = selfRun;
  $('btnConsoleRun').onclick = selfRun;
  $('btnSelf').onclick = () => {
    const box = $('consoleBox');
    box.classList.toggle('hide');
    const open = !box.classList.contains('hide');
    $('btnSelf').textContent = open ? '收起控制台' : '控制台';
    if (open) $('selfInput').focus();
  };
  $('btnFillSample').onclick = () => {
    if (state.current && state.current.samples && state.current.samples[0]) {
      $('selfInput').value = state.current.samples[0].in;
      updateInputLines();
      $('selfInput').focus();
      toast('已填入样例输入');
    } else toast('本题没有样例');
  };
  $('btnClearInput').onclick = () => {
    $('selfInput').value = '';
    updateInputLines();
    $('selfInput').focus();
    toast('输入已清空');
  };
  $('btnClearOut').onclick = () => {
    setConsoleStatus('未运行');
    setConsoleOut('点「运行自测」后，程序输出会显示在这里', 'muted');
  };
  $('btnScrollTop').onclick = () => { $('selfInput').scrollTop = 0; };
  $('selfInput').addEventListener('input', updateInputLines);
  updateInputLines();
  $('btnTemplate').onclick = () => { setCode(TEMPLATE); toast('已插入基础模板'); };
  $('btnImport').onclick = () => $('fileInput').click();
  $('btnSaveCode').onclick = saveCodeFile;
  $('fileInput').onchange = (e) => {
    const f = e.target.files && e.target.files[0];
    e.target.value = '';
    importCodeFile(f, true);
  };
  const editorWrap = document.querySelector('.editor-wrap');
  if (editorWrap) {
    const stop = (e) => { e.preventDefault(); e.stopPropagation(); };
    ['dragenter', 'dragover'].forEach((ev) => editorWrap.addEventListener(ev, (e) => {
      stop(e); editorWrap.classList.add('dragging');
    }));
    ['dragleave', 'dragend'].forEach((ev) => editorWrap.addEventListener(ev, (e) => {
      if (e.target === editorWrap) editorWrap.classList.remove('dragging');
    }));
    editorWrap.addEventListener('drop', (e) => {
      stop(e);
      editorWrap.classList.remove('dragging');
      const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      importCodeFile(f, false);
    });
  }
  $('btnResetCode').onclick = () => {
    if (!state.current) return;
    setCode(templateFor(state.current));
    toast('已清空代码');
  };
  $('resultHead').onclick = () => expandResult(!$('resultPanel').classList.contains('expanded'));
  $('btnRun').onclick = selfRun;

  $('resetProgress').onclick = async () => {
    if (!confirm('确定清空本机的做题记录吗？（代码草稿保留）')) return;
    await fetch('/api/progress/reset', { method: 'POST' });
    state.progress = {};
    updateProgressBar();
    renderSidebar();
    toast('进度已清空');
  };

  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      saveCodeFile();
      return;
    }
    if (e.ctrlKey && e.key === 'Enter') { e.preventDefault(); submit(); }
    if (e.ctrlKey && (e.key === 's' || e.key === 'S')) { e.preventDefault(); selfRun(); }
  });

  window.addEventListener('hashchange', () => {
    const m = location.hash.match(/#p=([\w-]+)/);
    if (m) selectProblem(m[1], false);
  });

  aiBind();
  aiDebugBind();
  bookBind();
  rpgBind();
  bindStats();
}

async function boot() {
  loadStars();
  bind();
  rpg = rpgLoad();
  try {
    const [pr, pg] = await Promise.all([
      fetch('/api/problems').then((r) => r.json()),
      fetch('/api/progress').then((r) => r.json()),
    ]);
    state.problems = pr.problems || [];
    state.byId = Object.fromEntries(state.problems.map((p) => [p.id, p]));
    state.progress = pg || {};
    rpgSyncFromProgress({ announce: true });
    for (const p of state.problems) {
      if (p.chapter === 1) state.open['ch:1'] = true;
    }
  } catch (e) {
    toast('无法连接本地服务，请确认 server.py 正在运行');
  }
  updateProgressBar();
  renderSidebar();
  const m = location.hash.match(/#p=([\w-]+)/);
  if (m && state.byId[m[1]]) selectProblem(m[1], false);
  else if (state.problems.length) selectProblem(state.problems[0].id, false);
  if (typeof arenaAfterData === 'function') arenaAfterData();
  if (typeof grammarAfterData === 'function') grammarAfterData();
  bookLoadManifest().catch(() => {});
}

boot();
