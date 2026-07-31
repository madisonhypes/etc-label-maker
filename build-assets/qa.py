import sys, pathlib
from playwright.sync_api import sync_playwright

APP = pathlib.Path(r"C:\Users\micro\Documents\11PROGRAM-FILES\ETC Label Maker\app.html").as_uri()
OUT = pathlib.Path(r"C:\Users\micro\AppData\Local\Temp\claude\C--Users-micro-Documents-claudeCode\6049f3c8-e1aa-4739-811b-8bd701f60226\scratchpad")

LARGE = [("Indica","Cookie Glue","27"),("Sativa","Pineapple Punch","27"),("Hybrid","White Widow","27")]
SMALL = [("Sativa","Blue Dream","74"),("Sativa","Strawberry Mango","78"),("Sativa","Pineapple Express","76"),
         ("Hybrid","Lunar Roar","70"),("Hybrid","Island Dream","78"),("Hybrid","Jet Fuel OG","78"),
         ("Indica","Peach Passion Kush","77"),("Indica","Grandaddy Purp","85"),("Indica","Cherry Diesel","80")]
SMALL = SMALL*3  # fill all 9 rows (27 labels) to check spacing

def fill(page, records, size):
    page.select_option("#labelSize", size)
    # each row is one label now; add rows until there are enough
    while page.locator("#rows tr").count() < len(records):
        page.click("#addRow")
    for i,(t,n,c) in enumerate(records):
        rows = page.locator("#rows tr")
        r = rows.nth(i)
        r.locator("select.typesel").select_option(t)
        r.locator("td.col-name input").fill(n)
        r.locator("td.col-thc input").fill(c)
    page.wait_for_timeout(400)

with sync_playwright() as p:
    b = p.chromium.launch()
    for size, recs in [("large",LARGE),("small",SMALL)]:
        page = b.new_page(viewport={"width":1280,"height":900}, device_scale_factor=2)
        page.goto(APP)
        page.wait_for_timeout(300)
        fill(page, recs, size)
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT/f"ui_{size}.png"))
        page.pdf(path=str(OUT/f"sheet_{size}.pdf"), prefer_css_page_size=True, print_background=False)
        print("done", size)
        page.close()
    b.close()
print("QA complete")
