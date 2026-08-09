#!/usr/bin/env python3
"""Step 5 - a real looping product video, not a flip-book GIF.

A static hero cannot show depth, and a 24-frame GIF shows it badly: the motion
stutters and the file is bigger than the video. This renders a full sinusoidal
camera cycle so the last frame meets the first exactly, composites every frame
into the photographed interior, and encodes an H.264 loop.

  python 05_video.py --dir <iteration> --palette well --seconds 6 [--fps 24]

Needs: blender on PATH, ffmpeg on PATH, a backdrop in pipeline/backdrops/.
"""
import argparse, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REND = ROOT / "product" / "render_blender.py"
COMP = ROOT / "product" / "pipeline" / "04_composite.py"
PY = ROOT / ".venv" / "bin" / "python"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"HIBA: {' '.join(map(str, cmd))[:120]}\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--palette", default="well")
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--backdrop", default="warm-shelf")
    ap.add_argument("--flags", default="--frame --paper --recessed")
    ap.add_argument("--keep-frames", action="store_true",
                    help="tartsa meg a kockakat, hogy mas hatterre is menjen")
    ap.add_argument("--cx", type=float, default=0.44)
    ap.add_argument("--base", type=float, default=0.94)
    ap.add_argument("--height", type=float, default=0.88)
    a = ap.parse_args()

    d = pathlib.Path(a.dir)
    frames = int(round(a.seconds * a.fps))
    work = d / "video_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    print(f"[video] {frames} kocka ({a.seconds:g}s @ {a.fps}fps)")
    run(["blender", "-b", "-P", str(REND), "--", str(d / "layers"),
         str(work / "f.png"), "plate", a.palette, *a.flags.split(), "--orbit",
         str(frames)])

    bg = ROOT / "product" / "pipeline" / "backdrops" / f"{a.backdrop}.png"
    plates = sorted(work.glob("f_f*.png"))
    if not plates:
        sys.exit("nem keszult kocka")
    print(f"[video] {len(plates)} kocka kompozitalasa a fotora")
    for i, p in enumerate(plates):
        run([str(PY), str(COMP), "--bg", str(bg), "--art", str(p),
             "--out", str(work / f"c{i:04d}.png"), "--cx", str(a.cx),
             "--base", str(a.base), "--height", str(a.height),
             "--warm", "1.02", "--square"])

    out = d / "video.mp4"
    # yuv420p + even dimensions so every player accepts it; the loop is in the
    # camera path, so no palindrome trickery is needed
    run(["ffmpeg", "-y", "-framerate", str(a.fps), "-i", str(work / "c%04d.png"),
         "-vf", "scale=1080:-2:flags=lanczos", "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)])
    if not a.keep_frames:
        shutil.rmtree(work)
    mb = out.stat().st_size / 1e6
    print(f"[video] kesz: {out}  {mb:.1f} MB  {a.seconds:g}s loop")


if __name__ == "__main__":
    main()
