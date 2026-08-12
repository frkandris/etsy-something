---
type: Method
title: Böngészős adatvégpontok — Apify nélküli mérés
description: Négy végpont, ami a bejelentkezett böngésző-munkamenetből tömegesen lekérhető: Etsy Marketplace Insights, Etsy autocomplete, Etsy bolt-oldal és a SalesDoe API. Ezek eddig nem voltak dokumentálva, és emiatt egy kör kézzel ment.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-12T16:30:00Z
---

# Böngészős adatvégpontok

**Miért van ez az oldal:** a wiki eddig a *forrásokat* nevezte meg ([[methods/measurement-chain]],
`CLAUDE.md`), de azt nem, hogy **hogyan lehet őket tömegesen lekérdezni**. Emiatt a 2026-08-12-i
3D-körben előbb kézzel kattintgattam, és a felhasználónak kellett szólnia, hogy a SalesDoe létezik.
Ez az oldal ezt pótolja.

Mind a négy végpont **a bejelentkezett böngésző-munkamenetből, azonos eredetről (`fetch` +
`credentials:'include'`)** hívható, tehát Apify-keret nélkül is megy.

## 1. Etsy Marketplace Insights — kereslet, első kézből

```
GET /your/shops/me/marketplace-insights/search?query=<kifejezés>
```

A lap **szerver oldalon renderelt**, és a számok beágyazva érkeznek. A keresendő minta:

```json
"stats":{"searchTerm":"vase stl","searchVolume":318,"avgTotalListings":7619,
         "cvr":1,"queryCvr":0.000662...}
```

| mező | jelentés |
|---|---|
| `searchVolume` | keresés az elmúlt 30 napban |
| `avgTotalListings` | versengő listingek száma |
| `cvr` | konverzió-besorolás, egész. Látott tartomány 0–4; a felületen a `cvr=1` felirata „Low". A többi egész szó szerinti címkéje **nincs igazolva**. |
| `queryCvr` | tényleges konverzió (eladás / keresés) |

Ugyanebben a lapban van még:

- `"quotaData":{"totalQuota":15,"remainingQuota":15}` — **a lekérdezéseket nem csökkenti** (60+
  lekérdezés után is 15 maradt); valószínűleg a mentett keresésekre vonatkozik.
- `"listingCards":[...]` — a top listingek **boltnévvel**: `title`, `rating`, `numberOfReviews`,
  `shopName`, `badgeText`, `isStarSeller`, `price.formattedPrice`, `formattedOriginalPrice`,
  `formattedDiscountText`. **Ez adja a bolt-populációt** kereséssel, Apify nélkül.
- `"similarSearchTerms"` — 2026-08-12-én üresen jött vissza minden lekérdezésnél.

## 2. Etsy autocomplete — hosszú farok generátor

```
GET /suggestions_ajax.php?search_query=<mag>
```

JSON-t ad: `{"results":[{"query":"stl files"}, ...]}`. Magonként ~10 javaslat; a `<span class=…>`
kezdetű sorok bolt-név javaslatok, azokat el kell dobni. 36 magból **204 egyedi kifejezés** jött.

**Figyelem:** egy javaslat azt jelenti, hogy az Etsy látta a lekérdezést — **nem azt, hogy van
volumene**. Minden javaslatot le kell mérni az 1. pontban, mielőtt következtetnénk belőle.

## 3. Etsy bolt-oldal — eladás, kor, katalógus

```
GET /shop/<boltnév>
```

A renderelt szövegből: `<szám> Sales`, `<szám> months|years on Etsy`, `<szám> items`, értékelés
`4.9 (89)`, `Star Seller`. **Fontos:** külső eredetről (`credentials:'omit'`) hívva a DataDome
bot-védelem fogja meg; azonos eredetről, bejelentkezve átmegy.

## 4. SalesDoe API — bevétel, ország, deviza, tagek

**Ez a legfontosabb, amit eddig nem tudtunk.** A SalesDoe felülete boltonként egy kattintás volt —
és a [[faq]] pont ezért utasította el a niche-kutatásra. **Van mögötte API, tehát a kattintás-érv
elavult:**

```
GET /api/shops/shop?shop_name=<név>     → shopData
GET /api/shops/shop/<shopId>            → results (listingek), tags, price, weightedPrice, count
```

`shopData` mezői: `shopId`, `created` (unix), `favorites`, `review_count`, `review_average`,
`transaction_sold_count`, `shop_location_country_iso`, **`sales_per_month`**, `currency_code`.

A listing-végpont `results` tömbje listingenként adja a `price`-t, a `tags`-et, a `views`-t és a
**`listing_type`**-ot (`download` vs fizikai) — ez utóbbi adja a **katalógus digitális arányát**,
ami a bevételi képlet harmadik bemenete.

**Ami NEM avult el:** a [[pitfalls/2026-08-06-salesdoe-list-vs-sale-price]]. A `price` továbbra is
a lista- és az akciós ár között ingadozik, tehát a belőle számolt bevétel **felső becslés**, és a
mélyen diszkontálóknál torzít a legjobban. Ahol tartós akció van, ott az akciós árat külön kell
megszerezni — pl. az 1. pont `listingCards`-jából (`formattedOriginalPrice` +
`formattedDiscountText`).

## Devizák, amikre nincs rögzített árfolyamunk

A [[decisions/2026-08-06-exchange-rates]] kilenc devizát rögzít (USD, EUR, GBP, CAD, AUD, SGD, SEK,
HKD, MYR). A 3D-körben ezeken kívül **MAD, CHF és TRY** is előjött. **Ezekre nem számoltam
HUF-ot** — árfolyamot kitalálni ugyanaz a hibaosztály lenne, mint a populáció nélküli szám. Amíg a
felhasználó nem rögzít rájuk kurzust, ezek a boltok darabszámmal szerepelnek, HUF nélkül.

## Provenancia

A 2026-08-12-i 3D-kör mérései: [[findings/3d-print-market-structure]],
[[findings/3d-print-first-look]]. Kapcsolódik: [[methods/measurement-chain]],
[[methods/data-collection-pipeline]], [[methods/apify-actors]].
