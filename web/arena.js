/* ============================================================
   算法竞技场
   - 限时赛制：闪电赛 / 标准赛 / 远征赛
   - 竞速积分：AC 越早，得分越高
   - 本地赛季：竞技分、段位、连续参赛、历史战绩
   - 赛后结算：逐题成绩、时间轴、战绩卡、AI 复盘
   ============================================================ */
'use strict';

const ARENA_KEY = 'oj.arena.v1';
const ARENA_BASE = { 1: 120, 2: 180, 3: 280, 4: 400, 5: 560 };
const ARENA_MAX_HISTORY = 18;

const ARENA_MODES = {
  sprint: {
    key: 'sprint',
    name: '闪电赛',
    duration: 20,
    count: 2,
    bands: [[1, 2], [2, 3]],
    difficultyText: '1 – 3 星',
    tone: 'cyan',
    blurb: '短促、轻快，用一场小型冲刺找回手感。',
    kicker: 'SPRINT',
  },
  standard: {
    key: 'standard',
    name: '标准赛',
    duration: 45,
    count: 3,
    bands: [[1, 2], [2, 3], [4, 5]],
    difficultyText: '1 – 5 星',
    tone: 'blue',
    blurb: '最经典的赛制：一道稳、一道想、一道拼。',
    kicker: 'STANDARD',
  },
  expedition: {
    key: 'expedition',
    name: '远征赛',
    duration: 75,
    count: 4,
    bands: [[1, 2], [2, 3], [3, 4], [4, 5]],
    difficultyText: '1 – 5 星',
    tone: 'violet',
    blurb: '四道题的耐力考验，留给愿意多坐一会儿的人。',
    kicker: 'EXPEDITION',
  },
};

const ARENA_TIERS = [
  { name: '青铜', roman: 'BRONZE', min: 0, color: '#b9a58a' },
  { name: '白银', roman: 'SILVER', min: 300, color: '#b8c4d4' },
  { name: '黄金', roman: 'GOLD', min: 750, color: '#f1c46b' },
  { name: '铂金', roman: 'PLATINUM', min: 1400, color: '#8fd8cf' },
  { name: '钻石', roman: 'DIAMOND', min: 2200, color: '#8ab4ff' },
  { name: '大师', roman: 'MASTER', min: 3200, color: '#d8a6ff' },
];

let arena = null;
let arenaTicker = null;
let arenaRecapRecord = null;
let arenaBindDone = false;

/* ---------------- 基础工具 ---------------- */

function arenaEsc(value) {
  return esc(String(value == null ? '' : value));
}

function arenaDefault() {
  return {
    points: 0,
    contests: 0,
    best: 0,
    totalSolved: 0,
    streak: 0,
    lastDate: '',
    history: [],
    active: null,
    lastRecord: null,
  };
}

function arenaLoad() {
  let saved = null;
  try {
    saved = JSON.parse(localStorage.getItem(ARENA_KEY) || 'null');
  } catch (e) { }
  const base = arenaDefault();
  if (!saved || typeof saved !== 'object') return base;
  const result = Object.assign(base, saved);
  result.history = Array.isArray(saved.history) ? saved.history.filter((r) => r && r.id) : [];
  if (result.active && (!Array.isArray(result.active.problems) || !result.active.problems.length)) {
    result.active = null;
  }
  if (!result.lastRecord || !result.lastRecord.id) result.lastRecord = null;
  return result;
}

function arenaSave() {
  if (!arena) return;
  try { localStorage.setItem(ARENA_KEY, JSON.stringify(arena)); } catch (e) { }
}

function arenaTierInfo(points) {
  const value = Math.max(0, Number(points) || 0);
  let current = ARENA_TIERS[0];
  let index = 0;
  for (let i = 0; i < ARENA_TIERS.length; i++) {
    if (value >= ARENA_TIERS[i].min) {
      current = ARENA_TIERS[i];
      index = i;
    }
  }
  const next = ARENA_TIERS[index + 1] || null;
  const span = next ? Math.max(1, next.min - current.min) : 1;
  const progress = next ? Math.max(0, Math.min(100, ((value - current.min) / span) * 100)) : 100;
  return Object.assign({}, current, {
    next: next ? next.name : '巅峰',
    nextMin: next ? next.min : current.min,
    progress,
    remain: next ? Math.max(0, next.min - value) : 0,
  });
}

function arenaClock(sec) {
  const total = Math.max(0, Math.floor(Number(sec) || 0));
  const mm = Math.floor(total / 60);
  const ss = total % 60;
  return String(mm).padStart(2, '0') + ':' + String(ss).padStart(2, '0');
}

function arenaDuration(min) {
  return min >= 60 ? (min / 60).toFixed(min % 60 ? 1 : 0) + ' 小时' : min + ' 分钟';
}

function arenaDateKey(ts) {
  const d = new Date(ts || Date.now());
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

function arenaDateLabel(ts) {
  const d = new Date(ts || Date.now());
  return String(d.getMonth() + 1).padStart(2, '0') + ' / ' + String(d.getDate()).padStart(2, '0') + ' ' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
}

function arenaYesterdayKey(ts) {
  const d = new Date(ts || Date.now());
  d.setDate(d.getDate() - 1);
  return arenaDateKey(d.getTime());
}

function arenaDiffStars(diff) {
  const d = Math.max(1, Math.min(5, Number(diff) || 1));
  return '★'.repeat(d) + '☆'.repeat(5 - d);
}

function arenaStatusLabel(status, attempts) {
  if (status === 'AC') return '已通过';
  if (status === 'try') return attempts ? '尝试 ' + attempts + ' 次' : '尝试过';
  return '未动';
}

function arenaGrade(record) {
  if (!record) return { key: 'D', label: 'KEEP GOING', color: '#a9b6c5' };
  const ratio = record.score / Math.max(1, record.maxScore || 1);
  if (record.solved === record.count && ratio >= 0.85) return { key: 'S', label: 'PERFECT', color: '#ffd76b' };
  if (record.solved === record.count) return { key: 'A', label: 'ALL CLEAR', color: '#7ee1c1' };
  if (record.solved / Math.max(1, record.count) >= 0.66) return { key: 'B', label: 'GOOD RUN', color: '#8ab4ff' };
  if (record.solved > 0) return { key: 'C', label: 'ON BOARD', color: '#d8a6ff' };
  return { key: 'D', label: 'KEEP GOING', color: '#a9b6c5' };
}

function arenaRecordFor(record) {
  if (!record) return null;
  if (record.id === (arena.lastRecord && arena.lastRecord.id)) return arena.lastRecord;
  return (arena.history || []).find((r) => r.id === record.id) || null;
}

/* ---------------- 赛题抽取 ---------------- */

function arenaPickProblems(mode) {
  const judged = (state.problems || []).filter((p) => p && p.has_judge);
  if (!judged.length) return [];

  const recent = new Set();
  (arena.history || []).slice(0, 5).forEach((record) => {
    (record.problems || []).forEach((item) => recent.add(item.id));
  });

  const unsolved = judged.filter((p) => {
    const progress = state.progress && state.progress[p.id];
    return !(progress && progress.status === 'AC');
  });
  let source = unsolved.length >= mode.count ? unsolved : judged;

  const picked = [];
  const used = new Set();
  const chapters = new Set();

  const pickFrom = (pool, band) => {
    let candidates = pool.filter((p) => {
      if (used.has(p.id)) return false;
      const d = Number(p.difficulty) || 1;
      return d >= band[0] && d <= band[1];
    });
    if (!candidates.length) {
      candidates = judged.filter((p) => {
        if (used.has(p.id)) return false;
        const d = Number(p.difficulty) || 1;
        return d >= band[0] && d <= band[1];
      });
    }
    if (!candidates.length) {
      candidates = judged.filter((p) => !used.has(p.id));
    }
    if (!candidates.length) return null;

    let freshChapter = candidates.filter((p) => !chapters.has(p.chapter));
    if (freshChapter.length) candidates = freshChapter;
    let notRecent = candidates.filter((p) => !recent.has(p.id));
    if (notRecent.length) candidates = notRecent;

    return candidates[Math.floor(Math.random() * candidates.length)];
  };

  for (const band of mode.bands) {
    const p = pickFrom(source, band);
    if (!p) break;
    picked.push(p);
    used.add(p.id);
    chapters.add(p.chapter);
  }

  // 极端情况下补满，保证赛制不会因为去重策略缺题。
  if (picked.length < mode.count) {
    const fallback = judged.filter((p) => !used.has(p.id));
    while (picked.length < mode.count && fallback.length) {
      const p = fallback.splice(Math.floor(Math.random() * fallback.length), 1)[0];
      picked.push(p);
      used.add(p.id);
    }
  }

  return picked.slice(0, mode.count);
}

function arenaMakeEntry(problem, label) {
  const diff = Math.max(1, Math.min(5, Number(problem.difficulty) || 1));
  return {
    id: problem.id,
    label,
    title: problem.title || problem.id,
    difficulty: diff,
    base: ARENA_BASE[diff] || 200,
    status: 'todo',
    attempts: 0,
    points: 0,
    acAt: null,
    solveSec: null,
    penalty: 0,
    lastVerdict: '',
  };
}

function arenaPointsFor(entry, acAt, startedAt, duration) {
  const ratio = Math.max(0, Math.min(1, (acAt - startedAt) / (duration * 60000)));
  const speedFactor = 1 - 0.35 * ratio;
  return Math.max(10, Math.round(entry.base * speedFactor));
}

function arenaRecalc(active) {
  const a = active || (arena && arena.active);
  if (!a) return;
  a.score = a.problems.reduce((sum, p) => sum + (p.status === 'AC' ? p.points : 0), 0);
  a.penalty = a.problems.reduce((sum, p) => sum + (p.status === 'AC' ? p.penalty : 0), 0);
  a.solved = a.problems.filter((p) => p.status === 'AC').length;
  a.maxScore = a.problems.reduce((sum, p) => sum + p.base, 0);
}

/* ---------------- 开始 / 计时 / 结算 ---------------- */

function arenaStart(modeKey) {
  if (!arena) arena = arenaLoad();
  if (arena.active) { toast('还有一场比赛正在进行'); return; }
  const mode = ARENA_MODES[modeKey];
  if (!mode) return;
  if (!state.problems || !state.problems.length) { toast('题库还在加载，请稍候'); return; }

  const picks = arenaPickProblems(mode);
  if (picks.length < mode.count) { toast('当前可判题不足，暂时无法开赛'); return; }

  const startedAt = Date.now();
  const entries = picks.map((p, i) => arenaMakeEntry(p, String.fromCharCode(65 + i)));
  const maxScore = entries.reduce((sum, p) => sum + p.base, 0);
  arena.active = {
    id: 'ar-' + startedAt.toString(36) + '-' + Math.random().toString(36).slice(2, 6),
    modeKey: mode.key,
    modeName: mode.name,
    duration: mode.duration,
    count: mode.count,
    startedAt,
    endsAt: startedAt + mode.duration * 60000,
    problems: entries,
    score: 0,
    penalty: 0,
    solved: 0,
    maxScore,
    currentId: entries[0].id,
  };
  arenaSave();

  arenaEnterLive();
  setView('oj');
  arenaRenderSide();
  arenaUpdateLive();
  arenaStartTicker();
  selectProblem(entries[0].id, false);
  arenaRenderSide();
  toast('比赛开始 · ' + mode.name + '，计时已启动');
}

function arenaEnterLive() {
  document.body.classList.add('arena-live');
  const head = $('arenaHeadLive');
  if (head) head.classList.remove('hide');
  arenaRenderSide();
  arenaUpdateLive();
}

function arenaExitLive() {
  document.body.classList.remove('arena-live');
  const head = $('arenaHeadLive');
  if (head) head.classList.add('hide');
  const side = $('arenaSide');
  if (side) side.innerHTML = '';
}

function arenaStartTicker() {
  arenaStopTicker();
  if (!arena || !arena.active) return;
  arenaTicker = setInterval(arenaTick, 1000);
  arenaTick();
}

function arenaStopTicker() {
  if (arenaTicker) {
    clearInterval(arenaTicker);
    arenaTicker = null;
  }
}

function arenaTick() {
  if (!arena || !arena.active) {
    arenaStopTicker();
    return;
  }
  const a = arena.active;
  const now = Date.now();
  const rem = Math.max(0, Math.ceil((a.endsAt - now) / 1000));
  arenaUpdateLive(rem);
  if (rem <= 0) arenaFinish(true, { auto: true, reason: 'timeout' });
}

function arenaUpdateLive(remOverride) {
  if (!arena || !arena.active) return;
  const a = arena.active;
  const now = Date.now();
  const rem = remOverride == null ? Math.max(0, Math.ceil((a.endsAt - now) / 1000)) : remOverride;
  const elapsed = Math.max(0, Math.min(a.duration * 60000, now - a.startedAt));
  const timeText = arenaClock(rem);
  const urgent = rem <= 300;

  const headTime = $('arenaHeadTime');
  if (headTime) {
    headTime.textContent = timeText;
    headTime.classList.toggle('urgent', urgent);
  }
  const headScore = $('arenaHeadScore');
  if (headScore) headScore.textContent = a.score;
  const headSolved = $('arenaHeadSolved');
  if (headSolved) headSolved.textContent = a.solved + ' / ' + a.count;

  const sideTime = $('arenaSideTime');
  if (sideTime) {
    sideTime.textContent = timeText;
    sideTime.classList.toggle('urgent', urgent);
  }
  const sideScore = $('arenaSideScore');
  if (sideScore) sideScore.textContent = a.score;
  const sideSolved = $('arenaSideSolved');
  if (sideSolved) sideSolved.textContent = a.solved + ' / ' + a.count + ' 解出';
  const sideProgress = $('arenaSideProgress');
  if (sideProgress) sideProgress.style.width = Math.min(100, (elapsed / (a.duration * 60000)) * 100) + '%';

  const homeTime = $('arenaHomeTime');
  if (homeTime) homeTime.textContent = timeText;
  const homeScore = $('arenaHomeScore');
  if (homeScore) homeScore.textContent = a.score;
  const homeSolved = $('arenaHomeSolved');
  if (homeSolved) homeSolved.textContent = a.solved + ' / ' + a.count;
}

function arenaOnSubmit(problem, result) {
  if (!arena || !arena.active || !problem || !result) return;
  const a = arena.active;
  const entry = a.problems.find((p) => p.id === problem.id);
  if (!entry) return;

  const now = Date.now();
  const verdict = String(result.verdict || 'WA');

  if (verdict === 'AC') {
    if (entry.status !== 'AC') {
      const acAt = Math.min(now, a.endsAt);
      entry.status = 'AC';
      entry.acAt = acAt;
      entry.solveSec = Math.max(0, Math.floor((acAt - a.startedAt) / 1000));
      entry.points = arenaPointsFor(entry, acAt, a.startedAt, a.duration);
      entry.penalty = Math.floor((acAt - a.startedAt) / 60000) + entry.attempts * 5;
      arenaRecalc(a);
      arenaSave();
      arenaRenderSide();
      arenaUpdateLive();
      toast('赛题 ' + entry.label + ' 已通过 · +' + entry.points + ' 分');
      if (a.solved >= a.count) {
        setTimeout(() => {
          if (arena && arena.active && arena.active.id === a.id) {
            arenaFinish(true, { auto: true, allSolved: true });
          }
        }, 1100);
      }
    }
    return;
  }

  if (entry.status === 'AC') return;
  entry.status = 'try';
  entry.attempts += 1;
  entry.lastVerdict = verdict;
  arenaSave();
  arenaRenderSide();
}

function arenaFinish(auto, opts) {
  if (!arena || !arena.active) return;
  arenaStopTicker();
  const a = arena.active;
  const options = opts || {};
  const now = Date.now();
  const tierBefore = arenaTierInfo(arena.points);
  const elapsed = Math.max(0, Math.min(a.duration * 60000, now - a.startedAt));
  const solved = a.problems.filter((p) => p.status === 'AC').length;
  const score = a.problems.reduce((sum, p) => sum + (p.status === 'AC' ? p.points : 0), 0);
  const penalty = a.problems.reduce((sum, p) => sum + (p.status === 'AC' ? p.penalty : 0), 0);
  const maxScore = a.problems.reduce((sum, p) => sum + p.base, 0);
  const allSolved = solved === a.count;
  const completionBonus = solved > 0 ? 6 : 0;
  const earned = Math.round((score / Math.max(1, maxScore)) * 52) + solved * 12 + completionBonus + (allSolved ? 18 : 0);

  const today = arenaDateKey(now);
  if (arena.lastDate === today) {
    // 同一天多赛不重复累加连续天数
  } else if (arena.lastDate === arenaYesterdayKey(now)) {
    arena.streak += 1;
  } else {
    arena.streak = 1;
  }
  arena.lastDate = today;

  arena.points += earned;
  arena.contests += 1;
  arena.best = Math.max(arena.best, score);
  arena.totalSolved += solved;
  const tierAfter = arenaTierInfo(arena.points);

  const record = {
    id: a.id,
    modeKey: a.modeKey,
    modeName: a.modeName,
    duration: a.duration,
    count: a.count,
    startedAt: a.startedAt,
    endedAt: now,
    elapsed: Math.min(a.duration * 60000, elapsed),
    score,
    maxScore,
    solved,
    penalty,
    allSolved,
    auto: !!auto,
    aborted: !!options.aborted,
    earned,
    tierBefore: tierBefore.name,
    tierAfter: tierAfter.name,
    arenaPointsBefore: arena.points - earned,
    arenaPointsAfter: arena.points,
    streak: arena.streak,
    date: today,
    problems: a.problems.map((p) => ({
      id: p.id,
      label: p.label,
      title: p.title,
      difficulty: p.difficulty,
      base: p.base,
      status: p.status,
      attempts: p.attempts,
      points: p.status === 'AC' ? p.points : 0,
      solveSec: p.solveSec,
      penalty: p.status === 'AC' ? p.penalty : 0,
      lastVerdict: p.lastVerdict,
    })),
  };

  arena.active = null;
  record.grade = arenaGrade(record).key;
  arena.lastRecord = record;
  arena.history.unshift(record);
  arena.history = arena.history.slice(0, ARENA_MAX_HISTORY);
  arenaSave();
  arenaStopTicker();
  arenaExitLive();
  setView('arena');
  arenaRender();
  arenaShowRecap(record);
  if (auto && options.reason === 'timeout') toast('时间到，比赛已自动结算');
}

/* ---------------- 侧栏比赛控制台 ---------------- */

function arenaRenderSide() {
  const side = $('arenaSide');
  if (!side) return;
  if (!arena || !arena.active) {
    side.innerHTML = '';
    return;
  }
  const a = arena.active;
  const current = a.currentId;
  const rem = Math.max(0, Math.ceil((a.endsAt - Date.now()) / 1000));
  const probs = a.problems.map((p) => {
    const selected = p.id === current ? ' on' : '';
    const statusClass = p.status === 'AC' ? ' ac' : (p.status === 'try' ? ' try' : '');
    const stateText = p.status === 'AC'
      ? 'AC · +' + p.points
      : (p.status === 'try' ? '尝试 ' + p.attempts + ' 次' : '未动');
    return '<button class="arena-prob' + selected + statusClass + '" data-arena-problem="' + arenaEsc(p.id) + '" type="button">'
      + '<span class="arena-prob-letter">' + arenaEsc(p.label) + '</span>'
      + '<span class="arena-prob-copy"><b>' + arenaEsc(p.title) + '</b><small>' + arenaDiffStars(p.difficulty) + ' · ' + p.base + ' 基础分</small></span>'
      + '<span class="arena-prob-state">' + arenaEsc(stateText) + '</span>'
      + '</button>';
  }).join('');

  side.innerHTML = '<div class="arena-side-inner">'
    + '<div class="arena-side-kicker">LIVE · ' + arenaEsc(a.modeName) + '</div>'
    + '<h2 class="arena-side-title">正在比赛</h2>'
    + '<div class="arena-side-timerline">'
    + '<div><b class="arena-side-time' + (rem <= 300 ? ' urgent' : '') + '" id="arenaSideTime">' + arenaClock(rem) + '</b><span>剩余时间</span></div>'
    + '<div class="arena-side-score"><b id="arenaSideScore">' + a.score + '</b><small>/ ' + a.maxScore + ' 分</small></div>'
    + '</div>'
    + '<div class="arena-side-track"><i id="arenaSideProgress"></i></div>'
    + '<div class="arena-side-meta"><span id="arenaSideSolved">' + a.solved + ' / ' + a.count + ' 解出</span><span>AC 越早，积分越高</span></div>'
    + '<div class="arena-side-probs">' + probs + '</div>'
    + '<div class="arena-side-divider"></div>'
    + '<p class="arena-side-tip"><b>提交即结算。</b> 每题按 AC 时的剩余时间计分；提前完成全部题目会自动交卷。</p>'
    + '<button class="arena-side-finish" id="arenaSideFinish" type="button">交卷 · 结算</button>'
    + '<div class="arena-side-foot">计时结束自动结算 · 提交记录照常保存</div>'
    + '</div>';
  arenaUpdateLive(rem);
}

/* ---------------- 赛场主页 ---------------- */

function arenaRender() {
  const workspace = $('arenaWorkspace');
  if (!workspace) return;
  if (arena && arena.active) {
    arenaRenderLivePage();
    return;
  }
  const tier = arenaTierInfo(arena.points);
  const history = arena.history || [];
  const historyHtml = history.length
    ? history.map((rec) => '<div class="arena-record" data-arena-record="' + arenaEsc(rec.id) + '" role="button" tabindex="0">'
      + '<div><span class="arena-record-mode">' + arenaEsc(rec.modeName) + ' · ' + rec.solved + '/' + rec.count + ' 解出</span>'
      + '<small>' + arenaEsc(arenaDateLabel(rec.endedAt)) + ' · 评级 ' + arenaEsc(rec.grade || arenaGrade(rec).key) + ' · 罚时 ' + rec.penalty + '</small></div>'
      + '<div class="arena-record-score">' + rec.score + '<small> 分</small></div>'
      + '<span class="arena-record-delta">+' + rec.earned + ' 竞技分</span>'
      + '</div>').join('')
    : '<div class="arena-empty"><b>还没有战绩</b>选一个赛制，开始第一场。</div>';

  const modes = Object.values(ARENA_MODES).map((mode, i) => {
    const idx = String(i + 1).padStart(2, '0');
    return '<article class="arena-mode-card" data-tone="' + mode.tone + '">'
      + '<div class="arena-mode-top"><span class="arena-mode-index">' + idx + '</span><span>' + mode.kicker + '</span></div>'
      + '<h3>' + mode.name + '</h3>'
      + '<p>' + mode.blurb + '</p>'
      + '<div class="arena-mode-meta"><span>' + mode.count + ' 题</span><span>' + mode.difficultyText + '</span><span>' + mode.duration + ' 分钟</span></div>'
      + '<button class="arena-start" data-arena-mode="' + mode.key + '" type="button">开始比赛 <span>›</span></button>'
      + '</article>';
  }).join('');

  workspace.innerHTML = '<section class="arena-hero">'
    + '<div class="arena-hero-top"><span class="arena-kicker">SEASON 01 · LOCAL LEAGUE</span><span class="arena-season-chip">2026 · GUIYANG</span></div>'
    + '<div class="arena-hero-body">'
    + '<div class="arena-hero-copy"><div class="arena-eyebrow">ALGORITHM ARENA</div>'
    + '<h1>算法竞技场</h1>'
    + '<p>把会做的题，变成一场能赢的比赛。限时、竞速、即时结算；每一场都为你的本地题库生成一套独一无二的赛题。</p>'
    + '<div class="arena-hero-actions"><button class="arena-btn primary" data-arena-scroll="modes" type="button">选择赛制 <span>→</span></button>'
    + '<button class="arena-btn ghost" data-arena-scroll="rules" type="button">赛场规则</button></div></div>'
    + '<div class="arena-pass"><span class="arena-pass-label">CURRENT TIER</span>'
    + '<div class="arena-ring" style="--p:' + tier.progress.toFixed(1) + ';--tier:' + tier.color + '"><div class="arena-ring-core"><b>' + tier.name + '</b><small>' + tier.roman + '</small></div></div>'
    + '<div class="arena-pass-points"><b>' + arena.points + '</b><span>竞技分</span></div>'
    + '<div class="arena-pass-next">' + (tier.next === '巅峰' ? '已达巅峰' : '距离' + tier.next + '还差 ' + tier.remain + ' 分') + '</div>'
    + '</div></div>'
    + '<div class="arena-hero-stats">'
    + '<div><b>' + arena.contests + '</b><span>已参赛</span></div>'
    + '<div><b>' + (arena.best || '—') + '</b><span>单场最高分</span></div>'
    + '<div><b>' + arena.totalSolved + '</b><span>赛内 AC</span></div>'
    + '<div><b>' + arena.streak + '</b><span>连续参赛天</span></div>'
    + '</div></section>'
    + '<div class="arena-body-grid">'
    + '<section class="arena-main-col"><div class="arena-section-head" id="arenaModsHead"><h2>选择赛制</h2><span>每一场都是一次重新抽题</span></div>'
    + '<div class="arena-mode-grid">' + modes + '</div>'
    + '<section class="arena-rules" id="arenaRules"><h3>赛场规则</h3><div class="arena-rules-grid">'
    + '<p><b>竞速积分：</b>每题按 AC 时刻计算，越早完成，分数越高。</p>'
    + '<p><b>罚时：</b>AC 前每次错误尝试 +5 分钟，最终计入赛后罚时。</p>'
    + '<p><b>提前交卷：</b>可以随时结束并结算；全部解出会自动完成比赛。</p>'
    + '<p><b>题目来源：</b>只从本地可判题库抽取，优先选择未 AC 和有章节差异的题。</p>'
    + '<p><b>赛题揭晓：</b>开赛前不显示题目，开赛后按 A/B/C 顺序解锁。</p>'
    + '<p><b>AI 助教：</b>赛中依然可用，但先自己读题、先自己写代码。</p>'
    + '</div></section></section>'
    + '<aside class="arena-aside"><div class="arena-history-card"><h3>最近战绩 <small>竞技场 · 本地赛季</small></h3>' + historyHtml + '</div>'
    + '<div class="arena-tip-card"><div class="arena-tip-kicker">ONE MORE ROUND</div><p><b>从 20 分钟开始。</b> 闪电赛最适合检验手感；标准赛适合一次完整的训练；远征赛留给愿意坐久一点的人。</p></div>'
    + '</aside></div>';
}

function arenaRenderLivePage() {
  const workspace = $('arenaWorkspace');
  if (!workspace || !arena.active) return;
  const a = arena.active;
  const rem = Math.max(0, Math.ceil((a.endsAt - Date.now()) / 1000));
  const cards = a.problems.map((p) => '<div class="arena-live-card' + (p.status === 'AC' ? ' ac' : '') + '">'
    + '<b>' + arenaEsc(p.label) + ' · ' + arenaEsc(p.title) + '</b>'
    + '<small>' + arenaDiffStars(p.difficulty) + ' · ' + (p.status === 'AC' ? '已通过 +' + p.points + ' 分' : arenaStatusLabel(p.status, p.attempts)) + '</small>'
    + '</div>').join('');
  workspace.innerHTML = '<section class="arena-hero arena-hero-live">'
    + '<div class="arena-hero-top"><span class="arena-kicker">LIVE · ' + arenaEsc(a.modeName) + '</span><span class="arena-season-chip">比赛进行中</span></div>'
    + '<div class="arena-hero-body"><div class="arena-hero-copy"><div class="arena-eyebrow">ALGORITHM ARENA</div>'
    + '<h1 id="arenaHomeTime">' + arenaClock(rem) + '</h1>'
    + '<p>这一场正在计时。左侧比赛面板可以切换赛题；提交后即时更新得分。</p>'
    + '<div class="arena-hero-actions"><button class="arena-btn primary" data-arena-resume type="button">回到做题 <span>→</span></button>'
    + '<button class="arena-btn ghost" data-arena-finish type="button">交卷并结算</button></div></div>'
    + '<div class="arena-pass"><span class="arena-pass-label">LIVE SCORE</span>'
    + '<div class="arena-pass-points"><b id="arenaHomeScore">' + a.score + '</b><span>/ ' + a.maxScore + ' 分</span></div>'
    + '<div class="arena-side-meta" style="margin-top:10px"><span id="arenaHomeSolved">' + a.solved + ' / ' + a.count + '</span><span>已解出</span></div>'
    + '</div></div>'
    + '<div class="arena-hero-stats"><div><b>' + a.count + '</b><span>赛题数</span></div><div><b>' + a.duration + '</b><span>分钟</span></div><div><b>' + a.solved + '</b><span>已通过</span></div><div><b>' + a.penalty + '</b><span>当前罚时</span></div></div>'
    + '</section><section class="arena-live-board"><h2>赛题面板</h2><div class="arena-live-cards">' + cards + '</div></section>';
}

/* ---------------- 赛后总结 ---------------- */

function arenaShowRecap(record) {
  const rec = arenaRecordFor(record) || record;
  if (!rec) return;
  arenaRecapRecord = rec;
  const recap = $('arenaRecap');
  const content = $('arenaRecapContent');
  if (!recap || !content) return;

  const stats = '<div class="arena-recap-stats">'
    + '<div><b>' + rec.score + '</b><span>本场得分</span></div>'
    + '<div><b>' + rec.solved + ' / ' + rec.count + '</b><span>题目通过</span></div>'
    + '<div><b>' + rec.penalty + '</b><span>罚时</span></div>'
    + '<div><b>+' + rec.earned + '</b><span>竞技分</span></div>'
    + '</div>';

  const problemHtml = rec.problems.map((p) => '<div class="arena-recap-problem' + (p.status === 'AC' ? ' ac' : '') + '">'
    + '<span class="letter">' + arenaEsc(p.label) + '</span>'
    + '<div><b>' + arenaEsc(p.title) + '</b><small>' + arenaDiffStars(p.difficulty) + ' · ' + p.base + ' 基础分</small></div>'
    + '<span class="result">' + (p.status === 'AC' ? 'AC · +' + p.points : (p.status === 'try' ? '尝试 ' + p.attempts + ' 次' : '未提交')) + '</span>'
    + '</div>').join('');

  const dots = rec.problems.map((p) => {
    if (p.status !== 'AC' || p.solveSec == null) return '';
    const pct = Math.max(1.5, Math.min(97, ((p.solveSec * 1000) / (rec.duration * 60000)) * 100));
    return '<span class="arena-timeline-dot" style="left:' + pct.toFixed(1) + '%" data-label="' + arenaEsc(p.label) + ' · ' + arenaClock(p.solveSec) + '"></span>';
  }).join('');

  const badges = '<span>' + arenaEsc(rec.modeName) + '</span>'
    + '<span>' + arenaClock(Math.floor(rec.elapsed / 1000)) + ' 用时</span>'
    + (rec.allSolved ? '<span class="gold">ALL CLEAR · 全解</span>' : '')
    + (rec.aborted ? '<span>提前结束</span>' : '')
    + '<span>' + arenaEsc(rec.tierBefore) + ' → ' + arenaEsc(rec.tierAfter) + '</span>';
  const grade = arenaGrade(rec);

  content.innerHTML = '<div class="arena-recap-hero">'
    + '<div class="arena-recap-kicker">MATCH REPORT · ' + arenaEsc(rec.date) + '</div>'
    + '<h2>' + arenaEsc(rec.modeName) + ' · ' + (rec.allSolved ? '完美收官' : '完赛') + '</h2>'
    + '<p class="arena-recap-sub">' + (rec.solved ? '节奏已经留下，下一场可以更快。' : '这场没有 AC，但每一次尝试都算数。') + '</p>'
    + '<div class="arena-recap-scoreline"><b>' + rec.score + '</b><span>/ ' + rec.maxScore + ' 分</span></div>'
    + '<div class="arena-recap-badges">' + badges + '</div>'
    + '<div class="arena-recap-grade" style="--grade:' + grade.color + '"><b>' + grade.key + '</b><small>' + grade.label + '</small></div>'
    + '</div>' + stats
    + '<div class="arena-recap-body">'
    + '<div class="arena-recap-section-title"><span>逐题成绩</span><small>罚时按 AC 时间 + 错误尝试计算</small></div>'
    + '<div class="arena-recap-problems">' + problemHtml + '</div>'
    + '<div class="arena-recap-section-title" style="margin-top:15px"><span>AC 时间轴</span><small>' + arenaDuration(rec.duration) + '场</small></div>'
    + '<div class="arena-recap-timeline">' + dots + '</div>'
    + '<div class="arena-recap-actions">'
    + '<button class="primary" data-arena-review type="button">让 AI 复盘</button>'
    + '<button data-arena-card type="button">保存战绩卡</button>'
    + '<button data-arena-again type="button">再来一场</button>'
    + '<span class="spacer"></span><button data-arena-close type="button">回到竞技场</button>'
    + '</div></div>';

  recap.classList.remove('hide');
  document.body.classList.add('arena-recap-open');
}

function arenaCloseRecap() {
  const recap = $('arenaRecap');
  if (recap) recap.classList.add('hide');
  document.body.classList.remove('arena-recap-open');
  arenaRecapRecord = null;
}

function arenaSaveCard() {
  const rec = arenaRecapRecord;
  if (!rec) return;
  const canvas = document.createElement('canvas');
  canvas.width = 1200;
  canvas.height = 630;
  const ctx = canvas.getContext('2d');
  if (!ctx) { toast('当前浏览器不支持生成战绩卡'); return; }

  const bg = ctx.createLinearGradient(0, 0, 1200, 630);
  bg.addColorStop(0, '#08152b');
  bg.addColorStop(.58, '#10294d');
  bg.addColorStop(1, '#091932');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, 1200, 630);

  const glow = ctx.createRadialGradient(1000, 60, 0, 1000, 60, 520);
  glow.addColorStop(0, 'rgba(79,169,255,.42)');
  glow.addColorStop(1, 'rgba(79,169,255,0)');
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, 1200, 630);

  ctx.strokeStyle = 'rgba(255,255,255,.08)';
  ctx.lineWidth = 1;
  for (let x = 0; x <= 1200; x += 48) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 630); ctx.stroke();
  }
  for (let y = 0; y <= 630; y += 48) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1200, y); ctx.stroke();
  }

  ctx.strokeStyle = 'rgba(169, 215, 255, .22)';
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.arc(1020, 100, 118, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = 'rgba(169, 215, 255, .12)';
  ctx.beginPath(); ctx.arc(1020, 100, 154, 0, Math.PI * 2); ctx.stroke();
  ctx.strokeStyle = 'rgba(255, 213, 128, .20)';
  ctx.beginPath(); ctx.arc(1020, 100, 190, 0, Math.PI * 2); ctx.stroke();

  ctx.fillStyle = '#a8d7ff';
  ctx.font = '700 15px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText('MATCH REPORT · LOCAL OJ', 72, 77);
  ctx.fillStyle = '#ffffff';
  ctx.font = '700 62px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText(rec.modeName + ' 完赛', 72, 154);
  ctx.fillStyle = 'rgba(205,230,255,.58)';
  ctx.font = '400 19px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText(rec.date + ' · ' + arenaDateLabel(rec.endedAt), 72, 198);

  ctx.fillStyle = '#ffffff';
  ctx.font = '800 150px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText(String(rec.score), 68, 365);
  ctx.fillStyle = 'rgba(255,229,166,.9)';
  ctx.font = '600 20px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText('分 / ' + rec.maxScore, 72, 405);

  const grade = arenaGrade(rec);
  ctx.fillStyle = grade.color;
  ctx.font = '800 96px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText(grade.key, 908, 260);
  ctx.font = '600 13px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillStyle = 'rgba(230,242,255,.48)';
  ctx.fillText(grade.label, 914, 286);

  const badges = [
    '通过 ' + rec.solved + ' / ' + rec.count,
    '罚时 ' + rec.penalty,
    rec.allSolved ? 'ALL CLEAR' : '节奏复盘',
    '+ ' + rec.earned + ' 竞技分',
  ];
  let bx = 72;
  ctx.font = '500 15px "Microsoft YaHei", "PingFang SC", sans-serif';
  badges.forEach((badge) => {
    const w = ctx.measureText(badge).width + 22;
    ctx.fillStyle = 'rgba(255,255,255,.075)';
    ctx.beginPath();
    ctx.roundRect(bx, 444, w, 32, 16);
    ctx.fill();
    ctx.fillStyle = 'rgba(224,240,255,.70)';
    ctx.fillText(badge, bx + 11, 465);
    bx += w + 9;
  });

  ctx.fillStyle = 'rgba(206,232,255,.58)';
  ctx.font = '500 16px "Microsoft YaHei", "PingFang SC", sans-serif';
  const problemLine = rec.problems.map((p) => p.label + (p.status === 'AC' ? ' ✓' : ' ·')).join('   ');
  ctx.fillText(problemLine, 72, 528);

  ctx.fillStyle = 'rgba(255,255,255,.42)';
  ctx.font = '400 14px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText('本地 OJ · 从语法到算法 · 贵阳生活题库', 72, 580);

  ctx.fillStyle = 'rgba(255,255,255,.76)';
  ctx.font = '700 34px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText(rec.tierAfter, 930, 560);
  ctx.fillStyle = 'rgba(174,213,250,.52)';
  ctx.font = '400 12px "Microsoft YaHei", "PingFang SC", sans-serif';
  ctx.fillText('CURRENT TIER', 930, 580);

  const finish = (url) => {
    const link = document.createElement('a');
    link.download = 'OJ-竞技场-' + rec.modeName + '-' + rec.date + '.png';
    link.href = url;
    document.body.appendChild(link);
    link.click();
    link.remove();
    if (url.indexOf('blob:') === 0) setTimeout(() => URL.revokeObjectURL(url), 1000);
    toast('战绩卡已保存到下载文件夹');
  };

  if (canvas.toBlob) {
    canvas.toBlob((blob) => {
      if (!blob) { toast('战绩卡生成失败'); return; }
      finish(URL.createObjectURL(blob));
    }, 'image/png');
  } else {
    finish(canvas.toDataURL('image/png'));
  }
}

function arenaReviewRecord() {
  const rec = arenaRecapRecord;
  if (!rec) return;
  if (typeof aiSetMode !== 'function' || typeof aiOpen !== 'function') {
    toast('AI 助教暂未就绪');
    return;
  }
  const problemLines = rec.problems.map((p) => {
    const time = p.solveSec == null ? '未通过' : arenaClock(p.solveSec);
    return p.label + '「' + p.title + '」：' + (p.status === 'AC' ? 'AC，用时 ' + time + '，+' + p.points + ' 分' : (p.status === 'try' ? '未通过，尝试 ' + p.attempts + ' 次' : '未提交'));
  }).join('\n');
  const prompt = '请作为我的算法竞赛教练，复盘我在本地 OJ「算法竞技场」的这场比赛。\n'
    + '赛制：' + rec.modeName + '（' + rec.count + ' 题 / ' + rec.duration + ' 分钟）\n'
    + '结果：' + rec.solved + '/' + rec.count + ' 通过，得分 ' + rec.score + '/' + rec.maxScore + '，罚时 ' + rec.penalty + '\n'
    + '逐题情况：\n' + problemLines + '\n\n'
    + '请用 Markdown 输出：1）这场比赛的节奏诊断；2）每道题的得失与关键卡点；3）下一场最值得练的 1 个具体方向（不要泛泛而谈）；4）给我一个 20 分钟内可执行的训练动作。';
  aiSetMode('review');
  aiOpen();
  const input = $('aiInput');
  if (input) {
    input.value = prompt;
    input.focus();
    try { input.dispatchEvent(new Event('input', { bubbles: true })); } catch (e) { }
  }
  toast('已把本场战绩放进 AI 复盘，点击发送即可');
}

function arenaAgain() {
  const rec = arenaRecapRecord;
  if (!rec) return;
  const modeKey = rec.modeKey;
  arenaCloseRecap();
  arenaStart(modeKey);
}

/* ---------------- 事件 ---------------- */

function arenaBind() {
  if (arenaBindDone) return;
  arenaBindDone = true;

  const workspace = $('arenaWorkspace');
  if (workspace) {
    workspace.addEventListener('click', (e) => {
      const start = e.target.closest('[data-arena-mode]');
      if (start) { arenaStart(start.dataset.arenaMode); return; }
      const scroll = e.target.closest('[data-arena-scroll]');
      if (scroll) {
        const target = scroll.dataset.arenaScroll === 'rules' ? $('arenaRules') : $('arenaModsHead');
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      const record = e.target.closest('[data-arena-record]');
      if (record) {
        const rec = arenaRecordFor({ id: record.dataset.arenaRecord });
        if (rec) arenaShowRecap(rec);
        return;
      }
      if (e.target.closest('[data-arena-resume]')) { setView('oj'); return; }
      if (e.target.closest('[data-arena-finish]')) { arenaAskFinish(); return; }
    });
  }

  const side = $('arenaSide');
  if (side) {
    side.addEventListener('click', (e) => {
      const problem = e.target.closest('[data-arena-problem]');
      if (problem) {
        if (!arena || !arena.active) return;
        arena.active.currentId = problem.dataset.arenaProblem;
        arenaSave();
        arenaRenderSide();
        selectProblem(problem.dataset.arenaProblem, false);
        setView('oj');
        return;
      }
      if (e.target.closest('#arenaSideFinish')) arenaAskFinish();
    });
  }

  const headFinish = $('arenaHeadFinish');
  if (headFinish) headFinish.addEventListener('click', arenaAskFinish);

  const confirm = $('arenaConfirm');
  if (confirm) {
    confirm.addEventListener('click', (e) => {
      if (e.target === confirm || e.target.closest('[data-arena-confirm-cancel]')) {
        confirm.classList.add('hide');
        return;
      }
      if (e.target.closest('[data-arena-confirm-go]')) {
        confirm.classList.add('hide');
        arenaFinish(false, { aborted: false });
      }
    });
  }

  const recap = $('arenaRecap');
  if (recap) {
    recap.addEventListener('click', (e) => {
      if (e.target === recap || e.target.closest('[data-arena-close]') || e.target.closest('#arenaRecapClose')) {
        arenaCloseRecap();
        return;
      }
      if (e.target.closest('[data-arena-review]')) { arenaReviewRecord(); return; }
      if (e.target.closest('[data-arena-card]')) { arenaSaveCard(); return; }
      if (e.target.closest('[data-arena-again]')) { arenaAgain(); return; }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const recapEl = $('arenaRecap');
    if (recapEl && !recapEl.classList.contains('hide')) { arenaCloseRecap(); return; }
    const confirmEl = $('arenaConfirm');
    if (confirmEl && !confirmEl.classList.contains('hide')) confirmEl.classList.add('hide');
  });
}

function arenaAskFinish() {
  if (!arena || !arena.active) return;
  const confirm = $('arenaConfirm');
  if (!confirm) { arenaFinish(false, {}); return; }
  const a = arena.active;
  const body = $('arenaConfirmText');
  if (body) {
    body.textContent = '当前 ' + a.solved + ' / ' + a.count + ' 题通过，得分 ' + a.score + '。交卷后会立即结算，剩余时间不会保留。';
  }
  confirm.classList.remove('hide');
}

function arenaBoot() {
  arena = arenaLoad();
  arenaBind();
  if (arena.active) {
    document.body.classList.add('arena-live');
    const head = $('arenaHeadLive');
    if (head) head.classList.remove('hide');
    arenaRenderSide();
    arenaStartTicker();
  }
  if (currentView === 'arena') arenaRender();
}

function arenaAfterData() {
  if (!arena) arena = arenaLoad();
  if (arena.active) {
    if (Date.now() >= arena.active.endsAt) {
      arenaFinish(true, { auto: true, reason: 'timeout' });
      return;
    }
    document.body.classList.add('arena-live');
    const head = $('arenaHeadLive');
    if (head) head.classList.remove('hide');
    const currentId = arena.active.currentId || (arena.active.problems[0] && arena.active.problems[0].id);
    if (currentId && state.byId && state.byId[currentId]) {
      if (!state.current || state.current.id !== currentId) {
        selectProblem(currentId, false);
      }
    }
    arenaRenderSide();
    arenaStartTicker();
  }
  if (currentView === 'arena') arenaRender();
}

arenaBoot();

/* app.js 的数据加载可能晚于本文件执行；数据到位后再补一次同步。 */
setTimeout(() => {
  if (state.problems && state.problems.length && !(arena && arena.active && document.body.classList.contains('arena-live'))) {
    arenaAfterData();
  }
}, 1200);
