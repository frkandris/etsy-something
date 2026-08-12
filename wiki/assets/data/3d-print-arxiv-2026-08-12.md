# 3D nyomtatás — tudományos irodalomkutatás (arXiv-fókusz)

**Dátum:** 2026-08-12 · **Készítette:** claude-opus-5 (Claude Code) · **Státusz:** nyers kutatási anyag

Ez a fájl a **3D nyomtatás mint második Etsy-irány** szakirodalmi felmérése, még a marketplace-adatok
lehúzása előtt. A meglévő layered/multilayer SVG kutatáshoz nem kapcsolódik közvetlenül; külön
irány.

**Ellenőrzési szabály, amit követtem:** minden tételnél van arXiv-azonosító, DOI vagy általam
ténylegesen lekért URL. Ahol a teljes szöveget nem tudtam megnyitni (paywall, 403, PDF-táblázat),
ott ez **külön oda van írva** — azok a számok nem tekintendők igazoltnak. Az arXiv-azonosítókat az
`arxiv.org/abs/<id>` oldal vagy az `export.arxiv.org` API alapján ellenőriztem; a DOI-kat a Crossref
API-n keresztül.

---

## Összefoglaló

**1. A fizetős 3D-fájl nem geometriát ad el.** Az ingyenes oldal hatalmas és jogilag nyitott:
Özkil 158 373 Thingiverse-modelljéből **90,6% nyílt licencű, és a CC-licenceknek csak 13,8%-a tiltja
a kereskedelmi felhasználást** [A1]. Amit egy fizetős fájl hozzátehet, az a **garantáltan ép
geometria** (a repozitóriumok tele vannak nem-manifold, önmetsző hálókkal — Thingi10K [A4]) és a
**dokumentáció**: Alcock négy dokumentált vevői akadálya (összeszerelés, testreszabhatóság,
nyomtathatóság az adott gépen, készítési mód) [A5, D9] gyakorlatilag egy listing-checklist.

**2. A letöltésszám nem kereslet.** Novak 30 népszerű modellt követett 500 napig: **7 823 249
letöltésre 19 425 „make" jutott, és az arány 1:474-ről 1:784-re romlott** [A2]. Bármilyen
volumen-becslés, ami letöltésre épül, nagyságrendekkel felülbecsli a fizetőképes keresletet.

**3. A parametrikus template erősebb termék, mint a kész fájl** — de csak ha a vevő érzi, hogy ő
tervezte. Kyriakou (MIS Quarterly) szerint **a metamodelleket többször hasznosítják újra, mint az
általuk generált konkrét modelleket** [A9/D8]; Franke–Schreier szerint a saját tervezésű termékre a
fizetési hajlandóság kb. **+100%** [D1, D2] — viszont Franke 2010 kimutatja, hogy a prémium az
**érzékelt saját hozzájáruláson** múlik [D3], vagyis egy „egy kattintás, kész" automata
személyre szabás akár kevesebbet is érhet, mint egy lassabb, látható konfigurátor.

**4. A generatív 3D ma látványra optimalizál, nem nyomtathatóságra — és a licenc buktató.** A SEG
[C10] mérése szerint a TRELLIS kimenetének normalizált támaszigénye 0,343, a nyomtathatóságra
optimalizált változaté 0,176; a GenMF [C11] pedig azt mutatja, hogy egyszínű nyomtatásnál a
textúrába kódolt részlet **elvész**, mert a generált modellek a látványt textúrában, nem
geometriában tárolják. Licencoldalon: **a Hunyuan3D 2.0 és 2.1 licence kifejezetten nem érvényes az
Európai Unióban** [L] — Magyarországról nem használható jogtisztán.

---

## A) A piac és a digitális javak közgazdaságtana

### A/1. Thingiverse és STL-repozitóriumok — nagy mintás empíria

**[A1] Collective design in 3D printing: A large scale empirical study of designs, designers and evolution**
Ali Gürcan Özkil · 2017 · Design Studies 51:66–89 · DOI 10.1016/j.destud.2017.04.004 ·
teljes szöveg: https://backend.orbit.dtu.dk/ws/files/140695987/design_studies_final.pdf
A legfontosabb adathalmaz-tanulmány. **158 373 nyilvános design / 247 768 felhasználó.** A designok
**92,6%-a „dormant"** (soha nem lett belőle derivatíva), csak 7,4% „fertile". Ugyanakkor a designok
**51%-a (81 039 db) derivatíva vagy hibrid**, és mindössze **7 994 gyökér-designra (a hálózat 5%-a)**
vezethetők vissza; a nem triviális gyökér-designok átlagos termékenysége 21,4. **A dolgok 90,6%-a
nyílt (CC vagy GNU) licencű, és a CC-licenceknek csak 13,8%-a tiltja a kereskedelmi felhasználást.**
Vezető kategóriák: 3D-nyomtató alkatrészek/szerszámok, telefontokok/tartók, rendszerezők/kulcstartók,
művészeti figurák. *Nekünk:* ez az ingyenes kínálat alakja, amivel versenyeznénk — hatalmas, jórészt
mozdulatlan, és jogilag szinte teljesen újrahasznosítható, kereskedelmileg is.

**[A2] 500 days of Thingiverse: a longitudinal study of 30 popular things for 3D printing**
James I. Novak · 2020 · Rapid Prototyping Journal 26(10):1723–1731 · DOI 10.1108/RPJ-01-2020-0021 ·
preprint: https://edditiveblog.wordpress.com/wp-content/uploads/2020/10/500-days-of-thingiverse-preprint.pdf
30 top modell követése 2018-08 és 2020-01 között. A #3DBenchy átlépte az 1 millió letöltést; a
legmagasabb mért ütem **698 letöltés/nap**; a befutott slágerek **60–300 letöltés/nap** szinten
platóznak. A 30 modellre összesen **7 823 249 letöltés, de csak 19 425 „make"** — a konverzió
**1 make / 474 letöltésről 1 / 784-re romlott**. A platform 1 141 450 → 1 625 050 dologra nőtt
(+42,4%), a nézettség/letöltés/like 83–99%-kal, de a make/remix/komment csak ~25–28%-kal.
*Nekünk:* a letöltés→tényleges nyomtatás tölcsér brutálisan veszteséges; egy ingyenes letöltés
nagyon gyenge jelzés a fizetési hajlandóságra.

**[A3] Thingiverse: review and analysis of available files**
Felix W. Baumann, Dieter Roller · 2018 · Int. J. Rapid Manufacturing 7(1):83 · DOI 10.1504/IJRAPIDM.2018.089731
Véletlen minta: 10 000 véletlen ThingID-ból **3 528 létezett és volt letölthető** (azaz **~65%-a az
azonosítóknak halott/privát/törölt**). Explicit hosszú-farok megállapítás: „a legtöbb kiszámított
metrikát az összes elemzett modell kevesebb mint 20%-a uralja" — nézettségben, letöltésben és
geometriában is. Domináns licenc: CC-BY-SA.

**[A4] Thingi10K: A Dataset of 10,000 3D-Printing Models**
Qingnan Zhou, Alec Jacobson · 2016 · arXiv:1605.04797 · https://arxiv.org/abs/1605.04797
10 000 valós Thingiverse-modell geometriai minőség-benchmarkja: manifoldság, önmetszés, genus,
plusz kontextus (licencek, tagek, eszközök). Az absztrakt szerint a gyűjtemény kifejezetten a
„vadon" előforduló hibákat (self-intersections, non-manifoldness) reprezentálja.
*Nekünk:* ez a bizonyíték arra, hogy a repozitóriumi geometria jelentős része törött — egy fizetős,
garantáltan tiszta fájl valódi minőségi differenciáló. (Az absztraktot ellenőriztem; a neten
keringő „X% zárt háló eszközönként" számok a teljes cikkben vannak, azokat **nem** ellenőriztem.)

**[A5] Barriers to Using, Customizing, and Printing 3D Designs on Thingiverse**
Celena Alcock, Nathaniel Hudson, Parmit K. Chilana · 2016 · ACM GROUP '16, 195–199 ·
DOI 10.1145/2957276.2957301 · https://hci.cs.sfu.ca/AlcockGroup16.pdf
2015 szeptemberi minta: **23 285 design, 22 952 design-specifikus komment, 21 893 felhasználói
profil.** Négy akadály: (1) hogyan használják/szerelik össze a tárgyat, (2) **hogyan lehet a designt
testreszabni vagy remixelni**, (3) hogyan fog nyomtatódni az adott gépen, (4) hogyan készült.
*Nekünk:* kész checklist arra, mit kell a listingbe és a mellékelt PDF-be tenni, hogy csökkenjen a
visszatérítést generáló supportkérdés.

### A/2. Remix és derivatív mű

**[A6] Copy, Transform, Combine: Exploring the Remix as a Form of Innovation**
Christoph M. Flath, Sascha Friesike, Marco Wirth, Frédéric Thiesse · 2017 ·
Journal of Information Technology 32(4):306–325 · DOI 10.1057/s41265-017-0043-9
Hat év Thingiverse-adat. Nyolc összetett remix-mintát vezet le, *konvergens* (sok szülő) és
*divergens* (sok gyerek) csoportra bontva, és leírja, mely platform-funkciók (Customizer, „remix
this thing") hajtják a remixelést. (Az absztraktot ellenőriztem; a másodlagos forrásokban szereplő
„&gt;100 000 remixelt design" számot **nem**.)

**[A7] Creativity and productivity in product design for additive manufacturing: Mechanisms and platform outcomes of remixing**
Sascha Friesike, Christoph M. Flath, Marco Wirth, Frédéric Thiesse · 2019 ·
Journal of Operations Management 65(8):735–752 · DOI 10.1016/j.jom.2018.10.004
81 remix-alapú design kvalitatív kódolása → hat mechanizmus (kreativitás: inspiráció, játék,
tanulás; produktivitás: gyorsaság, javítás, felhatalmazás). Kvantitatívan: a remixelés növeli a
designok mennyiségét és sokféleségét, és **a remixelő tervezők designjait szignifikánsan gyakrabban
nyomtatják ki ténylegesen** — azaz a remix-leszármazás korrelál azzal, hogy a fájl *működik*.

**[A8] Toward a Theory of Remixing in Online Innovation Communities**
Michael A. Stanko · 2016 · Information Systems Research 27(4):773–791 · DOI 10.1287/isre.2016.0650
Regresszió **498 Thingiverse-innováción**. A közösségi interakció (kommentek, engagement) erősen
előrejelzi, hogy egy designt remixelnek-e; **a főoldali kiemelésnek nincs szignifikáns hatása**; a
láthatóság és a remixelés között **fordított U** alakú kapcsolat van.
*Nekünk:* a derivatív keresletet az engagement hajtja, nem a platform-promóció.

**[A9] Knowledge Reuse for Customization: Metamodels in an Open Design Community for 3D Printing**
Harris Kyriakou, Jeffrey V. Nickerson, Gaurav Sabnis · 2017 · MIS Quarterly 41(1):315–332 ·
DOI 10.25300/MISQ/2017/41.1.17 · preprint arXiv:1702.08072 · https://arxiv.org/abs/1702.08072
A Thingiverse Customizer-tanulmány. Harmadik újrahasznosítási módot azonosít („reuse for
customization"), és empirikusan kimutatja, hogy **a parametrikus metamodelleket gyakrabban
hasznosítják újra, mint az általuk generált konkrét modelleket**, és a hatás erősebb, ha a
metamodellt tapasztaltabb tervező készítette.
*Nekünk:* ez a legerősebb publikált bizonyíték arra, hogy egy parametrikus template jobb terjesztett
eszköz, mint egy fix fájl.

**[A10] Networks of Innovation in 3D Printing**
Harris Kyriakou, Steven Englehardt, Jeffrey V. Nickerson · 2013 · arXiv:1311.0529 ·
https://arxiv.org/abs/1311.0529
Korai, feltáró tanulmány a Thingiverse remix-hálózat szerkezetéről; amellett érvel, hogy a
remix-hálózat struktúrájából nyomon követhető az innováció és detektálható az új ötlet-kombinációk
megjelenése. Keretezésre jó, számokat nem ad.

**[A11] Collective Innovation in Open Source Hardware**
Harris Kyriakou, Jeffrey V. Nickerson · 2014 · arXiv:1404.1799 · Collective Intelligence 2014
Kvantitatív eredmény az absztraktban nincs — csak keretezésre idézhető.

**[A12] Remix in 3D Printing**
Spiros Papadimitriou, Evangelos E. Papalexakis, Bin Liu, Hui Xiong · 2015 · WWW '15 Companion,
367–368 · DOI 10.1145/2740908.2745943
⚠️ **Korrekció, ami fontos:** ez a cikk **nem** Kyriakou/Nickerson munkája — több webes forrás
összekeveri őket. Öt év Thingiverse-adat; a remix-kapcsolatokban egyszerre mutat ki **homofíliát és
inverz homofíliát** a fő metrikák mentén, erősebben, mint a szokásos közösségi/tartalmi kapcsolatok.

**[A13] „A Lot of Moving Parts": A Case Study of Open-Source Hardware Design Collaboration in the Thingiverse Community**
Kathy Cheng, Shurui Zhou, Alison Olechowski · 2024 · arXiv:2406.12801 · PACM HCI 2024 ·
https://arxiv.org/abs/2406.12801
Egyetlen projekt (DrawBot) 29 oldalas esettanulmánya kommentszálakon és designváltozásokon
keresztül. Dokumentálja, hogy a Thingiverse-en nincs verziókezelés és merge, azaz valódi
együttműködésre alkalmatlan. *Nekünk:* magyarázza, miért nem születnek karbantartott termékek a
nyílt repozitóriumokban — ez rés egy karbantartott, verziózott fizetős katalógusnak.

**[A14] Conflict or Collaboration — The Impact of Knowledge Endowment Heterogeneity on Remix in Open Collaborative Communities**
Juan Tan, Congcong Qi, Xiaohui Gao és mtsai · 2022 · Frontiers in Psychology 13:941448 ·
DOI 10.3389/fpsyg.2022.941448
SEM **25 032 Thingiverse felhasználó/design rekordon**. Az explicit tudás-heterogenitás növeli a
remix **mennyiségét**, de csökkenti a **minőségét**; az implicit heterogenitás növeli a mennyiséget
minőségi hatás nélkül. A remix-készlet módszertanilag leggyengébb darabja, de valódi N-nel.

### A/3. Licencelés, szellemi tulajdon, kalózkodás

**[A15] Preventing Others from Commercializing Your Innovation: Evidence from Creative Commons Licenses**
Erdem Dogukan Yilmaz, Tim Meyer, Milan Miric · 2023 · arXiv:2309.00536 · https://arxiv.org/abs/2309.00536
A legjobb modern licencválasztási számok. Végleges panel: **182 453 design 30 093 tervezőtől**;
**~98% CC-licencű**; **15,5% derivatíva**. A követőszám megduplázódása **+10 százalékponttal** növeli
a NonCommercial licenc választásának valószínűségét (és +2,6 pp-tal a NoDerivatives-ét); ha egy
design derivatíva, az **+2,94 pp-tal** növeli az NC valószínűségét (a ~15%-os alaphoz képest
+19,6%); a kiemelés **+183% követőnövekedéssel** jár együtt.
*Nekünk:* ahogy az ingyenes oldal alkotói státuszt szereznek, egyre inkább lezárják a kereskedelmi
újrahasznosítást — vagyis a „veszek egy ingyenes STL-t és eladom" idővel **jogilag kockázatosabb**
lesz, nem kevésbé.

**[A16] Cultures of sharing in 3D printing: what can we learn from the licence choices of Thingiverse users?**
Jarkko Moilanen, Angela Daly, Ramon Lobato, Darcy W. E. Allen · 2015 · Journal of Peer Production 6:1–13 ·
SSRN 2440027 · https://eprints.qut.edu.au/95070/21/Cultures_of_sharing_in_3D_printing_what_can_we_learn_from_the_licence_choices_o.pdf
**68 618 nyilvános Thing.** Licencmegoszlás: **CC-BY 36%, CC-BY-SA 36%, CC-BY-NC 10%, CC-BY-NC-SA 8%,
GPL 2.0 4%**; a négy legnépszerűbb licenc a Thingek **89,84%-a**; CC összesen 89%. **A két
legnépszerűbb választás mindkettő megengedi a kereskedelmi felhasználást.** Emellett: a fájlok
**~42%-a privát**, és csak 6% van „in progress"-nek jelölve — azaz nagy a rejtett készlet, és a
„nyitottság" részben látszat.

**[A17] A Legal and Empirical Study of 3D Printing Online Platforms and an Analysis of User Behaviour (Study I)**
Dinusha Mendis, Davide Secchi · 2015-03 · UK Intellectual Property Office, report 2015/41 ·
https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/421221/A_Legal_and_Empirical_Study_of_3D_Printing_Online_Platforms_and_an_Analysis_of_User_Behaviour_-_Study_I.pdf
Több platformra kiterjed: **385 118 fájl, ~104 000 felhasználó.** Platformmegoszlás: 123D 31 974
felhasználó (30,6%), GrabCAD a felhasználók 19,7%-a de **a fájlok 28,2%-a**, Thingiverse 16 385
felhasználó (15,6%). **A feltöltött fájlok 65%-án nincs semmilyen licencjelzés.** Tagek:
**a 'miniature', 'art' és 'jewellery' egyenként ≈10%**, a 'design' ≈7%.
*Nekünk:* a dekoratív/ajándék jellegű tartalom dominál — pontosan az Etsy-átfedés. Márkanevet
tartalmazó leírás ritka (max 1,3%), de a márkakulcsszavak **~30%-a Apple-termékekre** vonatkozik.

**[A18] License choice in open 3D printing content community: Are current license options sufficient?**
Su Jung Jee, So Young Sohn · 2018 · Telematics and Informatics 35(8):2242–2253 ·
DOI 10.1016/j.tele.2018.09.003
Logit modell Thingiverse-metaadatokon. A licencpreferencia élesen eltér **funkcionális vs. nem
funkcionális (esztétikai)** tartalomra, de a sok „mindkettő" jellegű tételnél nincs szignifikáns
elkülönülés — a szerzők szerint a jelenlegi CC-opciók nem elegendők 3D-tartalomra.
*Nekünk:* egy dekoratív-de-funkcionális niche (mint a layered SVG vagy egy nyomtatható tárgy)
pontosan ebben a szürke zónában ül.

**[A19] Patents, Meet Napster: 3D Printing and the Digitization of Things**
Deven R. Desai, Gerard N. Magliocca · 2013/2014 · 102 Georgetown Law Journal 1691 ·
https://doi.org/10.31228/osf.io/3urhd (postprint rekord)
A kanonikus jogi keretezés: a 3D nyomtatás „azt teszi a fizikai tárgyakkal, amit az MP3 a zenével".
Otthoni nyomtatási kivételt javasol, és a DMCA notice-and-takedown kiterjesztését a szabadalmaztatott
tárgyak fájljait tároló platformokra. *Nekünk:* magyarázza, miért *szerzői jogi* alakú a takedown-
kockázat a fájlpiacokon a gyakorlatban, nem szabadalmi.

**[A20] The complementarity of openness: How MakerBot leveraged Thingiverse in 3D printing**
Joel West, George Kuk · 2016 · Technological Forecasting and Social Change 102:169–181 ·
DOI 10.1016/j.techfore.2015.07.025
A platformkockázat-tanulmány: hogyan sajátította ki egy cég egy nyílt közösség értékét, beleértve a
2012–13-as licenc/ToS-botrányt. **Fenntartás:** a metaadatot Crossrefen ellenőriztem, a teljes
szöveget nem nyitottam meg — a részletek **igazolatlanok**.

### A/4. Nulla határköltség, hosszú farok (nincs 3D-specifikus munka; ez az átvihető alap)

**[A21] Goodbye Pareto Principle, Hello Long Tail: The Effect of Search Costs on the Concentration of Product Sales**
Erik Brynjolfsson, Yu (Jeffrey) Hu, Duncan Simester · 2011 · Management Science 57(8):1373–1386 ·
DOI 10.1287/mnsc.1110.1371
Az internetes csatorna eladáseloszlása szignifikánsan kevésbé koncentrált az offline-nál **még akkor
is, ha a kínálat és az árak azonosak** — a hajtóerő az alacsonyabb keresési költség és az ajánló-
felületek. *Nekünk:* egy niche életképessége a platform kereső- és ajánlófelületének függvénye,
vagyis az SEO/tag-munka nem marketing-díszítés, hanem maga a mechanizmus.

**[A22] Research Commentary — Long Tails vs. Superstars: The Effect of Information Technology on Product Variety and Sales Concentration Patterns**
Erik Brynjolfsson, Yu Jeffrey Hu, Michael D. Smith · 2010 · Information Systems Research 21(4):736–747 ·
DOI 10.1287/isre.1100.0325
Taxonómia a hosszú farok és a szupersztár-hatás összeegyeztetésére, és a mérésükre használható
metrikák (Gini, top-X részesedés) buktatóival. *Nekünk:* módszertani ellenőrzés bármelyik
koncentrációs állításunkra.

**[A23] Intellectual Property Strategy and the Long Tail: Evidence from the Recorded Music Industry**
Laurina Zhang · 2018 · Management Science 64(1):24–42 · DOI 10.1287/mnsc.2016.2562
⚠️ **Részben igazolatlan:** a kiadó nem adja ki az absztraktot a Crossref/S2/OpenAlex felé, és a
fizetős szöveget nem tudtam megnyitni. Másodlagos források (és a Yilmaz 2023 [A15] benne idézett
hivatkozása) szerint a védelem lazítása (DRM eltávolítása) átlagosan **~10%-kal** növelte a digitális
eladást, a nyereség a **kis eladású albumokra (~30–40%)** koncentrálódott, a topeladóknál gyakorlatilag
nulla volt. Ha az irány igaz, ez a legerősebb elérhető bizonyíték arra, hogy a **kevésbé megszorító
licenc pont az ismeretlen, hosszú-farok eladónak használ** — ami az új Etsy-bolt helyzete.

**[A24] How do firms make money selling digital goods online?**
Anja Lambrecht, Avi Goldfarb, Alessandro Bonatti, Anindya Ghose, Daniel G. Goldstein, Randall A. Lewis ·
2014 · Marketing Letters 25(3):331–341 · DOI 10.1007/s11002-014-9310-5
Áttekintés a közel nulla határköltségű javak monetizálási modelljeiről (verziózás, bundle,
freemium, hirdetés, komplementerek). **Fenntartás:** csak metaadatot ellenőriztem, absztraktot nem
találtam — a tartalomleírás a címből/folyóiratból következtetve, **igazolatlan**.

---

## B) Mi nyomtatható jól és mi nem — terméktervezési korlátok

> **Figyelmeztetés a szakasz egészére:** ez a terület **nincs arXiv-en**. Célzott lekérdezések
> (`abs:"support-free" AND abs:"additive manufacturing"`, `abs:"print-in-place"`,
> `abs:"printability"`) 4–5 releváns találatot adtak, azok is robotikai/metaanyag-témájúak. A DfAM
> tervezési szabályok a szakfolyóiratokban (Additive Manufacturing, Rapid Prototyping Journal), a
> szabványokban (ISO/ASTM 52910 sorozat) és **gyártói tudásbázisokban** élnek. Az utóbbiakat külön
> megjelölöm — **nem lektorált forrás.**

**[B1] Topology optimization of 3D self-supporting structures for additive manufacturing**
Matthijs Langelaar · 2016 · Additive Manufacturing 12:60–70 · DOI 10.1016/j.addma.2016.06.010
A támasz nélküli („self-supporting") tervezés kanonikus optimalizálási hivatkozása: a maximális
túlnyúlásszöget mint szűrőt építi be a topológiaoptimalizálásba, így a kimenet eleve támasz nélkül
nyomtatható. Crossrefen ellenőrzött metaadat; 201 hivatkozás. *Nekünk:* ez a formális alapja annak,
amit a gyakorlatban 45°-os szabályként ismerünk.

**[B2] Support-Free Hollowing for 3D Printing via Voronoi Diagram of Ellipses**
Mokwon Lee, Qing Fang, Joonghyun Ryu és mtsai · 2017 · arXiv:1708.06577 ·
https://arxiv.org/abs/1708.06577
Belső üregesítés ellipszis-Voronoi-diagrammal úgy, hogy ne kelljen belső támasz.
*Nekünk:* anyagköltség-csökkentés dekoratív tömör tárgyaknál (szobrocska, figura) belső támasz
nélkül.

**[B3] Multi-Axis Support-Free Printing of Freeform Parts with Lattice Infill Structures**
Yamin Li, Kai Tang, Dong He · 2020 · arXiv:2007.00413 · https://arxiv.org/abs/2007.00413
Geodetikus távolságmezőre épülő rácsos kitöltés többtengelyes, önhordó nyomtatáshoz.
*Nekünk:* korlátozott relevancia — többtengelyes gépet feltételez, nem konzumer FDM-et.

**[B4] AgentsCAD: Automated Design for Manufacturing of FDM Parts via Multi-Agent LLM Reasoning and Geometric Feature Recognition**
Emmanuel George, Christopher Keefe, Peter Pak, Amir Barati Farimani · 2026 · arXiv:2607.02448 ·
https://arxiv.org/abs/2607.02448
Többügynökös rendszer, ami STEP-fájlt olvas, **45°-os küszöb felett detektálja a túlnyúlásokat**,
él-szomszédsági topológiagráfot épít, opcionálisan GraphSAGE-modellből (MFCAD++, **59 665 alkatrész**)
szemantikus jellemzőcímkéket injektál, majd egy LLM-ügynök átorientálást, lekerekítést, letörést
javasol; egy vision-modell ellenőrzi a renderelt nézeteket. Kimenet: módosított STEP + emberi
jelentés. *Nekünk:* a legkonkrétabb publikált „DfM automatizálás" — de az értékelés egyetlen
madárodú-esettanulmány, nem statisztika.

**[B5] A Characterization of 3D Printability**
Ioannis Fudos, Margarita Ntousia, Vasiliki Stamati és mtsai (8 szerző) · 2020 · arXiv:2010.12930 ·
https://arxiv.org/abs/2010.12930
„Printability score" bevezetése: egy modell nyomtathatósági valószínűsége adott AM-gépen, háló-
komplexitás és alkatrész-jellemzők alapján. Kísérleti validáció FDM, Binder Jetting és Polyjet
gépeken. **Az absztraktban nincsenek konkrét mm/fok küszöbök** — a pontszám módszere érdekes, a
számok nem szerepelnek benne.

**[B6] Parallelobox: Improved Decomposition for Optimized Parallel Printing using Axis-Aligned Bounding Boxes**
Hayley Hatton, Muhammed Khalid, Umar Manzoor, John Murray · 2026 · arXiv:2603.29579 ·
https://arxiv.org/abs/2603.29579
Modell-dekompozíció tengelyigazított befoglaló dobozokkal, hogy több nyomtatón párhuzamosan
lehessen nyomtatni; a benchmark „parallel printing time" metrikán veri a rekurzív szimmetria és a
kocka-vázas megközelítéseket. **Konkrét számokat az absztrakt nem közöl.**
*Nekünk:* csak akkor releváns, ha valaha fizikai terméket gyártanánk; digitális fájleladásnál nem.

**[B7] Chopper: partitioning models into 3D-printable parts**
Linjie Luo, Ilya Baran, Szymon Rusinkiewicz, Wojciech Matusik · 2012 · ACM TOG (SIGGRAPH Asia) ·
DOI 10.1145/2366145.2366148
A modell-feldarabolás kanonikus munkája: nyomtatótér-korlát, összeszerelhetőség, esztétika és
szilárdság mint együttes célfüggvény.

**[B8] Stress relief: improving structural strength of 3D printable objects**
Ondrej Stava, Juraj Vanek, Bedrich Benes, Nathan Carr, Radomír Měch · 2012 · ACM TOG (SIGGRAPH) ·
DOI 10.1145/2185520.2185544
Automatikus szerkezeti gyengeség-detektálás és javítás (falvastagítás, tartóborda, üregesítés) egy
nyomtatandó modellen. *Nekünk:* a „vékony nyúlvány letörik postázás közben / nyomtatás közben"
probléma formális kezelése — ugyanaz a családja a problémának, mint a papírvágásnál a 2 mm-es
minimális web.

**[B9] Fabricating articulated characters from skinned meshes**
Moritz Bächer, Bernd Bickel, Doug L. James, Hanspeter Pfister · 2012 · ACM TOG (SIGGRAPH) ·
DOI 10.1145/2185520.2185543
Skinned (animációs) hálóból közvetlenül gyártható **ízelt** karakter: automatikus ízület-elhelyezés
és -méretezés a bőrözési súlyokból. *Nekünk:* ez a legközelebbi formális rokona a mai Etsy-slágernek,
az „articulated print-in-place" figuráknak — de a cikk **utólag összeszerelt** ízületeket feltételez,
nem helyben nyomtatottakat.

**[B10] Polygon mesh repairing: an application perspective**
Marco Attene, Marcel Campen, Leif Kobbelt · 2013 · ACM Computing Surveys 45(2) ·
DOI 10.1145/2431211.2431214
A háló-javítás referencia-áttekintése: milyen hibatípusok vannak (lyuk, önmetszés, nem-manifold él,
degenerált háromszög, fordított normális), és melyik algoritmuscsalád melyiket oldja meg. Kiegészítő:
Attene, *A lightweight approach to repairing digitized polygon meshes*, The Visual Computer 2010,
DOI 10.1007/s00371-010-0416-3 (a MeshFix alapja).

**[B11] Implicit Toolpath Generation for Functionally Graded Additive Manufacturing via Gradient-Informed Slicing**
Charles Wade, Devon Beck, Robert MacCurdy · 2025 · arXiv:2505.08093 · https://arxiv.org/abs/2505.08093
Multi-material FDM szeletelés implicit geometria- és anyagmezőkből. A második stratégia
„közvetlenül a gradiens ellenében nyomtat, hogy **kiküszöbölje a purge-öt** és csökkentse a
hulladékot". **Konkrét százalékot a purge-csökkentésre nem közöl.**
*Nekünk:* ez a legközelebbi tudományos érintés az AMS/színváltós nyomtatás purge-hulladékához — és a
válasza az, hogy a probléma szeletelő-szintű, nem tervezői.

**[B12] Slice-100K: A Multimodal Dataset for Extrusion-based 3D Printing**
Anushrut Jignasu, Kelly O. Marshall, Ankush Kumar Mishra és mtsai · 2024 · arXiv:2407.04180 ·
NeurIPS 2024 · https://arxiv.org/abs/2407.04180
**100 000+ G-code fájl** a hozzájuk tartozó CAD-modellel, LVIS-kategóriával, geometriai
tulajdonságokkal és renderekkel (Objaverse-XL + Thingi10K forrásból).
*Nekünk:* ha valaha automatizált nyomtathatóság-ellenőrzőt építenénk, ez a tanítóadat.

### Gyártói (nem lektorált) tervezési szabályok

Ezeket **külön kezeljük** a lektorált irodalomtól. Forrás: Protolabs Network (korábban 3D Hubs)
tudásbázis, amit ténylegesen lekértem:

- https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
- https://www.hubs.com/knowledge-base/key-design-considerations-3d-printing/
- https://www.hubs.com/knowledge-base/selecting-optimal-shell-and-infill-parameters-fdm-3d-printing/

A konkrét számok a lenti „Számszerű tervezési szabályok" szakaszban.

---

## C) Generatív 3D — mennyire használható ma termékgyártásra

### C/1. A generátorok (mit adnak ki valójában)

**[C1] DreamFusion: Text-to-3D using 2D Diffusion**
Ben Poole, Ajay Jain, Jonathan T. Barron, Ben Mildenhall · 2022-09-29 · arXiv:2209.14988 ·
https://arxiv.org/abs/2209.14988
A Score Distillation Sampling bevezetése: 2D diffúziós modellel optimalizál egy NeRF-et, 3D
tanítóadat nélkül. **Kimenete NeRF, nem háló** — nyomtatásra közvetlenül alkalmatlan, és lassú
(per-prompt optimalizáció). Történeti alap, nem termelési eszköz.

**[C2] Magic3D: High-Resolution Text-to-3D Content Creation**
Chen-Hsuan Lin, Jun Gao, Luming Tang és mtsai (10 szerző, NVIDIA) · 2022-11-18 · arXiv:2211.10440 ·
https://arxiv.org/abs/2211.10440
Kétfázisú optimalizáció: durva NeRF, majd **textúrázott háló** finomítás nagy felbontású latens
diffúzióval. Kb. **2× gyorsabb a DreamFusionnál**, és a felhasználók **61,7%-ban** preferálták.
Kód/súly nem publikus.

**[C3] Point-E: A System for Generating 3D Point Clouds from Complex Prompts**
Alex Nichol, Heewoo Jun, Prafulla Dhariwal, Pamela Mishkin, Mark Chen (OpenAI) · 2022-12-16 ·
arXiv:2212.08751 · https://arxiv.org/abs/2212.08751
1–2 perc egyetlen GPU-n, **1–2 nagyságrenddel gyorsabb** az optimalizációs módszereknél, cserébe
gyengébb minőség. **Kimenete pontfelhő** — külön hálósítás kell hozzá.

**[C4] Shap-E: Generating Conditional 3D Implicit Functions**
Heewoo Jun, Alex Nichol (OpenAI) · 2023-05-03 · arXiv:2305.02463 · https://arxiv.org/abs/2305.02463
Implicit függvény paramétereit generálja, ami **textúrázott hálóként ÉS NeRF-ként is** renderelhető;
gyorsabban konvergál és jobb mintaminőséget ad, mint a Point-E. Súlyok publikusak (MIT).
*Nekünk:* ma már inkább történeti — a minőség messze elmarad a 2024–2026-os natív 3D modellektől.

**[C5] TripoSR: Fast 3D Object Reconstruction from a Single Image**
Dmitry Tochilkin, David Pankratz, Zexiang Liu és mtsai (Stability AI + Tripo) · 2024-03-04 ·
arXiv:2403.02151 · https://arxiv.org/abs/2403.02151
Egyetlen képből **0,5 másodperc alatt** 3D háló, transformer (LRM) alapon. **MIT licenc alatt
kiadva** — kifejezetten ezt hangsúlyozza az absztrakt.

**[C6] InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models**
Jiale Xu, Weihao Cheng, Yiming Gao, Xintao Wang, Shenghua Gao, Ying Shan (Tencent ARC) · 2024-04-10 ·
arXiv:2404.07191 · https://arxiv.org/abs/2404.07191
Multiview diffúzió + ritka nézetű rekonstrukció, **10 másodperc alatt**; differenciálható
izofelület-kinyeréssel közvetlenül a hálóreprezentáción optimalizál (mélység- és normális-
felügyelettel). Kód és súlyok publikusak (GitHub: Apache-2.0 jelvény).

**[C7] Structured 3D Latents for Scalable and Versatile 3D Generation (TRELLIS)**
Jianfeng Xiang, Zelong Lv, Sicheng Xu, Yu Deng, Ruicheng Wang, Bowen Zhang, Dong Chen, Xin Tong,
Jiaolong Yang (Microsoft Research) · 2024-12-02 · arXiv:2412.01506 · CVPR'25 Spotlight ·
https://arxiv.org/abs/2412.01506 · repo: https://github.com/microsoft/TRELLIS
Egységes „Structured LATent" (SLAT) reprezentáció, ami **Radiance Field, 3D Gaussian ÉS háló**
formátumra is dekódolható. **Max 2 milliárd paraméter, 500 000 elemű 3D adathalmazon** tanítva.
Szöveg- és képfeltételes generálás, lokális 3D szerkesztés.
*Nekünk:* **ez a jelenlegi alapértelmezett választás** — MIT licenc, nyílt súlyok, és a
nyomtathatósági szakirodalom (SEG [C10]) is ezt használja alapmodellként. Utódja, a TRELLIS.2,
projektoldalon létezik (https://microsoft.github.io/TRELLIS.2/), de **arXiv-cikket nem találtam
hozzá** — a `ti:"TRELLIS"` lekérdezés 10 találata mind más témájú.

**[C8] Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation**
Zibo Zhao, Zeqiang Lai, Qingxiang Lin és mtsai (Tencent Hunyuan) · 2025-01-21 · arXiv:2501.12202 ·
https://arxiv.org/abs/2501.12202
Kétkomponensű rendszer: Hunyuan3D-DiT (alak, flow-alapú diffúziós transformer) + Hunyuan3D-Paint
(textúra). **Licenckorlát az EU-ra — lásd a licencszakaszt. Ez nekünk kizáró ok.**

**[C9] Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material**
Team Hunyuan3D és mtsai (~50 szerző) · 2025-06-18 · arXiv:2506.15442 · https://arxiv.org/abs/2506.15442
PBR-anyagokkal; a cikk teljes adatelőkészítési, tanítási, kiértékelési és deployment-útmutatót ad.
**Ugyanaz az EU-kizárás.**

**[C10] TripoSG** · 2025 · arXiv:2502.06608 · repo: https://github.com/VAST-AI-Research/TripoSG
Kód MIT; a HuggingFace `VAST-AI/TripoSG` modellkártyán is **MIT** szerepel. **Fenntartás:** az
arXiv-absztraktot nem kértem le külön, az azonosítót a repóból vettem — a cím és a szerzőlista
**igazolatlan**.

**[C11] MeshAnything: Artist-Created Mesh Generation with Autoregressive Transformers**
Yiwen Chen, Tong He, Di Huang és mtsai (12 szerző) · 2024-06-14 · arXiv:2406.10163 ·
https://arxiv.org/abs/2406.10163
A hálókinyerést generálási feladatként kezeli, és **százszor kevesebb lapból** álló, „artist-created"
topológiájú hálót ad, a pontosság megtartásával.
*Nekünk:* nyomtatásnál a lapszám önmagában nem gond (a szeletelő úgyis háromszögesít), de a
**tiszta topológia** igen: kevesebb degenerált háromszög, kevesebb javítási igény.

**[C12] Advances in 3D Generation: A Survey**
Xiaoyu Li, Qi Zhang, Di Kang, Weihao Cheng, Yiming Gao és mtsai · 2024-01-31 · arXiv:2401.17807 ·
https://arxiv.org/abs/2401.17807
Rendszerezett áttekintés a 3D reprezentációkról, a generálási paradigmákról (feedforward,
optimalizáció-alapú, procedurális, novel view synthesis), adathalmazokról és nyitott kérdésekről.
Belépő olvasmány, nem termékdöntési input.

### C/2. Kifejezetten NYOMTATHATÓSÁGRA optimalizáló munkák

Ez a legfontosabb alszakasz, és **nagyon kicsi**. Négy releváns munkát találtam, mind 2025 novembere
után.

**[C13] From Prompts to Printable Models: Support-Effective 3D Generation via Offset Direct Preference Optimization (SEG)**
Chenming Wu, Xiaofan Li, Chengkai Dai · 2025-11-20 · arXiv:2511.16434 · https://arxiv.org/abs/2511.16434
**Ez a legközvetlenebbül releváns cikk az egész kutatásban.** Kimondja, hogy „a jelenlegi
text-to-3D modellek a vizuális hűséget priorizálják, de gyakran figyelmen kívül hagyják a fizikai
gyárthatóságot, ami túlzott támaszstruktúrát igénylő geometriákat eredményez". A megoldás:
támaszstruktúra-szimuláció beépítése a tanításba (Direct Preference Optimization with an Offset).
Mért eredmények (a HTML-verzió tábláiból, `arxiv.org/html/2511.16434v1`):

| Benchmark | metrika | TRELLIS | DPO | DRO | **SEG** |
|---|---|---|---|---|---|
| Thingi10k-Val | NSV (normalizált támaszvolumen) | 0,343 | 0,310 | 5,999 | **0,176** |
| Thingi10k-Val | NSV* (számtani átlag) | 1,255 | 1,200 | 18,467 | **0,587** |
| GPT-3DP-Val | NSV | 0,504 | 0,432 | 6,128 | **0,222** |
| GPT-3DP-Val | NSV* | 1,265 | 1,021 | 19,642 | **0,691** |

*Nekünk:* a TRELLIS nyers kimenetének támaszigénye **kb. kétszerese** a nyomtathatóságra
optimalizált változaténak. Vagyis ha ma generatív 3D-t használnánk termékhez, a támasz-/utómunka-
költség beépített, és a szakirodalom szerint kb. felezhető — de a SEG súlyai nem publikusak.

**[C14] Appearance-Preserving Refinement of Generated 3D Assets for Monochromatic Fabrication (GenMF)**
Chentao Shen, Chen Jia, Mingjie Huang, Zhuang Zhang, Haisen Zhao, Xiangru Huang · 2026-06-25 (v2: 06-27) ·
arXiv:2606.26850 · https://arxiv.org/abs/2606.26850
**A második legfontosabb.** Megfogalmazza pontosan azt a problémát, amibe egy Etsy-eladó belefutna:
„a [generált modellek] vizuális hűségének nagy része textúrában van kódolva, nem geometriában.
Amikor ilyen assetet egyszínű anyaggal gyártanak, a textúra-információ nagyrészt elvész, és a
vizuálisan fontos részletek eltűnnek, még ha az eredeti geometria hűen megmarad is." A javasolt
GenMF keretrendszer geometriai finomítással állítja vissza a megjelenést, miközben kezeli, hogy az
éles lokális jellemzők feszültséggócot és gyártási kockázatot okoznak. **Konkrét számok az
absztraktban nincsenek; a cikk bírálat alatt.**

**[C15] Decoder Generates Manufacturable Structures: A Framework for 3D-Printable Object Synthesis**
Abhishek Kumar · 2026-01-07 · arXiv:2601.08015 · https://arxiv.org/abs/2601.08015
Dekóder-alapú generálás, ami explicit gyártási korlátokat (túlnyúlásszög, falvastagság, szerkezeti
integritás) tart be. Jelentett **96,8%-os gyárthatósági arány**. **Fenntartás:** 8 oldal, 3 ábra,
1 tábla, egyszerzős, ismert konferencia-elfogadás nélkül — az eredményt óvatosan kezeljük.

**[C16] PrintAnything: Learning an Intermediate Representation for 3D printing G-code Generation**
Sangmin Hong, Daniel Sungho Jung, Heewon Kim, Kyoung Mu Lee · 2026-07-30 · ECCV 2026 ·
arXiv:2607.27729 · https://arxiv.org/abs/2607.27729
Megkerüli a hálót: pontfelhőből közvetlenül generál futtatható G-code-ot, szeletenkénti
pontprojekcióval és egy „G-plan" 2D reprezentációval (occupancy + region + flow map). Indoklása
szó szerint a mi problémánk: „a legtöbb 3D nyomtatási pipeline vízhatlan hálót igényel bemenetként…
a pontfelhőből rekonstruált hálók gyakran tartalmaznak geometriai artefaktumokat… amelyeket nehéz
javítani, és nyomtatási hibához vezethetnek."

### C/3. Háló-javítás („make it printable")

**[C17] Robust Watertight Manifold Surface Generation Method for ShapeNet Models**
Jingwei Huang, Hao Su, Leonidas Guibas · 2018-02-05 · arXiv:1802.01698 · https://arxiv.org/abs/1802.01698
Oktree-reprezentáció + izofelület-kinyerés + visszavetítés az eredeti hálóra. Garantáltan korrekt
2-manifold topológiát ad ShapeNet-modellekre. (Ez a széles körben használt „Manifold" eszköz.)

**[C18] ManifoldPlus: A Robust and Scalable Watertight Manifold Surface Generation Method for Triangle Soups**
Jingwei Huang, Yichao Zhou, Leonidas Guibas · 2020-05-23 · arXiv:2005.11621 · https://arxiv.org/abs/2005.11621
Az előbbi utódja: **nem támaszkodik a bemenő háromszögek normálisaira**, és pontosan visszaadja a
nulla-térfogatú struktúrákat is. Objektum-szinttől város-szintig működik.
*Nekünk:* ez a de facto nyílt eszköz arra, hogy egy generált vagy scannelt „triangle soup"-ból
vízhatlan hálót csináljunk. A [B10] Attene-áttekintés adja hozzá a hibataxonómiát.

### C/4. Melléktermékek, amiket érdemes látni

**[C19] Mirror Illusion Art (AutoMIA)**
Xiaopei Zhu, Zeyuan Li, Jun Zhu, Xiaolin Hu · 2026-07-02 · arXiv:2607.02015 ·
https://arxiv.org/abs/2607.02015 · kód: https://github.com/zxp555/AutoMIA
Két célképből (elölnézet + tükörkép) automatikusan tervez **nyomtatható** 3D illúzió-tárgyat, alakot
és színt együtt optimalizálva. **~76 másodperc és 2,6 GB memória** egyetlen RTX 3090-en.
*Nekünk:* ez egy kész, publikált, nyílt kódú **termékkategória-generátor** — pontosan az a fajta
„wow-faktoros ajándéktárgy", ami az Etsy-n eladható, és amihez nincs kínálat.

**[C20] Particulate: Feed-Forward 3D Object Articulation**
Ruining Li, Yuxin Yao, Chuanxia Zheng, Christian Rupprecht, Joan Lasenby, Shangzhe Wu, Andrea Vedaldi ·
2025-12-12 (v2: 2026-03-27) · arXiv:2512.11798 · https://arxiv.org/abs/2512.11798
Egy 3D hálóból **másodpercek alatt** kikövetkezteti a 3D részeket, a kinematikai hierarchiát és a
mozgáskorlátokat. *Nekümk:* az „articulated" (ízelt) figurák automatikus előállításához ez a
hiányzó lépés — de a modell ízületeket *azonosít*, nem **print-in-place** hézagokat *tervez*.

---

## D) Paraméteres és személyre szabott termék

### D/1. Fizetési hajlandóság és a személyre szabás közgazdaságtana

**[D1] Value Creation by Toolkits for User Innovation and Design: The Case of the Watch Market**
Nikolaus Franke, Frank Piller · 2004 · DOI 10.1111/j.0737-6782.2004.00094.x
A design-toolkit irodalom alapköve: akik toolkittel maguk konfigurálták az órájukat, kb. **+100%
fizetési hajlandóságot** mutattak a standard termékhez képest (contingent valuation és Vickrey
aukció). *Nekünk:* ez az érv amellett, hogy konfigurátort/previewt szállítsunk, ne statikus fájlt.
**Fenntartás:** Crossref-metaadat ellenőrizve, teljes szöveg nem — a „+100%" a másodlagos
irodalomból és Schreier 2006-ból származik.

**[D2] The value increment of mass-customized products: an empirical assessment**
Martin Schreier · 2006 · DOI 10.1002/cb.183
Három további kategórián (telefontok, póló, sál) reprodukálja az eredményt, szintén **100% feletti**
átlagos WTP-növekménnyel, és lebontja négy összetevőre: **preferencia-illeszkedés, észlelt egyediség,
szerzőségi büszkeség, folyamat-élvezet**. *Nekünk:* ez a négy dolog az, amit egy személyre szabott
listing ténylegesen hirdethet. **Fenntartás:** Crossref-metaadat ellenőrizve, absztrakt másodlagos.

**[D3] The „I Designed It Myself" Effect in Mass Customization**
Nikolaus Franke, Martin Schreier, Ulrike Kaiser · 2010 · Management Science 56(1):125–140 ·
DOI 10.1287/mnsc.1090.1077 · https://pubsonline.informs.org/doi/10.1287/mnsc.1090.1077
Öt kísérlet: a saját tervezésű termék WTP-je **túlmutat** azon, amit a preferencia-illeszkedés és a
ráfordított erőfeszítés magyaráz; a maradék a teljesítményérzésből jön, és az **észlelt saját
hozzájárulás** moderálja. *Nekünk:* **ez a legfontosabb figyelmeztetés az egész D szakaszban** — egy
konfigurátor, ami láthatóvá teszi a vevő döntéseit (élő preview, „a te designod"), több értéket fog
be, mint egy csendben automatizáló. A teljesen automatikus generálás **elpusztíthatja a prémium egy
részét.**

**[D4] Customer Perceived Value for Self-designed Personalised Products Made Using Additive Manufacturing**
Syahibudil Ikhwan Abdul Kudus, R. Ian Campbell, Richard Bibb · 2016 · DOI 10.24867/ijiem-2016-4-121 ·
http://ijiemjournal.uns.ac.rs/images/journal/volume7/06-Abdul-Kudus-IJIEM_2016_December-special-issue.pdf
Kísérleti vizsgálat (Loughborough Design School) 3D-nyomtatott személyre szabott termékekről,
Product Value és Experiential Value bontásban. A végfelhasználók **minden mérőszámon** magasabbra
értékelték a 3D-nyomtatott személyre szabott terméket a tömeggyártottnál. Kisebb és kevésbé
szigorú, mint a Franke-vonal, de az egyetlen kifejezetten AM-toolkit keretezésű.

**[D5] Personal fabrication as an operational strategy: Value of delegating production to customer using 3D printing**
Nagarajan Sethuraman, Ali K. Parlaktürk, Jayashankar M. Swaminathan · 2023 ·
Production and Operations Management · DOI 10.1111/poms.13981 ·
https://onlinelibrary.wiley.com/doi/abs/10.1111/poms.13981
Analitikus modell pontosan az Etsy digitális-termék üzletről: a cég a **designt** adja el, a vevő
személyre szabja és legyártja. Fő eredmény: az érték kinyerése **horizontális** testreszabással
(ízlés/variáció) működik, **vertikálissal** (minőségi szintek) nagyon nehéz.
*Nekünk:* téma/név/stílus-variációt árulj, ne „prémium minőség" upsellt. (DOI és megállapítások
több forráson egyeztetve; a cikktörzs fizetős.)

**[D6] Self-design fun: Should 3D printing be employed in mass customization operations?**
Shu Guo, Tsan-Ming Choi, Sai-Ho Chung · 2022 · European Journal of Operational Research 299(3):883–897 ·
DOI 10.1016/j.ejor.2021.07.009
Ellensúly az optimista WTP-irodalomhoz: **alacsony keresletű piacokon még a maximális
termékváltozatosság és a „self-design fun" együtt sem teszi nyereségessé** a 3D-nyomtatás alapú
tömeges személyre szabást; a haszon a kockázatkereső fogyasztói szegmensekre és a visszáru-/átfutási
idő kezelésére koncentrálódik. *Nekünk:* vékony niche-ben a variáció nem ingyen pénz.

**[D7] Emergence of Home Manufacturing in the Developed World: Return on Investment for Open-Source 3-D Printers**
Emily E. Petersen, Joshua Pearce · 2017 · Technologies 5(1):7 · DOI 10.3390/technologies5010007 ·
https://www.mdpi.com/2227-7080/5/1/7
A **vevő** oldalát árazza be. A YouMagine top-100 designja és Amazon-összehasonlítók alapján egy
konzumer nyomtató öt év alatt **>100% ROI**-t hoz olcsó helyettesítéseken; drága tételeknél a
megtérülés **<6 hónap**, ROI **986%**.
*Nekünk:* ez magyarázza, miért horgonyzódik a fájlvevő ára a „olcsóbb, mint megvenni a tárgyat"
ponthoz — a letöltés értékplafonja a fizikai tárgy kiskereskedelmi ára.

### D/2. Parametrikus / programozott CAD, Customizer-adat, végfelhasználói eszközök

**[D8] Knowledge Reuse for Customization** — lásd [A9]. A metamodell > modell eredmény.

**[D9] Barriers to Using, Customizing, and Printing 3D Designs on Thingiverse** — lásd [A5].

**[D10] Free and Open Source 3-D Model Customizer for Websites to Democratize Design with OpenSCAD**
Yuenyong Nilsiam, Joshua M. Pearce · 2017 · Designs 1(1):5 · DOI 10.3390/designs1010005 ·
https://www.mdpi.com/2411-9660/1/1/5
Saját hosztolható webes konfigurátor OpenSCAD parametrikus kód fölé, tervezés + implementáció +
validáció. Két explicit motiváció: az átlagfogyasztó nem elég képzett saját termék tervezéséhez, és
a **licencprobléma** — a Thingiverse-típusú customizerek arra kényszerítik a felhasználót, hogy
lemondjon a származtatott designok jogairól. Esettanulmány: testreszabható nyomtatható
mellprotézis. *Nekünk:* kész terv egy **saját tulajdonú** konfigurátorra.

**[D11] Understanding the Challenges of OpenSCAD Users for 3D Printing**
J. Felipe Gonzalez, Thomas Pietrzak, Audrey Girouard, Géry Casiez · 2024 · CHI '24 ·
arXiv:2408.01796 · DOI 10.1145/3613904.3642566 · https://arxiv.org/abs/2408.01796
20 OpenSCAD-felhasználós interjús vizsgálat. Még ez az önszelektált, programozás-orientált
populáció is küzd a 3D térbeli megértéssel, a validációval és kódhibakereséssel, az **organikus
formákkal**, és a kód↔nézet navigációval.
*Nekünk:* realitáscsekk — a szkript-vezérelt CAD **geometrikus/parametrikus** termékcsaládokra jó,
**organikus/művészi** formákra rossz. Egy „állatfigura-generátor" nem OpenSCAD-feladat.

**[D12] Facilitating the Parametric Definition of Geometric Properties in Programming-Based CAD**
J. Felipe Gonzalez, Thomas Pietrzak, Audrey Girouard, Géry Casiez · 2024 · UIST '24 ·
arXiv:2408.01815 · DOI 10.1145/3654777.3676417 · https://arxiv.org/abs/2408.01815
Pontosan a variánsgenerálás nehéz részéről szól: hogyan lesz a bedrótozott geometriából **változó**,
hogy a modell újrahasznosítható és testreszabható legyen újratervezés nélkül.

**[D13] pARam: Leveraging Parametric Design in Extended Reality to Support the Personalization of Artifacts for Personal Fabrication**
Evgeny Stemasov, Simon Demharter, Max Rädler, Jan Gugenheimer, Enrico Rukzio · 2024 · CHI '24 ·
arXiv:2403.09607 · DOI 10.1145/3613904.3642083 · https://arxiv.org/abs/2403.09607
Parametrikus konfiguráció + helyszíni XR-preview, hogy a laikus ne absztrakt számokat állítson.
n=20, HoloLens 2, XR vs. desktop összehasonlítás. *Nekünk:* az átvihető tanulság az, hogy **a vevő
rosszul konfigurál, ha a paraméterek absztraktak** — konkrét, kontextusos preview (méret valós
tárgyhoz képest, jelenetbe illesztett render) teszi használhatóvá a konfigurátort.

**[D14] The Road to Ubiquitous Personal Fabrication: Modeling-Free Instead of Increasingly Simple**
Evgeny Stemasov, Enrico Rukzio, Jan Gugenheimer · 2021 · IEEE Pervasive Computing 20(1) ·
arXiv:2101.02467 · https://arxiv.org/abs/2101.02467
Amellett érvel, hogy a terület tévesen hajszolja az egyre egyszerűbb modellezőeszközöket, miközben a
gyakorlatban a tartalom zöme **remixeléssel** készül, és az automatizálás, remixelés és **template**
a tömeges elterjedés útja. **Fenntartás:** az absztrakt nem tartalmaz százalékot a remix arányára;
a „tartalom zöme remix" konceptuális állítás, nem mért szám ebben a cikkben (a mért szám az [A1]-ben
van: 51% derivatíva).

**[D15] Mix&Match: Towards Omitting Modelling Through In-Situ Alteration and Remixing of Model Repository Artifacts in Mixed Reality**
Evgeny Stemasov, Tobias Wagner, Jan Gugenheimer, Enrico Rukzio · 2020 · arXiv:2003.09169 ·
https://arxiv.org/abs/2003.09169
Kevert valóságban böngészhető repozitórium, helyszíni preview és CSG-műveletek valós és virtuális
geometrián. Kiemeli, hogy a **környezeti kényszerek mérése (pl. hézag)** az, amit nem lehet kiszervezni.

**[D16] SliceHub: Augmenting Shared 3D Model Repositories with Slicing Results for 3D Printing**
Faraz Faruqi, Kenneth Friedman, Leon Cheng, Michael Wessely, Sriram Subramanian, Stefanie Mueller ·
2021 · arXiv:2109.14722 · https://arxiv.org/abs/2109.14722
Előre kiszámított szeletelési eredmények (nyomtatási idő, anyagfogyás felbontásonként és
méretezésenként) a repozitóriumi modellekhez.
*Nekünk:* kész ötlet egy differenciáló listing-elemre — **„ennyi ideig nyomtatódik, ennyi filamentet
eszik" táblázat** minden termékhez. Ez pontosan az [A5] harmadik akadályát oldja meg.

**[D17] Style2Fab: Functionality-Aware Segmentation for Fabricating Personalized 3D Models with Generative AI**
Faraz Faruqi, Ahmed Katary, Tarik Hasic, Amira Abdel-Rahman, Nayeemur Rahman, Leandra Tejedor,
Mackenzie Leake, Megan Hofmann, Stefanie Mueller · 2023 · UIST '23 · arXiv:2309.06379 ·
DOI 10.1145/3586183.3606723 · https://arxiv.org/abs/2309.06379
**1000 Thingiverse-modell** kvalitatív elemzéséből funkcionalitás-taxonómiát épít, majd
félautomatikusan **funkcionális vs. esztétikai** részekre bontja a hálót, hogy a generatív
stilizálás csak az esztétikait érintse.
*Nekünk:* ez a biztonsági korlát, amire egy személyre szabó pipeline-nak szüksége van — a vevő
neve/fotója/mintája a dekoratív felületre kerül, anélkül hogy elrontaná az illeszkedést, a hézagokat
vagy a nyomtathatóságot.

**[D18] P3D-Bench: Benchmarking MLLMs for Parametric 3D Generation and Structural Reasoning**
Yikang Yang, Zhanpeng Hu, Youtian Lin, Mengqi Zhou, Jingxi Xu és mtsai · 2026-06-09 ·
arXiv:2606.11152 · https://arxiv.org/abs/2606.11152
LLM-ek **kód-alapú** 3D generálásának benchmarkja (JSON, OpenSCAD, CadQuery, Three.js):
**400 text-to-3D, 400 image-to-3D eset és 203 annotált összeállítás**, pontozva futtathatóságra,
geometriai hűségre, topológiára, szövegre alapozott kényszerekre, többnézetes szemantikai
illeszkedésre és rész-szintű struktúrára. Lényeg: a lefutó és hihetően renderelő programok is
gyakran **nem** adják vissza a helyes parametrikus geometriát, és a többrészes összeállítás a
legnehezebb eset. *Nekünk:* az LLM-generált parametrikus CAD **ma nem** kézzel nem érintett
variánsgyár — a biztonságos architektúra: **ember által írt template + LLM tölti ki a paramétereket.**

### D/3. Kép → dombormű / litofánia

**[D19] Digital bas-relief from 3D scenes**
Tim Weyrich, Jia Deng, Connelly Barnes, Szymon Rusinkiewicz, Adam Finkelstein · 2007 ·
ACM TOG (SIGGRAPH) 26(3) · DOI 10.1145/1276377.1276417
A dombormű-tömörítés kanonikus módszere: adott 3D jelenetből, kamerából és néhány
frekvencia-csillapítási paraméterből olyan reliefet állít elő, ami rögzített nézőpontból megőrzi az
észlelt 3D formát drasztikusan összenyomott magasságtartományban.
*Nekünk:* minden fotó→plakett / relief-medál termék ennek a problémának a speciális esete; a
paraméterezés (mely frekvenciákat tartod meg) maga a tervezői szabályozó.

**[D20] Making bas-reliefs from photographs of human faces**
Zhongping Wu, Ralph R. Martin, Frank C. Langbein, Paul L. Rosin és mtsai · 2013 ·
Computer-Aided Design 45(3) · DOI 10.1016/j.cad.2012.11.002
Kétlépcsős pipeline **egyetlen szemből fényképezett arcképből**: előbb hihető dombormű-*kép*
szintézise, majd shape-from-shading a relief-geometriához. Explicit motiváció: érmék és emlékérmék.
**Fenntartás:** Crossrefen ellenőrzött metaadat; a ScienceDirect törzs 403-mal elutasított, a
módszerleírás másodlagos forrásból.

**[D21] Neural Modeling of Portrait Bas-Relief From a Single Photograph**
Yu-Wei Zhang, Ping Luo, Hao Zhou, Zhongping Ji, Hui Liu, Yanzhao Chen, Caiming Zhang · 2023 ·
IEEE TVCG 29(12):5008–5019 · DOI 10.1109/TVCG.2022.3197354 · https://pubmed.ncbi.nlm.nih.gov/35939483/
Végponttól végpontig kép→mélység fordítás portré-domborműhöz. Az adatproblémát félautomatikus
pipeline-nal oldja meg, ami **~23 000 szintetikus fotó/dombormű párt** generál (normáltérképek
fotókból → pixelenkénti mélység-rekonstrukció), majd architektúrákat hasonlít össze kvantitatív
metrikákkal **és** hivatásos művészi értékeléssel.
*Nekünk:* ez az aktuális state of the art egy fotó→dombormű termékvonal automatizálására, és
egyben minta a saját tanítóadat előállítására.

**[D22] Data for all: Tactile graphics that light up with picture-perfect resolution**
Jordan C. Koehler és mtsai (Bryan F. Shaw laborja, Baylor) · 2022 · Science Advances 8(33) ·
DOI 10.1126/sciadv.abq2640 · https://www.science.org/doi/10.1126/sciadv.abq2640
Az egyetlen szigorú kvantitatív **litofánia**-vizsgálat, amit találtunk. Vak és látó résztvevők
(**n = 360**) öt litofánia-formát értelmeztek tapintással vagy látással **≥79%-os pontossággal**.
*Nekünk:* számok a litofánia olvashatóságáról, plusz egy akadálymentesítési termékszög
(tapintható + háttérvilágított ajándék), amire az Etsy-n gyakorlatilag senki nem hivatkozik
bizonyítékkal. **Fenntartás:** a szerzőlistát nem tudtam teljesen ellenőrizni.

---

## Licencek — mit lehet kereskedelmileg használni és mit nem

Ez a szakasz azért kapott külön helyet, mert a projektben **már egyszer buktató volt** (Depth
Anything V2). Minden sort a hivatkozott URL-en ellenőriztem 2026-08-12-én.

| Modell / eszköz | Licenc | Kereskedelmi használat | Forrás |
|---|---|---|---|
| **TRELLIS** (Microsoft) | MIT (kód és súlyok) | **Igen, korlátozás nélkül** | https://github.com/microsoft/TRELLIS |
| **TripoSR** (Stability + Tripo) | MIT | **Igen** | arXiv:2403.02151 absztrakt: „Released under the MIT license" |
| **TripoSG** (VAST-AI) | MIT (kód); a HF-modellkártyán is MIT | **Igen** | https://github.com/VAST-AI-Research/TripoSG · https://huggingface.co/VAST-AI/TripoSG |
| **InstantMesh** (Tencent ARC) | Apache-2.0 (repo-jelvény) | **Igen** | https://github.com/TencentARC/InstantMesh — *a súlyok külön licence a modellkártyán nem volt kiolvasható, ellenőrizendő* |
| **Shap-E / Point-E** (OpenAI) | MIT | **Igen** | https://github.com/openai/shap-e |
| **Hunyuan3D 2.0** (Tencent) | Tencent Hunyuan 3D 2.0 Community License | **NEM az EU-ban.** A licenc szó szerint: „THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA." Egyébként 1 M havi aktív felhasználóig ingyenes kereskedelmi használat, attribúcióval. | https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE |
| **Hunyuan3D 2.1** (Tencent) | Tencent Hunyuan 3D 2.1 Community License | **Ugyanaz az EU/UK/Dél-Korea kizárás**, ugyanaz az 1 M MAU küszöb. | https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE |
| **Stable Fast 3D** (Stability AI) | Stability AI Community License | Igen, **1 M USD éves árbevétel alatt** ingyenes (fölötte Enterprise licenc kell). | https://huggingface.co/stabilityai/stable-fast-3d |
| **Meshy** (SaaS) | Ingyenes csomag: **CC BY 4.0** (kereskedelmi használat megengedett, **de attribúció kötelező**). Fizetős csomag: teljes privát tulajdon, attribúció nélkül. A jogok ahhoz a csomaghoz kötődnek, amin a modell készült. | Igen, feltételekkel | https://help.meshy.ai/en/articles/9992001-can-i-use-my-generated-assets-for-commercial-projects |
| **Tripo3D** (SaaS) | Ingyenes felhasználó: **a Tripo tartja meg a jogokat**, kereskedelmi használat engedély nélkül nem. Fizetős: a felhasználóé, kereskedelmi használat megengedett — **de tilos versengő modellt/szolgáltatást építeni belőle**. | Csak fizetős csomagban | https://www.tripo3d.ai/terms |
| **Depth Anything V2 — Small** | Apache-2.0 | **Igen** | https://huggingface.co/depth-anything/Depth-Anything-V2-Small |
| **Depth Anything V2 — Large** | **CC-BY-NC-4.0** | **NEM** | https://huggingface.co/depth-anything/Depth-Anything-V2-Large |

**A legfontosabb tanulság:** a Hunyuan3D-család a jelenlegi minőségi élmezőny egyik tagja, és
**számunkra Magyarországról jogilag nem elérhető** — a licenc az EU-ban nem alkalmazandó. Ez
ugyanaz a hibaosztály, mint a Depth Anything V2 Base/Large/Giant esete: a modellcsalád nyílt
súlyokkal jön, és mégsem használható. **A biztonságos alapértelmezés a TRELLIS (MIT).**

Külön figyelmeztetés a bemeneti oldalra: a Thingiverse-készlet 90,6%-a nyílt licencű [A1], de a
CC-licencek 13,8%-a NC [A1], és a NC-választás valószínűsége **nő** a szerző népszerűségével [A15].
Vagyis „letöltök egy ingyenes STL-t és eladom" pontosan a **legnépszerűbb** modelleknél sérti a
licencet.

---

## Konkrét, számszerű tervezési szabályok

**Jelölés:** ✅ = lektorált vagy szabvány forrás · ⚠️ = gyártói/oktatási tudásbázis, nem lektorált ·
❌ = általánosan ismert gyakorlati szám, amihez **nem találtam** ellenőrizhető forrást.

| # | Szabály | Érték | Forrás | Megbízhatóság |
|---|---|---|---|---|
| 1 | Maximális támasz nélküli túlnyúlás FDM-en | **45°** a függőlegestől; 45°-nál az új réteget az előző **50%-a** támasztja alá | https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/ | ⚠️ |
| 2 | Ugyanez algoritmikus kényszerként | a max. túlnyúlásszög mint szűrő a topológiaoptimalizálásban | Langelaar 2016, DOI 10.1016/j.addma.2016.06.010 [B1] | ✅ |
| 3 | Ugyanez automatizált DfM-detektorban | **45°-os küszöb** a túlnyúlás-detektáláshoz | AgentsCAD, arXiv:2607.02448 [B4] | ✅ |
| 4 | Maximális áthidalás (bridging) látható megereszkedés nélkül | **< 5 mm** | Protolabs Network, `how-design-parts-fdm-3d-printing` | ⚠️ |
| 5 | Minimális falvastagság, amit minden gép elvisz | **≥ 0,8 mm** | Protolabs Network, `key-design-considerations-3d-printing` | ⚠️ |
| 6 | Ajánlott héjvastagság | **2 fúvókaátmérő** (tipikusan 0,8 mm) | Protolabs Network, `selecting-optimal-shell-and-infill-parameters` | ⚠️ |
| 7 | Függőleges tüske (pin) küszöb | **> 5 mm** átmérő: perem + kitöltés; **< 5 mm**: csak perem, kitöltés nélkül | Protolabs Network, `how-design-parts-fdm-3d-printing` | ⚠️ |
| 8 | Elefántláb / tapadás kezelése | **45°-os letörés vagy lekerekítés** minden tálcát érintő élre | Protolabs Network, `how-design-parts-fdm-3d-printing` | ⚠️ |
| 9 | Függőleges furat | az FDM **alulméretezi**; kritikus furatot alulméretezve nyomtass és fúrd fel | Protolabs Network, `how-design-parts-fdm-3d-printing` | ⚠️ |
| 10 | Alapértelmezett kitöltés | **18–20%** a legtöbb esetre elég; **≥50%** ha csavart hajtanak bele | Protolabs Network, `selecting-optimal-shell-and-infill-parameters` | ⚠️ |
| 11 | Kitöltés → szilárdság | 25% → 50%: kb. **+25%** szilárdság; 50% → 75%: kb. **+10%** | Protolabs Network, `selecting-optimal-shell-and-infill-parameters` | ⚠️ |
| 12 | Generatív modell támaszigénye | TRELLIS nyers kimenet NSV **0,343**, nyomtathatóságra optimalizálva **0,176** (Thingi10k-Val) | SEG, arXiv:2511.16434 [C13] | ✅ |
| 13 | Kényszer-tudatos generatív dekóder gyárthatósági aránya | **96,8%** | arXiv:2601.08015 [C15] | ✅ (egyszerzős, óvatosan) |
| 14 | Litofánia olvashatóság | **n = 360** résztvevő, **≥79%** pontosság tapintással vagy látással | Science Advances 8(33), DOI 10.1126/sciadv.abq2640 [D22] | ✅ |
| 15 | **Illesztési hézag mozgó/print-in-place alkatrészek közt** | — | **NEM TALÁLTAM ellenőrizhető forrást** | ❌ |
| 16 | **Anyagfüggő zsugorodás (PLA/PETG/ABS/ASA) számszerűen** | — | **NEM TALÁLTAM ellenőrizhető forrást** ebben a körben | ❌ |
| 17 | **Vase mode / spiralize falvastagság-ajánlás** | — | **NEM TALÁLTAM ellenőrizhető forrást** | ❌ |
| 18 | **Minimális domborított/mélyített szöveg mérete** | — | **NEM TALÁLTAM ellenőrizhető forrást** | ❌ |
| 19 | **AMS/MMU purge-hulladék mennyisége színváltásonként** | — | csak kvalitatív: a gradiens-alapú szeletelés „kiküszöböli a purge-öt" | arXiv:2505.08093 [B11] — szám nélkül |

**Referencia-szabvány:** a DfAM tervezési követelmények hivatalos kerete az **ISO/ASTM 52910**
(„Additive manufacturing — Design — Requirements, guidelines and recommendations"). Létezését
Crossrefen ellenőriztem (pl. DIN EN ISO/ASTM 52910:2022-09, DOI 10.31030/3376541), de **a szabvány
szövege fizetős, nem nyitottam meg** — a benne lévő konkrét értékeket nem tudom idézni.

---

## Amit NEM találtam

Ez a szakasz legalább olyan fontos, mint a fenti. Ahol nincs irodalom, ott **empirikusan kell
mérni**, és a mérést a wiki `findings/` alá kell tenni populációval együtt.

### Piac és közgazdaságtan

1. **Az Etsy digitális letöltésekről nincs tudományos irodalom.** Az arXiv `all:"Etsy"` lekérdezés
   25 találata mind vagy ETSI távközlési szabvány, vagy egy exobolygó-műszer, vagy az Etsy saját
   ML/hirdetési mérnöki cikke (pl. arXiv:1711.01377, arXiv:2302.01255). **Nulla** eladó-oldali
   közgazdasági munka. A neten keringő „a top 10% eladó adja a GMS 50%+-át", „3,2 Mrd USD digitális
   szegmens", „87% margin" típusú számok blog/SEO tartalmak, követhető módszertan nélkül —
   **ne idézzük őket bizonyítékként.**
2. **A Printables, Cults3D, MyMiniFactory és MakerWorld akadémiailag nem létezik.** Az
   `all:"MyMiniFactory" OR all:"Cults3D"` lekérdezés **0 találat**. A repozitórium-közgazdaságtan
   teljes egészében Thingiverse-alapú, és többnyire **2013–2018-as adatokból** — vagyis a fizetős
   marketplace-ek és a Bambu/MakerWorld pontrendszer korszaka **előttről**. Ez valódi, aktuális rés.
3. **Nincs semmi a fizetős vs. ingyenes STL árazásáról vagy árrugalmasságáról.** Egyetlen
   tanulmány sem becsli, mennyiért kel el egy nyomtatható fájl, vagy hogyan reagál a kereslet az árra.
4. **A fizetős fájlok kalózkodását senki nem mérte.** A 3D-nyomtatási IP-irodalom vagy doktrinális
   (jogi szaklapok), vagy interjús. Nincs mérés szivárgási arányról, újrafeltöltésről vagy
   bevételkiesésről. `all:"digital goods" AND all:"piracy"` → 0 találat.
5. **A 3MF formátumról közgazdasági kontextusban semmi** — csak geometria/adathalmaz-cikkek
   (pl. Slice-100K [B12]).

### Tervezés és nyomtathatóság

6. **A print-in-place mechanizmusoknak nincs formális irodalma.** Az `abs:"print-in-place"`
   lekérdezés egyetlen érdemi találatot adott (arXiv:2606.20549, robotkéz-generálás, ami
   mellékesen említi a print-in-place ízületeket). Az ízelt karakterekről szóló grafikai munka
   ([B9] Bächer 2012) **utólag összeszerelt** ízületeket feltételez. **A hézagméret — a
   print-in-place termék legfontosabb egyetlen száma — sehol nincs publikálva.** Ez az első dolog,
   amit empirikusan mérni kell.
7. **A konkrét FDM tervezési szabályok (fok, mm, tolerancia) nincsenek arXiv-en**, és a lektorált
   szakfolyóiratokban is inkább optimalizálási módszerként, nem táblázatos szabályként. A használható
   számok gyártói tudásbázisokból jönnek. Ez fordítottja a papírvágásos tapasztalatunknak, ahol a
   2 mm-es minimális web saját mérésből jött — itt is **saját teszt-artefaktumot kell nyomtatni**.
8. **Vase mode / spiralize: nulla szakirodalom.** Se tervezési szabály, se szilárdsági vizsgálat.
9. **A multi-material / AMS purge-hulladék mennyiségileg nincs mérve.** Egyetlen érintőleges
   cikk [B11], az is szeletelő-oldali megoldásról, szám nélkül. Pedig ez közvetlen **anyagköltség**,
   és a színes nyomtatás a fő termékkülönböztető lenne.

### Generatív 3D

10. **Nincs független benchmark arról, hány százalékban ad vízhatlan, nyomtatható hálót az egyes
    generátor.** A SEG [C13] a támaszvolument méri, nem a manifoldságot; a GenMF [C14] a megjelenést;
    a [C15] 96,8%-a saját modelljére vonatkozik. **Egy összehasonlító „TRELLIS vs. TripoSG vs.
    InstantMesh: hány %-a a kimenetnek szeletelhető javítás nélkül" mérés nem létezik** — és ez
    pontosan az a szám, ami eldönti, használható-e generatív 3D termékgyártásra. Ezt magunknak kell
    megmérnünk.
11. **A TRELLIS.2-nek nincs arXiv-cikke** — csak projektoldala. Ha rá építenénk, a licencet és a
    képességeket a repóból kell ellenőrizni, nem publikációból.
12. **Nincs munka a generált modell → eladható termék teljes láncáról** (generálás → javítás →
    méretezés → szeletelés → tesztnyomtatás → listing). A darabok megvannak, a lánc nincs mérve.

### Személyre szabás

13. **A fizetési hajlandóságot senki nem mérte személyre szabott *digitális fájlra*.** A teljes
    Franke/Schreier-vonal fizikai, saját tervezésű tárgyra vonatkozik. Egy parametrikus template
    vagy egy személyre szabási *szolgáltatás* letöltésként eladva empirikusan feltérképezetlen.
14. **A litofánia gyakorlatilag nincs az arXiv-en** — explicit `all:"lithophane"` lekérdezés
    **0 találat**. A Science Advances akadálymentesítési cikken [D22] kívül csak szakmai tutorialok
    vannak. Nincs akadémiai munka litofánia-*generáló algoritmusról* vagy a vastagság/rétegmagasság
    és az észlelt minőség kapcsolatáról.
15. **Semmi a névből/szóból/sziluettből generált ajándéktárgyakról.** A dombormű-irodalom arcokat és
    jeleneteket fed le; a tipográfia- és sziluett-vezérelt személyre szabás — ami az Etsy-n a
    volumeneladó — akadémiailag érintetlen.
16. **A Thingiverse Customizer az egyetlen konfigurátor publikált használati adattal**, és az az
    adat **2015–2017-es** [A5, A9]. Nincs 2020 utáni vizsgálat arról, a letöltések/eladások hány
    százaléka testreszabott, hány paramétert tolerálnak a felhasználók, és hol hagyják abba.
17. **A testreszabás költségét egyszemélyes eladóra senki nem mérte** — egy paraméter hozzáadásának,
    egy variáns generálásának, egy személyre szabási supportkérdés megválaszolásának marginális
    ráfordítása.
18. **A dombormű/heightmap kutatás sosem optimalizál nyomtathatóságra** — nincs munka, ami a relief-
    tömörítést együtt optimalizálná minimális jellemzőmérettel, rétegmagassággal, túlnyúlással,
    vagy (a layered-cut esetben) diszkrét anyagvastagsággal. **A többrétegű vágás matematikailag egy
    kvantált dombormű-probléma, amit a grafikai irodalom nem tárgyal.**
19. **Az „I designed it myself" hatást soha nem tesztelték automatizált személyre szabással szemben**
    [D3]. Mivel a prémium az *észlelt hozzájáruláson* múlik, elképzelhető, hogy egy egykattintásos
    automata generálás **kevesebbet** ér, mint egy lassabb interaktív konfigurátor. Nem tesztelt, és
    kereskedelmileg döntő.

---

## Módszertani megjegyzések

- **Lekérdezett források:** arXiv API (`export.arxiv.org/api/query`) és `arxiv.org/abs` oldalak;
  Crossref API (`api.crossref.org`); GitHub raw LICENSE fájlok; HuggingFace modellkártyák; gyártói
  tudásbázisok. A Semantic Scholar API 429-cel elutasított, ezért a DOI-ellenőrzés Crossrefen ment.
- **Amit nem tudtam megnyitni:** a legtöbb Elsevier/Wiley/INFORMS teljes szöveg (fizetős), az
  ISO/ASTM 52910 szabvány, és a Bambu Lab wiki (402). A SEG PDF-táblázatai a PDF-ből nem voltak
  olvashatók, de az arXiv HTML-verzióból igen — az ott szereplő számokat használtam.
- **A webes keresési keret elfogyott** a munkamenet során (200/200 WebSearch hívás), ami a gyártói
  tervezési szabályok gyűjtését korlátozta. Egy következő körben a Prusa és a Bambu Lab
  tudásbázisát érdemes célzottan végigmenni.
</content>
</invoke>
