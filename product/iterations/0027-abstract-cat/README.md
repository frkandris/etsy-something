# 0027 — absztrakt macska, a katalógus-referencia stílusában

A felhasználó három teljes listing-rácsot küldött ugyanattól az eladótól. Ebből olvasott recept:
- egységes ár 2 056 HUF (30% off 2 939-ről) MINDEN listingen
- fehér/krém mező, lebegő motívum, keret nélkül a designban
- **olvadó/csepegő** organikus rétegformák (nem ornamens, nem jelenet)
- visszafogott földes paletta VÁLTAKOZÓ világos-sötét lépcsővel
- fehér és rusztikus fa keret egyaránt; enteriőr fotó háttérrel
- iparosított sablon: számok 0-9, kutyafajták, farm-állatok, ünnepek — ugyanaz a séma

Ebben a körben három valódi kódhiba derült ki, mind eltakarta a művet:
1. a keret boolean nyílása csak a mélység 28%-ánál kezdődött, ezért a keret hátsó része
   TÖMÖR lapként ült a mű előtt — csak a két legelső réteg bukkant ki
2. a háttérlap z-pozíciója fix −0,4 mm volt, miközben a papírvastagság 2 mm lett; belemetszett
   az 1. rétegbe
3. a `--white-top` ág miatt a keret egyáltalán nem épült meg — amit keretnek hittünk, az a
   fehér fedőlap éle volt

Trace: 7 réteg, 0 nyak, min-part 120, `--no-keyhole` (keretbe megy).
