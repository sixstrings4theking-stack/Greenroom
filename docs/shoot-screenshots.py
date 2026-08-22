"""ChartBench user-guide screenshot shoot — drives headless Chrome through
every documented state and saves PNGs into docs/guide-assets/.

Two kinds of image:
  * full frames ("NN-name.png") — the whole 1720x1100 window, so toolbars
    never wrap and nothing looks squished;
  * close-ups ("cu-name.png") — one element (or a union of elements) cropped
    out of a device-pixel-ratio-2 capture with a little padding, for the
    guide's two-column callouts where a control is shown large.
Run with the local server up:  python -m http.server 8934  (repo root)."""
import os, io, time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

OUT = r"C:\Users\Matt\Documents\WorshipTools\docs\guide-assets"
os.makedirs(OUT, exist_ok=True)
URL = "http://localhost:8934/chart-builder/index.html"
DPR = 2

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1720,1100")
opts.add_argument(f"--force-device-scale-factor={DPR}")
opts.add_argument("--hide-scrollbars")
opts.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(options=opts)
driver.set_window_size(1720, 1100)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'window.confirm = () => true;'})

def js(code):
    return driver.execute_script(code)

def shot(name):
    time.sleep(0.35)
    png = driver.get_screenshot_as_png()
    Image.open(io.BytesIO(png)).save(os.path.join(OUT, name), optimize=True)
    print("shot:", name)

# Rect of one element, or the union of several (CSS pixels, viewport-relative).
RECT_JS = """
const sels = arguments[0];
const rects = [];
for(const sel of sels){ for(const e of document.querySelectorAll(sel)){ const r = e.getBoundingClientRect(); if(r.width && r.height) rects.push(r); } }
if(!rects.length) return null;
const x = Math.min(...rects.map(r=>r.left)), y = Math.min(...rects.map(r=>r.top));
const x2 = Math.max(...rects.map(r=>r.right)), y2 = Math.max(...rects.map(r=>r.bottom));
return {x, y, w: x2-x, h: y2-y};
"""
def crop(name, selectors, pad=10, rect=None):
    time.sleep(0.3)
    r = rect or driver.execute_script(RECT_JS, selectors if isinstance(selectors, list) else [selectors])
    if not r:
        print("WARN: nothing to crop for", name, selectors); return
    img = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
    box = (max(0, int((r['x']-pad)*DPR)), max(0, int((r['y']-pad)*DPR)),
           min(img.width, int((r['x']+r['w']+pad)*DPR)), min(img.height, int((r['y']+r['h']+pad)*DPR)))
    img.crop(box).save(os.path.join(OUT, name), optimize=True)
    print("crop:", name, box)

# Tight rect around the TEXT inside elements (a centered heading's box spans
# the whole page; its words don't) — for close-ups that should zoom in.
TEXT_RECT_JS = """
const sels = arguments[0];
const rects = [];
for(const sel of sels){ for(const e of document.querySelectorAll(sel)){ const r = document.createRange(); r.selectNodeContents(e); for(const rr of r.getClientRects()){ if(rr.width && rr.height) rects.push(rr); } } }
if(!rects.length) return null;
const x = Math.min(...rects.map(r=>r.left)), y = Math.min(...rects.map(r=>r.top));
const x2 = Math.max(...rects.map(r=>r.right)), y2 = Math.max(...rects.map(r=>r.bottom));
return {x, y, w: x2-x, h: y2-y};
"""
def crop_text(name, selectors, pad=12):
    r = driver.execute_script(TEXT_RECT_JS, selectors if isinstance(selectors, list) else [selectors])
    crop(name, None, pad=pad, rect=r)

def wait_for(cond_js, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        if js("return !!(" + cond_js + ")"):
            return True
        time.sleep(0.2)
    raise RuntimeError("timeout waiting for: " + cond_js)

# ---- 1. first launch: demo seed + NN intro popup ----
driver.get(URL + "?v=guide1")
wait_for("document.querySelector('#songList') && document.querySelector('#songList').textContent.includes('Romans 11')", 20)
wait_for("document.querySelector('#nnIntroBackdrop')", 10)
shot("01-first-launch-intro.png")
js("document.getElementById('nnIntroDismiss').click()")
time.sleep(0.3)

# ---- seed two extra public-domain songs so the library looks real ----
driver.execute_async_script("""
const done = arguments[arguments.length-1];
(async () => {
  await DB.putSong({title:'Amazing Grace', artist:'John Newton', ccli:'', copyright:'', copyrightMode:'PD', churchCcli:'', key:'NN',
    preferredKeys:['G','A'], capo:'', notationStyle:'roman', titleAlign:'center', tags:['hymn','classic'], libraries:['Full Catalog'],
    content:'Verse 1:\\n[1]Amazing grace how [4]sweet the [1]sound\\nThat saved a [5]wretch like [1]me\\n[1]I once was lost but [4]now am [1]found\\nWas blind but [5]now I [1]see\\n\\nChorus:\\n[4]My chains are [1]gone, I\\'ve been set [5]free\\n\\nVerse 2:\\nThe Lord has promised good to me\\n\\nChorus:\\n',
    versions:[], createdAt:Date.now(), updatedAt:Date.now()});
  await DB.putSong({title:'How Great Thou Art', artist:'Stuart K. Hine', ccli:'', copyright:'', copyrightMode:'PD', churchCcli:'', key:'NN',
    preferredKeys:['C'], capo:'', notationStyle:'roman', titleAlign:'center', tags:['hymn'], libraries:['Full Catalog'],
    content:'Verse 1:\\n[1]O Lord my God, when [4]I in awesome [1]wonder\\nConsider [2m]all the worlds thy [5]hands have [1]made\\n\\nChorus:\\nThen sings my [4]soul, my [1]Savior God to [5]thee\\n',
    versions:[], createdAt:Date.now()-86400000, updatedAt:Date.now()-86400000});
  done();
})();
""")
driver.get(URL + "?v=guide2")
wait_for("document.querySelector('#songList') && document.querySelector('#songList').textContent.includes('Amazing Grace')", 15)
js("document.getElementById('nnIntroDismiss')?.click()")
time.sleep(0.3)
shot("02-fresh-app.png")
crop("cu-sidebar-head.png", ["#libraryFilters", "#sidebar .sb-head", "#keyFilters", "#tagFilters"], pad=8)
crop("cu-topbar.png", "#topbar", pad=6)
crop("cu-topbar-right.png", ["#btnLyricsOnly", "#btnSettings"], pad=8)
crop("cu-topbar-left.png", ["#btnNew", "#btnImportFolder"], pad=8)
crop("cu-save-saved.png", "#btnSave", pad=8)

# ---- 3. open Romans 11: canonical chart view ----
js("""
const rows = Array.from(document.querySelectorAll('#songList .song-item'));
rows.find(r => r.textContent.includes('Romans 11')).click();
""")
wait_for("document.getElementById('mTitle').value === 'Romans 11'", 10)
# The demo opens in its remembered Display Key (G); the canonical shots are
# the Nashville view, so switch to NN first.
js("const s = document.getElementById('mDisplayKey'); if(s.value !== 'NN'){ s.value = 'NN'; s.dispatchEvent(new Event('change', {bubbles:true})); }")
time.sleep(0.8)  # preview render
shot("03-chart-open.png")
crop("cu-meta-bar.png", "#metaBar", pad=6)
crop("cu-section-bar.png", "#structBarChart", pad=6)
crop("cu-display-key.png", "#structBarChart .right-controls", pad=8)
crop("cu-preview-head.png", "#previewPane .pane-head", pad=6)
crop("cu-editor-head.png", "#editorPane .pane-head", pad=6)
crop("cu-song-map.png", "#previewScroll .cs-title, #previewScroll .cs-artist, #previewScroll .cs-copyright, #previewScroll .cs-roadmap", pad=14)
crop("cu-preferred-key.png", ["#preferredKeyPicker", "#preferredKeyChips"], pad=8)
crop("cu-song-list.png", "#songList", pad=8)

# ---- 4. chord picker (edit an existing chord) ----
js("""
const ta = document.getElementById('editor');
const idx = ta.value.indexOf('[37]');
ta.focus(); ta.setSelectionRange(idx+1, idx+1);
ta.dispatchEvent(new MouseEvent('dblclick', {bubbles:true, clientX:420, clientY:300}));
""")
wait_for("!document.getElementById('chordPopup').classList.contains('hidden')")
shot("04-chord-picker.png")
crop("cu-chord-picker.png", "#chordPopup", pad=8)
js("document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape'}))")
time.sleep(0.3)
# the same picker in a letter key (C), inserting on a word with no chord yet
js("const s = document.getElementById('mDisplayKey'); s.value = 'C'; s.dispatchEvent(new Event('change', {bubbles:true}));")
time.sleep(0.5)
js("""
const ta = document.getElementById('editor');
const idx = ta.value.indexOf('unsearchable');
ta.focus(); ta.setSelectionRange(idx, idx + 12);
ta.dispatchEvent(new MouseEvent('dblclick', {bubbles:true, clientX:420, clientY:330}));
""")
wait_for("!document.getElementById('chordPopup').classList.contains('hidden')")
crop("cu-chord-picker-c.png", "#chordPopup", pad=8)
js("document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape'}))")
time.sleep(0.2)
js("const s = document.getElementById('mDisplayKey'); s.value = 'NN'; s.dispatchEvent(new Event('change', {bubbles:true}));")
time.sleep(0.5)

# ---- 5. note annotation popup (right-click) ----
js("""
const ta = document.getElementById('editor');
const idx = ta.value.indexOf('counselor');
ta.focus(); ta.setSelectionRange(idx, idx);
ta.dispatchEvent(new MouseEvent('contextmenu', {bubbles:true, clientX:500, clientY:330}));
""")
wait_for("!document.getElementById('notePopup').classList.contains('hidden')")
js("document.getElementById('npInput').value = 'Repeat 2x'")
shot("05-note-popup.png")
crop("cu-note-popup.png", "#notePopup", pad=8)
js("document.body.dispatchEvent(new MouseEvent('mousedown', {bubbles:true}))")
time.sleep(0.3)

# ---- 5b. Key Change popup ----
js("document.getElementById('btnKeyChange')?.click()")
time.sleep(0.4)
if js("return !!document.querySelector('#keyChangePopup') && !document.querySelector('#keyChangePopup').classList.contains('hidden')"):
    crop("cu-key-change.png", "#keyChangePopup", pad=8)
    js("document.querySelector('#keyChangePopup #kcCancel')?.click()")
    time.sleep(0.2)

# ---- 6. Display Key G + Capo 2 (letter view, Unsaved state) ----
js("""
const sel = document.getElementById('mDisplayKey');
sel.value = 'G'; sel.dispatchEvent(new Event('change', {bubbles:true}));
""")
time.sleep(0.5)
js("""
const capo = document.getElementById('mCapo');
capo.value = '2'; capo.dispatchEvent(new Event('change', {bubbles:true}));
""")
time.sleep(0.8)
shot("06-letters-capo.png")
crop("cu-save-unsaved.png", "#btnSave", pad=8)
crop("cu-display-key-g.png", "#structBarChart .right-controls", pad=8)
crop("cu-capo-chart.png", "#previewScroll .cs-title, #previewScroll .cs-roadmap, #previewScroll .cs-meta", pad=14)
# restore: back to NN, no capo (leave dirty flag; harmless in headless)
js("""
const capo = document.getElementById('mCapo'); capo.value=''; capo.dispatchEvent(new Event('change', {bubbles:true}));
const sel = document.getElementById('mDisplayKey'); sel.value='NN'; sel.dispatchEvent(new Event('change', {bubbles:true}));
""")
time.sleep(0.5)

# ---- 7. CC license picker ----
js("document.querySelector('#copyrightModeControls [data-mode=\"CC\"]').click()")
time.sleep(0.4)
shot("07-cc-picker.png")
crop("cu-cc-picker.png", ["#copyrightModeControls", "#ccInlineControls"], pad=8)
crop_text("cu-cc-chart-line.png", ["#previewScroll .cs-title", "#previewScroll .cs-artist", "#previewScroll .cs-copyright"], pad=16)
js("document.querySelector('#copyrightModeControls [data-mode=\"\\u00a9\"]')?.click()")
time.sleep(0.3)

# ---- 8. Export Chart picker ----
js("document.getElementById('btnExport').click()")
wait_for("document.querySelector('.lxp-backdrop')")
shot("08-export-picker.png")
crop("cu-export-picker.png", ".lxp-modal", pad=8)
js("document.querySelector('.lxp-backdrop #lxpClose').click()")
time.sleep(0.3)

# ---- 9-10. Lyrics mode: collective grid, then individual last slide ----
js("document.getElementById('btnLyricsOnly').click()")
time.sleep(0.8)
js("""
const btn = document.querySelector('#slideViewModeControl [data-mode="collective"]');
if(btn && !btn.classList.contains('active')) btn.click();
""")
time.sleep(0.5)
shot("09-lyrics-collective.png")
crop("cu-lyrics-ribbon.png", "#structBarLyrics", pad=6)
crop("cu-lyrics-editor-head.png", "#editorPane .pane-head", pad=6)
js("document.querySelector('#slideViewModeControl [data-mode=\"individual\"]').click()")
time.sleep(0.4)
js("for(let i=0;i<10;i++){ const b=document.getElementById('slideNextBtn'); if(!b.disabled) b.click(); }")
time.sleep(0.4)
shot("10-lyrics-individual.png")
crop("cu-slide-footnote.png", "#previewScroll .slide-box", pad=10)

# ---- 11. Lyrics export picker ----
js("document.getElementById('btnExport').click()")
wait_for("document.querySelector('.lxp-backdrop')")
shot("11-lyrics-export-picker.png")
crop("cu-lyrics-export-picker.png", ".lxp-modal", pad=8)
js("document.querySelector('.lxp-backdrop #lxpClose').click()")
time.sleep(0.2)
js("document.getElementById('btnLyricsOnly').click()")  # exit lyrics mode
time.sleep(0.5)

# ---- 12. Set List Builder ----
js("localStorage.removeItem('wcb_setlist_v1'); localStorage.removeItem('wcb_setlist_name_v1'); document.getElementById('btnSetList').click()")
wait_for("document.querySelector('.slb-backdrop')")
js("""
const rows = Array.from(document.querySelectorAll('.slb-row'));
const romans = rows.find(r => r.textContent.includes('Romans 11'));
const grace = rows.find(r => r.textContent.includes('Amazing Grace'));
romans.querySelector('.slb-add').click();
grace.querySelector('.slb-add').click();
romans.querySelector('.slb-add').click();
""")
time.sleep(0.4)
js("""
const keys = document.querySelectorAll('.slb-key');
keys[0].value = 'G'; keys[0].dispatchEvent(new Event('change'));
const capos = document.querySelectorAll('.slb-capo');
capos[1].value = '3'; capos[1].dispatchEvent(new Event('change'));
const name = document.querySelector('#slbSetName'); name.value = 'Sunday, Aug 24'; name.dispatchEvent(new Event('input'));
""")
time.sleep(0.3)
shot("12-setlist.png")
crop("cu-slb-set-bar.png", ".slb-set-bar", pad=8)
crop("cu-slb-entry.png", ".slb-entry", pad=8)
crop("cu-slb-library.png", ".slb-library", pad=6)
crop("cu-slb-actions.png", ".slb-head .slb-actions", pad=8)
# save the set and open the saved-sets panel
js("document.querySelector('#slbSaveSet').click()")
time.sleep(0.5)
driver.execute_async_script("""
const done = arguments[arguments.length-1];
(async () => {
  const saved = await DB.getPref('saved_setlists_v1', null) || [];
  saved.push({id:'11111111-2222-4333-8444-555555555555', name:'Christmas Eve', createdAt: Date.now()-86400000*9, updatedAt: Date.now()-86400000*9, entries: saved[0] ? saved[0].entries.slice(0,2) : []});
  saved.push({id:'22222222-2222-4333-8444-555555555555', name:'Youth Night', createdAt: Date.now()-86400000*3, updatedAt: Date.now()-86400000*3, entries: saved[0] ? saved[0].entries.slice(0,1) : []});
  await DB.setPref('saved_setlists_v1', saved);
  done();
})();
""")
js("document.querySelector('#slbSavedToggle').click()")
time.sleep(0.5)
shot("16-setlist-saved.png")
crop("cu-slb-saved-panel.png", [".slb-set-bar", "#slbSavedPanel"], pad=8)
js("document.querySelector('.slb-backdrop #slbClose').click()")
time.sleep(0.3)

# ---- 13. Circle of Fifths (opens its own window) ----
main_handle = driver.current_window_handle
js("document.getElementById('btnCircle').click()")
time.sleep(1.2)
handles = driver.window_handles
circle = [h for h in handles if h != main_handle]
if circle:
    driver.switch_to.window(circle[0])
    # Tall enough that the whole wheel is inside the viewport, then trim the
    # spare background below it so the figure is just the window's content.
    driver.set_window_size(780, 1100)
    time.sleep(1.0)
    img = Image.open(io.BytesIO(driver.get_screenshot_as_png())).convert('RGB')
    bg = img.getpixel((4, img.height - 4))
    bottom = img.height
    while bottom > 0 and all(abs(a - b) < 6 for a, b in zip(img.getpixel((img.width // 2, bottom - 1)), bg)) and \
          all(abs(a - b) < 6 for a, b in zip(img.getpixel((img.width // 4, bottom - 1)), bg)):
        bottom -= 1
    img.crop((0, 0, img.width, min(img.height, bottom + 24 * DPR))).save(os.path.join(OUT, "13-circle.png"), optimize=True)
    print("shot: 13-circle.png (trimmed to", bottom, ")")
    driver.close()
    driver.switch_to.window(main_handle)
else:
    print("WARN: circle window did not open")
time.sleep(0.3)

# ---- 14. Settings drawer (+ section close-ups by heading) ----
js("document.getElementById('btnSettings').click()")
time.sleep(0.8)
shot("14-settings.png")
def drawer_section(name, heading, pad=8):
    r = driver.execute_script("""
const heading = arguments[0];
const hs = [...document.querySelectorAll('.drawer-body h4')];
const i = hs.findIndex(h => h.textContent.trim().startsWith(heading));
if(i < 0) return null;
const top = hs[i].getBoundingClientRect();
const body = document.querySelector('.drawer-body').getBoundingClientRect();
const bottom = (i+1 < hs.length) ? hs[i+1].getBoundingClientRect().top - 8 : body.bottom - 8;
return {x: body.left + 6, y: top.top, w: body.width - 12, h: bottom - top.top};
""", heading)
    if r and r['h'] > 20: crop(name, None, pad=pad, rect=r)
    else: print("WARN: drawer section not found", heading)
# scroll the drawer so the lower sections are in view when cropped
drawer_section("cu-settings-display.png", "Display Preferences")
js("document.querySelector('.drawer-body').scrollTop = 10000")
time.sleep(0.4)
drawer_section("cu-settings-data.png", "Data")
drawer_section("cu-settings-folder.png", "Library Folder")
drawer_section("cu-settings-feedback.png", "Feedback")
js("document.querySelector('.drawer-backdrop #drawerClose').click()")
time.sleep(0.3)

# ---- 15. Download Software popup ----
js("document.getElementById('btnDownloadApp').click()")
wait_for("document.querySelector('.lxp-backdrop')")
shot("15-download.png")
js("document.querySelector('.lxp-backdrop #dlClose').click()")

# ---- 17. Library folder reconnect strip (simulated) + backup nudge ----
js("""
document.getElementById('mirrorNudge').classList.remove('hidden');
document.getElementById('mirrorNudgeText').innerHTML = 'Library folder <b>ChartBench Library</b> needs reconnecting this session.';
""")
time.sleep(0.3)
crop("cu-mirror-nudge.png", "#mirrorNudge", pad=8)
js("document.getElementById('mirrorNudge').classList.add('hidden')")

driver.quit()
print("DONE — all shots saved to", OUT)
