# Secure Supplies — Open Hardware Index

**Live: https://securesupplies.github.io/hardware/**

Every Stanley A. Meyer water fuel cell, VIC, gas management, gas processor,
steam resonator and Hydrogen Hot Rod ECU board published by Secure Supplies
Group / Donatelli LLC. Searchable, filterable by category, and every card links
straight to the PCBWay project page where the bare board can be ordered.

## How it stays current — automatically

`index.html` reads the PCBWay member library **live in the visitor's browser**
via PCBWay's public JSONP listing endpoint. There is no stored copy of the
catalogue and no build step. Publish a new board on PCBWay and it appears on
this page the moment someone loads it. View counts are always today's numbers.

One page load = 18 JSONP requests (12 boards each), roughly one second.

## Files

| Path | What |
|---|---|
| `index.html` | The whole site. Self-contained, no dependencies, no build |
| `build/build_index.py` | Optional fallback — writes a static `data/catalogue.json` snapshot if PCBWay's live endpoint is ever withdrawn |

## If PCBWay changes the endpoint

The two things to edit at the top of the `<script>` block in `index.html`:

```
const BMBNO='E9AF6EAA-8A83-4F';
const API='https://member.pcbway.com/Project/GetProject_ShareProjectList?bmbno='+BMBNO+'&type=';
```

Categories are keyword rules in `CATRULES` in the same block — add a board type
by adding a regex there.

## Commercial role

PCBWay sells the bare board at their price. This index makes all 200+ findable
in one place and routes buyers on to:

- **Patreon shop** — manuals, kits, assembled hardware
- **Patreon tiers** — schematics, build support, the full library

Secure Supplies Group / Donatelli LLC · securesupplies.us · 24/7 Desk (520) 435-1881
