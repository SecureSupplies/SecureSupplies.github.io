#!/usr/bin/env python3
"""Rebuild data/catalogue.json from the live PCBWay member library."""
import json, re, sys, time, urllib.request, pathlib, datetime

BMBNO = "E9AF6EAA-8A83-4F"
API = ("https://member.pcbway.com/Project/GetProject_ShareProjectList"
       "?callback=cb&bmbno={b}&type=&page={p}")
UA = {"User-Agent": "Mozilla/5.0 (compatible; SecureSuppliesIndexBot/1.0)"}
ROOT = pathlib.Path(__file__).resolve().parent.parent

CATS = [
 ('ECU / Speeduino / Hydrogen Hot Rod', r'speeduino|speedunio|hyduino|core8|teensy|can hub|canpico|egt|map/baro|miata|honda|m50|m52|m60|drop bear|ignitor|stim|\becu\b|ardu-stim|molex|dbw|auxiliary outputs'),
 ('Steam Resonator & EPG', r'steam resonator|\bepg\b'),
 ('Gas Processor & Ionisation', r'gas processor|led gas processor|led array|optical lens|intake|exhaust|egr|laser|spark pug|spark plug|ozonat'),
 ('Water Fuel Cell & Cell Hardware', r'wfc|water fuel cell|cell tubes|tube cell|anode|cathode|spacer|top cap|lower cap|tube holder|resonant cavity|pressure|flash back|fuel line|single cell|6 cell|9 cell|11 cell|cell holder|water body|nano bubble water fuel cell|9 tube'),
 ('VIC, Bobbins, Cores & Chokes', r'\bvic\b|bobbin|choke|u-core|u core|e core|ballast|balast|balun|impedance|bifilar|transformer'),
 ('Voltrolysis Power & Switch Drivers', r'8xa|9xa|9xb|9xd|9xam|\bscr\b|half bridge|h bridge|switch driver|switching circuit|\beec\b|electron extract|voltrolysis|alternator|power supply|home heater|puharich'),
 ('GMS Control Cards', r'\bgms\b|gate tuning|frequency generator|digital control|accelerator|taco|distributor|feedback|safety|voltage card|analog|analogue|pulse frequency|trigger board|auto start|autofill|les banki|injector card|matrix|db 37|k00|k11|k2 |k3 |k7 |k8|k20|solenoid|warning board|sequential gate|variable gate'),
 ('Energy Harvesting & Experimental', r'rectenna|rf power|energy harvesting|\btpu\b|tesla|battery charger|atu-100|magnetic propulsion|dynamysthesis'),
]
def category(t):
    tl = t.lower()
    for name, pat in CATS:
        if re.search(pat, tl):
            return name
    return 'Other Boards & Parts'

def fetch(page, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(API.format(b=BMBNO, p=page), headers=UA)
            raw = urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'replace')
            return json.loads(raw[raw.index('(') + 1: raw.rindex(')')])
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(3 * (i + 1))

def main():
    first = fetch(1)
    total = first["TotalCount"]
    pages = (total + 11) // 12
    items = list(first["DataList"])
    for p in range(2, pages + 1):
        items += fetch(p)["DataList"]
        time.sleep(0.6)
    seen, rows = set(), []
    for it in items:
        pid = it["Id"]
        if pid in seen:
            continue
        seen.add(pid)
        img = (it.get("CoverPic") or it.get("Pics") or "").split("?")[0]
        rows.append({
            "id": pid,
            "title": (it.get("Title") or "").strip(),
            "url": "https://www.pcbway.com/project/shareproject/%s.html" % it["FileName"],
            "image": img,
            "views": it.get("Views", 0),
            "date": (it.get("AddDate") or "")[:10],
            "category": category(it.get("Title") or ""),
        })
    rows.sort(key=lambda r: -r["views"])
    out = {
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "count": len(rows),
        "total_views": sum(r["views"] for r in rows),
        "source": "https://www.pcbway.com/project/member/?bmbno=" + BMBNO,
        "boards": rows,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "catalogue.json").write_text(json.dumps(out, separators=(",",":")), encoding="utf-8")
    print("wrote %d boards, %d total views" % (len(rows), out["total_views"]))
    if len(rows) < 100:
        print("REFUSING: suspiciously few boards", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
