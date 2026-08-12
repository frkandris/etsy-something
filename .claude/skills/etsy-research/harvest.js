/* Etsy-kutatás böngészős gyűjtői.  window.ER-t telepíti.
 *
 * Futtatás: egy BEJELENTKEZETT etsy.com fülön (a SalesDoe-hoz egy salesdoe.com fülön).
 * Minden hívás azonos eredetről megy, credentials:'include' — kívülről a DataDome fogja meg.
 *
 * A CDP-hívás 45 s után elszáll, ezért minden ciklus 8-as adagokra van szabva, és az
 * eredmény a window-on gyűlik. Egy adag lefutása után hívd újra a következő nyolccal.
 *
 *   ER.demand(["stl files", ...])   → ER.mi     kereslet: volumen, listingszám, konverzió
 *   ER.longtail(["stl", ...])       → ER.sugg   hosszú farok javaslatok (Set)
 *   ER.cards(["stl files", ...])    → ER.cards  top listingek boltnévvel, akciós árral
 *   ER.shops(["NenoWorks", ...])    → ER.shop   Etsy bolt-oldal: eladás, kor, katalógus
 *   ER.salesdoe(["NenoWorks", ...]) → ER.sd     SalesDoe: bevétel, deviza, tagek, letöltés%
 *   ER.dump()                       → kompakt JSON minden gyűjtöttből
 */
(() => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const med = a => { a = a.filter(x => x != null).sort((x, y) => x - y);
                     return a.length ? a[Math.floor(a.length / 2)] : null; };

  // egy JSON-tömb kivágása a nyers HTML-ből, zárójel-párosítással
  const sliceArr = (html, key) => {
    const k = html.indexOf('"' + key + '":['); if (k < 0) return null;
    let i = html.indexOf('[', k), d = 0;
    for (let j = i; j < html.length; j++) {
      if (html[j] === '[') d++;
      else if (html[j] === ']') { d--; if (!d) return html.slice(i, j + 1); }
    }
    return null;
  };

  const ER = window.ER = window.ER || { mi: {}, sugg: new Set(), cards: [], shop: {}, sd: {} };

  /* 1. KERESLET — Marketplace Insights. A számok a szerver-renderelt lapba vannak ágyazva. */
  ER.demand = async terms => {
    for (const t of terms) {
      if (ER.mi[t]) continue;
      try {
        const html = await fetch('/your/shops/me/marketplace-insights/search?query=' +
          encodeURIComponent(t), { credentials: 'include' }).then(r => r.text());
        const m = html.match(/"stats":\{"searchTerm":"[^"]*","searchTermHash":"[^"]*","searchVolume":(\d+),"avgTotalListings":(\d+),"cvr":(\d+),"queryCvr":([\d.eE-]+)/);
        if (m) {
          const vol = +m[1], lst = +m[2];
          ER.mi[t] = { vol, listings: lst, cvr: +m[3], queryCvr: +m[4],
                       per1000: lst ? +(vol * 1000 / lst).toFixed(1) : null,
                       cvrPermille: +(+m[4] * 1000).toFixed(2) };
        } else ER.mi[t] = { err: /"isQuotaReached":true/.test(html) ? 'QUOTA' : 'noparse' };
      } catch (e) { ER.mi[t] = { err: String(e).slice(0, 40) }; }
      await wait(700);
    }
    return Object.keys(ER.mi).length;
  };

  /* 2. HOSSZÚ FAROK — az Etsy saját kiegészítője. Javaslat != volumen: mérd le ER.demand-del! */
  ER.longtail = async seeds => {
    for (const s of seeds) {
      try {
        const j = await fetch('/suggestions_ajax.php?search_query=' + encodeURIComponent(s),
          { credentials: 'include' }).then(r => r.json());
        (j.results || []).forEach(r => r.query && !r.query.includes('<span') && ER.sugg.add(r.query));
      } catch (e) {}
      await wait(260);
    }
    return ER.sugg.size;
  };

  /* 3. KÍNÁLAT + BOLTOK — a Marketplace Insights lapjába ágyazott top listingek. */
  ER.cards = async terms => {
    for (const t of terms) {
      try {
        const html = await fetch('/your/shops/me/marketplace-insights/search?query=' +
          encodeURIComponent(t), { credentials: 'include' }).then(r => r.text());
        const arr = sliceArr(html, 'listingCards');
        if (!arr) continue;
        for (const c of JSON.parse(arr)) ER.cards.push({
          term: t, title: (c.title || '').slice(0, 85), shop: c.shopName,
          revs: +c.numberOfReviews || 0, rating: c.rating ? +c.rating : null,
          badge: c.badgeText || null, star: !!c.isStarSeller,
          price: c.price?.formattedPrice || null,
          orig: c.price?.formattedOriginalPrice || null,   // <- az akciós ár forrása
          disc: c.price?.formattedDiscountText || null });
      } catch (e) {}
      await wait(650);
    }
    return ER.cards.length;
  };

  /* specialista = legalább 3 KÜLÖN listinggel rangsorol. Aki egyszer szerepel, az zaj. */
  ER.specialists = (min = 3) => {
    const by = {};
    for (const c of ER.cards) {
      const s = by[c.shop] = by[c.shop] || { titles: new Set(), revs: 0, terms: new Set() };
      if (!s.titles.has(c.title)) { s.titles.add(c.title); s.revs += c.revs; }
      s.terms.add(c.term);
    }
    return Object.entries(by).filter(([, v]) => v.titles.size >= min)
      .map(([k, v]) => ({ shop: k, listings: v.titles.size, revs: v.revs, terms: v.terms.size }))
      .sort((a, b) => b.listings - a.listings);
  };

  /* 4. BOLT-OLDAL — eladás, kor, katalógusméret. Azonos eredetről kell hívni. */
  ER.shops = async names => {
    for (const n of names) {
      if (ER.shop[n]) continue;
      try {
        const html = await fetch('/shop/' + n, { credentials: 'include' }).then(r => r.text());
        const txt = new DOMParser().parseFromString(html, 'text/html').body.innerText.replace(/\s+/g, ' ');
        const sales = (txt.match(/([\d,]+)\s+Sales/) || [])[1];
        const age = txt.match(/(\d+)\s+(month|year)s?\s+on Etsy/i);
        const items = (txt.match(/(\d[\d,]*)\s+items?\b/i) || [])[1];
        const rate = txt.match(/\b([45]\.\d)\s*\((\d[\d,]*)\)/);
        ER.shop[n] = { sales: sales ? +sales.replace(/,/g, '') : null,
          months: age ? (age[2].toLowerCase() === 'year' ? +age[1] * 12 : +age[1]) : null,
          items: items ? +items.replace(/,/g, '') : null,
          rating: rate ? +rate[1] : null, reviews: rate ? +rate[2].replace(/,/g, '') : null,
          star: /Star Seller/i.test(txt) };
      } catch (e) { ER.shop[n] = { err: 1 }; }
      await wait(800);
    }
    return Object.keys(ER.shop).length;
  };

  /* 5. SALESDOE — bevétel, deviza, tagek, letöltés-arány.  SALESDOE.COM fülön futtasd!
   * FIGYELEM: a price a lista- és az akciós ár között ingadozik -> minden ebből számolt
   * bevétel FELSŐ BECSLÉS. Tartós akciónál az akciós árat az ER.cards orig/disc mezőjéből vedd. */
  ER.salesdoe = async names => {
    for (const n of names) {
      if (ER.sd[n]) continue;
      try {
        const s = await fetch('/api/shops/shop?shop_name=' + encodeURIComponent(n),
          { credentials: 'include' }).then(r => r.json());
        const d = s.shopData; if (!d) { ER.sd[n] = { err: 'noshop' }; continue; }
        await wait(500);
        const L = await fetch('/api/shops/shop/' + d.shopId, { credentials: 'include' }).then(r => r.json());
        const rows = L.results || [];
        const prices = rows.map(x => x.price?.amount ? x.price.amount / (x.price.divisor || 100) : null);
        const tag = {}; rows.forEach(x => (x.tags || []).forEach(t => tag[t] = (tag[t] || 0) + 1));
        ER.sd[n] = { country: d.shop_location_country_iso, cur: d.currency_code,
          opened: new Date(d.created * 1000).toISOString().slice(0, 7),
          sold: d.transaction_sold_count, spm: d.sales_per_month,
          favs: d.favorites, revs: d.review_count, rate: d.review_average,
          listings: L.count, sampled: rows.length,
          downloads: rows.filter(x => x.listing_type === 'download').length,
          priceMed: med(prices), aggPrice: L.price,
          topTags: Object.entries(tag).sort((a, b) => b[1] - a[1]).slice(0, 8).map(x => x[0]) };
      } catch (e) { ER.sd[n] = { err: String(e).slice(0, 40) }; }
      await wait(900);
    }
    return Object.keys(ER.sd).length;
  };

  /* Árfolyam: CSAK a decisions/2026-08-06-exchange-rates rögzített devizái.
   * Ami nincs itt, arra NEM számolunk HUF-ot — kitalálni tilos. */
  ER.FX = { USD: 316.33, EUR: 364.60, GBP: 426.0, CAD: 226.0, AUD: 222.8,
            SGD: 246.7, SEK: 33.42, HKD: 40.32, MYR: 77.35 };
  ER.huf = (spm, price, cur) => (ER.FX[cur] && price) ? Math.round(spm * price * ER.FX[cur]) : null;

  ER.dump = () => JSON.stringify({
    demand: ER.mi,
    longtail: [...ER.sugg],
    specialists: ER.specialists(),
    shops: ER.shop,
    salesdoe: Object.fromEntries(Object.entries(ER.sd).map(([k, v]) => [k, v.err ? v :
      { ...v, hufPerMonth: ER.huf(v.spm, v.priceMed, v.cur), fxKnown: !!ER.FX[v.cur] }]))
  });

  return 'ER telepítve: demand, longtail, cards, specialists, shops, salesdoe, huf, dump';
})();
