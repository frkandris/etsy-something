#!/usr/bin/env python3
"""Design styles — the pipeline makes several distinct product looks, not one.

A style bundles everything that has to agree end to end: how the depth map is
drawn, how many levels it wants, how the layers are traced, and how the render
presents it. Keeping them in one place is what stops a "paper cut" design from
being rendered on a plywood palette, which is how the whisker colour and the
keyhole kept ending up wrong.

  from styles import STYLES
  STYLES["papercut-colour"]["render_flags"]

Fields
  prompt      appended to the subject prompt in 00_generate.py
  levels      how many depth levels the look needs
  trace       flags for 02_trace.py
  render      view + palette + flags for render_blender.py
  note        why this style exists / what market evidence backs it
"""

STYLES = {
    # ---------------------------------------------------------------- paper
    "papercut-colour": dict(
        note="A papíros piac fő formája: telített kartonrétegek fehér fedőlap "
             "nyílásában, keretben. Bizonyíték: PaperCutMari 49 listing-review, "
             "wiki/findings/paper-layered-market.",
        prompt=("Bold flat shapes only, no fine line work. Each depth level is a "
                "large simple silhouette that nests inside the one behind it. "
                "Leave a clear margin - no shape may touch the outer edge."),
        levels=7,
        trace=["--no-keyhole", "--min-part", "130"],
        render=["lifestyle", "catref", "--frame", "--paper", "--white-top"],
    ),
    "papercut-mono": dict(
        note="Ugyanaz a konstrukció egy tónuscsaládban - a semleges lakberendezési "
             "vevőnek, aki nem akar színes falat.",
        prompt=("Bold flat shapes only. The levels should read purely by depth, "
                "not by colour, so keep the silhouettes clean and distinct."),
        levels=7,
        trace=["--no-keyhole", "--min-part", "130"],
        render=["lifestyle", "moonlit", "--frame", "--paper", "--white-top"],
    ),
    # ---------------------------------------------------------------- laser
    "wood-relief": dict(
        note="A lézeres oldal fő formája: 3 mm rétegelt lemez, önhordó, "
             "kulcslyukkal a falra. Itt a vágásbiztonsági riport ér a legtöbbet "
             "(wiki/pitfalls/2026-08-09-overlapping-side-buckets).",
        prompt=("Carved wooden relief feel: broad ribbons and solid masses, "
                "nothing thinner than a finger. Ornament may reach the border."),
        levels=6,
        trace=["--solid-back"],
        render=["hero", "catteal", "--frame", "--accent", "--grain"],
    ),
    "wood-terrain": dict(
        note="Valódi domborzati adatból (00b_terrain.py) - nem képmodellel. "
             "wiki/findings/geographic-motifs.",
        prompt=None,                    # DEM-driven, no image model
        levels=7,
        trace=["--solid-back"],
        render=["hero", "terrain", "--grain"],
    ),
    # ---------------------------------------------------------------- accent
    "splatter-pop": dict(
        note="Foltszínes, lebegő motívum üres mezőn - a legerősebb thumbnail, "
             "de a legkevésbé kézműves hatás.",
        prompt=("The head floats alone in a large EMPTY field with no border and "
                "no ornament. Every level is an organic paint-splatter blob with "
                "soft drips. Few, LARGE, simple shapes."),
        levels=8,
        trace=["--no-keyhole", "--min-part", "120"],
        render=["lifestyle", "splatter", "--frame", "--paper", "--white-top"],
    ),
}


def describe():
    w = max(len(k) for k in STYLES)
    for k, v in STYLES.items():
        print(f"{k:<{w}}  {v['levels']} szint  render={' '.join(v['render'][:2])}")
        print(f"{'':<{w}}  {v['note']}")


if __name__ == "__main__":
    describe()
