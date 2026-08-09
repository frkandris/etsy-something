# 0032 — süllyesztett szerkezet, teljes négyzetes lapokkal

A 0031 folytatása. Ott a fedőlap kör alakú maradt, mert a képmodell korongot rajzolt a kért
éltől élig tartó lap helyett. Itt a `--full-panel` kapcsoló kényszeríti ki: ami a design
sziluettjén kívül esik, az minden laphoz hozzáadódik, tehát minden lap teljes négyzet, csak
nyílásokkal — pontosan úgy, ahogy a referencia-termékek épülnek.

## Amit a sorrend tanított

Az unió először **0,79 mm-es szilánkokat** gyártott a korong pereme és a négyzet sarka között,
majd egy záró bufferrel 1,39 mm-t — mindkettő a 2 mm-es cél alatt, a kapu jogosan állította meg.
A megoldás nem nagyobb buffer volt, hanem a **sorrend**: a panel-uniót a nyak-gyógyító lánc
ELÉ kellett tenni, hogy a meglévő gépezet takarítsa el. Utána 6,03 mm a leggyengébb darab.

Ez ugyanaz a mintázat, mint a korábbi „a lánc gyógyítással záruljon" tanulság: nem új javítás
kell, hanem a meglévőt a helyes ponton futtatni.

Riport: 6 kért szintből 5 valódi réteg (1 összevonva), 0 nyak, leggyengébb 6,03 mm.
