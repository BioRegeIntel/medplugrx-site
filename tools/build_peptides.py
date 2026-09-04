#!/usr/bin/env python3
"""Generates the Peptides division pages under /peptides/ from shared chrome.
Run from the repo root:  python3 tools/build_peptides.py
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "peptides")
os.makedirs(OUT, exist_ok=True)

BASE = "https://www.medplugrx.com/peptides/"

MARK = '''<span class="plugmark"><svg width="{s}" height="{s}" viewBox="-92 -92 184 184" filter="url(#glo)">
<g fill="none" stroke="url(#au)" stroke-width="4.6" stroke-linecap="round">
<g class="lyr l1"><path d="M0,-70 C34,-14 34,14 0,44 C-34,14 -34,-14 0,-70 Z"/></g>
<g class="lyr l2"><g transform="rotate(120)"><path d="M0,-70 C34,-14 34,14 0,44 C-34,14 -34,-14 0,-70 Z" mask="url(#wa)"/></g></g>
<g class="lyr l3"><g transform="rotate(240)"><path d="M0,-70 C34,-14 34,14 0,44 C-34,14 -34,-14 0,-70 Z" mask="url(#wb)"/></g></g></g>
<circle class="lring" r="76" fill="none" stroke="url(#au)" stroke-width="1.1"/>
<circle class="lcore" r="5" fill="url(#au)"/></svg></span>'''

DEFS = '''<div id="cursor"></div><div id="prog"></div>
<svg id="motif" viewBox="-92 -92 184 184"><use href="#weave"/></svg>
<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="au" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#F5E9C4"/><stop offset=".55" stop-color="#C9A860"/><stop offset="1" stop-color="#7A5A21"/></linearGradient>
<mask id="wa"><rect x="-200" y="-200" width="400" height="400" fill="#fff"/><circle cx="-30" cy="17" r="10" fill="#000"/></mask>
<mask id="wb"><rect x="-200" y="-200" width="400" height="400" fill="#fff"/><circle cx="30" cy="17" r="10" fill="#000"/><circle cx="0" cy="-34" r="10" fill="#000"/></mask>
<filter id="glo" x="-60%" y="-60%" width="220%" height="220%">
<feGaussianBlur stdDeviation="3.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<g id="weave">
<g fill="none" stroke="url(#au)" stroke-width="4.6" stroke-linecap="round">
<path d="M0,-70 C34,-14 34,14 0,44 C-34,14 -34,-14 0,-70 Z"/>
<path d="M0,-70 C34,-14 34,14 0,44 C-34,14 -34,-14 0,-70 Z" transform="rotate(120)" mask="url(#wa)"/>
<path d="M0,-70 C34,-14 34,14 0,44 C-34,14 -34,-14 0,-70 Z" transform="rotate(240)" mask="url(#wb)"/></g>
<circle r="76" fill="none" stroke="url(#au)" stroke-width="1.1" opacity=".45"/>
<circle r="5" fill="url(#au)"/></g>
</defs></svg>'''

MENU = [("the-pen.html", "The Pen"), ("portfolio.html", "Portfolio"),
        ("manufacturing.html", "Manufacturing"), ("packaging.html", "Packaging"), ("facts.html", "Facts")]

SPLIT_FULL = '<section class="divsplit" aria-label="Choose a division"><a class="dp reg" href="../index.html"><img src="../a/dna-helix.jpg" alt="" aria-hidden="true"><span class="tx"><span class="dk">Division 01</span><span class="dl">Regenerative Medicine</span><span class="dd">Umbilical-derived exosome and cellular preparations, counted and characterized per lot, supplied to a closed physician register.</span><span class="go">Enter Regenerative Medicine</span></span></a><a class="dp pep on" href="index.html"><img src="../a/pen-hero.jpg" alt="" aria-hidden="true"><span class="tx"><span class="dk">Division 02</span><span class="dl">Peptides</span><span class="dd">Seventy-three pharmaceutical-manufactured peptides, pre-filled in a certified injector pen. No vial, no reconstitution.</span><span class="go">Enter Peptides</span></span></a></section>\n'
SPLIT_SHORT = '<section class="divsplit short" aria-label="Choose a division"><a class="dp reg" href="../index.html"><img src="../a/dna-helix.jpg" alt="" aria-hidden="true"><span class="tx"><span class="dk">Division 01</span><span class="dl">Regenerative Medicine</span><span class="dd">Umbilical-derived exosome and cellular preparations, counted and characterized per lot, supplied to a closed physician register.</span><span class="go">Enter Regenerative Medicine</span></span></a><a class="dp pep on" href="index.html"><img src="../a/pen-hero.jpg" alt="" aria-hidden="true"><span class="tx"><span class="dk">Division 02</span><span class="dl">Peptides</span><span class="dd">Seventy-three pharmaceutical-manufactured peptides, pre-filled in a certified injector pen. No vial, no reconstitution.</span><span class="go">Enter Peptides</span></span></a></section>\n'


GHOSTS = ["Peptides &#183; Pen &#183; Portfolio &#183; Fill &#183; ", "0.01 mL per click &#183; Seventy-three &#183; Zero failures &#183; ", "Measured, not claimed &#183; Licensed manufacture &#183; ", "Metal &#183; Molded &#183; Certified &#183; Pre-filled &#183; "]
_gi = [0]
def lux(extra="", kind="bfield", photo=None):
    """Opens a textured section: live gold field + drifting ghost type behind the copy."""
    _gi[0] += 1
    words = GHOSTS[_gi[0] % len(GHOSTS)] * 3
    cv = '<canvas class="bfield dense"></canvas>' if kind == "bfield" else '<canvas class="gflow"></canvas>'
    img = f'<img class="tex" src="../a/{photo}" alt="" aria-hidden="true">' if photo else ''
    rev = ' rev' if _gi[0] % 2 else ''
    cls = "lux photo" if photo else "lux"
    style = ' style="%s"' % extra if extra else ""
    return '<section class="%s"%s>%s%s<div class="ghost%s" aria-hidden="true"><span>%s</span></div>' % (cls, style, img, cv, rev, words)

def nav(active):
    items = "".join(
        f'<li><a class="lk{" act" if f == active else ""}" href="{f}">{t}</a></li>' for f, t in MENU)
    return f'''<nav id="nav"><div class="wrap">
<a class="brand" href="index.html"><svg width="34" height="34" viewBox="-92 -92 184 184"><use href="#weave"/></svg>
<span class="nm serif">MED PLUG<em>RX</em></span></a>
<ul id="menu">{items}</ul>
<a href="../access.html" class="btn">Physician Access</a>
<button id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
</div></nav>'''

FOOTER = '''<footer><div class="wrap"><div class="cols">
<div><a class="brand" href="index.html" style="margin-bottom:20px">
<svg width="44" height="44" viewBox="-92 -92 184 184"><use href="#weave"/></svg>
<span class="serif" style="font-size:13px;letter-spacing:.30em">MED PLUG RX</span></a>
<p style="max-width:330px;line-height:1.85">Pharmaceutical-manufactured peptides, delivered in a certified injector pen. Supplied direct to licensed physicians, with the documentation to match.</p></div>
<div><h4>Peptides</h4><a href="the-pen.html">The Pen</a><a href="portfolio.html">Portfolio</a><a href="manufacturing.html">Manufacturing</a><a href="packaging.html">Packaging</a><a href="facts.html">Facts</a></div>
<div><h4>Documentation</h4><a href="../coamedplug">Peptide COA Archive</a><a href="../coapens">Pen COA Archive</a><a href="../coajungmoney">Jung Money COA Archive</a><a href="../standards.html">Standards</a></div>
<div><h4>Access</h4><a href="../access.html">Physician Account</a><a href="../refer.html">Refer a Colleague</a><a href="../index.html">Regenerative Medicine</a><a href="../privacy.html">Privacy Notice</a><a href="../terms.html">Terms of Use</a></div>
<div><h4>Contact</h4>
<a href="mailto:info@medplugrx.com">info@medplugrx.com</a>
<span style="display:block;margin-top:10px;color:#A9A39A;font-size:13px;line-height:1.8">Houston, Texas<br>United States</span></div>
</div>
<div class="legal">&copy; 2026 Med Plug RX. All rights reserved.<br>
Distribution restricted to licensed physicians and qualified facilities. Compounding eligibility varies by substance and is confirmed against current FDA bulk drug substance lists at the point of order. The injector pen is manufactured under ISO 13485:2016 and certified under EU MDR 2017/745; a premarket notification has been submitted to the FDA and is under review. No clearance determination has been issued, and none is claimed or implied by this site.<br>
No statement on this site has been evaluated by the Food and Drug Administration. Clinical application, indication and patient selection remain the sole responsibility of the treating physician.</div>
</div></footer>
<script src="../a/app.js"></script></body></html>'''

def head(title, desc, path, og="pep-couple.jpg"):
    t, d = html.escape(title), html.escape(desc)
    url = BASE + ("" if path == "index.html" else path)
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}">
<link rel="stylesheet" href="../a/style.css"><link rel="stylesheet" href="../a/peptides.css">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="theme-color" content="#0a0908">
<meta name="author" content="Med Plug RX">
<meta property="og:type" content="website"><meta property="og:site_name" content="Med Plug RX"><meta property="og:locale" content="en_US">
<meta property="og:url" content="{url}"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:image" content="https://www.medplugrx.com/a/{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="https://www.medplugrx.com/a/{og}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","@id":"{url}#webpage","url":"{url}","name":"{t}","description":"{d}","isPartOf":{{"@id":"https://www.medplugrx.com/#website"}},"about":{{"@id":"https://www.medplugrx.com/#organization"}}}}</script>
</head><body>
'''

def pre():
    return f'''<div id="pre"><div style="position:relative;z-index:2;display:flex;flex-direction:column;align-items:center">
{MARK.format(s=150)}<div class="pt serif">Med Plug RX &middot; Peptides</div><div class="pb"><i></i></div></div></div>
'''

def hero_short(img, badge, h1, sub, extra_cls=""):
    return f'''<div class="hero short">
<div class="hstack"></div><img class="hart pg{extra_cls}" src="../a/{img}" alt="" aria-hidden="true"><div class="veil"></div><canvas id="field"></canvas><div class="sweep"></div>
<div class="wrap"><div class="hero-in">
<div class="badge"><span class="dot"></span>{badge}</div>
<div style="display:flex;justify-content:center;margin:34px 0 0">{MARK.format(s=128)}</div>
<h1 class="serif"><span class="shim">{h1}</span></h1>
<div class="sub">{sub}</div>
</div></div></div>
'''

def bleed(img, eyebrow, h2, p, cls="", imgcls=""):
    return f'''<div class="bleed{(' '+cls) if cls else ''}">
<img class="bg{(' '+imgcls) if imgcls else ''}" src="../a/{img}" alt="" aria-hidden="true">
<div class="inner"><div class="eyebrow rv">{eyebrow}</div>
<h2 class="serif rv" data-d="1">{h2}</h2>
<p class="rv" data-d="2">{p}</p></div></div>
'''

def final(eyebrow, h2, p, a1=("../access.html", "Request Physician Account"), a2=("../access.html", "Request A Sample")):
    return f'''<section class="final lux"><canvas class="gflow"></canvas><div class="wrap">
<div style="display:flex;justify-content:center;margin-bottom:10px">{MARK.format(s=60)}</div>
<div class="eyebrow rv">{eyebrow}</div>
<h2 class="serif shim rv" data-d="1">{h2}</h2>
<p class="rv" data-d="2">{p}</p>
<div class="cta rv" data-d="3"><a href="{a1[0]}" class="btn btn-solid">{a1[1]}</a>
<a href="{a2[0]}" class="btn">{a2[1]}</a></div></div></section>
'''

def shead(eyebrow, h2, p=""):
    return f'''<div class="shead"><div class="eyebrow rv">{eyebrow}</div>
<h2 class="serif rv" data-d="1">{h2}</h2>{f'<p class="rv" data-d="2">{p}</p>' if p else ''}</div>'''

def kv(rows):
    out = '<div class="kv">'
    for r in rows:
        hi = len(r) > 2 and r[2]
        out += f'<div class="r{" hi" if hi else ""}"><div class="k">{r[0]}</div><div class="v">{r[1]}</div></div>'
    return out + '</div>'

def chips(items, gold=()):
    return '<div class="chips">' + "".join(
        f'<span class="chip{" au" if i in gold else ""}">{i}</span>' for i in items) + '</div>'

MARQ_PEP = '''<div class="marq"><div class="track">
<b>TIRZEPATIDE</b><i>&#9670;</i><b>RETATRUTIDE</b><i>&#9670;</i><b>BPC-157</b><i>&#9670;</i><b>TB-500</b><i>&#9670;</i><b>CJC-1295</b><i>&#9670;</i><b>IPAMORELIN</b><i>&#9670;</i><b>GHK-Cu</b><i>&#9670;</i><b>NAD+</b><i>&#9670;</i><b>MOTS-c</b><i>&#9670;</i><b>SEMAX</b><i>&#9670;</i><b>PT-141</b><i>&#9670;</i><b>GLUTATHIONE</b><i>&#9670;</i>
<b>TIRZEPATIDE</b><i>&#9670;</i><b>RETATRUTIDE</b><i>&#9670;</i><b>BPC-157</b><i>&#9670;</i><b>TB-500</b><i>&#9670;</i><b>CJC-1295</b><i>&#9670;</i><b>IPAMORELIN</b><i>&#9670;</i><b>GHK-Cu</b><i>&#9670;</i><b>NAD+</b><i>&#9670;</i><b>MOTS-c</b><i>&#9670;</i><b>SEMAX</b><i>&#9670;</i><b>PT-141</b><i>&#9670;</i><b>GLUTATHIONE</b><i>&#9670;</i>
</div></div>'''

MARQ_CERT = '''<div class="marq"><div class="track">
<b>ISO 13485:2016</b><i>&#9670;</i><b>EU MDR 2017/745</b><i>&#9670;</i><b>ISO 11608-1:2022</b><i>&#9670;</i><b>ISO 11608-2:2022</b><i>&#9670;</i><b>ISO 13926</b><i>&#9670;</i><b>GRADE A / ISO 5 FILL</b><i>&#9670;</i><b>ICH Q1B</b><i>&#9670;</i><b>QA BATCH RELEASE</b><i>&#9670;</i>
<b>ISO 13485:2016</b><i>&#9670;</i><b>EU MDR 2017/745</b><i>&#9670;</i><b>ISO 11608-1:2022</b><i>&#9670;</i><b>ISO 11608-2:2022</b><i>&#9670;</i><b>ISO 13926</b><i>&#9670;</i><b>GRADE A / ISO 5 FILL</b><i>&#9670;</i><b>ICH Q1B</b><i>&#9670;</i><b>QA BATCH RELEASE</b><i>&#9670;</i>
</div></div>'''

# ───────────────────────────── HOME ─────────────────────────────
def page_home():
    p = head("Med Plug RX Peptides — Pharmaceutical-Manufactured Peptides in a Certified Injector Pen",
             "73 peptides, pre-filled by a licensed pharmaceutical manufacturer and delivered in an ISO 13485 / EU MDR certified injector pen. Two device tiers, 0.01 mL per click, supplied to licensed physicians.",
             "index.html", og="pen-trio.jpg")
    p += pre() + DEFS + nav("index.html") + SPLIT_FULL
    p += f'''<div class="hero">
<div class="hstack"></div><img class="hart pen" src="../a/pen-hero.jpg" alt="" aria-hidden="true"><div class="veil"></div><canvas id="field"></canvas><div class="sweep"></div>
<div class="wrap"><div class="hero-in">
<div class="badge"><span class="dot"></span>Physician Use Only &#183; United States</div>
<div class="markrow">{MARK.format(s=104)}</div>
<h1 class="serif"><span class="shim">Leave the vial behind.</span></h1>
<div class="sub">Peptide delivery, re-engineered.</div>
<p class="lede">Pharmaceutical-manufactured peptides, delivered in a certified injector pen. No reconstitution, no syringe, no arithmetic at the patient end &#8212; the patient selects a dose and the device meters it.</p>
<div class="cta"><a href="../access.html" class="btn btn-solid">Request Physician Account</a>
<a href="the-pen.html" class="btn">See The Pen</a></div></div></div>
</div><div class="stats"><div class="wrap">
<div class="stat rv lit"><div class="n serif shim"><span class="cnt" data-to="73">73</span></div><div class="l">Peptides available pre-filled</div></div>
<div class="stat rv lit" data-d="1"><div class="n serif shim">0.01<span style="font-size:.5em"> mL</span></div><div class="l">Dose increment per click</div></div>
<div class="stat rv lit" data-d="2"><div class="n serif shim">2</div><div class="l">Device tiers &#183; metal &amp; disposable</div></div>
<div class="stat rv lit" data-d="3"><div class="n serif shim">0</div><div class="l">Preparation steps at the patient end</div></div>
</div></div>'''
    # the collection
    p += lux() + f'''<div class="wrap">{shead("The Division", "Pen. Portfolio. Fill.", "Three things have to be right at once: the device, the compound, and the facility that put one inside the other. Each is documented on its own page.")}
<div class="prods">
<a class="prod tilt rv" href="the-pen.html"><div class="ph"><img src="../a/pen-trio.jpg" alt="" loading="lazy"></div>
<div class="body"><div class="tag">01 &#183; The Delivery Device</div><h3 class="serif">The Pen</h3><div class="type">Metal Reusable &#183; Molded Disposable</div>
<p>Two device tiers on one dosing platform. 0.01 mL per click, audible and tactile, on a 3 mL ISO 11608-2 cartridge. Sixty independent measurements, zero failures.</p></div></a>
<a class="prod tilt rv" data-d="1" href="portfolio.html"><div class="ph"><img src="../a/pep-gown.jpg" alt="" loading="lazy" style="object-position:50% 20%"></div>
<div class="body"><div class="tag">02 &#183; The Portfolio</div><h3 class="serif">Seventy-Three Peptides</h3><div class="type">One Standard &#183; Six Families</div>
<p>Metabolic and GLP-1, growth hormone secretagogues, repair and regenerative, melanocortins, neuroactive and longevity, immune and established actives.</p></div></a>
<a class="prod tilt rv" data-d="2" href="manufacturing.html"><div class="ph"><img src="../a/iso5.jpg" alt="" loading="lazy"></div>
<div class="body"><div class="tag">03 &#183; The Fill</div><h3 class="serif">Licensed Manufacture</h3><div class="type">Synthesis To Released Batch</div>
<p>Three tiers supply this market. Only one holds a national drug manufacturing license and cannot ship without formal QA release. That is the tier supplying Med Plug RX.</p></div></a>
</div></div></section>'''
    p += bleed("pep-couple.jpg", "The Inflection Point", "Every category that can<br>move to a pen, has.",
               "Insulin took two decades. GLP-1 took five &#8212; in front of the same patients now asking about peptides. They have already held a pen. Reconstitution survives here for one reason: the supply chain behind it was never pharmaceutical. That has changed.", imgcls="shiftr headroom")
    p += lux(kind="gflow") + f'''<div class="wrap">{shead("Timing", "The advantage is temporary.<br>That is what makes it worth taking.", "Format transitions reward the earliest mover, not the best one. For a defined period you are not competing on price &#8212; you are offering something competitors cannot source.")}
<div class="trio quad">
<div class="tcard rv"><div class="tn serif">I</div><h3 class="serif">Price Insulation</h3><p>Compete on experience while the format is scarce. Sterile cartridge filling, closure integrity validation and dose accuracy testing are not capabilities a compounding operation adds quickly.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">II</div><h3 class="serif">Retention</h3><p>Reorder behavior attaches to the delivery, not the compound. A patient who has dialed a dose does not go back to drawing one.</p></div>
<div class="tcard rv" data-d="2"><div class="tn serif">III</div><h3 class="serif">Referral</h3><p>A pen is an object patients describe. A vial is not.</p></div>
<div class="tcard rv" data-d="3"><div class="tn serif">IV</div><h3 class="serif">Authority</h3><p>First mover is remembered as the name that introduced it. The constraint is upstream, and it is already solved.</p></div>
</div></div></section>'''
    p += MARQ_PEP
    p += lux() + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">The Patient End</div><h2 class="serif">Six steps to two.</h2>
<p>Attrition concentrates at the first self-administration and the first reorder. Both are preparation events. Remove the preparation and you remove the moment the patient decides this is too much.</p>
<p><b>No measurement. No arithmetic.</b> No judgment about whether the solution looks properly mixed.</p>
<div class="cta" style="justify-content:flex-start;margin-top:30px"><a href="the-pen.html" class="btn">The Pen In Detail</a></div></div>
<div class="steps">
<div><h4>From a vial</h4><ol><li>Reconstitute with measured diluent</li><li>Swirl and wait for full dissolution</li><li>Swab stopper, draw with syringe</li><li>Expel air, verify graduation by eye</li><li>Administer</li><li>Store the vial, track the in-use date</li></ol></div>
<div class="pen"><h4>From a pen</h4><ol><li>Fit needle tip</li><li>Dial dose, administer, discard tip</li></ol></div>
</div></div></div></section>'''
    p += bleed("pep-gym.jpg", "The Field", "Built Around<br>Healthspan", "The physicians on our register are building longevity, aesthetic and metabolic practice around characterized compounds. What we owe them is a supply that is documented, consistent and never substituted.", imgcls="subj-l")
    p += lux() + f'''<div class="wrap"><div class="split">
<div class="imgbox rv"><img src="../a/pep-yacht.jpg" alt="" loading="lazy"></div>
<div><div class="eyebrow">The Patient</div><h2 class="serif">They have already<br>held a pen.</h2>
<p>The patients now asking about peptides are the same patients who dialed a GLP-1 dose last year. The format they expect is the one they already know; anything else reads as a step backward.</p>
<p>A pen is an object patients describe to friends. A vial is not.</p>
<div class="cta" style="justify-content:flex-start;margin-top:26px"><a href="portfolio.html" class="btn">See The Portfolio</a></div></div>
</div></div></section>'''
    p += lux(photo="pep-face.jpg") + f'''<div class="wrap">{shead("Allocation", "Supplied By Register,<br>Not By Volume", "Accounts are verified against state licensure before a single pen moves. We do not sell to consumers, we do not list on marketplaces, and we do not discount to win an order.")}
<div class="trio">
<div class="tcard rv"><div class="tn serif">01</div><h3 class="serif">Metabolic &amp; Longevity</h3><div class="type">GLP-1 &#183; Healthspan Programs</div><p>For programs built around metabolic and cellular health, directed entirely by the physician.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">02</div><h3 class="serif">Aesthetic &amp; Regenerative</h3><div class="type">Skin, Repair &amp; Recovery</div><p>For the practices where the result is visible, photographed and referred.</p></div>
<div class="tcard rv" data-d="2"><div class="tn serif">03</div><h3 class="serif">Performance &amp; Sports Medicine</h3><div class="type">Recovery &amp; Musculoskeletal</div><p>For specialists who demand the same lot-level record they demand everywhere else.</p></div>
</div></div></section>'''
    p += MARQ_CERT
    p += final("Samples Available", "Let&#8217;s put a pen<br>in your hand.", "Samples of both device tiers are available to verified physician accounts, filled or unfilled. The full certification package and the 56-page laboratory report are released on NDA.")
    return p + FOOTER

# ───────────────────────────── THE PEN ─────────────────────────────
def page_pen():
    p = head("The Injector Pen — Two Device Tiers, One Dosing Platform | Med Plug RX Peptides",
             "Metal reusable and molded disposable injector pens on one dosing mechanism: 0.01 mL per click, 3 mL ISO 11608-2 cartridge, ISO 13485 and EU MDR certified, sixty independent accuracy measurements with zero failures.",
             "the-pen.html", og="pen-trio.jpg")
    p += pre() + DEFS + nav("the-pen.html") + SPLIT_SHORT
    p += hero_short("pen-trio.jpg", "The Delivery Device", "Two device tiers.<br>One dosing platform.", "Reusable Metal &#183; Disposable Molded")
    p += f'''<div class="stats"><div class="wrap">
<div class="stat rv lit"><div class="n serif shim">5</div><div class="l">Finishes in production</div></div>
<div class="stat rv lit" data-d="1"><div class="n serif shim">20<span style="font-size:.5em"> N</span></div><div class="l">Maximum trigger force, verified</div></div>
<div class="stat rv lit" data-d="2"><div class="n serif shim">3<span style="font-size:.5em"> mL</span></div><div class="l">ISO 11608-2 cartridge</div></div>
<div class="stat rv lit" data-d="3"><div class="n serif shim">60 / 0</div><div class="l">Measurements &#183; failures</div></div>
</div></div>'''
    p += lux(photo="pen-wet.jpg") + f'''<div class="wrap">{shead("The Object", "Equipment, not medical supply.", "No other supplier in this channel offers a metal reusable and a plastic disposable on the same mechanism. Same needle, same dosing, no retraining.")}
<div class="tiers">
<div class="tier rv"><h3 class="serif">Reusable, metal-bodied</h3><div class="lab">Enterprise Tier</div>
{kv([("Device type","Multi-use, replaceable cartridge"),("Body","Machined metal, five finishes"),("Maximum dose","80 units"),("Cartridge","Replaceable; patient keeps the device"),("Length &#183; diameter","173.9 mm &#183; 17.2 mm"),("Needle-hub diameter","14.6 mm"),("Dose window","Transparent holder, volume visible"),("Trigger force","20 N maximum")])}</div>
<div class="tier rv" data-d="1"><h3 class="serif">Disposable, molded</h3><div class="lab">Volume Tier</div>
{kv([("Device type","Single-use, pre-filled, not reusable"),("Body","Opaque molded polymer, three-piece"),("Maximum dose","60 units"),("Cartridge","Pre-loaded; discarded when spent"),("Length","160.9 mm &#177; 3 mm"),("Needle-end diameter","Approx. 15.1 mm"),("Housing","Opaque, no cartridge window"),("Trigger force","20 N maximum")])}</div>
</div>
<div class="chiplab" style="margin-top:64px">Shared across both tiers</div>
{chips(["0.01 mL per click, audible and tactile","Universal needle thread","3 mL ISO 11608-2 / ISO 13926 cartridge","8.2&#8211;8.3 mm stopper","No dose advance without reset"], gold=())}
<p class="fine">Plastic reads as disposable. A weighted metal body reads as equipment, and patients treat it accordingly. Five finishes in production: allocate one per protocol and the commonest at-home error &#8212; the wrong device &#8212; disappears.</p>
</div></section>'''
    p += bleed("pep-tux.jpg", "The Object", "Weight is<br>a signal.", "A pen that feels like equipment is kept, charged with a fresh cartridge and reordered. A pen that feels like packaging is thrown away with the box.", imgcls="shiftr")
    p += lux() + f'''<div class="wrap">{shead("Independent Verification", "Sixty measurements.<br>Zero failures.", "Accredited third-party laboratory, ISO 11608-1:2022 and ISO 11608-2:2022. Tolerance interval at k = 3.154.")}
<div class="tblwrap"><table class="tbl"><thead><tr><th>Target volume</th><th>Units</th><th>Measured average</th><th>Std deviation</th><th>Required range</th><th>Result</th></tr></thead><tbody>
<tr><td>0.01 mL</td><td>20</td><td>0.0113 mL</td><td>0.0020 mL</td><td>0.000 &#8211; 0.020</td><td class="pass">Pass</td></tr>
<tr><td>0.30 mL</td><td>20</td><td>0.2979 mL</td><td>0.0026 mL</td><td>0.285 &#8211; 0.315</td><td class="pass">Pass</td></tr>
<tr><td>0.60 mL</td><td>20</td><td>0.5973 mL</td><td>0.0042 mL</td><td>0.570 &#8211; 0.630</td><td class="pass">Pass</td></tr>
</tbody></table></div>
<div class="figs">
<div class="fig rv"><div class="n">&#177;0.0027</div><div class="l">Worst-case deviation from target, mL</div></div>
<div class="fig rv" data-d="1"><div class="n">0</div><div class="l">Failures across all test items</div></div>
<div class="fig rv" data-d="2"><div class="n">5 / 23 / 40</div><div class="l">&#176;C reliability, 60 units per condition</div></div>
</div>
<p class="fine">Full 56-page report under NDA. Report number and laboratory identity are released to verified physician accounts on request.</p>
</div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">Needle Integrity</div><h2 class="serif">One pass through rubber.<br>Damage you cannot see.</h2>
<p>Under electron microscopy, a needle that did nothing but pass through a vial stopper showed <b>5.46% tip deformation</b>. On inspection, the injectors saw none.</p>
<p>A pen needle never meets a stopper.</p>
<div class="figs"><div class="fig"><div class="n">5.46%</div><div class="l">Deformation after one stopper pass</div></div><div class="fig"><div class="n">17.3%</div><div class="l">Punctures shedding rubber fragments</div></div></div></div>
<div><div class="needle"><div class="lab">As manufactured</div>
<svg viewBox="0 0 600 70" aria-hidden="true"><line x1="0" y1="35" x2="560" y2="35" stroke="rgba(201,168,96,.35)" stroke-dasharray="4 6"/><path d="M40,22 L520,35 L40,48 Z" fill="#DAD4C8"/><path d="M40,22 L520,35" stroke="#fff" stroke-width="1.2"/><circle cx="520" cy="35" r="7" fill="none" stroke="#6FB5A2" stroke-width="2"/></svg>
<div class="cap">Bevel intact</div>
<div class="lab">After one stopper pass</div>
<svg viewBox="0 0 600 70" aria-hidden="true"><line x1="0" y1="35" x2="560" y2="35" stroke="rgba(201,168,96,.35)" stroke-dasharray="4 6"/><path d="M40,22 L500,33 L512,28 L520,38 L506,41 L40,48 Z" fill="#8E8880"/><path d="M40,22 L500,33" stroke="#C9A860" stroke-width="1.2"/><path d="M500,33 L512,28 L520,38" fill="none" stroke="#C9A860" stroke-width="1.4"/><circle cx="516" cy="35" r="8" fill="none" stroke="#B85C4A" stroke-width="2"/></svg>
<div class="cap">Rolled, blunted, barbed at the point</div></div>
<div class="panel quote"><div class="src">The literature&#8217;s own conclusion</div><div class="q">Avoid piercing the stopper altogether.</div></div>
<p class="fine" style="margin-top:22px">Akintilo et al., Journal of Cosmetic Dermatology, 2025 &#8212; SEM of 45 needle tips. Coring incidence from 150 stopper punctures, 18&#8211;21G, rising to 56% at 18G and 45&#176;. Illustrations schematic.</p></div>
</div></div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">Photostability</div><h2 class="serif">The degradation pathway nobody accounts for.</h2>
<p>Stability talk in this channel is all thermal. Light is treated as a labelling formality. Residues absorbing near-UV &#8212; tryptophan, tyrosine, phenylalanine, cysteine &#8212; oxidise directly, cascading into methionine and histidine.</p>
<p><b>And it cannot be modelled.</b> Thermal decay follows Arrhenius. Photostability has no accepted predictive equivalent, and damage can occur within hours.</p>
<div class="panel" style="margin-top:30px"><h3 class="serif">The engineering answer</h3><p>Exposure accrues in lux-hours, so storage governs it &#8212; not the seconds of an injection. A reconstituted vial is clear glass on a shelf for weeks. A capped pen keeps its cartridge dark for its whole life.</p></div></div>
<div><div class="chiplab">Susceptibility follows the sequence</div>
{kv([("Higher","GLP-1 agonists, MOTS-c, melanocortins, glutathione, NAD+"),("Lower","BPC-157, KPV, GHK-Cu &#8212; no aromatic or sulfur residues"),("ICH Q1B","1.2 million lux-hours visible, 200 W&#183;h/m&#178; near-UV")])}
<p class="fine">Photo-oxidation pathways per Kerwin &amp; Remmele and subsequent forced-degradation literature. Exposure conditions per ICH Q1B.</p></div>
</div></div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap">{shead("Regulatory Standing", "Certified as a medical device,<br>not sold as an accessory.")}
<div class="trio">
<div class="tcard rv"><div class="tn serif">ISO</div><h3 class="serif">ISO 13485:2016</h3><p>Quality management system certification for medical devices, held by the device manufacturer. Scope covers the development and manufacture of pen injectors and disposable sterile injection needles.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">EU</div><h3 class="serif">EU MDR 2017/745</h3><p>Certified as a Class I device with measuring function, assessed under Annex IX. Coverage extends to cartridge syringes and pen injectors.</p></div>
<div class="tcard rv" data-d="2"><div class="tn serif">FDA</div><h3 class="serif">510(k) Status</h3><p>A premarket notification has been submitted and is under review. No clearance determination has been issued, and none is claimed or implied by this site.</p></div>
</div>
<p class="fine">Most competing supply in this channel carries no device certification at all. The full certification package is released on NDA.</p>
</div></section>'''
    p += MARQ_CERT
    p += final("Samples Available", "Hold both tiers.", "Samples of the metal and the disposable device are available to verified physician accounts, filled or unfilled.")
    return p + FOOTER

# ───────────────────────────── PORTFOLIO ─────────────────────────────
FAMS = [
    ("Metabolic &amp; GLP-1", ["Tirzepatide","Liraglutide","Retatrutide","Cagrilintide","Orforglipron","Mazdutide","Ecnoglutide","Dulaglutide","Pramlintide"]),
    ("Growth Hormone Secretagogues", ["Ipamorelin","Sermorelin","Tesamorelin","Hexarelin","CJC-1295","CJC-1295 w/ DAC","GHRP-2","GHRP-6","AOD9604","IGF-1 LR3","MGF","PEG-MGF"]),
    ("Repair &amp; Regenerative", ["BPC-157","TB-500","TB-500 Frag 1-4","GHK-Cu","ARA-290","Larazotide"]),
    ("Melanocortins", ["Melanotan II","Afamelanotide","Setmelanotide","Bremelanotide"]),
    ("Neuroactive &amp; Longevity", ["Selank","Semax","DSIP","Dihexa","Epitalon","MOTS-c","Humanin","Elamipretide","Pinealon"]),
    ("Immune &amp; Antimicrobial", ["KPV","LL-37","Thymalfasin","Zinc Thymulin"]),
    ("Established Actives", ["Oxytocin","Desmopressin","Leuprolide","Lanreotide","Gonadorelin","Kisspeptin-10","Glutathione","NAD+"]),
]

def page_portfolio():
    p = head("The Portfolio — Seventy-Three Peptides, One Standard | Med Plug RX Peptides",
             "Seventy-three peptides supplied pre-filled from a licensed pharmaceutical manufacturer: metabolic and GLP-1, growth hormone secretagogues, repair and regenerative, melanocortins, neuroactive and longevity, immune and established actives.",
             "portfolio.html", og="pep-gown.jpg")
    p += pre() + DEFS + nav("portfolio.html") + SPLIT_SHORT
    p += hero_short("pep-gown.jpg", "The Portfolio", "Seventy-three peptides,<br>one standard.", "Six Families &#183; Pre-Filled &#183; Licensed Manufacture")
    fam_html = ""
    for i, (name, names) in enumerate(FAMS):
        joined = "<i>&#183;</i>".join(names)
        fam_html += f'<div class="fam rv"><div class="fh"><div class="eyebrow">{name}</div><div class="ct serif">{len(names):02d}</div></div><div class="names">{joined}</div></div>'
    p += lux(photo="pep-vanity.jpg") + f'''<div class="wrap">{shead("The Range", "Every compound, one fill standard.", "Each peptide is synthesised, filled, lyophilised and QA-released under the same national drug manufacturing license, and ships with a certificate of analysis.")}
<div class="fams">{fam_html}</div>
<div class="panel" style="margin-top:56px"><h3 class="serif">Combinations</h3><p>Two compounds in a single 3 mL cartridge, one administration. Current SKUs include BPC-157 with TB-500, CJC-1295 with Ipamorelin, and PT-141 with Oxytocin.</p></div>
<p class="fine">Compounding eligibility varies by substance and is confirmed against current FDA bulk drug substance lists at the point of order. Listing here is not a representation that any substance is eligible for any particular use.</p>
</div></section>'''
    p += MARQ_PEP
    p += bleed("pep-face.jpg", "The Standard", "Measured,<br>Not Claimed", "The figure on the certificate is the figure measured on that lot &#8212; purity, assay, endotoxin and sterility &#8212; never averaged from a batch. If the record does not match the cartridge, we do not take the lot.", imgcls="shiftr")
    p += lux(kind="gflow") + f'''<div class="wrap">{shead("Documentation", "Certificates of analysis,<br>archived by product.", "Every lot released to a physician account carries its certificate. The archives are public; the manufacturer identity behind them is released on NDA.")}
<div class="trio">
<a class="tcard rv" href="../coamedplug" style="text-decoration:none;color:inherit;display:block"><div class="tn serif">COA</div><h3 class="serif">Peptide Archive</h3><div class="type">Lyophilised &amp; Pre-Mixed</div><p>Per-lot certificates for the peptide range.</p></a>
<a class="tcard rv" data-d="1" href="../coapens" style="text-decoration:none;color:inherit;display:block"><div class="tn serif">COA</div><h3 class="serif">Pen Archive</h3><div class="type">Pre-Filled Cartridges</div><p>Per-lot certificates for peptides supplied in the injector pen.</p></a>
<a class="tcard rv" data-d="2" href="../coajungmoney" style="text-decoration:none;color:inherit;display:block"><div class="tn serif">COA</div><h3 class="serif">Jung Money Archive</h3><div class="type">Partner Label</div><p>Per-lot certificates for the Jung Money line.</p></a>
</div></div></section>'''
    p += final("Physician Accounts Only", "Request the range.", "Verified physician accounts receive the full portfolio sheet, current SKU availability and per-compound eligibility on request.", a2=("the-pen.html", "See The Pen"))
    return p + FOOTER

# ───────────────────────────── MANUFACTURING ─────────────────────────────
PROCESS = ["Raw material review","Raw material release","Solid-phase synthesis","Cleavage and deprotection","Crude isolation","Chromatographic purification","Desalting and salt exchange","API lyophilization","API release","Sterile compounding","Sterilizing filtration","Aseptic filling","Partial stoppering","Lyophilizer loading","Freezing","Primary drying","Secondary drying","Backfill and stoppering","Crimp capping","Closure integrity","Finished product testing","QA batch release","Stability and transport"]
GOLD = {"Solid-phase synthesis","Cleavage and deprotection","Crude isolation","Chromatographic purification","Desalting and salt exchange","API lyophilization","API release","QA batch release"}
API_TESTS = ["Sequence confirmation","HPLC / UPLC purity","Related substances","Assay or peptide content","Moisture","Counterion content","Elemental impurities","Bioburden","Bacterial endotoxins","Appearance and solubility"]
FP_TESTS = ["Appearance and cake morphology","Identification","Assay or potency","Purity and related substances","Degradation products","Fill volume and dose uniformity","Residual moisture","Reconstitution time and clarity","pH and osmolality","Visible and subvisible particles","Sterility","Bacterial endotoxins","Container closure integrity","Dose delivery accuracy"]

def page_manufacturing():
    p = head("Manufacturing — Synthesis to Released Batch, Under One License | Med Plug RX Peptides",
             "Three tiers supply the peptide market; only one is a licensed pharmaceutical manufacturer. Grade A / ISO 5 aseptic fill, 0.22 µm sterilizing filtration, 99%+ purity per lot, QA batch release, US inspection and assembly, 2–8°C cold chain.",
             "manufacturing.html", og="iso5.jpg")
    p += pre() + DEFS + nav("manufacturing.html") + SPLIT_SHORT
    p += hero_short("iso5.jpg", "The Fill", "Synthesis to released batch,<br>under one license.", "Licensed Pharmaceutical Manufacture")
    p += f'''<div class="stats"><div class="wrap">
<div class="stat rv lit"><div class="n serif shim">ISO 5</div><div class="l">Grade A aseptic filling</div></div>
<div class="stat rv lit" data-d="1"><div class="n serif shim">0.22<span style="font-size:.5em"> &#181;m</span></div><div class="l">Sterilizing-grade membrane</div></div>
<div class="stat rv lit" data-d="2"><div class="n serif shim">99%+</div><div class="l">Purity verified per lot</div></div>
<div class="stat rv lit" data-d="3"><div class="n serif shim">2&#8211;8<span style="font-size:.5em"> &#176;C</span></div><div class="l">Cold chain, data-logged</div></div>
</div></div>'''
    p += lux(photo="iso5.jpg") + f'''<div class="wrap">{shead("The Fill", "Three tiers supply this market.<br>Only one is a pharmaceutical manufacturer.")}
<div class="trio">
<div class="tcard rv"><div class="tn serif">Tier One</div><h3 class="serif">Research Use Only</h3><p>Not for human use. No drug license, no aseptic validation, no batch release authority. Purity is supplier-asserted.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">Tier Two</div><h3 class="serif">cGMP Contract</h3><p>Good manufacturing practice, often for a narrow scope. Frequently fill-and-finish rather than end-to-end.</p></div>
<div class="tcard rv" data-d="2" style="border-color:rgba(201,168,96,.55)"><div class="tn serif">Tier Three</div><h3 class="serif" style="color:var(--gold)">Licensed Pharmaceutical Manufacturer</h3><p>Holds a national drug manufacturing license. Synthesises the active ingredient, makes the finished sterile product, and cannot ship without formal QA release. This is the tier supplying Med Plug RX.</p></div>
</div>
<p class="fine">Most competing supply is Tier One at worst and Tier Two at best. <a href="#process">Batch release is a legal constraint, not a policy</a> &#8212; product without it may not enter shipment.</p>
</div></section>'''
    p += lux("padding-top:0").replace('<section class="lux"','<section id="process" class="lux"') + f'''<div class="wrap">{shead("Process", "Twenty-three steps.<br>One roof.", "Gold marks the steps where a fill-and-finish operation would be receiving material rather than making it.")}
{chips(PROCESS, gold=GOLD)}
<div class="trio" style="margin-top:64px">
<div class="tcard rv"><div class="tn serif">Grade A / ISO 5</div><p>Aseptic filling under HEPA filtration, unidirectional airflow and barrier isolators.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">0.22 mm</div><p>Sterilizing-grade membrane, integrity tested pre-use and post-use.</p></div>
<div class="tcard rv" data-d="2"><div class="tn serif">99%+ per lot</div><p>Purity verified per lot, with a certificate of analysis supplied.</p></div>
</div></div></section>'''
    p += bleed("cryo-store.jpg", "The Standard", "Nothing ships<br>unreleased.", "A licensed manufacturer cannot release a batch on a policy or a promise. Release is a legal act, signed by qualified persons against the tested record of that lot.")
    p += lux() + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">Chain Of Custody</div><h2 class="serif">Where each stage happens, stated plainly.</h2>
<p>Product is examined against specification before it reaches a buyer, not after a complaint. Domestic assembly removes an international leg and cuts custody transfers under temperature control.</p>
<div class="panel" style="margin-top:30px"><h3 class="serif">Cold chain</h3><p>Premixed liquids ship at 2&#8211;8&#176;C in qualified insulated packaging with data loggers, evaluated routes and defined transport limits.</p></div></div>
<div>{kv([("API synthesis","Licensed pharmaceutical facility, overseas"),("Sterile drug product","Same facility &#8212; aseptic fill, lyophilization, QA release"),("Device manufacture","ISO 13485 and EU MDR certified manufacturer"),("Inbound inspection","United States",True),("Assembly and finishing","United States",True),("Packaging and dispatch","United States, direct to the buyer",True)])}
<p class="fine">This site does not represent the finished drug product as manufactured in the United States. Manufacturer identity, address and license numbers are redacted pending NDA.</p></div>
</div></div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap">{shead("Release Testing", "Tested before a batch may ship.")}
<div class="chiplab">Active ingredient release</div>{chips(API_TESTS)}
<div class="chiplab">Finished product release</div>{chips(FP_TESTS)}
<div class="psplit" style="margin-top:64px">
<div><div class="chiplab">Cited</div>{kv([("Needle deformation","Akintilo et al., J Cosmetic Dermatology, 2025 &#8212; SEM, 45 tips"),("Coring incidence","150 stopper punctures, 18&#8211;21G"),("Photo-oxidation","Kerwin &amp; Remmele; ICH Q1B")])}</div>
<div><div class="chiplab">Withheld pending NDA</div>{kv([("Manufacturers","Names, addresses, license numbers"),("Certificates","Drug manufacturing license and GMP certificate numbers"),("Laboratory report","Independent dose-accuracy report, 56 pages")])}</div>
</div></div></section>'''
    p += MARQ_CERT
    p += final("Documentation On NDA", "Read the file<br>before you order.", "The certification package, manufacturer identity and the independent laboratory report are released to verified physician accounts under NDA.", a2=("portfolio.html", "See The Portfolio"))
    return p + FOOTER

# ───────────────────────────── PACKAGING ─────────────────────────────
def page_packaging():
    p = head("Packaging &amp; Market Position — A Retail Object, Not a Dispensing Container | Med Plug RX Peptides",
             "Rigid book-style box with magnetic flip lid, die-cut tray for the pen and needle tips, instructions printed inside the lid. How the Med Plug RX pen compares with cleared device suppliers and consumer accessories.",
             "packaging.html", og="pep-vanity.jpg")
    p += pre() + DEFS + nav("packaging.html") + SPLIT_SHORT
    p += hero_short("pep-vanity.jpg", "The Presentation", "A retail object,<br>not a dispensing container.", "Presentation &#183; Market Position", extra_cls=" vt")
    p += lux() + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">The Box</div><h2 class="serif">Wrapped board.<br>Magnetic closure.</h2>
<p>Rigid book-style box with a magnetic flip lid. Wrapped board, not a folding carton. Instructions print inside the lid; the pen and its needle tips sit in a fitted tray beneath.</p>
{kv([("Construction","Wrapped board, magnetic closure"),("Inside lid","Three-step instruction panel"),("Tray","Die-cut, seats pen and needle tips"),("Window","72 &#215; 23 mm die-cut, front panel"),("Artwork","Four print versions approved")])}
<p class="fine">Reference unit in the black finish specified for Med Plug RX. Each version carries the MEDPLUG lockup, compound and dosage, quality marks, a QR code, and storage copy on the reverse.</p></div>
<div class="boxfig rv"><img src="../a/pen-box.png" alt="Med Plug RX injector pen presentation box, open, showing the die-cut tray and needle-tip lid" loading="lazy"></div>
</div></div></section>'''
    p += bleed("pep-couple.jpg", "The Unboxing", "What arrives<br>is the brand.", "The patient never sees the facility, the license or the laboratory report. They see the box, the weight of the pen and the first dose. All three are designed to be described.", imgcls="shiftr headroom")
    p += lux(photo="pen-stand.jpg") + f'''<div class="wrap">{shead("Market Position", "Against what is<br>currently available.", "Competitor attributes as published on each manufacturer&#8217;s own materials, reviewed August 2026. Pricing is excluded by choice and addressed directly.")}
<div class="tblwrap"><table class="tbl cmp"><thead><tr><th></th><th class="mp">Med Plug RX</th><th>Cleared device supplier</th><th>Consumer accessory</th></tr></thead><tbody>
<tr><td class="rk">Body material</td><td class="mp">Metal reusable and molded disposable</td><td>Plastic, including the reusable model</td><td>Aluminum</td></tr>
<tr><td class="rk">Device tiers</td><td class="mp">Two, one dosing platform</td><td>One</td><td>One</td></tr>
<tr><td class="rk">Maximum dose</td><td class="mp">80 metal / 60 disposable</td><td>80 units</td><td>60 units</td></tr>
<tr><td class="rk">Certification</td><td class="mp">ISO 13485 and EU MDR</td><td>ISO 13485, ISO 9001; 510(k) cleared</td><td>None listed</td></tr>
<tr><td class="rk">Independent testing</td><td class="mp">56-page report, 60 accuracy measurements</td><td>ISO 11608-1 compliance stated</td><td>None listed</td></tr>
<tr><td class="rk">Supplied pre-filled</td><td class="mp">Yes &#8212; 73 peptides, licensed pharmaceutical manufacturer</td><td>No &#8212; device only</td><td>No &#8212; device only</td></tr>
<tr><td class="rk">Packaging</td><td class="mp">Custom magnetic box, four artworks, needle tips included</td><td>Standard commercial</td><td>Retail; needles not included</td></tr>
</tbody></table></div>
</div></section>'''
    p += MARQ_PEP
    p += final("Samples Available", "Let&#8217;s put a pen<br>in your hand.", "Samples of both tiers are available to verified physician accounts, filled or unfilled, in the presentation box.")
    return p + FOOTER


# ───────────────────────────── FACTS ─────────────────────────────
def page_facts():
    p = head("Facts — May a 503A Pharmacy Fill Cartridges and Dispense Them in Pens? | Med Plug RX Peptides",
             "A regulatory reference on container-closure format for compounded sterile preparations: what Section 503A actually conditions, why a cartridge-loaded pen is not a prefilled autoinjector, and how cartridge fill-finish is done under USP 797.",
             "facts.html", og="pen-hero.jpg")
    p += pre() + DEFS + nav("facts.html") + SPLIT_SHORT
    p += hero_short("pen-wet.jpg", "Regulatory Reference", "May a 503A pharmacy fill cartridges<br>and dispense them in pens?", "Container-Closure Format &#183; Compounded Sterile Preparations")
    p += lux() + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">Short Answer</div><h2 class="serif">Yes.</h2>
<p>Section 503A restricts <b>who</b> may compound, <b>which substances</b>, and <b>under what conditions</b>. It does not restrict container-closure format. Nothing in the statute or in USP &lt;797&gt; limits a compounded sterile preparation to a vial.</p>
<p>The confusion comes from conflating a cartridge-loaded pen with a prefilled autoinjector &#8212; two different regulatory objects.</p></div>
<div><div class="chiplab">01 &#183; What Section 503A actually conditions</div>
{kv([("Who","Compounding by a licensed pharmacist or physician, in a state-licensed pharmacy"),("Why","Pursuant to a valid patient-specific prescription"),("What","Bulk drug substances meeting the statutory criteria &#8212; a USP or NF monograph, the FDA bulks list, or a component of an approved drug &#8212; accompanied by a certificate of analysis"),("Not a copy","Not essentially a copy of a commercially available drug"),("Standards","Compliance with applicable USP chapters, including &lt;797&gt; for sterile preparations")])}
<p class="fine">None of these conditions concerns container-closure format. There is no provision restricting compounded sterile preparations to vials, and none excluding cartridges.</p></div>
</div></div></section>'''
    p += lux("padding-top:0", photo="pen-stand.jpg") + f'''<div class="wrap">{shead("02 &#183; The Distinction", "Three configurations.<br>Three different answers.", "FDA&#8217;s guidance on pen, jet and related injectors treats configuration as determinative. Objections to compounding &#8220;into pens&#8221; almost always describe the second row. A cartridge-loaded pen is the first.")}
<div class="tblwrap"><table class="tbl cmp"><thead><tr><th>Configuration</th><th class="mp">Regulatory treatment</th></tr></thead><tbody>
<tr class="brand"><td>General-use, cartridge-loaded pen</td><td class="mp">Device cleared on its own. Class II under 21 CFR 880.5860 or 880.6920. Drug is a separate product; the patient loads a cartridge. <b>This is the format in question.</b></td></tr>
<tr><td>Prefilled autoinjector</td><td>Combination product. Drug sealed in at manufacture, device discarded with it. Requires an NDA or BLA. A compounder cannot create this.</td></tr>
<tr><td>Co-packaged</td><td>Application-holder activity. Drug and device marketed together under one application.</td></tr>
</tbody></table></div></div></section>'''
    p += bleed("pen-hero.jpg", "03 &#183; The Cartridge", "A cartridge is packaging,<br>not a device.", "An ISO 11608-3 / ISO 13926 3 mL cartridge is a container-closure system &#8212; vial and syringe functions in a single piece of pharmaceutical packaging. Compounders already dispense in prefilled syringes; selecting a cartridge is the same category of decision. The pen body is a separate, durable, non-sterile, single-patient device the pharmacy does not manufacture.", imgcls="shiftr")
    p += lux() + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">04 &#183; How It Is Done</div><h2 class="serif">Eight steps,<br>one cleanroom.</h2>
<p>Container-closure selection is governed by USP &lt;797&gt; on the same terms as any other &#8212; sterility assurance, closure integrity, and beyond-use dating.</p></div>
<div class="steps" style="grid-template-columns:1fr"><div class="pen"><ol>
<li>Compound from bulk API and diluent to the prescription.</li>
<li>Sterilizing filtration through a 0.22 &#181;m membrane.</li>
<li>Fill the empty sterile glass cartridge from the bottom, using a precision syringe or peristaltic pump with sterile disposable tubing.</li>
<li>Mechanically insert the rubber plunger to seal the cartridge.</li>
<li>All of the above within an ISO 5 laminar flow hood or barrier isolator inside a certified cleanroom.</li>
<li>Seat the sealed cartridge in a compatible pen shell.</li>
<li>Overfill to account for dead space in the mechanism and needle, so the final dose is not short.</li>
<li>Inspect for air and cracks; label with patient name, directions and BUD.</li></ol></div></div>
</div></div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap">{shead("05 &#183; Established Practice", "Equipment lines are not built<br>for a market that cannot exist.")}
<div class="trio">
<div class="tcard rv"><div class="tn serif">I</div><h3 class="serif">Equipment exists for this</h3><p>Vendors build benchtop, semi-automated cartridge fill-finish systems designed for cleanroom use and marketed to 503A operations, including published material on 503A peptide fill-finish readiness.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">II</div><h3 class="serif">Cleared pens are marketed to compounders</h3><p>A US manufacturer holds 510(k) clearance for both a reusable and a disposable cartridge pen and markets them explicitly to 503A and 503B pharmacies, selling ready-to-use 3 mL cartridges alongside them.</p></div>
<div class="tcard rv" data-d="2"><div class="tn serif">III</div><h3 class="serif">FDA contemplates the category</h3><p>The general-use injector is a standing device classification premised on the drug being supplied separately &#8212; a configuration that only makes sense if someone other than the device maker fills the cartridge.</p></div>
</div></div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap"><div class="psplit">
<div><div class="eyebrow">06 &#183; Where The Myth Comes From</div><h2 class="serif">Not the law.<br>The plant.</h2>
<p>A vial line is not a cartridge line. Cartridges are filled bottom-up and generally require vacuum stoppering to clear air from behind the stopper after filling. Cartridge closure-integrity testing differs from vial methods and needs its own validation.</p>
<p><b>A pharmacy without that tooling correctly says &#8220;we can&#8217;t do that&#8221;</b> &#8212; a true statement about its own capability that is then restated as a rule about compounding.</p></div>
<div><div class="chiplab">07 &#183; It works at either scale</div>
{kv([("Benchtop &#183; small batch","Semi-automated cleanroom fill-finish equipment sized for small runs. Capability without committing to a production line."),("High throughput &#183; 50-state volume","These operations already hold filling capital, engineering and validation staff. The question is adding cartridge tooling and validation &#8212; not whether the format is permitted.")])}
<p class="fine">The legal analysis is identical at either scale. Only the equipment decision changes.</p></div>
</div></div></section>'''
    p += lux("padding-top:0") + f'''<div class="wrap">{shead("08 &#183; What This Does Not Address", "One question answered.<br>Four left to your counsel.", "This reference answers whether the cartridge-and-pen format is available to a 503A. It does not answer the following.")}
<div class="trio quad">
<div class="tcard rv"><div class="tn serif">A</div><h3 class="serif">Substance eligibility</h3><p>Whether a given molecule may be compounded at all is separate, and governed by the bulks lists, monographs and the essentially-a-copy provisions.</p></div>
<div class="tcard rv" data-d="1"><div class="tn serif">B</div><h3 class="serif">Device marketing status</h3><p>Any pen used must itself be lawfully marketable in the United States. Format permission is not device permission.</p></div>
<div class="tcard rv" data-d="2"><div class="tn serif">C</div><h3 class="serif">State boards</h3><p>Boards of pharmacy set and inspect against their own requirements, which vary.</p></div>
<div class="tcard rv" data-d="3"><div class="tn serif">D</div><h3 class="serif">Dating</h3><p>Format does not extend a beyond-use date. BUD is assigned under USP &lt;797&gt; and supporting data as with any other preparation.</p></div>
</div>
<div class="panel quote" style="margin-top:56px"><div class="src">Regulatory reference &#183; not legal advice</div><div class="q" style="font-size:clamp(18px,2vw,24px)">Prepared as a regulatory reference, not as legal advice. Confirm with counsel and with your board of pharmacy before changing dispensing format.</div></div>
</div></section>'''
    p += MARQ_CERT
    p += final("Documentation On NDA", "Read the file<br>before you order.", "The certification package, manufacturer identity and the independent laboratory report are released to verified physician accounts under NDA.", a2=("the-pen.html", "See The Pen"))
    return p + FOOTER

PAGES = {"index.html": page_home, "facts.html": page_facts, "the-pen.html": page_pen, "portfolio.html": page_portfolio,
         "manufacturing.html": page_manufacturing, "packaging.html": page_packaging}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(fn())
        print("wrote peptides/" + name)
