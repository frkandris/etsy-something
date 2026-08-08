#!/usr/bin/env python3
"""What actually sells (reviews) vs what is listed (catalogue) vs what is searched.

Reviews are the only listing-level, dated sales signal we have. A review is a
lower bound on a sale, and the ratio between motifs is what matters, not the
absolute count.
"""
import json, collections, pathlib, datetime as dt, statistics as st

D = pathlib.Path(__file__).resolve().parent.parent / "data"
rev = json.load(open(D / "reviews.json"))
cat = json.load(open(D / "catalog_sample.json"))
verified = {r["shop"] for r in json.load(open(D / "layered_adjusted.json")) if r["share"] >= 0.8}

MOTIF = {
    "mandala / zentangle": ("mandala", "zentangle", "rosette"),
    "állat": ("dog", "cat", "wolf", "lion", "tiger", "horse", "deer", "bird", "owl",
              "elephant", "dragon", "fish", "butterfly", "bear", "fox", "animal",
              "panda", "giraffe", "turtle", "hummingbird", "eagle"),
    "vallási": ("cross", "jesus", "christ", "virgin mary", "buddha", "religio",
                "islam", "allah", "ayat", "church", "angel", "prayer", "faith",
                "bible", "saint", "guadalupe", "patriotic cross"),
    "természet / fa": ("tree", "forest", "mountain", "nature", "leaf", "landscape",
                       "sunset", "ocean", "wave", "sea", "beach"),
    "virágos": ("flower", "floral", "rose", "lotus", "sunflower", "botanical", "daisy"),
    "ünnep / szezon": ("christmas", "halloween", "easter", "valentine", "pumpkin",
                       "santa", "snowflake", "thanksgiving", "winter", "holiday"),
    "norse / kelta": ("viking", "norse", "odin", "thor", "celtic", "valhalla",
                      "yggdrasil", "rune", "pagan", "dragon"),
    "ember / portré": ("woman", "man", "face", "portrait", "girl", "couple",
                       "family", "silhouette of"),
    "hazafias": ("american flag", "patriotic", "usa", "veteran", "eagle flag"),
    "jármű / gép": ("car", "truck", "motorcycle", "bike", "plane", "ship", "train",
                    "boat", "tractor"),
}
TYPE = {
    "shadow box / papercut": ("shadow box", "shadowbox", "papercut", "paper cut",
                              "light box", "cardstock"),
    "fali panel": ("wall art", "wall decor", "wall panel", "wall hanging"),
    "egyéb tárgy": ("clock", "vase", "box", "sign", "ornament", "coaster", "lamp"),
}


def label(title, table, default="egyéb"):
    t = title.lower()
    for k, ws in table.items():
        if any(w in t for w in ws):
            return k
    return default


# ---- supply: what the shops actually list (24-listing sample per shop) -----
supply = collections.Counter()
for r in cat:
    if r["shop_name"] in verified:
        supply[label(r["title"], MOTIF)] += 1
S = sum(supply.values())

# ---- demand-side proof: what gets reviewed --------------------------------
sold = collections.Counter()
sold_type = collections.Counter()
recent = collections.Counter()
CUT = dt.datetime(2026, 2, 8)          # last 6 months
by_listing = collections.Counter()
for r in rev:
    t = r.get("listing_title") or ""
    if not t:
        continue
    m = label(t, MOTIF)
    sold[m] += 1
    sold_type[label(t, TYPE)] += 1
    by_listing[t] += 1
    try:
        if dt.datetime.strptime(r["date"][:10], "%Y-%m-%d") >= CUT:
            recent[m] += 1
    except Exception:
        pass
R, RC = sum(sold.values()), sum(recent.values())

print(f"{len(rev)} review / {len(by_listing)} kulonbozo listing / {len(verified)} bolt")
print()
print("MOTIVUM: KINALAT vs TENYLEGES ELADAS")
print(f"{'motivum':24}{'listing %':>11}{'review %':>10}{'utolso 6 ho':>13}{'index':>8}")
for m in sorted(sold, key=lambda k: -sold[k]):
    sp = 100 * supply.get(m, 0) / S
    rp = 100 * sold[m] / R
    rc = 100 * recent.get(m, 0) / RC if RC else 0
    idx = rp / sp if sp else float("inf")
    flag = "  <-- alulkinalt" if idx > 1.4 else ("  <-- tulkinalt" if idx < 0.7 else "")
    print(f"{m:24}{sp:>10.1f}%{rp:>9.1f}%{rc:>12.1f}%{idx:>8.2f}{flag}")

print()
print("TERMEKTIPUS a review-kban")
T = sum(sold_type.values())
for k, v in sold_type.most_common():
    print(f"   {k:24}{100*v/T:>7.1f}%  ({v})")

print()
print("A LEGTOBBET ERTEKELT LISTINGEK (a friss eladas legjobb kozelitese)")
for t, n in by_listing.most_common(15):
    print(f"   {n:>3}x  {t[:88]}")

print()
print("NORSE / KELTA JELENLET")
nk = [t for t in by_listing if label(t, MOTIF) == "norse / kelta"]
print(f"   {len(nk)} listing, {sum(by_listing[t] for t in nk)} review "
      f"({100*sum(by_listing[t] for t in nk)/R:.1f}%)")
for t in sorted(nk, key=lambda x: -by_listing[x])[:8]:
    print(f"     {by_listing[t]:>3}x  {t[:84]}")
