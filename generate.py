#!/usr/bin/env python3
"""Generates all detail pages (experience: work/research/leadership, and
projects) from one shared template + a data list, so every page stays
visually consistent. Edit the DATA lists below (or just edit the generated
HTML files directly afterward) to swap in real content.

Prev/Next navigation on each page cycles within its own category (e.g. a
Work Experience page only links to other Work Experience pages), and the
breadcrumb/"back to" link reflects that category.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

CATEGORY_META = {
    "work": {"id": "work", "label": "Work Experience"},
    "research": {"id": "research", "label": "Research"},
    "leadership": {"id": "leadership", "label": "Leadership"},
    "projects": {"id": "projects", "label": "Projects"},
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}, {org} | Suraj Duvvapu</title>
<meta name="description" content="{lede_plain}" />
<link rel="stylesheet" href="../styles.css" />
</head>
<body>

<nav class="nav">
  <div class="container">
    <a href="../index.html" class="nav-logo">Suraj Duvvapu</a>
    <ul class="nav-links">
      <li><a href="../index.html#about">About</a></li>
      <li><a href="../index.html#work">Work</a></li>
      <li><a href="../index.html#research">Research</a></li>
      <li><a href="../index.html#leadership">Leadership</a></li>
      <li><a href="../index.html#projects">Projects</a></li>
      <li><a href="../index.html#contact">Contact</a></li>
    </ul>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</nav>

<header class="detail-hero">
  <div class="container">
    <div class="breadcrumb reveal">
      <a href="../index.html">Home</a> &rsaquo; <a href="../index.html#{section_id}">{crumb_label}</a> &rsaquo; {org}
    </div>
    <span class="eyebrow reveal">{crumb_label}</span>
    <h1 class="detail-title reveal">{title}</h1>
    <p class="detail-lede reveal">{lede}</p>
    {note_html}
    <div class="detail-meta reveal">
      <span><strong>Organization</strong> &nbsp;{org}</span>
      <span><strong>Dates</strong> &nbsp;{dates}</span>
      <span><strong>Location</strong> &nbsp;{location}</span>
    </div>
  </div>
</header>

<div class="container">
  {media_html}

  <div class="detail-grid">
    <article class="prose reveal">
      <h2>Overview</h2>
      <p{p_class}>{overview}</p>

      <h2>What I did</h2>
      <p{p_class}>{what_i_did}</p>

      <h2>Tools &amp; methods</h2>
      <p{p_class}>{tools_prose}</p>

      <h2>Outcome</h2>
      <p{p_class}>{outcome}</p>
    </article>

    <aside class="sidebar reveal">
      <h3>Skills &amp; tools</h3>
      <div class="tag-list">
        {tag_html}
      </div>
      <h3>Links</h3>
      <ul class="sidebar-links">
        {links_html}
      </ul>
    </aside>
  </div>

  <div class="detail-nav{nav_class}">
    {nav_html}
  </div>
</div>

<footer class="footer" id="contact">
  <div class="container">
    <div class="footer-top">
      <div>
        <h3 class="footer-heading">Let&rsquo;s talk engineering.</h3>
        <p class="text-muted mt-0">Open to new grad and internship opportunities in mechanical &amp; aerospace engineering.</p>
      </div>
      <div class="footer-links">
        <a href="mailto:duvvapu2@illinois.edu">Email</a>
        <a href="https://www.linkedin.com/in/suraj-duvvapu-634833288/" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://github.com/SurajDuvvapu" target="_blank" rel="noopener">GitHub</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year"></span> Suraj Duvvapu</span>
      <span>Built with plain HTML, CSS &amp; JS &middot; Deployed on GitHub Pages</span>
    </div>
  </div>
</footer>

<script src="../script.js"></script>
<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

ARROW_LEFT = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="transform: scaleX(-1);"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_RIGHT = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

def default_media_html(org_slug):
    """Placeholder media frame used until a page defines its own `media` (a
    list of (src, alt, caption) tuples rendered as a media gallery, see the
    tesla entry for an example)."""
    return (
        '<div class="media-frame reveal">\n'
        '    Add a photo, render, CAD screenshot, or diagram here. '
        f'Replace this placeholder frame in {org_slug}.html.\n'
        '  </div>'
    )


def media_gallery_html(images):
    """Builds a 3-up (responsive) image gallery. `images` is a list of
    (src, alt, caption) tuples, with `src` relative to the experience/
    or projects/ folder (e.g. "../assets/tesla/gantry-system.jpg")."""
    figures = "\n    ".join(
        f'<figure>\n'
        f'      <div class="media-thumb">\n'
        f'        <img src="{src}" alt="{alt}" loading="lazy" />\n'
        f'      </div>\n'
        f'      <figcaption>{caption}</figcaption>\n'
        f'    </figure>'
        for src, alt, caption in images
    )
    return f'<div class="media-gallery reveal">\n    {figures}\n  </div>'

EXPERIENCE = [
    dict(
        slug="tesla", category="work", org="Tesla", title="Mechanical Design Engineering Intern",
        filled=True,
        dates="July 2026 – December 2026 (Tentative)", location="Elgin, Illinois",
        lede="Designed automation hardware, including gantry systems, robotic end-of-arm tooling, and conveyance, for specialized, high-volume manufacturing lines.",
        note="Some details below are intentionally generalized or omitted to keep proprietary Tesla program and process information private.",
        media=[
            ("../assets/tesla/gantry-system.jpg",
             "Dual-axis linear gantry system with cable carriers, representative of the FESTO gantry systems designed for automated pick-and-place operations",
             "Representative dual-axis linear gantry system, illustrative of the FESTO gantry platforms used for automated pick-and-place operations."),
            ("../assets/tesla/fanuc-robot.jpg",
             "Six-axis FANUC industrial robot arm, the type of robot platform equipped with custom end-of-arm tooling",
             "Representative six-axis FANUC robot, the platform type equipped with the custom end-of-arm tooling (EOAT) designed during this internship."),
            ("../assets/tesla/tesla-logo.png",
             "Tesla logo",
             "Tesla, Mechanical Design Engineering Intern."),
        ],
        overview="As a Mechanical Design Engineering Intern, I designed hardware for Tesla's automated manufacturing lines: specialized systems built to handle nuanced, labor-intensive processes at high production volume. My work spanned the mechanical stack of these lines end to end, from motion systems and robotic tooling to the structural and material-handling components that tie a line together. I worked within a cross-functional project team to keep designs aligned with program direction and schedule.",
        what_i_did="I designed single- and double-axis FESTO gantry systems for automated pick-and-place and process operations, including a double-axis system that picked up a tray of product, removed the individual parts from their packaging, transferred them into an oven to bake, and removed them once complete. I designed End of Arm Tooling (EOAT) for FANUC robots, along with small actuator-driven assemblies for holdowns, pick-and-place, and alignment tasks. I also designed supporting mechanical systems, including funnels, chutes, plates, and conveyor systems, to move product through each line, as well as wire packs and wiring pathways for finished assemblies.</p>\n      <p>I validated robot, gantry, and actuator designs through FEA in SolidWorks, checking weight, sizing, and moments of inertia and how those factors changed with speed, and I validated designs for manufacturing, assembly, and service feasibility against engineering requirements before releasing component designs, 2D drawings, and bills of materials (BOMs). I created timing diagrams for all robotic components to coordinate motion sequencing across each line. I worked with cross-functional teams, including engineering, supply chain, production, and service, to resolve issues as they came up, and I participated in sourcing and supplier relationship management. I also designed several shop-floor tools and workbenches.",
        tools_prose="All CAD modeling, FEA validation, and drawings were done in SolidWorks, applying GD&T, Design for Manufacturing (DFM), and Design for Assembly (DFA) principles throughout, and reporting FEA/DFM study findings to the team. Applied academic engineering principles and lean strategies to solve design problems. Worked across a range of materials, including aluminum and steel (sheet metal and machined variants), Delrin, and various plastics.",
        outcome="Released 20+ parts and assemblies to production, contributed to 60+ parts and assemblies overall, and created or contributed to 60+ engineering drawings.",
        tags=["SolidWorks", "FEA", "GD&T", "DFM/DFA", "FESTO Gantry Systems", "FANUC EOAT"],
        links=[("Company site", "https://www.tesla.com")],
    ),
    dict(
        slug="collins-aerospace", category="work", org="Collins Aerospace", title="Manufacturing Engineering and Operations Co-Op",
        filled=True,
        dates="June 2025 – December 2025", location="Rockford, Illinois",
        lede="Designed custom shop-floor tooling and fixtures for military aircraft manufacturing programs, including the C-17, and supported production operations from tooling through shipping.",
        note="Some details below are intentionally generalized or omitted to keep proprietary Collins Aerospace program and process information private.",
        overview="As a Manufacturing Engineering and Operations Co-Op at Collins Aerospace (a division of RTX, formerly Raytheon Technologies), I supported manufacturing engineering and production operations for military aircraft programs, including the C-17. My work centered on designing custom shop-floor tooling and fixtures used directly by mechanics on the line, while also supporting the operations side of production &mdash; tracking unit status for customer reporting and resolving cross-functional issues that could hold up shipments.",
        what_i_did="I designed and developed 20+ custom shop-floor tools and fixtures in Siemens NX, including a multi-component C-17 actuator crimping tool, applying GD&amp;T and Design for Assembly (DFA) principles such as rail guides and snap-fit features; this tool reduced assembly time in its process step by 70%. I oversaw CNC milling for all custom tools and managed tooling for a shop floor of over 30 mechanics.</p>\n      <p>I also 3D printed and designed 300+ custom shadowboards for mechanics&rsquo; benches using Siemens NX and BambuLab printers, and developed a Python-based NX automation script using expressions that cut shadowboard design time by 50%. On the operations side, I developed and maintained customer report books for 5 product lines in Excel, tracking the manufacturing status of 300+ units across the full production timeline, and worked cross-functionally with quality, contracts, and shipping teams to process triages and coordinate shipments for 100+ units &mdash; resolving issues such as holds, incorrect documentation, and shipment inaccuracies.",
        tools_prose="Modeled and designed tooling in Siemens NX, applying GD&amp;T and DFA principles, and used NX&rsquo;s expression-driven automation to script parametric shadowboard designs in Python. 3D printed fixtures and shadowboards on BambuLab printers, oversaw CNC milling for custom tools, and used Excel to build and maintain customer report books tracking production status across product lines.",
        outcome="Released 20+ custom tools and fixtures to the shop floor, including a C-17 crimping tool that cut assembly time in its step by 70%; delivered 300+ custom shadowboards while cutting shadowboard design time in half; and kept customer-facing report books current across 5 product lines and 300+ units, supporting on-time shipment of 100+ units by resolving quality, documentation, and shipping issues as they arose.",
        tags=["Siemens NX", "GD&T", "DFA", "CNC Machining", "3D Printing", "Python", "Lean Manufacturing", "Excel"],
        links=[("Company site", "https://www.collinsaerospace.com")],
    ),
    dict(
        slug="midwest-nice", category="research", org="University of Illinois, Midwest NICE Aerospace Engineering Group",
        title="Undergraduate Researcher",
        dates="Placeholder dates", location="Urbana-Champaign, IL",
        lede="Placeholder one-sentence summary of the research focus and your role in it.",
        overview="Replace with context on the group's research area and the specific question your work addressed.",
        what_i_did="Replace with specifics: experiments run, models built, data collected/analyzed, or hardware built and tested.",
        tools_prose="Replace with the specific simulation, data-analysis, or lab tools/software you used.",
        outcome="Replace with the result: a finding, a working prototype, a paper/poster, or a dataset that advanced the project.",
        tags=["Research", "Data Analysis"],
        links=[("Research group site", "#")],
    ),
    dict(
        slug="baur-research-group", category="research", org="University of Illinois, Baur Research Group",
        title="Undergraduate Researcher",
        dates="Placeholder dates", location="Urbana-Champaign, IL",
        lede="Placeholder one-sentence summary of the research focus and your role in it.",
        overview="Replace with context on the lab's research area (e.g. structures/materials) and the specific question your work addressed.",
        what_i_did="Replace with specifics: specimens fabricated or tested, simulations run, or analysis performed.",
        tools_prose="Replace with the specific fabrication, testing, or simulation tools/software you used.",
        outcome="Replace with the result: a finding, a working test setup, or data that advanced the project.",
        tags=["Research", "Materials/Structures"],
        links=[("Research group site", "#")],
    ),
    dict(
        slug="motion-teaming-lab", category="research", org="University of Maryland, Motion and Teaming Laboratory",
        title="Intern",
        dates="Placeholder dates", location="College Park, MD",
        lede="Placeholder one-sentence summary of the lab's focus and your role.",
        overview="Replace with context on the lab's research area (e.g. robotics, human-robot teaming) and where your work fit in.",
        what_i_did="Replace with specifics: hardware built, code written, experiments run, or data collected.",
        tools_prose="Replace with the specific tools/software/languages you used.",
        outcome="Replace with the result: a working system, a finding, or a contribution to an ongoing project.",
        tags=["Robotics", "Systems"],
        links=[("Lab site", "#")],
    ),
    dict(
        slug="formula-sae", category="leadership", org="Illini Electric Motorsports, Formula SAE",
        title="Aerodynamics Project Lead",
        dates="Placeholder dates", location="Urbana-Champaign, IL",
        lede="Placeholder one-sentence summary: led the team's aero package design.",
        overview="Replace with context on the team, the car program/season, and your role leading the aero subteam.",
        what_i_did="Replace with specifics: CFD studies run, wing/diffuser/undertray design, wind-tunnel or track testing, and team leadership.",
        tools_prose="Replace with the specific CFD/CAD tools (e.g. SolidWorks, ANSYS Fluent) and manufacturing methods you used.",
        outcome="Replace with the result: downforce/drag numbers achieved, competition placement, or parts manufactured and raced.",
        tags=["CFD", "Aerodynamics", "Team Leadership"],
        links=[("Team site", "#")],
    ),
]

PROJECTS = [
    dict(
        slug="fea-final-project", category="projects", org="Finite Element Analysis", title="FEA Final Project",
        dates="Placeholder dates", location="University of Illinois",
        lede="Placeholder one-sentence summary of the structure/component analyzed and the goal of the project.",
        overview="Replace with the problem statement: what structure or component you modeled, and what question the analysis needed to answer.",
        what_i_did="Replace with specifics: mesh strategy, boundary conditions/loads, material models, and solver settings.",
        tools_prose="Replace with the specific FEA software used (e.g. ANSYS, Abaqus) and any scripting/automation.",
        outcome="Replace with the result: stresses/deflections found, design changes recommended, validation against hand calcs or test data.",
        tags=["FEA", "Structural Analysis"],
        links=[("Report / code", "#")],
    ),
    dict(
        slug="fea-midterm-project", category="projects", org="Finite Element Analysis", title="FEA Midterm Project",
        dates="Placeholder dates", location="University of Illinois",
        lede="Placeholder one-sentence summary of the analysis performed.",
        overview="Replace with the problem statement and scope of the project.",
        what_i_did="Replace with specifics: mesh strategy, boundary conditions/loads, material models, and solver settings.",
        tools_prose="Replace with the specific FEA software and methods used.",
        outcome="Replace with the result and what it showed.",
        tags=["FEA", "Structural Analysis"],
        links=[("Report / code", "#")],
    ),
    dict(
        slug="ae353-final-project", category="projects", org="AE 353: Aerospace Control Systems", title="AE 353 Final Project",
        dates="Placeholder dates", location="University of Illinois",
        lede="Placeholder one-sentence summary of the dynamic system modeled and controlled.",
        overview="Replace with the problem statement: the system's dynamics and the control objective.",
        what_i_did="Replace with specifics: the controller designed (e.g. state feedback, LQR), simulation setup, and tuning process.",
        tools_prose="Replace with the specific tools/languages used (e.g. Python, MATLAB/Simulink).",
        outcome="Replace with the result: performance achieved, stability margins, or simulation results.",
        tags=["Controls", "Dynamics", "Simulation"],
        links=[("Report / code", "#")],
    ),
    dict(
        slug="ae353-project-2", category="projects", org="AE 353: Aerospace Control Systems", title="AE 353 Project 2",
        dates="Placeholder dates", location="University of Illinois",
        lede="Placeholder one-sentence summary of the system modeled and controlled.",
        overview="Replace with the problem statement: the system's dynamics and the control objective.",
        what_i_did="Replace with specifics: the controller designed, simulation setup, and tuning process.",
        tools_prose="Replace with the specific tools/languages used.",
        outcome="Replace with the result and what it showed.",
        tags=["Controls", "Dynamics", "Simulation"],
        links=[("Report / code", "#")],
    ),
    dict(
        slug="ae370-final-project", category="projects", org="AE 370: Numerical Methods", title="AE 370 Final Project",
        dates="Placeholder dates", location="University of Illinois",
        lede="Placeholder one-sentence summary of the numerical method implemented and the problem it solved.",
        overview="Replace with the problem statement and why a numerical approach was needed.",
        what_i_did="Replace with specifics: the numerical scheme implemented, discretization, verification/validation approach.",
        tools_prose="Replace with the specific language/libraries used (e.g. Python, NumPy).",
        outcome="Replace with the result: accuracy achieved, convergence behavior, or comparison to analytical/experimental results.",
        tags=["Numerical Methods", "Simulation"],
        links=[("Report / code", "#")],
    ),
]


def build_nav_html(prev_item, next_item, section_id, crumb_label):
    back = f'<a href="../index.html#{section_id}" class="link-arrow">Back to all {crumb_label.lower()}</a>'
    if prev_item is None and next_item is None:
        return back
    prev_link = f'<a href="{prev_item["slug"]}.html" class="link-arrow">{ARROW_LEFT}&nbsp;{prev_item["org"]}</a>'
    next_link = f'<a href="{next_item["slug"]}.html" class="link-arrow">{next_item["org"]}&nbsp;{ARROW_RIGHT}</a>'
    return f"{prev_link}\n    {back}\n    {next_link}"


def render_group(items, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    # group items by category so prev/next cycles within the same category
    by_category = {}
    for item in items:
        by_category.setdefault(item["category"], []).append(item)

    for item in items:
        cat = CATEGORY_META[item["category"]]
        siblings = by_category[item["category"]]
        if len(siblings) > 1:
            i = siblings.index(item)
            prev_item = siblings[(i - 1) % len(siblings)]
            next_item = siblings[(i + 1) % len(siblings)]
        else:
            prev_item = next_item = None

        tag_html = "\n        ".join(f'<span class="tag">{t}</span>' for t in item["tags"])
        links_html = "\n        ".join(
            f'<li><a href="{href}" target="_blank" rel="noopener">{label} &rarr;</a></li>'
            for label, href in item["links"]
        )
        note_html = (
            f'<p class="text-muted reveal" style="font-size:0.92rem;font-style:italic;margin-top:0.6rem;max-width:700px;">{item["note"]}</p>'
            if item.get("note") else ""
        )
        media_html = (
            media_gallery_html(item["media"]) if item.get("media") else default_media_html(item["slug"])
        )
        html = TEMPLATE.format(
            title=item["title"],
            org=item["org"],
            org_slug=item["slug"],
            lede=item["lede"],
            lede_plain=item["lede"],
            dates=item["dates"],
            location=item["location"],
            overview=item["overview"],
            what_i_did=item["what_i_did"],
            tools_prose=item["tools_prose"],
            outcome=item["outcome"],
            p_class="" if item.get("filled") else ' class="placeholder"',
            note_html=note_html,
            media_html=media_html,
            tag_html=tag_html,
            links_html=links_html,
            section_id=cat["id"],
            crumb_label=cat["label"],
            nav_html=build_nav_html(prev_item, next_item, cat["id"], cat["label"]),
            nav_class="" if (prev_item or next_item) else " detail-nav-solo",
        )
        path = os.path.join(out_dir, f"{item['slug']}.html")
        with open(path, "w") as f:
            f.write(html)
        print("wrote", path)


render_group(EXPERIENCE, os.path.join(ROOT, "experience"))
render_group(PROJECTS, os.path.join(ROOT, "projects"))
