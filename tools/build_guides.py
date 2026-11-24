# data.json から読みもの記事（guide/*.html）とサイトマップを作る。
# 使い方: python3 tools/build_guides.py
import json, html, re, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://t-t0823.github.io/sports-rental-joken/"
D = [d for d in json.load(open(os.path.join(ROOT, "data.json"))) if d.get("active")]
TODAY = max(d["checked"] for d in D)
e = html.escape

def num(v): return "?" if v is None else str(v)

def table(rows, note_col=False):
    if not rows:
        return "<p>今のところ該当する店は見つかっていません。</p>"
    out = ['<div class="tw"><table><thead><tr><th>店</th><th>主な車種</th><th>年齢</th><th>免許の年数</th><th>MT/AT</th><th>場所</th><th>料金の目安</th></tr></thead><tbody>']
    for d in rows:
        yrs = (num(d["years"]) + "年〜" if d["years"] is not None else {"none":"制限なし","unstated":"記載なし"}.get(d.get("yearsRule"),"?")) + ("<br><small>MTはMT免許から</small>" if d.get("mtFromMt") and "MT" in d["trans"] and d["years"] is not None else "")
        link = d.get("aff") or d["src"]
        rel = "sponsored noopener" if d.get("aff") else "noopener nofollow"
        pr = '<span class="pr">PR</span>' if d.get("aff") else ""
        out.append(f'<tr><td class="sh"><a href="{e(link)}" target="_blank" rel="{rel}">{e(d["shop"])}</a>{pr}<br><small>{e(d["plan"])}</small></td>'
                   f'<td data-l="主な車種"><span>{e(d["cars"])}</span></td><td data-l="年齢"><span>{agetxt(d)}</span></td><td data-l="免許の年数"><span>{yrs}</span></td><td data-l="MT/AT"><span>{e(d["trans"])}</span></td>'
                   f'<td data-l="場所"><span>{e(d["areaText"])}</span></td><td data-l="料金の目安"><span>{e(d.get("price") or "店のページで確認")}</span></td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)

def agetxt(d):
    if d["age"] is not None: return f'{d["age"]}歳〜'
    return {"none":"制限なし","unstated":"記載なし"}.get(d.get("ageRule"),"?")
def known(d): return d["age"] is not None or d["years"] is not None or d.get("ageRule") or d.get("yearsRule")
def has(d, pat): return re.search(pat, d["cars"] + d["plan"]) is not None
def sort(rows): return sorted(rows, key=lambda d: (d["age"] if d["age"] is not None else 99, d["years"] if d["years"] is not None else 99))

GUIDES = []
def guide(slug, title, desc, body):
    GUIDES.append((slug, title, desc, body))

# 1. 若い人向け
young = sort([d for d in D if known(d) and (d["age"] is None or d["age"] <= 21) and (d["years"] is None or d["years"] <= 1)])
guide("young-21", "21歳・免許1年でも借りられるスポーツカー・高級車レンタカー",
 "21歳以下・免許取得1年程度でも借りられるスポーツカーと高級車のレンタカーを、年齢と免許の年数の条件でまとめました。",
 f"""<p>スポーツカーや高級車のレンタカーは「25歳以上・免許3年以上」のような厳しい条件が多く、20代前半だと断られることがよくあります。それでも、条件のゆるい店は全国にいくつかあります。</p>
<p>このページでは、<b>21歳以下でも、免許を取って1年ほどでも借りられる可能性がある店</b>だけを集めました。「制限なし」は公式に制限がないと書かれている店、「記載なし」は公式に条件が書かれていない店です。記載なしの店は、予約の前に店へ確認してください。</p>
<h2>条件のゆるい店の一覧</h2>
{table(young)}
<h2>若い人が借りるときの注意</h2>
<ul>
<li>同じ店でも車種ごとに条件が違うことがあります。GT-Rやポルシェなど高価な車ほど条件が厳しくなりがちです。</li>
<li>年齢と年数を満たしていても、任意保険の加入やクレジットカード、デポジットを求められることがあります。</li>
<li>21歳未満や免許1年未満は「免責補償に入れない」店もあり、事故のときの自己負担が大きくなります。</li>
</ul>
<p>自分の年齢と免許の年数を入れて全店を判定するには、<a href="../">条件くらべのトップページ</a>を使ってください。</p>""")

# 2. MT の条件
mtrows = sort([d for d in D if "MT" in d["trans"] and known(d)])
guide("mt-license-years", "MT車のレンタカーの条件「MT免許になってから何年」とは？AT限定を解除した人の注意点",
 "MT車のレンタカーでよくある「MT免許取得後○年以上」の条件と、AT限定解除した人の数え方、条件がゆるい店をまとめました。",
 f"""<p>MT（マニュアル）車のスポーツカーを借りるとき、いちばん分かりにくいのが免許の年数の数え方です。店によって、<b>普通免許を取ってからの年数</b>で見るところと、<b>MTで運転できるようになってからの年数</b>で見るところがあります。</p>
<h2>AT限定を解除した人は年数が短くなる</h2>
<p>最初からMT免許で取った人は、免許を取った日からそのまま数えます。一方、AT限定で取ってあとから限定解除をした人は、<b>解除した日から数え直し</b>になる店があります。たとえば免許3年でも、解除が半年前なら「MT免許0.5年」と扱われます。</p>
<p>ただし実際には、年数が少し足りなくても店の判断で貸してくれることがあります。当サイトではこの場合を「MT年数だけ不足」として表示し、問い合わせてみる価値がある店として残しています。</p>
<h2>MT車を貸し出している店と条件</h2>
<p>「MTはMT免許から」とある店は、MT免許になってからの年数で判断する店です。</p>
{table(mtrows)}
<h2>確認しておきたいこと</h2>
<ul>
<li>予約の前に「AT限定を解除して○か月ですが借りられますか」と、日付を添えて聞くと確実です。</li>
<li>免許証の「AT限定」表記が消えているかどうか、更新前の免許証では裏面の記載も見られます。</li>
</ul>
<p><a href="../">トップページ</a>で「MT免許になってから（年）」を入れると、MTの年数だけ足りない店も一緒に判定できます。</p>""")

# 3. GT-R
gtr = sort([d for d in D if has(d, r"GT-R|R3[2345]|BNR")])
guide("gtr-rental", "GT-Rをレンタカーで借りるには？R35とR32〜R34の年齢・免許の条件と料金",
 "日産GT-R（R35）とスカイラインGT-R（R32・R33・R34）を借りられるレンタカー店の年齢・免許の条件と料金の目安をまとめました。",
 f"""<p>GT-Rは国産スポーツカーの中でも特に人気が高く、レンタカーで借りたいという人も多い車です。現行のR35と、90年代のスカイラインGT-R（R32・R33・R34）では、借りられる店も条件もかなり違います。</p>
<h2>R35とR32〜R34の違い</h2>
<ul>
<li><b>R35（2007年〜）</b>：2ペダルのATなので、AT限定免許でも運転できます。メーカー系や高級車専門店が扱い、料金は1日3万〜7万円ほどが目安です。</li>
<li><b>R32〜R34</b>：すべてMT車です。台数が少なく、主に国産旧車・JDMを専門にする店が扱います。MT免許の年数を条件にする店が多くあります。</li>
</ul>
<h2>GT-Rを貸し出している店</h2>
{table(gtr)}
<h2>借りる前に</h2>
<ul>
<li>免責額（事故のときの自己負担）が10万〜30万円と高めの店が多いので、補償の内容を必ず確認してください。</li>
<li>走行距離の上限や、サーキット走行の禁止など、車種ごとの決まりがあることがあります。</li>
</ul>""")

# 4,5. 地域
def region(slug, name, title_area, prefs_note, rows_filter):
    rows = sort([d for d in D if rows_filter(d)])
    guide(slug, f"{title_area}でスポーツカー・高級車を借りられるレンタカー店まとめ",
     f"{title_area}でスポーツカーや高級車を借りられるレンタカー店を、年齢・免許の年数の条件と料金の目安つきでまとめました。",
     f"""<p>{title_area}でスポーツカーや高級車を借りられる店を、貸出の条件と一緒にまとめました。{prefs_note}</p>
<h2>{name}の店の一覧</h2>
{table(rows)}
<h2>選び方のポイント</h2>
<ul>
<li>まずは年齢と免許の年数を満たしているかを見て、次に料金と場所で選ぶと迷いません。</li>
<li>大手のレンタカー会社は料金が安めで、専門店は車種が豊富です。</li>
<li>人気の車は週末に埋まりやすいので、早めに予約するのがおすすめです。</li>
</ul>
<p>都道府県での絞り込みは<a href="../">トップページ</a>の「エリア」からできます。</p>""")
region("kansai", "関西", "大阪・関西", "大阪府を中心に、京都・兵庫・奈良などの店も含みます。", lambda d: "関西" in d["areas"])
region("kanto", "関東", "東京・関東", "東京都を中心に、神奈川・千葉・埼玉・茨城などの店も含みます。", lambda d: "関東" in d["areas"])

# 6. AT限定
atrows = sort([d for d in D if d["trans"] in ("AT", "2ペダル", "MT/AT", "車種による") and known(d)])
guide("at-only", "AT限定免許で乗れるスポーツカー・スーパーカーのレンタカー",
 "AT限定免許でも運転できるスポーツカー・スーパーカー（GT-R R35、ポルシェ、フェラーリなど）を借りられるレンタカー店をまとめました。",
 f"""<p>「スポーツカーはMTじゃないと乗れない」と思われがちですが、今のスポーツカーやスーパーカーの多くは2ペダル（AT）です。<b>AT限定免許でも運転できる車</b>はたくさんあります。</p>
<h2>AT限定で運転できる主な車</h2>
<ul>
<li>日産 GT-R（R35）、フェアレディZ（AT車）</li>
<li>ポルシェ 911・718（PDK）、タイカン</li>
<li>フェラーリ、ランボルギーニ、マクラーレンなどのスーパーカー</li>
<li>マツダ ロードスター、トヨタ GR86 のAT車</li>
</ul>
<h2>AT車を貸し出している店</h2>
<p>「MT/AT」「車種による」の店は、AT車があるかを予約の前に確認してください。</p>
{table(atrows)}
<p><a href="../">トップページ</a>で「AT限定免許」にチェックを入れると、AT車で借りられる店だけを判定できます。</p>""")

STYLE = """body{margin:0;background:#0e1013;color:#e8ecef;font-family:"Hiragino Sans","Noto Sans JP",system-ui,sans-serif;line-height:1.8}
.wrap{max-width:900px;margin:0 auto;padding:24px 18px 48px}a{color:#f0b429}
h1{font-size:23px;line-height:1.5;margin:8px 0 14px}h2{font-size:18px;margin:30px 0 10px;border-left:4px solid #f0b429;padding-left:10px}
p,li{font-size:15px;color:#d3d9de}small{color:#9aa4ad}.meta{font-size:12.5px;color:#9aa4ad}
.tw{overflow-x:auto;border:1px solid #2a3036;border-radius:10px}table{border-collapse:collapse;width:100%;min-width:760px;font-size:13px}
th,td{padding:8px 10px;border-bottom:1px solid #2a3036;text-align:left;vertical-align:top}th{background:#171b20;color:#aab3bd;white-space:nowrap}
@media (max-width:640px){.tw{border:0;overflow:visible}table{min-width:0}thead{display:none}table,tbody,tr,td{display:block;width:100%}
tr{border:1px solid #2a3036;border-radius:10px;margin-bottom:10px;padding:8px 12px;background:#14171b}
td{border:0;padding:3px 0;display:grid;grid-template-columns:6.5em 1fr;gap:8px}td.sh{display:block;font-size:15px;padding-bottom:6px;border-bottom:1px solid #2a3036;margin-bottom:4px}
td::before{content:attr(data-l);color:#9aa4ad;font-size:12px}td.sh::before{content:none}}
.pr{font-size:10px;border:1px solid currentColor;border-radius:4px;padding:0 4px;margin-left:5px;color:#f0b429}
.cta{display:inline-block;margin-top:18px;padding:10px 16px;background:#f0b429;color:#111;border-radius:9px;font-weight:700;text-decoration:none}
.list a{display:block;padding:10px 0;border-bottom:1px solid #2a3036;text-decoration:none}nav{font-size:13px}
.prbox{margin:22px 0;padding:14px 16px;border:1px solid #3a3320;background:#1a1710;border-radius:12px;font-size:14px}.prbox a{font-weight:700;margin-left:4px}
footer{color:#9aa4ad;font-size:12px;border-top:1px solid #2a3036;padding:18px;text-align:center}footer a{color:inherit}"""

def page(path, title, desc, body, canonical):
    note = '<p class="meta">当サイトはアフィリエイト広告（「PR」と表示したリンク）を利用しています。</p>'
    return f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}｜スポーツカー・高級車レンタカー 貸出条件くらべ</title>
<meta name="description" content="{e(desc)}"><link rel="canonical" href="{canonical}">
<link rel="icon" href="../favicon.ico" sizes="any"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="../apple-touch-icon.png"><meta name="theme-color" content="#0f1114"><meta property="og:image" content="https://t-t0823.github.io/sports-rental-joken/og-image.png"><meta name="twitter:card" content="summary_large_image"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="article">
<style>{STYLE}</style></head><body><div class="wrap">
<nav><a href="../">トップ（条件くらべ）</a> ／ <a href="./">読みもの一覧</a></nav>
<h1>{e(title)}</h1><p class="meta">更新日 {TODAY}　／　掲載の条件は各店の公式ページなどで確認したものです。予約の前に必ず公式ページで確認してください。</p>{note}
{body}
<a class="cta" href="../">自分の年齢と免許の年数で判定する →</a>
<aside class="prbox"><span class="pr">PR</span> スポーツカー以外の普通のレンタカーも、まとめて安く探すなら
  <a href="https://af.moshimo.com/af/c/click?a_id=5919875&amp;p_id=5701&amp;pc_id=15749&amp;pl_id=74036" target="_blank" rel="sponsored noopener">たびらいレンタカーで料金を比較する →</a><img src="https://i.moshimo.com/af/i/impression?a_id=5919875&amp;p_id=5701&amp;pc_id=15749&amp;pl_id=74036" width="1" height="1" style="border:none" alt="" loading="lazy"></aside>
</div><footer><a href="../privacy.html">運営者情報・プライバシーポリシー・広告について</a></footer></body></html>"""

os.makedirs(os.path.join(ROOT, "guide"), exist_ok=True)
for slug, title, desc, body in GUIDES:
    open(os.path.join(ROOT, "guide", slug + ".html"), "w").write(page(slug, title, desc, body, BASE + "guide/" + slug + ".html"))
idx = '<ul class="list" style="list-style:none;padding:0">' + "".join(f'<li><a href="{s}.html"><b>{e(t)}</b><br><small>{e(ds)}</small></a></li>' for s, t, ds, _ in GUIDES) + "</ul>"
open(os.path.join(ROOT, "guide", "index.html"), "w").write(page("index", "読みもの一覧", "スポーツカー・高級車レンタカーの貸出条件についての記事一覧です。", "<p>スポーツカー・高級車のレンタカーを借りるときに役立つ記事です。</p>" + idx, BASE + "guide/"))
urls = [BASE, BASE + "guide/", BASE + "privacy.html"] + [BASE + "guide/" + s + ".html" for s, *_ in GUIDES]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
print(len(GUIDES), "guides;", {s: b.count("<tr>") - 1 for s, _, _, b in GUIDES})
