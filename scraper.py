# コンサートスクウェア スクレイパー（完全版）
# 検索結果を全ページ巡回し、各公演の詳細ページから
# 出演者・会場・価格・説明(曲目含む)・公式URL 等を取得する。
#
# 使い方:
#   python scraper.py            # 全ページ巡回（詳細も取得）
#   python scraper.py --max 2    # 先頭2ページのみ（動作確認用）
#   python scraper.py --no-detail  # 一覧のみ（詳細ページを叩かない＝高速）
import argparse
import json
import re
import time
import requests
from bs4 import BeautifulSoup

BASE = "https://www.concertsquare.jp"
SEARCH = "/concert/search"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en-US;q=0.9",
}
SLEEP = 1.0  # アクセス間隔（秒）: サーバへの礼儀

session = requests.Session()
session.headers.update(HEADERS)


def _text(el):
    return el.get_text(strip=True) if el else None


def get(url):
    r = session.get(url, timeout=20)
    r.raise_for_status()
    time.sleep(SLEEP)
    return r.text


# ---- 一覧ページのパース ----
def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("div.detail"):
        a = card.select_one("h3.title a")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else BASE + href
        rows.append({
            "title": a.get_text(strip=True),
            "url": url,
            "date": _text(card.select_one("span.concert-date")),
            "day_week": _text(card.select_one("span.day_week")),
            "start_time": _text(card.select_one("span.start-time")),
            "venue": _text(card.select_one("div.location-wrap p")),
        })
    return rows


# ---- 詳細ページのパース ----
def parse_detail(html):
    soup = BeautifulSoup(html, "html.parser")
    d = {}

    # 公式/非公式タグ
    tag = soup.select_one(".c-private-tag")
    d["official"] = not (tag and "非公式" in tag.get_text())

    # サブタイトル
    d["sub_title"] = _text(soup.select_one(".c-concert-detail-sub-title h2"))

    # 都道府県
    d["prefecture"] = _text(soup.select_one("span.concert-area-prov a"))

    # 会場ホールページ
    hall = soup.select_one("a.concert-area-link")
    if hall:
        d["hall_url"] = BASE + hall.get("href", "")

    # 公式サイトURL
    pub = soup.select_one("a.public-url")
    d["public_url"] = pub.get("href") if pub else None

    # 出演者: 「役割: 名前 / 役割: 名前 …」の span を分解
    perf_span = soup.select_one("img[src='/img/group.svg']")
    performers = []
    if perf_span and perf_span.find_next("span"):
        raw = perf_span.find_next("span").get_text(" ", strip=True)
        for part in raw.split("/"):
            part = part.strip()
            if ":" in part:
                role, name = part.split(":", 1)
                performers.append({"role": role.strip(), "name": name.strip()})
            elif part:
                performers.append({"role": None, "name": part})
    d["performers"] = performers

    # 入場料: 券種名 + 価格
    prices = []
    for item in soup.select("div.concert-sheet-list-item"):
        prices.append({
            "name": _text(item.select_one(".concert-sheet-name")),
            "price": _text(item.select_one(".concert-sheet-price")),
        })
    d["prices"] = prices

    # 説明本文（曲目/プログラムはここに含まれることがある）
    body = soup.select_one("div.txt-wrap p.txt")
    text = body.get_text("\n", strip=True) if body else None
    d["description"] = text
    # 本文から曲目らしき記述を簡易抽出
    d["program_hint"] = None
    if text:
        m = re.search(r"(曲目|プログラム|演奏曲)[:：\s]*([^\n]{0,200})", text)
        if m:
            d["program_hint"] = m.group(0)

    return d


def save(rows):
    with open("concerts.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def scrape(max_pages=None, with_detail=True):
    all_rows = []
    page = 1
    while True:
        url = f"{BASE}{SEARCH}?page={page}&sort=1&dayType=3"
        rows = parse_list(get(url))
        if not rows:
            break
        print(f"page {page}: {len(rows)}件", flush=True)
        all_rows.extend(rows)
        save(all_rows)  # 一覧を随時保存（途中停止しても残す）
        page += 1
        if max_pages and page > max_pages:
            break

    if with_detail:
        internal = [r for r in all_rows if r["url"].startswith(BASE + "/blog")]
        for i, r in enumerate(internal, 1):
            try:
                r.update(parse_detail(get(r["url"])))
            except Exception as e:
                r["detail_error"] = str(e)
            if i % 20 == 0:
                print(f"  詳細取得 {i}/{len(internal)}", flush=True)
                save(all_rows)  # 詳細も随時保存
    save(all_rows)
    return all_rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=None, help="巡回する最大ページ数")
    ap.add_argument("--no-detail", action="store_true", help="詳細ページを取得しない")
    args = ap.parse_args()

    data = scrape(max_pages=args.max, with_detail=not args.no_detail)
    with open("concerts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"合計 {len(data)}件 -> concerts.json")
