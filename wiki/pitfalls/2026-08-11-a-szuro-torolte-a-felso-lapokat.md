---
type: Pitfall
title: A szilánkszűrő törölte a felső lapokat, majd a nyílásokat is
description: Két, egymást takaró hiba ugyanabban a szűrőben. Az elsőtől eltűnt a felső egy-két lap, a másodiktól a termék teljes formanyelve. Mindkettő kifogástalanul működő kód volt, rossz alanyra alkalmazva.
status: stable
generated:
  by: claude-fable-5
  at: 2026-08-11T04:00:00Z
---

# A szilánkszűrő törölte a felső lapokat, majd a nyílásokat is

## Tünet

A kész render egészen máshogy nézett ki, mint a generált illusztráció: lapos, sötét, az arc
felismerhetetlen. A felhasználó tette fel a helyes kérdést: „semmi nem indokolja, hogy ebből ez
legyen." A `report.json` közben zöld volt — minden réteg OK, nyak nélkül.

## Gyökérok — két hiba egymás mögött

**Első: a felső lapok.** A szilánkszűrő minden darabot elutasít, aminek a *karcsúsága*
(befoglaló méret ÷ saját legnagyobb beírt köre) meghalad egy küszöböt. Egy **felső lap definíció
szerint egy panel nagy nyílással**, tehát vékony gyűrű, tehát magas karcsúsági pontszám — a szűrő
pontosan ezt törölte. Innen jött, hogy hat kért lapból négy készült, a legfelső kettő csendben
eltűnt, és a mű laposnak látszott.

A helyes megkülönböztetés **nem a vékonyság**: egy vékony gyűrű, ami a keret része, nem tud kiesni;
egy középen lebegő vékony szalag igen.

**Második: a nyílások.** A javítás után a keretig érő darab kivételt kapott — de a `continue` a
*lyukak* ellenőrzését is átugrotta. Ezt a codex jelezte, és igaza volt. A kivétel javítása után
viszont kiderült, hogy **maga a lyukszűrés a rossz**: a karcsúsági teszt lyukakra futva ennek a
terméknek a teljes formanyelvét törölte, mert minden szalag alakú nyílás szilánknak minősül.

**Egy lyuk nem tud kiesni.** A karcsúság szerkezeti teszt darabokra. Nyílásokra csak területi alsó
határ van értelme; hogy egy nyílás hosszú és vékony-e, az tervezői kérdés, nem vágói.

## Hogyan derült ki

Nem tippeléssel — a tippjeim rendre megdőltek. A menet:

1. Feltevés: a pofa beleolvad a mezőbe, mert azonos a tónusuk. **Megmérve: hamis** — a mező tónusa
   100%-ban a témán kívül volt.
2. Feltevés: a tónus nem monoton a mélységgel. **Megmérve: majdnem hamis** — 33 értelmes régióból
   1 sértette meg.
3. Izolálás: a mélységtérkép hibátlan (az arc, a szem, az orr átmegy rajta), tehát a `02_trace` a
   hibás. Ez szűkítette le a keresést.
4. A `posterise` és a `mask_at` kimenetének kimérése: a maszkok területe 93 / 80 / 71 / 65 / 54 /
   50% — **hibátlan**. Tehát a hiba a maszkok után van.
5. Innen a szűrő már egy lépés volt.

## Alkalmazott korrekció

- a keretig érő darab mentesül a **karcsúsági** teszt alól, de a lyukvizsgálat alól nem;
- a nyílásokra nincs karcsúsági teszt, csak területi alsó határ;
- ha egy réteg *minden* darabja megbukik, a lánc leáll ahelyett, hogy a naplóban szűrést állítana
  és közben érintetlenül hagyná a réteget.

## Tanulság

**Egy szűrő, ami „mindenre" fut, mindig fut valamire, amire nem volt kitalálva.** Mielőtt egy
geometriai kritérium az összes elemre rákerül, meg kell nevezni, *milyen fizikai kudarcot* előz meg,
és megnézni, hogy az az alany egyáltalán képes-e arra a kudarcra. A karcsúság a „kiesik a lapból"
kudarcot előzi meg; a keret nem tud kiesni, egy lyuk pedig végképp nem.

Ellenőrizhető jövőbeli munkán: minden elutasító szabálynál írd le egy mondatban a kudarcot, amit
megakadályoz, és sorold fel, mely elemtípusokra értelmes.

## Provenancia

`product/pipeline/02_trace.py`. Kapcsolódik: [[workflows/recessed-papercut-pipeline]],
[[decisions/2026-08-11-keret-eloszor]].
