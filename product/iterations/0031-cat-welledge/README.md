# 0031 — süllyesztett szerkezet (a felhasználó olvasata a referenciáról)

A felhasználó a referenciákat nézve azt mondta: a legfelső réteg egy fehér lap, amiben lyukak
vannak — néhány kis kör, amin át véletlenszerű mélyebb rétegek látszanak, és egy nagyobb nyílás,
ami alatt a rétegek egyre távolabb és egyre sötétebbek. Ez **süllyesztett (intaglio)** szerkezet.

Az egész addigi pipeline **kiemelkedő reliefet** épített: kisebb rétegek egymás tetején.
A referencia ennek a fordítottja. A zoom a `ref-abstract-dog`-on egyértelműen mutatja: a kis
köröknek belső faluk és színes fenekük van, tehát átfúrt lyukak; és minden forma határán a felső
él sötétebb, vagyis a felület LEFELÉ lép.

## Amit ez a körben megváltozott

- **Generátor (`--recessed`)**: a mező a LEGVILÁGOSABB szint, mert az maga a felső lap; nincs
  kivágandó fekete háttér; a mélyedések sötétednek; szórt kis kerek nyílások a mezőben.
- **Paletta (`well`)**: sötétről világosra fut, nem fordítva — az 1. réteg a legmélyebb lap,
  az utolsó a fehér fedőlap.
- **Nem kellett z-fordítás a renderben**: a meglévő nesting-gépezet a megfordított
  mélységtérképpel magától a helyes sorrendet adja.

## Menet közben javított hiba

A `--white-top` és a `--recessed` kapcsoló **némán hatástalan volt**: a flageket az argv szűrése
UTÁN olvastam ki, a szűrő viszont már kivette őket, így mindig `False` lett. Minden flag most a
szűrés elé került. Ez magyarázza, miért nem változott a kép több körön át.

Riport: 6 réteg, 0 nyak, leggyengébb 4,57 mm.

## Ami még eltér a referenciától

A fedőlap itt **kör alakú**, a referenciában viszont a teljes négyzetet kitölti éltől élig.
A prompt már ezt kéri, de a modell még mindig korongot rajzol — ez a következő kör feladata.
