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
        slug="fea-final-project", category="projects", org="Finite Element Analysis", title="2D Thermal Finite Element Solver",
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
        links=[("Report / code", "#")],
    ),
    dict(
        slug="fea-midterm-project", category="projects", org="Finite Element Analysis", title="Stress Concentration and Plane-Stress Validity Study",
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
