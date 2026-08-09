# 0021 — macska 7. kör: szem külön szinten (A KAPU MEGÁLLÍTOTTA)

A kritikus P0-ja szerint kell meleg akcentus (zöld szem, rózsaszín orr), ezért a promptba
bekerült, hogy a szem és az orr külön, legvilágosabb szintű régió legyen.

Az eredmény **gyönyörű illusztráció, de rajz és nem mélységtérkép**: a bajszok hajszálvonalak
(300 mm-en ~0,6 mm), a díszpontok tűhegyek. A trace 0,03 mm-es szilánkokat mért, és az
export-kapu megállította.

**Tanulság:** minél részletesebb az illusztráció, annál kevésbé vágható. Ez GENERÁLÁSI és nem
trace-hiba. A 0022-ben ezért a prompt kemény minimum-vastagságot ír elő (semmi vonal, csak
tömör folt; a bajusz kúpos tömör ék; minimum 1/90 képszélesség).
