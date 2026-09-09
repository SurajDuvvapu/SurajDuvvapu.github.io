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
    <article class="prose">
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
      {links_section_html}
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


def report_figure(items, caption):
    """Builds one inline report-style figure to drop directly inside a prose
    field (overview/what_i_did/etc.), so images can sit right next to the
    paragraph they illustrate instead of being dumped in one gallery at the
    top of the page.

    `items` is a list of 1-3 (src, sublabel) tuples, one per image cell
    (e.g. a Python-vs-Abaqus comparison is 2 items). `src` is relative to
    the experience/ or projects/ folder, e.g. "../assets/foo/bar.png"; pass
    src=None to render a placeholder box (with `sublabel` as the note of
    what image belongs there) until the real image is ready to drop in, or
    a raw "<svg ...>...</svg>" string to embed a hand-drawn diagram inline
    instead of an <img> (used when the report figure was vector-drawn, e.g.
    a TikZ sketch, and has no source image file to link to).
    `caption` is the figure caption shown below the image(s).
    """
    cells = []
    for src, sublabel in items:
        if src and src.lstrip().startswith("<svg"):
            img = src
            sub = f'<div class="figure-sublabel">{sublabel}</div>' if sublabel else ""
        elif src:
            img = f'<img src="{src}" alt="{sublabel or caption}" loading="lazy" />'
            sub = f'<div class="figure-sublabel">{sublabel}</div>' if sublabel else ""
        else:
            img = f'<div class="figure-placeholder">{sublabel or "Add image here"}</div>'
            sub = ""
        cells.append(f'<div>{img}{sub}</div>')
    variant = {2: " figure-pair", 3: " figure-triple"}.get(len(items), "")
    media = "".join(cells)
    return (
        f'<figure class="report-figure{variant}">\n'
        f'      <div class="figure-media">{media}</div>\n'
        f'      <figcaption>{caption}</figcaption>\n'
        f'    </figure>'
    )


# Hand-drawn recreation of the custom arched-plate boundary-condition sketch
# from the FEA report (originally a LaTeX/TikZ figure, so there's no source
# image file for it). Faithful to the report's geometry: 0.50m wide, 0.30m
# base height, curved top rising to 0.40m at the center.
ARCH_SKETCH_SVG = """<svg viewBox="0 0 660 480" role="img" aria-labelledby="archSketchTitle" font-family="-apple-system, 'Helvetica Neue', Arial, sans-serif">
        <title id="archSketchTitle">Custom arched-plate heat transfer problem: geometry and boundary conditions</title>
        <defs>
          <marker id="archArrowRed" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#d1453b"/></marker>
          <marker id="archArrowPurple" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto"><path d="M0,0 L8,0 L4,8 Z" fill="#8452d5"/></marker>
          <marker id="archArrowGray" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#6e6e73"/></marker>
        </defs>
        <path d="M210,380 L560,380 L560,170 C476,100 294,100 210,170 Z" fill="none" stroke="#1d1d1f" stroke-width="2.5"/>
        <g stroke="#d1453b" stroke-width="2.2">
          <line x1="161" y1="338" x2="202" y2="338" marker-end="url(#archArrowRed)"/>
          <line x1="161" y1="296" x2="202" y2="296" marker-end="url(#archArrowRed)"/>
          <line x1="161" y1="254" x2="202" y2="254" marker-end="url(#archArrowRed)"/>
          <line x1="161" y1="212" x2="202" y2="212" marker-end="url(#archArrowRed)"/>
        </g>
        <text x="153" y="279" fill="#d1453b" font-size="19" text-anchor="end">q<tspan font-size="13" dy="-6">p</tspan><tspan dy="6"> = 6000 W/m&sup2;</tspan></text>
        <line x1="560" y1="170" x2="560" y2="380" stroke="#0071e3" stroke-width="5"/>
        <text x="572" y="279" fill="#0071e3" font-size="19" text-anchor="start">T = 75&deg;C</text>
        <g stroke="#8452d5" stroke-width="2.2">
          <line x1="280" y1="107" x2="280" y2="120" marker-end="url(#archArrowPurple)"/>
          <line x1="350" y1="86" x2="350" y2="99" marker-end="url(#archArrowPurple)"/>
          <line x1="420" y1="86" x2="420" y2="99" marker-end="url(#archArrowPurple)"/>
          <line x1="490" y1="107" x2="490" y2="120" marker-end="url(#archArrowPurple)"/>
        </g>
        <text x="385" y="55" fill="#8452d5" font-size="19" text-anchor="middle">h = 12, T&#8734; = 25&deg;C</text>
        <text x="385" y="415" fill="#4a4a4f" font-size="18" text-anchor="middle">Insulated bottom edge</text>
        <g stroke="#6e6e73" stroke-width="1.8">
          <line x1="105" y1="436" x2="157" y2="436" marker-end="url(#archArrowGray)"/>
          <line x1="105" y1="436" x2="105" y2="384" marker-end="url(#archArrowGray)"/>
        </g>
        <text x="167" y="441" fill="#6e6e73" font-size="16">x</text>
        <text x="98" y="374" fill="#6e6e73" font-size="16" text-anchor="end">y</text>
      </svg>"""

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
        lede="Designed shop-floor tooling and layouts and built a real-time tracking system for repair units in Collins Aerospace's Maintenance, Repair, and Operations (MRO) shop, supporting Ram Air Turbines, generators, and actuators.",
        note="Some details below are intentionally generalized or omitted to keep proprietary Collins Aerospace program and process information private.",
        media=[
            ("../assets/collins/rat-test-stand.jpg",
             "Ram Air Turbine (RAT) with propeller blades mounted on a test stand, representative of the units serviced in the repair shop",
             "Representative Ram Air Turbine (RAT) on a test stand, illustrative of the RAT, generator, and actuator units serviced in the repair shop."),
            ("../assets/collins/collins-aerospace-logo.png",
             "Collins Aerospace logo",
             "Collins Aerospace, Manufacturing Engineering and Operations Co-Op."),
        ],
        overview="As a Manufacturing Engineering and Operations Co-Op in the Maintenance, Repair, and Operations (MRO) division at Collins Aerospace (a division of RTX, formerly Raytheon Technologies) in Rockford, Illinois, I supported the repair shop that services Ram Air Turbines (RATs), generators, actuators, and other rotating and hydraulic components. My work spanned manufacturing engineering, designing tooling, fixtures, and shop-floor layouts, and operations, where I built and maintained the systems used to track units and shipments through the repair process and worked directly with customers.",
        what_i_did="I designed and developed 20+ custom shop-floor tools and fixtures in Siemens NX for the repair shop, including hand-held tools and pipe fixtures. One specific example was a multi-component C-17 actuator crimping tool, built applying GD&amp;T and Design for Assembly (DFA) principles such as rail guides and snap-fit features, which alone reduced assembly time in its process step by 70%. I also designed workbenches for the testing area, laid out the shop floor for the Paint and Wire departments, oversaw CNC milling for all custom tools, and managed tooling for a shop floor of over 30 mechanics.</p>\n      <p>I 3D printed and designed 300+ custom shadowboards for mechanics&rsquo; benches using Siemens NX and BambuLab printers, developing a Python-based NX automation script using expressions that cut shadowboard design time by 50%. I also managed purchasing and inventory for the office and shop floor, sourcing shop tools, 3D printers, workbenches, and office supplies, and designed custom nametags for everyone in the repair department.</p>\n      <p>On the operations side, I led the installation of a Real-Time Location System (RTLS) to track repair units across the shop floor, then built a live heatmap in Python to visualize unit location and shop-floor activity in real time. I developed and maintained customer report books for 5 product lines in Excel, tracking every unit through test (flagging turnbacks, issues, and holdups) and tracking every unit shipped out of the facility. I worked cross-functionally with quality, contracts, and shipping teams to process triages and coordinate shipments for 100+ units, and worked directly with clients and customers, delivering product updates, leading facility walkthroughs, and answering questions.",
        tools_prose="Modeled and designed tooling, fixtures, and shop-floor layouts in Siemens NX, applying GD&amp;T and DFA principles, and used NX&rsquo;s expression-driven automation to script parametric shadowboard designs in Python. Installed and configured a Real-Time Location System (RTLS) and built a live tracking heatmap in Python. 3D printed fixtures and shadowboards on BambuLab printers, oversaw CNC milling for custom tools, and used Excel to build and maintain customer report books and unit-tracking records across product lines.",
        outcome="Released 20+ custom tools, fixtures, and workbenches to the shop floor, one specific example being a C-17 crimping tool that cut assembly time in its step by 70%, and redesigned the Paint and Wire shop-floor layouts. Delivered 300+ custom shadowboards while cutting shadowboard design time in half, and stood up an RTLS-based live heatmap that gave the shop real-time visibility into unit location and status. Kept customer-facing report books current across 5 product lines and 300+ units, tracked every unit through test and shipment, and supported on-time delivery of 100+ shipped units by resolving quality, documentation, and shipping issues as they arose.",
        tags=["Siemens NX", "GD&T", "DFA", "CNC Machining", "3D Printing", "Python", "RTLS", "Lean Manufacturing", "Excel"],
        links=[("Company site", "https://www.collinsaerospace.com")],
    ),
    dict(
        slug="midwest-nice", category="research", org="University of Illinois, Midwest NICE Aerospace Engineering Group",
        title="Undergraduate Research Assistant — Drone-LiDAR-CFD Greenhouse Fertigation Study",
        filled=True,
        dates="August 2026 – Present", location="Urbana-Champaign, IL",
        lede="Supporting an AE 497 research project (led by Pratham Rao Puskur) that is developing a drone-based LiDAR and CFD workflow to diagnose fertigation non-uniformity in a deep winter greenhouse, focused on higher-fidelity CAD modeling and CFD simulation of the greenhouse airflow.",
        note="This project is ongoing (started August 2026). The descriptions below reflect the current research plan — what the project is set up to investigate and my role in it — rather than completed results, and will be updated as the work and any findings develop.",
        media=[
            ("../assets/midwest-nice/deep-winter-greenhouse-render.png",
             "Rendered CAD concept of a deep winter greenhouse with a steep, south-facing double-glazed glass wall",
             "Concept render of the deep winter greenhouse design the project is modeling — a passive-solar structure with a steep, south-facing glazed wall for heat retention through winter."),
        ],
        overview=(
            "Greenhouse fertilizer delivery is usually coupled directly to irrigation (fertigation), which means emitter clogging, pressure imbalance, drainage irregularity, and uneven greenhouse airflow can all cause nutrient delivery to vary spatially even when the nominal nutrient recipe is correct. The Midwest NICE group's project, led by Pratham Rao Puskur, is investigating whether a drone equipped with LiDAR can serve as a mobile sensing platform inside a deep winter greenhouse: mapping canopy and structural geometry accurately enough to feed a computational fluid dynamics (CFD) model of the greenhouse's internal airflow, and using that combination to flag likely dry spots, weak-growth zones, stagnant regions, and other delivery-related anomalies for closer inspection. I joined the project in August 2026 as the AE 298 undergraduate research assistant, brought on specifically to push the CAD and CFD side of the workflow to a higher standard than the initial models."
        ),
        what_i_did=(
            "My focus is on the two pieces the project identified as needing the most work: building a CAD model of the deep winter greenhouse that faithfully preserves its real geometry (roof shape, ridge and eave height, roll-up side vents, hinged ridge vents, row spacing and aisles) rather than a symbolic approximation, and running the CFD studies on top of it. The plan follows a staged sequence: first mapping the existing greenhouse and validating LiDAR accuracy against known targets and manual plant measurements, then measuring the baseline airflow field with the drone absent to avoid propeller-downwash contamination, and building a baseline CFD model validated against anemometer measurements before comparing candidate airflow layouts.</p>\n      "
            "<p>From there, the workflow calls for comparing four CAD-modeled airflow layouts under matched boundary conditions &mdash; the existing baseline, a cross-flow arrangement, a side-inlet/ridge-outlet arrangement, and a fan- or baffle-assisted layout &mdash; changing one design variable at a time while holding the greenhouse envelope constant, and evaluating them on canopy-zone uniformity and stagnant volume rather than bulk air exchange alone. Only after a layout is selected and the CFD model is validated does the plan move on to tracer-droplet deposition testing and, eventually, feasibility testing with actual nutrient-containing droplets.</p>\n      "
            "<p>Because the LiDAR-derived canopy geometry will eventually feed directly into the CFD domain (as a measured canopy envelope or a porous zone with experimentally supported drag properties), the CAD and CFD work is being built with that hand-off in mind from the start, rather than as a standalone geometry exercise."
        ),
        tools_prose=(
            "Building CAD models of the greenhouse envelope, vents, and crop rows, and setting up and running the corresponding CFD simulations, including mesh-independence testing across coarse, medium, and fine grids and near-wall mesh sizing based on a target dimensionless wall distance (y⁺), following the SST k-ω turbulence model identified in the project's literature review as best matched to prior validated greenhouse CFD studies."
        ),
        outcome=(
            "This work is in progress. Pratham's target for the project is an AIAA Journal submission; my contributions so far are the higher-fidelity CAD models and CFD simulation runs the project needed, with results to be added here as the staged experimental sequence (LiDAR validation, baseline CFD validation, layout comparison, and eventually droplet-transport testing) is carried out."
        ),
        tags=["CFD", "CAD Modeling", "LiDAR", "Airflow Simulation", "Greenhouse Systems"],
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
        slug="2d-thermal-finite-element-solver", category="projects", org="Finite Element Analysis", title="2D Thermal Finite Element Solver",
        filled=True,
        dates="Spring 2026", location="University of Illinois",
        lede="Built a 2D finite element solver in Python for steady-state and transient heat conduction, verified against Abaqus on both provided test cases and a custom problem built from scratch.",
        media=[
            ("../assets/fea-final-project/custom-arch-python.png",
             "Temperature contour plot of the custom arched-plate problem, solved with the Python FEA solver",
             "The custom arched-plate problem, the project&rsquo;s centerpiece result: a geometry designed from scratch and solved entirely with my own code."),
            ("../assets/fea-final-project/steady-state-hole-python.png",
             "Temperature contour plot of the fine rectangular mesh with a circular hole, solved with the Python FEA solver",
             "Steady-state validation on a curved, non-rectangular mesh &mdash; one of four provided test cases matched against Abaqus."),
            ("../assets/fea-final-project/forward-euler-1p1-dtcr-unstable.png",
             "Forward Euler temperature history plot showing numerical instability once the critical time step is exceeded",
             "The transient solver deliberately pushed past stability: Forward Euler oscillating and diverging once the time step exceeds &Delta;t_cr."),
        ],
        overview="This project turned a finite element solver I&rsquo;d built earlier in the semester for structural problems into a full two-dimensional thermal analysis tool, covering both steady-state and transient heat conduction. The question driving it was how much of a general FEA framework, equation numbering, assembly, and a partitioned solve, carries over to a completely different physical problem once the right element-level physics and boundary conditions are swapped in. I verified the solver at every stage against Abaqus, including on a thermal problem and mesh I designed myself rather than one that was handed to me.",
        what_i_did=(
            "The reused core of the solver was the FEA infrastructure: equation numbering, the location matrix, partitioned global assembly, and the partitioned solve. On top of that I built the physics for a steady-state thermal problem, (K<sub>k</sub> + K<sub>c</sub>)T = P<sub>Q</sub> + P<sub>q</sub> + P<sub>c</sub>, using the same isoparametric Q4 shape functions, Jacobian, and Gauss quadrature routines from the structural code, but swapping the strain-displacement matrix for a temperature-gradient matrix to form the conduction matrix. The genuinely new part was the boundary conditions: an edge-based applied heat flux, integrated as &int; N<sup>T</sup>q<sup>p</sup>t d&Gamma; over the loaded edge with one-dimensional Gauss quadrature, and edge-based convection, which needed both a convection matrix (row-sum lumped, per the project&rsquo;s requirements) and a convection load vector.</p>\n      "
            "<p>I validated the steady-state solver against Abaqus on four meshes, coarse and fine rectangles, a distorted rectangular mesh, and a mesh with a circular hole cut into it, comparing temperature contours side by side. All four matched Abaqus closely, including the distorted and curved-hole cases, confirming that the isoparametric mapping and edge integration were working correctly on non-rectangular elements and not just the easy rectangular ones.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-final-project/steady-state-hole-python.png", "Python solution"),
                    ("../assets/fea-final-project/steady-state-hole-abaqus.png", "Abaqus solution"),
                ],
                "Temperature contours for the fine mesh with a circular hole: the Python solver (left) versus Abaqus (right). The two match closely, confirming the isoparametric mapping and edge-integration routines handle curved, non-rectangular elements correctly.",
            )
            + "\n      <p>I also used the solver to compute heat flux across an internal edge shared by two elements, evaluated once from each element. The two values didn&rsquo;t match exactly, and that&rsquo;s expected: the temperature field is continuous across element boundaries, but its gradient (and therefore the heat flux, since q = &minus;k&nabla;T) generally isn&rsquo;t. It&rsquo;s a good illustration of a real FEA post-processing subtlety rather than a bug, and the mismatch would shrink under mesh refinement.</p>\n      "
            "<p>To test the solver on something it hadn&rsquo;t seen, I built an entirely new steady-state problem from scratch in Abaqus CAE: an arched plate with a curved top edge, a fixed heat flux on the left edge, a fixed temperature on the right edge, a convection boundary on the curved top, and an insulated bottom, meshed with more than 100 distorted DC2D4 elements. My Python solver matched the Abaqus result closely here too, which was the real test of whether the implementation generalized past the given test cases.</p>\n      "
            + report_figure(
                [(ARCH_SKETCH_SVG, None)],
                "The custom arched heat-transfer problem, built from scratch in Abaqus CAE: a fixed heat flux on the left edge, a fixed temperature on the right edge, convection on the curved top edge, and an insulated bottom edge.",
            )
            + report_figure(
                [
                    ("../assets/fea-final-project/custom-arch-python.png", "Python solution"),
                    ("../assets/fea-final-project/custom-arch-abaqus.png", "Abaqus solution"),
                ],
                "Temperature contours for the custom arched-plate problem: Python (left) versus Abaqus (right). The two solutions agree closely, including the curved contour bands near the convection boundary at the top.",
            )
            + "\n      <p>The last extension was time: I added a row-sum lumped capacitance matrix and implemented two time-integration schemes, explicit Forward Euler and implicit Crank-Nicolson, to solve the transient version of the same system. For Forward Euler I computed the critical time step from the largest eigenvalue of the system matrix and deliberately ran the solver at 0.1, 0.9, and 1.1 times that critical step to show its conditional stability directly: the first two settle smoothly toward steady state, and the 1.1&times; case visibly oscillates and diverges, exactly as the stability theory predicts. Crank-Nicolson, run at time steps well beyond Forward Euler&rsquo;s stability limit, stayed stable in every case, though accuracy visibly degraded into oscillation as the time step grew.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-final-project/forward-euler-0p1-dtcr.png", "0.1 Δtᴄᵣ — stable"),
                    ("../assets/fea-final-project/forward-euler-0p9-dtcr.png", "0.9 Δtᴄᵣ — stable"),
                    ("../assets/fea-final-project/forward-euler-1p1-dtcr-unstable.png", "1.1 Δtᴄᵣ — unstable"),
                ],
                "Forward Euler temperature histories at increasing fractions of the critical time step, for two nodes in the coarse rectangular mesh. Below the critical step the solution is smooth and converges; above it (1.1 &Delta;t_cr) the response visibly oscillates and diverges, exactly the conditional-stability behavior the theory predicts.",
            )
            + "\n      <p>I ran both schemes across two different mesh cases and tracked nodal temperature histories over time as each domain heated from a uniform initial temperature toward its steady-state distribution, covering the full arc from a static conduction solve to a stable, well-behaved transient one."
        ),
        tools_prose="Wrote the full solver, equation numbering, assembly, boundary conditions, and both time-integration schemes, from scratch in Python with NumPy, building on a structural FEA codebase from earlier in the course. Used Abaqus CAE and Abaqus/Standard, including DC2D4 thermal elements, to build the custom validation geometry and mesh and to independently solve every case for comparison. Used Matplotlib for all temperature contour and transient time-history plots.",
        outcome="Ended up with a working 2D thermal FEA solver that matched Abaqus temperature fields closely across five independent geometries, four given and one designed from scratch, and that correctly reproduced the textbook stability behavior of Forward Euler and Crank-Nicolson time integration, including inducing and confirming numerical instability once the Forward Euler critical time step was exceeded.",
        tags=["Python", "NumPy", "Finite Element Method", "Abaqus", "Heat Transfer", "Numerical Methods"],
        links=[],
    ),
    dict(
        slug="stress-concentration-and-plane-stress-validity-study", category="projects", org="Finite Element Analysis", title="Stress Concentration and Plane-Stress Validity Study",
        filled=True,
        dates="Spring 2026", location="University of Illinois",
        lede="Benchmarked FEA stress concentration around a circular hole against classical elasticity theory in Abaqus, then pushed the model through a finite-width parametric study and a 3D extension to find exactly where the plane-stress assumption stops holding.",
        media=[
            ("../assets/fea-midterm-project/s11-near-hole-finite-width.png",
             "S11 stress contour zoomed near the hole for the finite-width plate model",
             "Peak tensile stress concentration at the top of the hole in the finite-width model &mdash; the result the whole parametric study builds on."),
            ("../assets/fea-midterm-project/s33-3d-thick-plate-t400.png",
             "S33 out-of-plane stress contour for the thickest 3D plate model",
             "Out-of-plane stress in the 400&nbsp;mm-thick 3D model &mdash; the clearest visual evidence that plane stress no longer holds."),
            ("../assets/fea-midterm-project/stress-concentration-factor-comparison.png",
             "Plot comparing FEA-computed stress concentration factors to the reference curve across four plate widths",
             "FEA-computed stress concentration factors against the reference curve, within 2% across all four widths tested."),
        ],
        overview="This project worked through the classic problem of stress concentration around a circular hole in a loaded plate, building up in stages from a clean, idealized case to a fully three-dimensional one. I started with the textbook infinite-plate solution as a benchmark, verified it with a 2D finite element model, then deliberately narrowed the plate until the finite-width effects that theory ignores became significant, tracked how the stress concentration factor changed as a result, and finally extended the model into three dimensions to find out at what thickness the plane-stress assumption underlying the whole analysis actually stops being valid.",
        what_i_did=(
            "The first model was a quarter-symmetry Abaqus plate, 100&nbsp;mm &times; 100&nbsp;mm, with a 10&nbsp;mm hole radius and a uniform 1&nbsp;MPa tensile traction applied along the loaded edge, meant to approximate an infinite plate with a small hole in it. I used linear elastic, isotropic material properties (E&nbsp;=&nbsp;210,000&nbsp;MPa, &nu;&nbsp;=&nbsp;0.30), 2D plane-stress quadratic quadrilateral elements (CPS8), and a free mesh refined near the hole, where the stress gradients are steepest, and coarsened toward the far field to keep the model economical.</p>\n      "
            + report_figure(
                [("../assets/fea-midterm-project/mesh-quarter-symmetry.png", None)],
                "Quarter-symmetry mesh for the infinite-plate benchmark model, refined near the hole where stress gradients are steepest.",
            )
            + "\n      <p>Pulling the S11 and S22 stress contours confirmed the concentration builds exactly where theory predicts: a tensile peak near the top of the hole reaching roughly 3&sigma;, and a corresponding compressive region near the side of the hole in S22. Because that peak is a real physical feature of the solution rather than a meshing artifact, I set the contour limits to preserve it rather than clip it.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/s11-whole-domain-infinite-plate.png", "Whole domain"),
                    ("../assets/fea-midterm-project/s11-near-hole-infinite-plate.png", "Near-hole detail"),
                ],
                "S11 contours for the infinite-plate benchmark model: the tensile stress concentration peaks near the top of the hole, close to the theoretical 3&sigma; value.",
            )
            + report_figure(
                [
                    ("../assets/fea-midterm-project/s22-whole-domain-infinite-plate.png", "Whole domain"),
                    ("../assets/fea-midterm-project/s22-near-hole-infinite-plate.png", "Near-hole detail"),
                ],
                "S22 contours for the same model, showing the complementary compressive region near the side of the hole.",
            )
            + "\n      <p>To check the model quantitatively rather than just by eye, I extracted stress along two symmetry-edge paths, converted path distance to radial distance, and compared the result directly against the closed-form tangential stress solution &sigma;<sub>&theta;</sub> = (&sigma;/2)[1 + a&sup2;/r&sup2; &minus; (1 + 3a&#8308;/r&#8308;)cos&nbsp;2&theta;]. Along the y-axis (&theta;&nbsp;=&nbsp;90&deg;) the FEA curve approached the theoretical 3&sigma; peak at the hole boundary and decayed toward the far-field &sigma; as expected; along the x-axis (&theta;&nbsp;=&nbsp;0&deg;) it approached the theoretical &minus;&sigma; and recovered toward zero moving away from the hole. The agreement across both paths was close enough to confirm the quarter-symmetry model, boundary conditions, and mesh density were all doing their job before I started changing the geometry.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/theta-comparison-xaxis-infinite-plate.png", "Along x-axis (&theta; = 0&deg;)"),
                    ("../assets/fea-midterm-project/theta-comparison-yaxis-infinite-plate.png", "Along y-axis (&theta; = 90&deg;)"),
                ],
                "Abaqus path results versus the closed-form &sigma;<sub>&theta;</sub> solution &mdash; close agreement on both axes confirms the benchmark model.",
            )
            + "\n      <p>With the infinite-plate case validated, I intentionally broke the assumption it depends on: I narrowed the plate so the hole took up half its width (2a/w&nbsp;=&nbsp;0.5, with w&nbsp;=&nbsp;20&nbsp;mm), keeping the same material, boundary conditions, and mesh refinement strategy. Forcing the same load through a smaller net cross-section produced a noticeably larger stress concentration than the infinite-plate case, exactly as expected.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/s11-whole-domain-finite-width.png", "Whole domain"),
                    ("../assets/fea-midterm-project/s11-near-hole-finite-width.png", "Near-hole detail"),
                ],
                "S11 contours for the finite-width plate (2a/w = 0.5): the peak tensile stress near the hole is visibly higher than in the infinite-plate case.",
            )
            + "\n      <p>Repeating the same path-based comparison against the infinite-plate formula made the finite-width effect explicit: along the y-axis the Abaqus peak stress at the hole boundary now exceeded the theoretical 3&sigma; limit, and along the x-axis the compressive stress at the boundary was stronger than the analytical prediction, with a more pronounced overshoot before settling toward the far-field value. That's not a modeling error &mdash; it's exactly what should happen once the plate no longer satisfies the assumptions the infinite-plate formula was derived under.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/theta-comparison-xaxis-finite-width.png", "Along x-axis (&theta; = 0&deg;)"),
                    ("../assets/fea-midterm-project/theta-comparison-yaxis-finite-width.png", "Along y-axis (&theta; = 90&deg;)"),
                ],
                "The finite-width model diverges from the infinite-plate theory on both axes &mdash; expected, since the assumptions behind that formula no longer hold.",
            )
            + "\n      <p>That raised an obvious follow-up: how does the stress concentration factor actually trend as the plate gets wider and the finite-width effect fades? I built four more models at a fixed hole size (2a&nbsp;=&nbsp;20&nbsp;mm) but increasing widths &mdash; w&nbsp;=&nbsp;40, 50, 60, and 70&nbsp;mm (2a/w from 0.5 down to about 0.286) &mdash; pulled the peak S11 stress from each, and computed K<sub>t</sub>&nbsp;=&nbsp;&sigma;<sub>max</sub>/&sigma;<sub>nom</sub> against the nominal net-section stress &sigma;<sub>nom</sub>&nbsp;=&nbsp;&sigma;(w/(w&minus;2a)). All four FEA-computed K<sub>t</sub> values landed within 2% of a published reference curve fit, and both the FEA points and the reference curve moved the same direction: K<sub>t</sub> climbing back toward the infinite-plate limit of 3 as the width-to-hole ratio grew.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/s11-near-hole-w50.png", "w = 50 mm"),
                    ("../assets/fea-midterm-project/s11-near-hole-w60.png", "w = 60 mm"),
                    ("../assets/fea-midterm-project/s11-near-hole-w70.png", "w = 70 mm"),
                ],
                "S11 concentration near the hole across three of the four widths tested, all plotted on the same contour scale &mdash; the peak visibly relaxes as the plate widens.",
            )
            + report_figure(
                [("../assets/fea-midterm-project/stress-concentration-factor-comparison.png", None)],
                "FEA-computed stress concentration factors across all four widths, within 2% of the reference curve fit at every point.",
            )
            + "\n      <p>The last stage tested the assumption sitting underneath everything up to that point: plane stress. I took the w&nbsp;=&nbsp;40&nbsp;mm finite-width geometry from earlier and extended it into a full 3D, eighth-symmetry solid model at three thicknesses &mdash; t&nbsp;=&nbsp;4, 40, and 400&nbsp;mm (0.1w, 1.0w, and 10.0w) &mdash; using quadratic 3D brick elements, the same material properties and loading, and symmetry conditions on all three coordinate planes. The in-plane S11 stress concentration stayed anchored at the same geometric location, near the top of the hole, across all three thicknesses, which was reassuring on its own: the basic in-plane behavior doesn't change just because the plate gets thicker.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/s11-3d-thin-plate-t4.png", "t = 4 mm"),
                    ("../assets/fea-midterm-project/s11-3d-medium-plate-t40.png", "t = 40 mm"),
                    ("../assets/fea-midterm-project/s11-3d-thick-plate-t400.png", "t = 400 mm"),
                ],
                "S11 contours for the three 3D thickness models &mdash; the in-plane concentration holds its location and shape as thickness increases.",
            )
            + "\n      <p>The real story was in S33, the out-of-plane normal stress a true plane-stress model assumes is zero everywhere. For the thin plate (t&nbsp;=&nbsp;4&nbsp;mm) it stayed small, around 0.09&nbsp;MPa at the interior mid-plane and decaying to about 0.06&nbsp;MPa at the free surface &mdash; only on the order of 1&ndash;2% of the roughly 4.5&nbsp;MPa peak in-plane stress. For the medium plate (t&nbsp;=&nbsp;40&nbsp;mm) it jumped to about 0.95&nbsp;MPa at the mid-plane, more than 20% of the peak in-plane stress, and for the thick plate (t&nbsp;=&nbsp;400&nbsp;mm) it stayed near 1.0&nbsp;MPa through most of the interior before dropping off close to the free surface. Visually, the thick model's S33 field wasn't confined to a small region near the hole the way plane-stress theory would suggest &mdash; it persisted through most of the interior, which is the clearest sign the model had left plane stress behind.</p>\n      "
            + report_figure(
                [
                    ("../assets/fea-midterm-project/s33-3d-thin-plate-t4.png", "t = 4 mm"),
                    ("../assets/fea-midterm-project/s33-3d-medium-plate-t40.png", "t = 40 mm"),
                    ("../assets/fea-midterm-project/s33-3d-thick-plate-t400.png", "t = 400 mm"),
                ],
                "S33 (out-of-plane) contours across the same three thicknesses. A true plane-stress state would show zero everywhere &mdash; instead, S33 grows substantially with thickness.",
            )
            + report_figure(
                [
                    ("../assets/fea-midterm-project/through-thickness-s33-thin-t4.png", "t = 4 mm"),
                    ("../assets/fea-midterm-project/through-thickness-s33-thick-t400.png", "t = 400 mm"),
                ],
                "S33 through the plate thickness at the point of peak concentration, thin versus thick: the thin plate relaxes toward zero as theory predicts, while the thick plate stays elevated through nearly the whole interior.",
            )
            + "\n      <p>Taken together, the four stages traced a clear line from theory to its limits: the infinite-plate solution held up well under the quarter-symmetry benchmark, narrowing the plate produced exactly the departure from that theory the finite-width behavior predicts, the K<sub>t</sub> parametric sweep matched the reference curve to within 2% across four widths, and the 3D extension pinned down concretely where plane stress breaks down &mdash; solid at t&nbsp;=&nbsp;4&nbsp;mm, questionable by t&nbsp;=&nbsp;40&nbsp;mm, and clearly invalid by t&nbsp;=&nbsp;400&nbsp;mm."
        ),
        tools_prose="Built and solved every model in Abaqus/CAE and Abaqus/Standard: CPS8 quadratic plane-stress elements for the 2D quarter-symmetry models, and quadratic 3D brick elements for the eighth-symmetry solid models. Used Abaqus path tools to extract stress along symmetry-edge and through-thickness paths, and Matplotlib for all theory-comparison and stress-concentration-factor plots.",
        outcome="Came out of it with a 2D stress-concentration model that matched the infinite-plate theory closely, a finite-width correction that tracked a published curve fit to within 2% across four plate widths, and a concrete, thickness-based answer to when plane stress is (and isn't) a valid assumption: solid at t&nbsp;=&nbsp;4&nbsp;mm, questionable by t&nbsp;=&nbsp;40&nbsp;mm, and clearly invalid by t&nbsp;=&nbsp;400&nbsp;mm, where out-of-plane stress remained near 1&nbsp;MPa through most of the plate's interior.",
        tags=["Abaqus", "Finite Element Method", "Stress Analysis", "Structural Mechanics", "3D Modeling"],
        links=[],
    ),
    dict(
        slug="lqr-trajectory-tracking-and-state-estimation-racing-drone", category="projects", org="Aerospace Control Systems", title="LQR-Based Trajectory Tracking and State Estimation for a Racing Drone",
        filled=True,
        dates="Spring 2026", location="University of Illinois",
        lede="Designed an LQR state-feedback controller and a Luenberger-style observer that fly a simulated quadrotor racing drone through a multi-ring course from noisy marker-position measurements alone, completing 27 of 30 randomized trials for a 90% success rate.",
        media=[
            ("../assets/ae353-racing-drone/simulator-snapshot.png",
             "Simulator snapshot of the quadrotor drone near the ring course, with the surrounding track geometry visible",
             "Simulator snapshot of the drone operating in the ring-course environment, included to confirm testing happened in the full visual simulation and not only on logged state data."),
            ("../assets/ae353-racing-drone/aggregate-success-rate.png",
             "Bar chart showing a 90 percent success rate over 30 randomized simulation trials",
             "27 of 30 randomized trials completed the course successfully: a 90% success rate against the 70% design requirement."),
            ("../assets/ae353-racing-drone/single-run-xy-path.png",
             "Horizontal flight path of the drone compared with the moving target path generated by the trajectory planner",
             "Logged horizontal flight path (solid) against the moving target path (dashed) generated by the trajectory planner, including the small looping corrections used to line the drone up with each ring."),
        ],
        overview="This project asked for a controller that could fly a simulated quadrotor drone through a sequence of rings without crashing, using only noisy measurements of two small markers mounted on the rotors, while also reacting to the next ring&rsquo;s position and to other drones nearby. That combination made it a genuine systems problem rather than a single textbook exercise: the controller had to stabilize the drone, estimate its full state from an incomplete and noisy sensor model, track a moving target through the course, and avoid the floor, ring edges, and other traffic, all at the same time. The target was a 70% completion rate over 30 randomized simulations, a requirement chosen specifically to reward a controller that could finish reliably rather than one tuned to look good on a single lucky run.",
        what_i_did=(
            "I modeled the drone with a 12-state nonlinear model (position, yaw/pitch/roll, and their rates) and linearized it about a hover equilibrium, where all commanded torques are zero and thrust exactly balances weight. The sensor model measures only the inertial-frame positions of two markers on the left and right rotors; the average of the two markers gives position, and their relative displacement gives orientation, which is what makes state estimation possible from such a limited measurement set. Before designing anything, I checked the controllability and observability matrices of the linearized system directly: both had full rank of 12, confirming that a state-feedback controller and a state observer were mathematically achievable about hover.</p>\n      "
            "<p>For stabilization I used a continuous-time linear quadratic regulator, solving the algebraic Riccati equation for the linearized dynamics. I weighted the attitude states an order of magnitude more heavily than the translational velocity states in the cost function, since excessive pitch and roll turned out to be the dominant cause of crashes and missed rings during tuning, and I kept the thrust penalty lower than the torque penalties so the drone could still climb and descend briskly through the course. The resulting closed-loop system had every eigenvalue with a negative real part (the slowest around &minus;0.68), confirming the design was stable about hover.</p>\n      "
            "<p>Because the controller only ever sees noisy marker positions rather than the full 12-state vector, I built a Luenberger-style observer with its gain computed by the dual LQR method, then fed the observer&rsquo;s state estimate back into the controller in place of the true state. The observer error dynamics were also asymptotically stable, with the slowest eigenvalue around &minus;0.37. As a first check on the whole loop, before testing on the full race course, I logged the marker measurements, position, attitude, and actuator commands over a short interval and confirmed the commanded and applied actuator values tracked each other closely and that the attitude states settled after an initial transient.</p>\n      "
            + report_figure(
                [("../assets/ae353-racing-drone/observer-controller-demo-response.png", None)],
                "Logged marker measurements, position, attitude, and actuator commands over a short interval, confirming the controller and observer loop behaved as expected before testing on the full course.",
            )
            + "\n      <p>The LQR controller alone only stabilizes the drone around a fixed desired state, so I added a trajectory generator to move that desired state through the course. The target position combined three effects: attraction toward the next ring&rsquo;s center, a lookahead point projected slightly through the ring so the drone would fly past the aperture instead of stopping at it, and repulsive corrections away from other drones, ring edges, and the floor. Close to a ring, the generator pulled in lateral error and slowed the target down to reduce edge clipping; far from a ring, it let the target move more aggressively so the drone could still finish inside the time limit. The clip below is one full autonomous run through the course using this final controller and trajectory generator.</p>\n      "
            + '<figure class="report-figure">\n'
            '      <div class="figure-media"><div><video src="../assets/ae353-racing-drone/video.mp4" controls preload="metadata" style="width:100%;display:block;background:#000;"></video></div></div>\n'
            '      <figcaption>Autonomous run through the full ring course using the final LQR controller, observer, and trajectory generator, the same controller used to produce the results below.</figcaption>\n'
            '    </figure>'
            + "\n      <p>Looking closely at one logged run shows both the strengths and the main weak point of the design. For most of the course the drone tracked the moving target closely, with tracking error concentrated in the 0.7&ndash;1.3 m band that shows up across the whole 30-trial dataset (the target is intentionally offset ahead of each ring center, so this isn&rsquo;t pure ring-center error). Late in this particular run, though, a ring transition triggered a large, fast attitude excursion: yaw, pitch, and roll all moved sharply within a couple of seconds, and the logged position then went flat, which is the signature of the vehicle leaving controlled flight rather than simply running out of simulation time. This matches the &ldquo;large attitude excursion&rdquo; and &ldquo;timeout&rdquo; categories that, together, accounted for the 3 of 30 trials that didn&rsquo;t finish: the controller itself stayed effective through normal flight, but an aggressive or poorly aligned approach to a later ring could occasionally push the drone into an attitude it couldn&rsquo;t recover from.</p>\n      "
            + report_figure(
                [("../assets/ae353-racing-drone/single-run-xy-path.png", None)],
                "Horizontal flight path (solid) against the target path (dashed) for one logged run: smooth tracking through most of the course, then a sharp bend late in the trajectory.",
            )
            + report_figure(
                [("../assets/ae353-racing-drone/single-run-timeseries.png", None)],
                "Time histories for the same run: position, tracking and observer error, attitude, and actuator commands. The attitude panel shows the large late-course excursion in yaw, pitch, and roll, after which the position trace goes flat.",
            )
            + "\n      <p>To judge the controller by more than one run, I evaluated it over 30 randomized simulations and logged the outcome, tracking error, observer error, completion time, and controller runtime for every trial. The drone finished 27 of the 30 courses, a 90% success rate against the 70% requirement, with the 3 non-finishes split between timeouts and one large attitude excursion.</p>\n      "
            + report_figure(
                [
                    ("../assets/ae353-racing-drone/aggregate-outcomes.png", "Outcome counts"),
                    ("../assets/ae353-racing-drone/aggregate-success-rate.png", "Success rate"),
                ],
                "Aggregate outcomes across 30 randomized trials: 27 finished, 1 failed, and 2 timed out, for a 90% success rate against the 70% requirement.",
            )
            + "\n      <p>Tracking error stayed concentrated between about 0.7 and 1.3 m across nearly all 30 trials, and the observer&rsquo;s position estimate stayed close to the true position for the large majority of samples, with occasional larger errors only during the most aggressive maneuvers.</p>\n      "
            + report_figure(
                [
                    ("../assets/ae353-racing-drone/aggregate-tracking-error.png", "Tracking error"),
                    ("../assets/ae353-racing-drone/aggregate-observer-error.png", "Observer position error"),
                ],
                "Aggregate tracking-error and observer-error histograms over all 30 trials: tracking error clusters between 0.7 and 1.3 m, and observer error stays close to zero for the large majority of samples.",
            )
            + "\n      <p>Successful runs finished in about 93 to 109 seconds, close to the 120 s simulation limit, which reflects a controller deliberately tuned for reliability over speed: earlier, more aggressive versions cleared some rings faster but clipped edges or lost attitude control more often. Controller runtime stayed under roughly 0.2 ms per call in almost every case, well below the simulation timestep, so computation speed was never the bottleneck.</p>\n      "
            + report_figure(
                [
                    ("../assets/ae353-racing-drone/aggregate-completion-times.png", "Completion time"),
                    ("../assets/ae353-racing-drone/aggregate-controller-runtime.png", "Controller runtime"),
                ],
                "Completion-time and controller-runtime histograms: successful trials finished in roughly 93&ndash;109 s, and the controller ran in well under a millisecond per call.",
            )
            + report_figure(
                [("../assets/ae353-racing-drone/aggregate-failure-categories.png", None)],
                "Failure and success categories over the 30 aggregate trials: finishing was by far the most common outcome, with timeout and a large attitude excursion accounting for the rest.",
            )
            + "\n      <p>Taken together, the results traced a clear path from a linearized, provably stable design to a controller that held up under randomized, nonlinear simulation: stable in theory, reliable in practice, and limited mainly by how it handled the occasional difficult approach to a later ring."
        ),
        tools_prose="Modeled the drone dynamics, computed the hover linearization, and solved both the controller and observer Riccati equations in Python with NumPy and SciPy, then implemented the trajectory generator and ran every trial in the provided drone-racing simulator. Used Matplotlib for every logged time history, histogram, and aggregate outcome plot, and recorded a full autonomous run of the final controller as a simulation video.",
        outcome="Ended up with a controller and observer pair that were provably stable in the linearized model and held up under real, nonlinear, noisy simulation: 27 of 30 randomized trials finished successfully for a 90% completion rate, well above the 70% requirement, with successful runs completing in roughly 93 to 109 seconds and a controller cheap enough to run many times faster than real time.",
        tags=["Python", "NumPy", "SciPy", "Control Systems", "LQR", "State Estimation", "Robotics Simulation"],
        links=[],
    ),
    dict(
        slug="reaction-wheel-attitude-control-with-star-tracker", category="projects", org="Aerospace Control Systems", title="Observer-Based Reaction-Wheel Attitude Control for a Spacecraft with a Star Tracker",
        filled=True,
        dates="Spring 2026", location="University of Illinois",
        lede="Designed an LQR attitude controller, a symmetric four-wheel/four-star sensing geometry, and a noisy star-tracker observer to hold a simulated spacecraft's docking attitude for 60 seconds against debris disturbances, clearing the reliability requirement with 30 of 40 randomized trials (75%) succeeding.",
        media=[
            ("../assets/spacecraft-star-tracker/simulator-snapshot.png",
             "Simulator snapshot of the spacecraft showing the symmetric four-reaction-wheel layout",
             "Simulator snapshot of the spacecraft, showing the symmetric four-wheel layout chosen to give nearly isotropic control authority."),
            ("../assets/spacecraft-star-tracker/star-tracks.png",
             "Tracked-star trajectories in the star-tracker image plane during a representative successful rollout",
             "Tracked-star trajectories in the image plane during a representative successful rollout. The four stars stay well inside the field-of-view boundary."),
            ("../assets/spacecraft-star-tracker/attitude-envelope.png",
             "Envelope of attitude magnitude across all successful rollouts, staying well below the requirement threshold",
             "Attitude-magnitude envelope across every successful rollout: the median settles around 0.03&ndash;0.05 rad, well below the 0.20 rad requirement threshold."),
        ],
        overview="AE353 Design Project 2 asked for a controller that could hold a simulated spacecraft at a fixed docking attitude for 60 seconds despite noisy star-tracker measurements and impulsive debris disturbances, with the simulator ending the run early if any tracked star left the star-tracker&rsquo;s field of view or any reaction wheel exceeded its speed limit. The formal requirement was written in &ldquo;shall&rdquo; form and tied to a specific verification procedure: with the final controller run over 40 randomized rollouts, at least 28 of them had to reach 60 seconds with all three terminal attitude angles inside &plusmn;0.20 rad. The real design question wasn&rsquo;t just nominal stabilization, since a controller can look great on one clean run and still fail under different noise, disturbances, or initial conditions; it was how to arrange the wheels and stars for balanced authority and margin, and how to keep a stabilizing linear controller reliable once the observer is noisy and the wheels are close to saturating.",
        what_i_did=(
            "I placed the four reaction-wheel axes symmetrically around the body and chose four tracked stars arranged symmetrically about the boresight, near the center of the field of view, to leave margin for attitude excursions before a star could leave the frame. With four wheels controlling three body-torque axes, this geometry also leaves a one-dimensional null space I could use later for momentum management without disturbing the commanded torque. I linearized the nonlinear spacecraft dynamics about the zero-attitude, zero-rate equilibrium to get a six-state model in yaw, pitch, roll, and their body rates, and confirmed the linearized system was fully controllable before designing anything on top of it.</p>\n      "
            + report_figure(
                [("../assets/spacecraft-star-tracker/boresight-view.png", None)],
                "Spacecraft view with the star-tracker boresight indicated. The symmetric star placement keeps the tracked stars centered, preserving margin within the field of view during moderate attitude excursions.",
            )
            + "\n      <p>For stabilization I designed a continuous-time LQR gain in body-torque coordinates, weighting attitude error the most heavily, body-rate damping second, and actuator effort third; that priority order came out of iterating on the design and watching where the closed loop actually struggled. Solving the algebraic Riccati equation gave a body-torque feedback gain that I then had to convert into four wheel-torque commands through the wheel-axis geometry matrix. A plain least-squares allocation of that conversion stabilized the nominal model but, under noisy rollouts, drove unnecessary wheel activity and let one wheel pair drift rapidly toward saturation.</p>\n      "
            "<p>I fixed that with a few practical additions layered on top of the base LQR law. The allocator became a weighted least-squares solve that penalizes wheels whose estimated speed is already high, discouraging the controller from continuing to load up a fast wheel. A second term, computed in the allocator&rsquo;s null space, slowly bleeds off stored wheel momentum without changing the commanded body torque at all. I smoothed the resulting command with a simple exponential filter to cut down on noise-driven chatter, and added a soft-braking rule that scales the command down as any wheel&rsquo;s estimated speed approaches its limit, well before the hard saturation bound, so the controller backs off gracefully instead of slamming into the limit. Together these turned a controller that was stable in theory into one that behaved well under real, noisy, disturbed simulation.</p>\n      "
            + '<figure class="report-figure">\n'
            '      <div class="figure-media"><div><video src="../assets/spacecraft-star-tracker/video.mp4" controls preload="metadata" style="width:100%;display:block;background:#000;"></video></div></div>\n'
            '      <figcaption>Full 60-second representative docking run using the final controller, observer, and wheel allocation scheme.</figcaption>\n'
            '    </figure>'
            + "\n      <p>On one representative 60-second rollout, all three attitude angles stayed comfortably inside the &plusmn;0.20 rad requirement bound the whole time, settling into a range of roughly 0.02 to 0.10 rad after the initial transient, with body rates generally within about &plusmn;0.08 rad/s. Wheel speeds stayed well clear of the &plusmn;50 rad/s limit, peaking below 30 rad/s, and the commanded torques stayed active throughout without ever showing sustained saturation. This run alone doesn&rsquo;t prove the design works, but it does show the closed-loop behavior is physically reasonable in the full nonlinear simulator, not just on paper.</p>\n      "
            + report_figure(
                [("../assets/spacecraft-star-tracker/representative-time-histories.png", None)],
                "Time histories for the representative rollout: attitude angles, attitude magnitude, body rates, wheel speeds, and commanded torques, all staying comfortably inside their respective limits for the full 60 seconds.",
            )
            + "\n      <p>The observer&rsquo;s estimation errors for the same run show where the noise actually lives: the roll-angle estimate was the noisiest of the three attitude channels, and the body-rate estimate about the x-axis was visibly noisier than the other two rate channels. That&rsquo;s part of why command smoothing and the soft-braking margin mattered: the raw noisy estimate was usable for feedback, but not clean enough to command straight through to the wheels without some filtering.</p>\n      "
            + report_figure(
                [("../assets/spacecraft-star-tracker/representative-estimation-errors.png", None)],
                "Observer estimation errors for the same rollout. The roll-angle estimate and the x-axis body-rate estimate carry the most noise, motivating the command smoothing and soft-braking margin used downstream.",
            )
            + "\n      <p>To check reliability rather than just one good run, I evaluated the final controller over 40 randomized rollouts with star-tracker noise and debris disturbances enabled. Thirty of the forty reached the full 60-second interval within the terminal-attitude bound, a 75% success rate against the 70% (28-of-40) requirement, with a mean survival time of 53.00 s and a mean RMS attitude magnitude of 0.0645 rad across the batch.</p>\n      "
            + report_figure(
                [
                    ("../assets/spacecraft-star-tracker/survival-time-histogram.png", "Survival time"),
                    ("../assets/spacecraft-star-tracker/rms-attitude-histogram.png", "RMS attitude magnitude"),
                ],
                "Survival-time and RMS-attitude-magnitude distributions across the 40-rollout batch. Survival time concentrates heavily at the full 60 s docking time, consistent with the 75% success rate.",
            )
            + "\n      <p>Plotting survival time against RMS attitude magnitude makes the failure mechanism clear: runs with low RMS attitude generally survive the full interval, while the early failures cluster at higher RMS values, meaning the spacecraft was tumbling too much before it ran out of field of view. Breaking outcomes down by category confirmed why: every one of the ten non-successes fell into star loss or a closely related early termination, and not a single rollout failed by exceeding the wheel-speed limit. The weighted allocation and soft braking were doing their job on the actuator side; the remaining weak point was keeping stars centered under large, randomized disturbances.</p>\n      "
            + report_figure(
                [
                    ("../assets/spacecraft-star-tracker/survival-vs-rms-scatter.png", "Survival time vs. RMS attitude"),
                    ("../assets/spacecraft-star-tracker/failure-mode-bar-chart.png", "Outcome categories"),
                ],
                "Survival time versus RMS attitude magnitude (left) and outcome categories (right): all ten non-successes were star-loss events, with zero wheel-speed-limit failures.",
            )
            + "\n      <p>Looking at the attitude-magnitude envelope across every successful run shows how consistent the controller was once past the initial transient: the 10th-to-90th-percentile band narrows quickly, and the median settles around 0.03 to 0.05 rad for most of the docking interval, comfortably below the 0.20 rad requirement.</p>\n      "
            + report_figure(
                [("../assets/spacecraft-star-tracker/attitude-envelope.png", None)],
                "Attitude-magnitude envelope (10th to 90th percentile, with median) across all successful rollouts. After the initial transient, the successful runs are fairly consistent and stay well under the requirement threshold.",
            )
            + "\n      <p>The overall lesson was that small-signal stability was never the hard part; an LQR gain stabilizes the linearized model easily. The real work, and the real source of remaining failures, was in the practical details: sensor geometry, noise-aware wheel allocation, momentum management, and saturation handling in the full nonlinear simulator."
        ),
        tools_prose="Computed the linearization, controllability check, and continuous-time Riccati solve for the LQR gain in Python with NumPy and SciPy, then implemented the wheel-torque allocator, null-space momentum draining, command smoothing, and soft-braking logic on top of the course-provided star-tracker observer and spacecraft simulator. Used Matplotlib for every time history, histogram, scatter plot, and envelope plot, and recorded a full 60-second docking run as a simulation video.",
        outcome="Ended up with a controller that satisfied the formal reliability requirement: 30 of 40 randomized rollouts succeeded (75%), against a 28-of-40 (70%) threshold, with a mean survival time of 53.00 s and mean RMS attitude magnitude of 0.0645 rad across the batch. The representative run held RMS attitude error to 0.0587 rad with a maximum wheel speed of 26.40 rad/s, and every one of the ten non-successes in the aggregate batch was a star-loss event rather than a wheel-speed-limit failure, pointing clearly at where the remaining design margin is spent.",
        tags=["Python", "NumPy", "SciPy", "Control Systems", "LQR", "State Estimation", "Spacecraft Attitude Control"],
        links=[],
    ),
    dict(
        slug="numerical-simulation-and-analysis-of-uav-pitch-dynamics", category="projects", org="Numerical Methods", title="A Numerical Simulation and Analysis of UAV Pitch Dynamics",
        filled=True,
        dates="Spring 2025", location="University of Illinois",
        lede="Built a fourth-order Runge-Kutta simulation of UAV pitch dynamics to study how damping, stiffness, and inertia shape the transient response, then compared an open-loop step input against a PD controller and verified the numerical method with a full convergence study.",
        media=[
            ("../assets/uav-pitch-dynamics/phase-portraits.png",
             "Phase portraits of pitch angle versus pitch rate for under-damped, critically damped, and overdamped cases",
             "Phase portraits of pitch angle versus pitch rate for three damping cases: the under-damped case spirals around the origin, the critically damped case cuts straight to it, and the overdamped case creeps in without oscillating."),
            ("../assets/uav-pitch-dynamics/step-vs-pd-control.png",
             "Comparison of pitch angle response using an open-loop step input versus a PD controller",
             "Step input versus PD control: the PD controller settles the pitch angle faster and with far less overshoot than the open-loop step response."),
            ("../assets/uav-pitch-dynamics/convergence-study.png",
             "Log-log plot of absolute error versus time step showing fourth-order convergence with a measured slope of 4.02",
             "Error-convergence study for the RK4 implementation: a log-log slope of 4.02 confirms the expected fourth-order global error."),
        ],
        overview="Pitch is the axis that governs a UAV&rsquo;s climb and descent, and how well a vehicle damps out pitch disturbances is a direct driver of stability, maneuverability, and safety. This project modeled UAV pitch motion as a single second-order ODE in the pitch angle, driven by inertia, aerodynamic stiffness, damping, and an external control moment, and used it to study two questions: how do the physical parameters (inertia, stiffness, and especially damping) shape the transient pitch response, and how much better does an active feedback controller do at rejecting that response than simply forcing a fixed input and waiting it out. Answering both meant building a numerical integrator accurate enough to trust, then using it to sweep across damping regimes and controller types.",
        what_i_did=(
            "I rewrote the second-order pitch equation as a first-order system in the state vector [&theta;, q] (pitch angle and pitch rate) and integrated it with a fourth-order Runge-Kutta (RK4) scheme, which combines four slope evaluations per step to cancel out lower-order error terms and reach a global error of O(&Delta;t&#8308;). Before trusting the integrator on the full problem, I validated it against the closed-form analytical solution of the homogeneous damped oscillator (zero control input, a known initial condition, and the standard underdamped solution in terms of the natural and damped frequencies). Running the same homogeneous case across a range of time steps and plotting the absolute error against &Delta;t on a log-log scale gave a measured slope of 4.02, matching RK4&rsquo;s theoretical fourth-order convergence almost exactly and confirming the implementation was correct rather than just plausible-looking.</p>\n      "
            + report_figure(
                [
                    ("../assets/uav-pitch-dynamics/convergence-study.png", "Convergence study"),
                    ("../assets/uav-pitch-dynamics/numerical-vs-analytical.png", "Numerical vs. analytical"),
                ],
                "Left: log-log error-convergence study giving a measured slope of 4.02, matching the theoretical fourth-order global error of RK4. Right: the RK4 solution overlaid on the closed-form analytical solution for the homogeneous case, essentially indistinguishable at &Delta;t = 0.01.",
            )
            + "\n      <p>With the integrator validated, I checked how coarse a time step could get away with staying accurate by comparing runs at &Delta;t = 0.005, 0.015, and 0.03: all three tracked each other closely, indicating that anything at or below roughly 0.03 s was a safe choice for this system. I still ran the main study at &Delta;t = 0.001 for extra margin, over a 6-second window with the moment of inertia and stiffness held fixed and the damping coefficient swept across several values to move the system between under-damped, critically damped, and overdamped behavior.</p>\n      "
            + report_figure(
                [("../assets/uav-pitch-dynamics/time-step-comparison.png", None)],
                "Pitch-angle response at three different time steps (0.005, 0.015, and 0.03 s): the curves overlay almost exactly, confirming the chosen step size was well within the stable, accurate range.",
            )
            + "\n      <p>Applying a step input at t = 2 s and sweeping the damping coefficient reproduced the classic second-order response families directly: at low damping the pitch angle overshoots substantially and oscillates with slowly decaying amplitude, at the critical damping value it returns to equilibrium in one smooth motion with no overshoot, and at high damping it approaches equilibrium monotonically but noticeably more slowly. That progression matches the theoretical overshoot relationship OS &asymp; exp(&minus;&zeta;&pi;/&radic;(1&minus;&zeta;&sup2;)) in terms of the damping ratio &zeta; = c/(2&radic;(I<sub>yy</sub>k)), where &zeta; &lt; 1 is under-damped, &zeta; = 1 is critical, and &zeta; &gt; 1 is overdamped.</p>\n      "
            + report_figure(
                [("../assets/uav-pitch-dynamics/step-response-damping-cases.png", None)],
                "Pitch-angle response to a step input at t = 2 s for three damping values: pronounced overshoot and oscillation at low damping, a single smooth return at critical damping, and a slower monotonic approach at high damping.",
            )
            + "\n      <p>The phase portraits (pitch angle plotted against pitch rate) make the same story visual: the under-damped trajectory spirals around the origin and, in the undamped limit, would circle forever, the critically damped trajectory cuts almost directly to the origin, and the overdamped trajectory creeps in along a slow arc with no oscillation. These are exactly the behaviors a feedback controller has to manage, and they made clear that under-damped response is the regime to actively suppress.</p>\n      "
            + report_figure(
                [("../assets/uav-pitch-dynamics/phase-portraits.png", None)],
                "Phase portraits of pitch angle versus pitch rate for the same three damping cases: the under-damped trajectory spirals repeatedly, the critically damped one heads almost straight to the origin, and the overdamped one creeps in without crossing it.",
            )
            + "\n      <p>Finally, I compared the open-loop step input against a proportional-derivative controller, u(t) = &minus;K<sub>p</sub>&theta;(t) &minus; K<sub>d</sub>q(t) with K<sub>p</sub> = 4.0 and K<sub>d</sub> = 1.0, continuously correcting the control moment based on both the current pitch error and its rate of change rather than applying one fixed input and waiting. The PD-controlled response converged to equilibrium markedly faster than the step response, with substantially less overshoot and almost no residual oscillation, which is the practical payoff of feedback: it actively counteracts the system&rsquo;s own momentum instead of just forcing it and hoping the natural damping handles the rest.</p>\n      "
            + report_figure(
                [("../assets/uav-pitch-dynamics/step-vs-pd-control.png", None)],
                "Step input versus PD control on the same system: the PD controller reaches equilibrium faster, with far less overshoot and almost no lingering oscillation.",
            )
            + "\n      <p>Taken together, the results tied a validated fourth-order numerical method to a clear physical story: damping governs the shape of the transient response exactly as the analytical overshoot formula predicts, and active feedback beats an open-loop input at every damping level by directly counteracting the system&rsquo;s motion instead of just exciting it and waiting."
        ),
        tools_prose="Implemented the RK4 integrator, the step and PD control laws, and the analytical validation case from scratch in Python with NumPy, and used Matplotlib for every time-series plot, phase portrait, and the log-log convergence study.",
        outcome="Ended up with an RK4 integrator whose measured convergence order (4.02) matched theory almost exactly, a clear demonstration of how the damping ratio moves the pitch response between under-damped, critically damped, and overdamped behavior consistent with the analytical overshoot formula, and a direct, quantified comparison showing the PD controller reaching equilibrium faster and with far less overshoot than an open-loop step input.",
        tags=["Python", "NumPy", "Numerical Methods", "Runge-Kutta (RK4)", "Dynamics &amp; Control", "PD Control"],
        links=[],
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
        links_section_html = (
            f'<h3>Links</h3>\n      <ul class="sidebar-links">\n        {links_html}\n      </ul>'
            if item.get("links") else ""
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
            links_section_html=links_section_html,
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
