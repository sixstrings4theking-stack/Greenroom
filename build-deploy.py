"""Builds the website upload bundle for thechartbench.com.

Output: C:\\Users\\Matt\\Documents\\ChartBench-deploy\\  (wiped and rebuilt)
        C:\\Users\\Matt\\Documents\\ChartBench-deploy.zip (same content, zipped)

Layout (upload the CONTENTS of the folder into the web root, e.g. /public):
    index.html              ChartBench itself (chart-builder/index.html)
    favicon.ico             the CB monogram
    sample-data/            demo songs seeded on a visitor's first launch
        manifest.json       the list of demo files below — keep in sync
        *.json              one ChartBench JSON per demo song
    docs/                   the User Guide the app's Guide button opens
        user-guide.html, ChartBench-User-Guide.pdf, guide-assets/
    greenroom/index.html    the Greenroom parent prototype, pointed at ../index.html

Demo songs come from chart-builder/sample-data/ in the repo (the source of
truth, so GitHub Pages and the website seed the same songs). Drop finished
demo files there, update manifest.json, re-run this script."""
import os, re, shutil, zipfile, json

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = r"C:\Users\Matt\Documents\ChartBench-deploy"
ZIP = OUT + ".zip"

def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

# 1. the app, at the root
copy(os.path.join(REPO, "chart-builder", "index.html"), os.path.join(OUT, "index.html"))
app = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
assert "const WEB_HOSTED_COPY = true;" in app, "index.html must be the hosted build (WEB_HOSTED_COPY = true)"

# 2. favicon
copy(os.path.join(REPO, "docs", "brand", "favicon.ico"), os.path.join(OUT, "favicon.ico"))

# 3. demo songs (+ manifest) from the repo's sample-data
sd_src = os.path.join(REPO, "chart-builder", "sample-data")
manifest = json.load(open(os.path.join(sd_src, "manifest.json"), encoding="utf-8"))
for name in manifest:
    path = os.path.join(sd_src, name)
    assert os.path.isfile(path), f"manifest lists {name} but it isn't in {sd_src}"
    copy(path, os.path.join(OUT, "sample-data", name))
copy(os.path.join(sd_src, "manifest.json"), os.path.join(OUT, "sample-data", "manifest.json"))

# 4. the user guide
docs_src = os.path.join(REPO, "docs")
copy(os.path.join(docs_src, "user-guide.html"), os.path.join(OUT, "docs", "user-guide.html"))
copy(os.path.join(docs_src, "ChartBench-User-Guide.pdf"), os.path.join(OUT, "docs", "ChartBench-User-Guide.pdf"))
assets_src = os.path.join(docs_src, "guide-assets")
for f in os.listdir(assets_src):
    if f.lower().endswith(".png"):
        copy(os.path.join(assets_src, f), os.path.join(OUT, "docs", "guide-assets", f))

# 5. Greenroom parent, re-pointed at the root app
gr = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
gr, n = re.subn(r"(['\"`])chart-builder/index\.html", r"\1../index.html", gr)
assert n >= 2, f"expected to rewrite the chart-builder references in the Greenroom index, rewrote {n}"
os.makedirs(os.path.join(OUT, "greenroom"), exist_ok=True)
open(os.path.join(OUT, "greenroom", "index.html"), "w", encoding="utf-8", newline="\n").write(gr)

# 6. upload notes
open(os.path.join(OUT, "UPLOAD-README.txt"), "w", encoding="utf-8").write(f"""ChartBench website bundle
=========================

Upload the CONTENTS of this folder (not the folder itself) into the site's
web root on IONOS (the /public directory the domain points at), so that
index.html is at https://thechartbench.com/index.html.

  index.html               the app
  favicon.ico
  sample-data/             demo songs seeded on a visitor's first launch
    manifest.json          must list every demo file by exact filename
    {chr(10).join('    ' + n + (' ' * max(1, 22 - len(n))) + 'demo song' for n in manifest)}
  docs/                    the User Guide (the app's Guide button opens docs/user-guide.html)
  greenroom/index.html     the Greenroom prototype (optional)

To replace a demo song: drop the finished ChartBench JSON into sample-data/
under the SAME filename listed in manifest.json (or add the file and the
name to the manifest). Visitors only get demo songs on their very first
launch, so changes here reach new visitors, not returning ones.

Rebuilt from the WorshipTools repo by build-deploy.py.
""")

# 7. zip (contents at the top level of the archive)
if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(OUT):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, OUT))

total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f"bundle: {OUT}  ({total/1e6:.1f} MB)")
print(f"zip:    {ZIP}  ({os.path.getsize(ZIP)/1e6:.1f} MB)")
print("demo songs:", manifest)
