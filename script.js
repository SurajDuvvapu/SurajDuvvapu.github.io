// ============================================================
// Shared interaction layer: nav shrink/blur, mobile menu,
// and scroll-reveal for cards/sections.
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
