# 静的サイト生成: concerts.json -> index.html（リポジトリ直下＝GitHub Pagesのルート公開用）
# データをHTMLに埋め込み、クライアント側で検索・絞り込み・並び替え・無限スクロールする単一ファイルを出力。
import json
import os
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(ROOT, "concerts.json"), encoding="utf-8") as f:
        return json.load(f)


def build():
    data = load()
    updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = json.dumps(data, ensure_ascii=False)

    html = TEMPLATE.replace("__UPDATED__", updated) \
                   .replace("__COUNT__", str(len(data))) \
                   .replace("__DATA__", payload)
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"生成: {out}（{len(data)}件, 更新 {updated}）")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>クラシックコンサート横断検索</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#F9F6F1; --card:#ffffff; --fg:#26221c; --sub:#8a8377; --line:#e7e0d4;
  --accent:#8a5a2b; --accent-soft:#f0e7d8; --free:#2f8a5b; --free-bg:#e3f3ea;
  --shadow:0 2px 8px rgba(0,0,0,.08); --shadow-h:0 4px 16px rgba(0,0,0,.12);
}
@media (prefers-color-scheme:dark){
  :root{--bg:#17140f; --card:#211d16; --fg:#ece7dd; --sub:#9b9384; --line:#332e24;
        --accent:#d7a86a; --accent-soft:#2b2417; --free:#5cc48c; --free-bg:#1e3128;
        --shadow:0 2px 8px rgba(0,0,0,.35); --shadow-h:0 4px 16px rgba(0,0,0,.5);}
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font-family:"Noto Sans JP",system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:820px;margin:0 auto;padding:0 18px}
h1,h2{font-family:"Noto Serif JP",serif}

/* ヘッダー */
header{background:var(--card);border-bottom:1px solid var(--line);
  padding:22px 0 18px;position:sticky;top:0;z-index:20;box-shadow:var(--shadow)}
h1{margin:0;font-size:1.32rem;font-weight:700;letter-spacing:.02em}
.subtitle{color:var(--sub);font-size:.85rem;margin-top:4px}
.updated{color:var(--sub);font-size:.72rem;margin-top:6px}

/* フィルター */
.filters{display:flex;flex-direction:column;gap:11px;margin-top:16px}
.period{display:flex;gap:7px;flex-wrap:wrap}
.period button{padding:7px 15px;border:1px solid var(--line);background:var(--bg);
  color:var(--sub);border-radius:99px;font-size:.85rem;cursor:pointer;font-family:inherit;transition:.15s}
.period button:hover{border-color:var(--accent)}
.period button.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:500}
.row2{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
.row2 input[type=search],.row2 select{padding:9px 13px;border:1px solid var(--line);
  border-radius:9px;background:var(--bg);color:var(--fg);font-size:.9rem;font-family:inherit}
.row2 input[type=search]{flex:1;min-width:190px}
.chk{display:flex;align-items:center;gap:6px;font-size:.86rem;color:var(--sub);cursor:pointer;white-space:nowrap}
.chk input{width:16px;height:16px;accent-color:var(--free)}

/* 件数 */
.count{color:var(--sub);font-size:.86rem;margin:20px 0 4px}
.count b{color:var(--accent);font-weight:700}

/* カード */
main{padding:0 0 70px}
.card{position:relative;display:flex;gap:18px;background:var(--card);
  border-radius:12px;padding:20px 22px;margin-top:18px;box-shadow:var(--shadow);
  transition:box-shadow .15s,transform .15s}
.card:hover{box-shadow:var(--shadow-h);transform:translateY(-1px)}
.date-col{flex:0 0 64px;text-align:center;border-right:1px solid var(--line);padding-right:16px}
.date-col .md{font-family:"Noto Serif JP",serif;font-size:1.5rem;font-weight:700;line-height:1.15;color:var(--accent);white-space:nowrap}
.date-col .w{font-size:.78rem;color:var(--sub);margin-top:3px}
.date-col .w.sat{color:#3a6ea5}.date-col .w.sun{color:#b5495b}
.info-col{flex:1;min-width:0}
.badge{float:right;margin-left:12px;font-size:.8rem;font-weight:700;padding:3px 11px;border-radius:99px;
  background:var(--accent-soft);color:var(--accent);white-space:nowrap}
.badge.free{background:var(--free-bg);color:var(--free)}
.card h2{font-size:1.15rem;margin:0 0 8px;font-weight:700;line-height:1.45}
.card h2 a{color:var(--fg);text-decoration:none}
.card h2 a:hover{color:var(--accent)}
.tags{margin:0 0 6px}
.tag-notable{display:inline-block;background:#fdecea;color:#c0392b;font-size:.74rem;
  font-weight:700;padding:2px 10px;border-radius:99px}
@media (prefers-color-scheme:dark){.tag-notable{background:#3a1f1c;color:#e78b83}}
.venue{font-size:.82rem;color:var(--sub);margin:2px 0}
.venue .map-link{color:var(--accent);text-decoration:none;margin-left:6px;font-size:.78rem;white-space:nowrap}
.venue .map-link:hover{text-decoration:underline}
.perf{font-size:.86rem;margin:8px 0 0}
.perf .lbl{color:var(--sub);margin-right:5px}
.perf .rest{display:none}.perf.open .rest{display:inline}
.morebtn{background:none;border:none;color:var(--accent);cursor:pointer;font-size:.82rem;
  font-family:inherit;padding:0 0 0 4px;text-decoration:underline}
.perf.open .morebtn{display:none}
details.prog{margin-top:10px}
details.prog summary{cursor:pointer;color:var(--accent);font-size:.84rem;font-weight:500;list-style:none}
details.prog summary::-webkit-details-marker{display:none}
details.prog summary::before{content:"▸ ";font-size:.75rem}
details.prog[open] summary::before{content:"▾ "}
details.prog .body{font-size:.85rem;color:var(--sub);margin-top:6px;white-space:pre-wrap}
.action-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;align-items:center}
.yt-btn{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;font-size:.82rem;font-weight:500;
  color:#c0392b;background:#fdecea;border-radius:8px;text-decoration:none}
.yt-btn:hover{opacity:.85}
.yt-btn .ico{color:#e02020;font-size:.9rem}
@media (prefers-color-scheme:dark){.yt-btn{background:#3a1f1c;color:#f0a49c}}
.ticket-btn{display:inline-block;padding:8px 18px;font-size:.85rem;font-weight:700;
  color:#fff;background:var(--accent);border-radius:8px;text-decoration:none}
.ticket-btn:hover{opacity:.88}
.search-ticket-link{font-size:.78rem;color:var(--sub);text-decoration:underline}
.empty{text-align:center;color:var(--sub);padding:70px 0}
#sentinel{height:1px}

/* フッター */
footer{text-align:center;color:var(--sub);font-size:.76rem;padding:26px 18px;border-top:1px solid var(--line)}
footer .note{margin-top:4px;font-size:.72rem}

/* スマホ */
@media (max-width:560px){
  .card{padding:16px 16px;gap:12px;flex-direction:row}
  .date-col{flex-basis:52px;padding-right:12px}
  .date-col .md{font-size:1.2rem}
  h1{font-size:1.14rem}
}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>🎻 クラシックコンサート横断検索</h1>
    <div class="subtitle">全国のクラシック公演をまとめて探せる</div>
    <div class="updated">最終更新: __UPDATED__</div>
    <div class="filters">
      <div class="period" id="period">
        <button data-p="today">今日</button>
        <button data-p="weekend">今週末</button>
        <button data-p="month">今月</button>
        <button data-p="next">来月</button>
      </div>
      <div class="row2">
        <input type="search" id="q" placeholder="公演名・会場・出演者・曲目で検索">
        <select id="pref"><option value="">都道府県（すべて）</option></select>
        <select id="sort">
          <option value="date">日付が近い順</option>
          <option value="new">新着順</option>
        </select>
        <label class="chk"><input type="checkbox" id="freeonly">無料のみ</label>
      </div>
    </div>
  </div>
</header>
<main class="wrap">
  <p class="count" id="count"></p>
  <div id="list"></div>
  <div id="sentinel"></div>
  <div id="empty"></div>
</main>
<footer>
  出典: コンサートスクウェア（www.concertsquare.jp）
  <div class="note">掲載情報は各公演の公式情報をご確認ください。</div>
</footer>

<script>
const DATA = __DATA__;
const TOTAL = DATA.length;
const BATCH = 50;

// --- 前処理 ---
function parseDate(s){
  if(!s) return null;
  const m = s.match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/);
  return m ? new Date(+m[1], +m[2]-1, +m[3]) : null;
}
function addedTime(d){
  const m = (d.url||'').match(/\/blog\/\d{4}\/(\d{4})(\d{2})(\d{2})/);
  return m ? new Date(+m[1], +m[2]-1, +m[3]).getTime() : 0;
}
function isFree(d){
  const ps = d.prices||[];
  if(!ps.length) return false;
  return ps.some(p => /無料|入場無料|^0円|￥0/.test((p.price||'')+' '+(p.name||'')));
}
function minPrice(d){
  const nums = (d.prices||[]).map(p=>parseInt((p.price||'').replace(/[^0-9]/g,''))).filter(n=>n>0);
  return nums.length ? Math.min(...nums) : null;
}
DATA.forEach(d=>{ d._date=parseDate(d.date); d._added=addedTime(d); d._free=isFree(d); d._min=minPrice(d); });

// 都道府県セレクト
const prefs=[...new Set(DATA.map(d=>d.prefecture).filter(Boolean))].sort();
const prefSel=document.getElementById('pref');
prefs.forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;prefSel.appendChild(o);});

// --- 期間判定 ---
function todayMid(){const t=new Date();t.setHours(0,0,0,0);return t;}
function periodRange(p){
  const t=todayMid();
  if(p==='today'){const e=new Date(t);e.setDate(e.getDate()+1);return [t,e];}
  if(p==='weekend'){ // 直近の土日
    const day=t.getDay(); const toSat=(6-day+7)%7;
    const sat=new Date(t);sat.setDate(sat.getDate()+toSat);
    const mon=new Date(sat);mon.setDate(mon.getDate()+2);return [sat,mon];
  }
  if(p==='month'){const s=new Date(t.getFullYear(),t.getMonth(),1);const e=new Date(t.getFullYear(),t.getMonth()+1,1);return [s,e];}
  if(p==='next'){const s=new Date(t.getFullYear(),t.getMonth()+1,1);const e=new Date(t.getFullYear(),t.getMonth()+2,1);return [s,e];}
  return null;
}

// --- 状態 ---
let state={q:'',pref:'',sort:'date',free:false,period:''};
let filtered=[], shown=0;
const listEl=document.getElementById('list'), countEl=document.getElementById('count'), emptyEl=document.getElementById('empty');
const esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const perfList=d=>(d.performers||[]).map(p=>p.role?`${p.role}: ${p.name}`:p.name);

function apply(){
  const q=state.q.toLowerCase();
  const range=state.period?periodRange(state.period):null;
  filtered=DATA.filter(d=>{
    if(state.pref && d.prefecture!==state.pref) return false;
    if(state.free && !d._free) return false;
    if(range){ if(!d._date) return false; const t=d._date.getTime(); if(t<range[0].getTime()||t>=range[1].getTime()) return false; }
    if(q){
      const hay=[d.title, d.venue, perfList(d).join(' '), d.description||''].join(' ').toLowerCase();
      if(!hay.includes(q)) return false;
    }
    return true;
  });
  if(state.sort==='new') filtered.sort((a,b)=>b._added-a._added);
  else filtered.sort((a,b)=>{const av=a._date?a._date.getTime():Infinity,bv=b._date?b._date.getTime():Infinity;return av-bv;});

  countEl.innerHTML=`<b>${filtered.length}件</b> / 全${TOTAL}件`;
  listEl.innerHTML=''; shown=0; emptyEl.innerHTML='';
  if(!filtered.length){ emptyEl.innerHTML='<p class="empty">条件に合う公演が見つかりませんでした。</p>'; return; }
  renderMore();
}

const WD=['日','月','火','水','木','金','土'];

// 主要ホール（注目バッジ判定用）
const MAJOR_HALLS=['サントリーホール','東京芸術劇場','東京文化会館','NHKホール','オーチャードホール',
  'みなとみらいホール','フェスティバルホール','兵庫県立芸術文化センター','びわ湖ホール','愛知県芸術劇場',
  'Kitara','いずみホール','紀尾井ホール','すみだトリフォニーホール'];
const ORCHESTRA_RE=/管弦楽団|フィルハーモニ|交響楽団|orchestra/i;

function isNotable(d){
  if(d._free) return true;
  if(d.venue && MAJOR_HALLS.some(h=>d.venue.includes(h))) return true;
  if((d.performers||[]).some(p=>ORCHESTRA_RE.test(p.name||''))) return true;
  return false;
}
// プログラム本文から最初の1曲（曲名+作曲者らしき断片）を抽出してYouTube検索語にする
function firstProgramItem(d){
  let text = d.program_hint || d.description;
  if(!text) return null;
  text = text.replace(/^(曲目|プログラム|演奏曲)[:：\s]*/,'');
  let first = text.split(/[\/\n、,]/)[0].trim();
  if(first.length > 50) first = first.slice(0,50);
  return first || null;
}
function ytSearchUrl(q){ return 'https://www.youtube.com/results?search_query='+encodeURIComponent(q); }
function mapsUrl(venue){ return 'https://www.google.com/maps/search/'+encodeURIComponent(venue.replace(/^[^|]*\|/,'')); }

function cardHTML(d){
  let md='',w='',wc='';
  if(d._date){ md=(d._date.getMonth()+1)+'/'+d._date.getDate(); const wi=d._date.getDay(); w=d.day_week||WD[wi]; wc=wi===6?'sat':wi===0?'sun':''; }
  else { md='—'; }
  // 料金バッジ
  let badge='';
  if(d._free) badge='<span class="badge free">入場無料</span>';
  else if(d._min!=null) badge=`<span class="badge">¥${d._min.toLocaleString()}${(d.prices||[]).length>1?'〜':''}</span>`;
  // 注目バッジ
  const tags = isNotable(d) ? '<div class="tags"><span class="tag-notable">注目</span></div>' : '';
  // 出演者（主要3名＋展開）
  const ps=perfList(d); let perf='';
  if(ps.length){
    const head=ps.slice(0,3).map(esc).join(' / ');
    const rest=ps.slice(3);
    const restHTML=rest.length?`<span class="rest"> / ${rest.map(esc).join(' / ')}</span><button class="morebtn" type="button">+${rest.length}名</button>`:'';
    perf=`<div class="perf"><span class="lbl">出演</span>${head}${restHTML}</div>`;
  }
  // プログラム（曲目/説明がある場合のみ）
  let prog='';
  const progBody = d.program_hint || d.description;
  if(progBody){ prog=`<details class="prog"><summary>プログラム</summary><div class="body">${esc(d.description||progBody)}</div></details>`; }
  // 会場＋地図リンク
  const venue=d.venue?`<div class="venue">📍 ${esc(d.venue)}<a class="map-link" href="${mapsUrl(d.venue)}" target="_blank" rel="noopener">地図</a></div>`:'';
  // YouTubeプレビュー（曲目がある場合のみ）
  const song=firstProgramItem(d);
  const yt = song ? `<a class="yt-btn" href="${ytSearchUrl(song)}" target="_blank" rel="noopener"><span class="ico">▶</span>この曲を聴く</a>` : '';
  // チケット導線：公式URLがあれば目立つボタン、無ければGoogle検索の控えめリンク
  const ticket = d.public_url
    ? `<a class="ticket-btn" href="${esc(d.public_url)}" target="_blank" rel="noopener">チケット・詳細を見る →</a>`
    : `<a class="search-ticket-link" href="https://www.google.com/search?q=${encodeURIComponent(d.title+' チケット')}" target="_blank" rel="noopener">「${esc(d.title)} チケット」で検索</a>`;
  return `<article class="card">
    <div class="date-col"><div class="md">${md}</div><div class="w ${wc}">${esc(w)}</div></div>
    <div class="info-col">
      ${badge}
      ${tags}
      <h2><a href="${esc(d.url)}" target="_blank" rel="noopener">${esc(d.title)}</a></h2>
      ${venue}${perf}${prog}
      <div class="action-row">${yt}${ticket}</div>
    </div></article>`;
}

function renderMore(){
  const next=filtered.slice(shown, shown+BATCH);
  const frag=document.createElement('div');
  frag.innerHTML=next.map(cardHTML).join('');
  while(frag.firstChild) listEl.appendChild(frag.firstChild);
  shown+=next.length;
}

// 出演者展開（イベント委譲）
listEl.addEventListener('click',e=>{
  if(e.target.classList.contains('morebtn')) e.target.closest('.perf').classList.add('open');
});

// 無限スクロール
new IntersectionObserver(es=>{
  if(es[0].isIntersecting && shown<filtered.length) renderMore();
},{rootMargin:'400px'}).observe(document.getElementById('sentinel'));

// --- イベント ---
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value.trim();apply();});
prefSel.addEventListener('change',e=>{state.pref=e.target.value;apply();});
document.getElementById('sort').addEventListener('change',e=>{state.sort=e.target.value;apply();});
document.getElementById('freeonly').addEventListener('change',e=>{state.free=e.target.checked;apply();});
document.getElementById('period').addEventListener('click',e=>{
  const b=e.target.closest('button'); if(!b) return;
  const p=b.dataset.p;
  if(state.period===p){ state.period=''; b.classList.remove('on'); }
  else { state.period=p; [...document.querySelectorAll('.period button')].forEach(x=>x.classList.toggle('on',x===b)); }
  apply();
});

apply();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
