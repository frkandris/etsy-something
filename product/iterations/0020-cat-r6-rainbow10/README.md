# 0020 — macska 6. kör: 10 réteg (a BIZTONSÁGI KAPU MEGÁLLÍTOTTA)

A kritikus javaslata szerint a szivárvány-irány 8-ról 10 rétegre menne (a PaperCutMari
mélységéért). A generálás és a trace lefutott, de a **8. rétegen maradt 1 gyógyíthatatlan nyak**,
ezért a lánc az export-kapunál megállt, és NEM írt ki fájlokat.

Ez a rendszer helyes működése, nem hiba: inkább nincs fájl, mint törékeny fájl. A `--draft`
kapcsolóval kikényszeríthető lenne, de az hibás terméket szállítana.

Tanulság: **több réteg = több esély gyógyíthatatlan nyakra**, mert minden réteg a mögötte
lévőhöz van klippelve, és a klippelés maga gyárt nyakat. A 10 réteg ennél a motívumnál a
felső határ felett van; 8 réteggel ugyanez a kép hibátlanul átment (0019).
