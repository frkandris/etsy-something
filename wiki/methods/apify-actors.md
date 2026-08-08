---
type: Method
title: Használt Apify actorok és költségük
description: Melyik actor mit ad, mennyibe került, és mire ne használd.
status: stable
generated:
  by: claude-opus-5
  at: 2026-08-07T20:00:00Z
---

# Apify actorok

A token a felhasználóé (STARTER csomag). **Összes költés ebben a kutatásban: ~22 USD**, ~15 futtatás.

| actor | mit ad | megjegyzés |
|---|---|---|
| `webdatalabs/etsy-scraper-pro` | keresési találat: `price`, `originalPrice`, `onSale`, `shopName`, `rating`, `reviewCount` | **az egyetlen, ami akciós + listaárat is ad**; `query` vagy `searchUrl`, `maxItems` |
| `getdataforme/etsy-shop-details-scraper` | bolt: `sold_count`, `create_date`, `active_listing_count`, `country_code`, `is_open`, ratingek | `ShopNames` tömb; futtatásonként ~100 bolt |
| `hello.datawizards/etsy-shop-scraper` | boltonként N listing címe és **listaára** | `shop_name` tömb + `itemLimit`; katalógus-mintavételhez |
| `axlymxp/etsy-shop-scraper` | csak bolt-szintű mezők | **listing árat nem ad** a `max_shop_listings` ellenére — erre ne használd |

## Költségbecslés újrafuttatáshoz

- Egy 100-találatos keresés: ~1,2 USD.
- 73–173 bolt bolt-adata: ~1–2 USD/futtatás.
- 65–73 bolt katalógus-mintavétele (24 listing/bolt): ~2 USD.

Egy teljes új niche felmérése (5 keresés + bolt-adat + katalógus) tehát nagyságrendileg **8–12 USD**.

## Amit megpróbáltunk és nem működött

**Google Sheets API `gcloud` ADC-vel:** a Google szervezeti policy letiltotta a gcloud klienst a
`spreadsheets` scope-ra („This app is blocked"). **rclone tokennel:** az rclone saját OAuth
projektjében a Sheets API nincs engedélyezve, és nem is engedélyezhető. Emiatt lett minden sheet-írás
Apps Script — lásd [[decisions/2026-08-06-apps-script-for-sheets]].
