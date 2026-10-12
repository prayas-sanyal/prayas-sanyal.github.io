import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets/data/snapshots"
OUT = ROOT / "assets/data/snapshot-thumbs"
WIDTHS = (640, 1280, 1920)

def url(path):
    return "/" + path.relative_to(ROOT).as_posix()

OUT.mkdir(exist_ok=True)
data = {}
for src in sorted(SRC.iterdir()):
    with Image.open(src) as im:
        icc = im.info.get("icc_profile")
        im = ImageOps.exif_transpose(im)
        srcset = []
        for w in sorted({min(w, im.width) for w in WIDTHS}):
            out = OUT / f"{src.name}-{w}.webp"
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, quality=90, method=6, icc_profile=icc)
            srcset.append({"url": url(out), "w": w})
        data[url(src)] = {"width": im.width, "height": im.height, "srcset": srcset}

(ROOT / "_data/snapshot_thumbs.json").write_text(json.dumps(data, indent=2))
