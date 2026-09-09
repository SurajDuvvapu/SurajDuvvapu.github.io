// ============================================================
// Shared interaction layer: nav shrink/blur, mobile menu,
// scroll-reveal for cards/sections, and the per-card skills
// carousel on the home page.
// ============================================================

(function () {
  const nav = document.querySelector(".nav");
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 8) nav.classList.add("scrolled");
      else nav.classList.remove("scrolled");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("nav-links-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  const revealTargets = document.querySelectorAll(".reveal, .reveal-stagger");
  if ("IntersectionObserver" in window && revealTargets.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            if (entry.target.classList.contains("reveal-stagger")) {
              Array.from(entry.target.children).forEach((child) =>
                child.classList.add("is-visible")
              );
            }
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    revealTargets.forEach((el) => {
      if (el.classList.contains("reveal-stagger")) {
        Array.from(el.children).forEach((child, i) => {
          child.style.setProperty("--i", i);
          child.classList.add("reveal");
        });
      }
      io.observe(el);
    });
  } else {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
  }
})();

// ============================================================
// Card skills carousel
// ------------------------------------------------------------
// Each [data-skill-carousel] holds a flat list of .skill-chip
// elements. We measure them, pack them into single-line "pages"
// that fit the card's width, then cross-fade page to page on a
// timer -- dwelling on each page, pausing on hover/focus, while
// the card is off screen, and while the tab is hidden.
// Falls back to plain wrapped chips if motion is reduced.
// ============================================================

(function () {
  const carousels = document.querySelectorAll("[data-skill-carousel]");
  if (!carousels.length) return;

  const reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return; // chips just wrap and all stay visible

  const DWELL = 3200; // ms each page is held on screen
  const GAP = 6; // px, matches the 0.4rem flex gap (rounded down for safety)
  const MAX_PER_PAGE = 4; // keeps wide cards rotating too, instead of showing everything at once

  const instances = [];

  function buildPages(inst) {
    const { track, chips } = inst;

    // Measure with the chips laid out flat and wrapping.
    track.classList.remove("is-carousel");
    chips.forEach((chip) => track.appendChild(chip));
    Array.from(track.querySelectorAll(".skill-page")).forEach((p) => p.remove());

    const available = track.clientWidth;
    if (!available) return false;

    const widths = chips.map((chip) => chip.getBoundingClientRect().width);

    const pages = [];
    let current = [];
    let used = 0;
    chips.forEach((chip, i) => {
      const w = widths[i];
      const needed = current.length ? used + GAP + w : w;
      if (current.length && (needed > available || current.length >= MAX_PER_PAGE)) {
        pages.push(current);
        current = [chip];
        used = w;
      } else {
        current.push(chip);
        used = needed;
      }
    });
    if (current.length) pages.push(current);

    // Avoid a lonely trailing chip: pull one back from the page before it
    // when the pair still fits on a line.
    if (pages.length > 1) {
      const last = pages[pages.length - 1];
      const prev = pages[pages.length - 2];
      if (last.length === 1 && prev.length > 2) {
        const moved = prev[prev.length - 1];
        const w = widths[chips.indexOf(moved)] + GAP + widths[chips.indexOf(last[0])];
        if (w <= available) {
          prev.pop();
          last.unshift(moved);
        }
      }
    }

    inst.pageEls = pages.map((group, i) => {
      const page = document.createElement("div");
      page.className = "skill-page" + (i === 0 ? " is-current" : "");
      group.forEach((chip) => page.appendChild(chip));
      return page;
    });

    track.classList.add("is-carousel");
    inst.pageEls.forEach((page) => track.appendChild(page));

    // Dots
    if (inst.dots) inst.dots.remove();
    inst.dotEls = [];
    inst.dots = null;
    if (inst.pageEls.length > 1) {
      const dots = document.createElement("div");
      dots.className = "skill-dots";
      dots.setAttribute("aria-hidden", "true");
      inst.pageEls.forEach((_, i) => {
        const dot = document.createElement("span");
        dot.className = "skill-dot" + (i === 0 ? " is-current" : "");
        dots.appendChild(dot);
        inst.dotEls.push(dot);
      });
      inst.root.appendChild(dots);
      inst.dots = dots;
    }

    inst.index = 0;
    return true;
  }

  function show(inst, i) {
    if (!inst.pageEls || !inst.pageEls.length) return;
    const next = ((i % inst.pageEls.length) + inst.pageEls.length) % inst.pageEls.length;
    inst.pageEls.forEach((page, n) => page.classList.toggle("is-current", n === next));
    inst.dotEls.forEach((dot, n) => dot.classList.toggle("is-current", n === next));
    inst.index = next;
  }

  function tick() {
    if (document.hidden) return;
    instances.forEach((inst) => {
      if (inst.paused || !inst.visible) return;
      if (inst.card && inst.card.matches(":hover")) return;
      if (!inst.pageEls || inst.pageEls.length < 2) return;
      show(inst, inst.index + 1);
    });
  }

  carousels.forEach((root) => {
    const track = root.querySelector(".skill-track");
    if (!track) return;
    const chips = Array.from(track.querySelectorAll(".skill-chip"));
    if (!chips.length) return;

    const inst = {
      root: root,
      track: track,
      chips: chips,
      pageEls: null,
      dotEls: [],
      dots: null,
      card: null,
      index: 0,
      paused: false,
      visible: true,
    };

    // Pause while the reader is looking at (or tabbing through) this card.
    // `paused` covers touch/focus; hover is read straight off :hover at tick
    // time so a stray mouseleave (e.g. mid reveal-animation) can't strand it.
    inst.card = root.closest(".card") || root;
    ["focusin", "touchstart"].forEach((evt) =>
      inst.card.addEventListener(evt, () => (inst.paused = true), { passive: true })
    );
    ["focusout", "touchend", "touchcancel"].forEach((evt) =>
      inst.card.addEventListener(evt, () => (inst.paused = false))
    );

    instances.push(inst);
  });

  if (!instances.length) return;

  function rebuildAll() {
    instances.forEach(buildPages);
  }

  // Only run the timer for carousels currently on screen.
  if ("IntersectionObserver" in window) {
    const vio = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const inst = instances.find((x) => x.root === entry.target);
          if (inst) inst.visible = entry.isIntersecting;
        });
      },
      { rootMargin: "80px 0px" }
    );
    instances.forEach((inst) => vio.observe(inst.root));
  }

  let started = false;
  const start = () => {
    if (started) return;
    started = true;
    rebuildAll();
    setInterval(tick, DWELL);
  };

  // Wait for webfonts so the chip widths we measure are the final ones.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(start, start);
  } else {
    start();
  }
  window.addEventListener("load", () => {
    if (started) rebuildAll();
    else start();
  });

  let resizeTimer = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(rebuildAll, 200);
  });
})();
