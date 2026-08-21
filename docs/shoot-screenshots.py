"""ChartBench user-guide screenshot shoot — drives headless Chrome through
every documented state and saves PNGs into docs/guide-assets/."""
import os, time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUT = r"C:\Users\Matt\Documents\WorshipTools\docs\guide-assets"
os.makedirs(OUT, exist_ok=True)
URL = "http://localhost:8934/chart-builder/index.html"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1720,1100")
opts.add_argument("--force-device-scale-factor=1.5")
opts.add_argument("--hide-scrollbars")
opts.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(options=opts)
driver.set_window_size(1720, 1100)

def js(code):
    return driver.execute_script(code)

def shot(name):
    time.sleep(0.35)
    driver.save_screenshot(os.path.join(OUT, name))
    print("shot:", name)

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
js("""
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
shot("02-fresh-app.png")

# ---- 3. open Romans 11: canonical chart view ----
js("""
const rows = Array.from(document.querySelectorAll('#songList .song-item'));
rows.find(r => r.textContent.includes('Romans 11')).click();
""")
wait_for("document.getElementById('mTitle').value === 'Romans 11'", 10)
time.sleep(0.8)  # preview render
shot("03-chart-open.png")

# ---- 4. chord picker (edit an existing chord) ----
js("""
const ta = document.getElementById('editor');
const idx = ta.value.indexOf('[37]');
ta.focus(); ta.setSelectionRange(idx+1, idx+1);
ta.dispatchEvent(new MouseEvent('dblclick', {bubbles:true, clientX:420, clientY:300}));
""")
wait_for("!document.getElementById('chordPopup').classList.contains('hidden')")
shot("04-chord-picker.png")
js("document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape'}))")
time.sleep(0.3)

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
js("document.body.dispatchEvent(new MouseEvent('mousedown', {bubbles:true}))")
time.sleep(0.3)

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
js("document.querySelector('#copyrightModeControls [data-mode=\"\\u00a9\"]')?.click()")
time.sleep(0.3)

# ---- 8. Export Chart picker ----
js("document.getElementById('btnExport').click()")
wait_for("document.querySelector('.lxp-backdrop')")
shot("08-export-picker.png")
js("document.querySelector('.lxp-backdrop #lxpClose').click()")
time.sleep(0.3)

# ---- 9-10. Lyrics mode: collective grid, then individual last slide ----
js("document.getElementById('btnLyricsOnly').click()")
time.sleep(0.8)
js("""
// force collective view for the grid shot
const btn = document.querySelector('#slideViewModeControl [data-mode="collective"]');
if(btn && !btn.classList.contains('active')) btn.click();
""")
time.sleep(0.5)
shot("09-lyrics-collective.png")
js("document.querySelector('#slideViewModeControl [data-mode=\"individual\"]').click()")
time.sleep(0.4)
js("for(let i=0;i<10;i++){ const b=document.getElementById('slideNextBtn'); if(!b.disabled) b.click(); }")
time.sleep(0.4)
shot("10-lyrics-individual.png")

# ---- 11. Lyrics export picker ----
js("document.getElementById('btnExport').click()")
wait_for("document.querySelector('.lxp-backdrop')")
shot("11-lyrics-export-picker.png")
js("document.querySelector('.lxp-backdrop #lxpClose').click()")
time.sleep(0.2)
js("document.getElementById('btnLyricsOnly').click()")  # exit lyrics mode
time.sleep(0.5)

# ---- 12. Set List Builder ----
js("localStorage.removeItem('wcb_setlist_v1'); document.getElementById('btnSetList').click()")
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
""")
time.sleep(0.3)
# re-render to show the selections
js("""
const backdrop = document.querySelector('.slb-backdrop');
""")
shot("12-setlist.png")
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
    driver.set_window_size(760, 800)
    time.sleep(0.8)
    shot("13-circle.png")
    driver.close()
    driver.switch_to.window(main_handle)
else:
    print("WARN: circle window did not open")
time.sleep(0.3)

# ---- 14. Settings drawer ----
js("document.getElementById('btnSettings').click()")
time.sleep(0.6)
shot("14-settings.png")
js("document.querySelector('.drawer-backdrop #drawerClose').click()")
time.sleep(0.3)

# ---- 15. Download Software popup ----
js("document.getElementById('btnDownloadApp').click()")
wait_for("document.querySelector('.lxp-backdrop')")
shot("15-download.png")
js("document.querySelector('.lxp-backdrop #dlClose').click()")

driver.quit()
print("DONE — all shots saved to", OUT)
