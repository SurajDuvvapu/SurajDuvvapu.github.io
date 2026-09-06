# Engineering Portfolio, Suraj Duvvapu

A static, no-build-step portfolio site (plain HTML/CSS/JS) in the Apple/Tesla
aesthetic: one accent color, big whitespace, large type, subtle scroll-reveal
animation.

## Structure

```
index.html                 Home page: bio, experience cards, project cards
styles.css                 Shared design system (colors, type, layout, animation)
script.js                  Nav scroll/mobile-menu + scroll-reveal behavior
experience/*.html          6 experience detail pages
projects/*.html            5 project detail pages
generate.py                Regenerates all 11 detail pages from one template + data list
assets/                    Put your photos/renders/screenshots here
```

## Editing content

Every page currently has **placeholder text** (in italics) marking what to
replace: bio, dates, locations, "what I did" write-ups, tools, outcomes, and
links. Two ways to fill these in:

1. **Fastest for now:** open `generate.py`, edit the `EXPERIENCE` and
   `PROJECTS` lists near the top (one Python dict per entry, no coding
   knowledge needed beyond editing the quoted text), then run:
   ```
   python3 generate.py
   ```
   This regenerates all 11 detail pages from the template so every page stays
   consistent. Also edit the matching card text directly in `index.html`
   (the home page cards aren't generated from `generate.py`).

2. **Direct editing:** once content is finalized, you can also hand-edit the
   HTML files in `experience/` and `projects/` directly, just keep the same
   structure (`<h2>` section headers, `<p class="prose">` etc.) so the styling
   still applies.

Add real photos/renders/diagrams to `assets/` (organize by page in a
subfolder, e.g. `assets/tesla/`) and swap them in for the placeholder
`.media-frame` block on each detail page. Two options:

- **Single image:** replace the block with an `<img>`:
  ```html
  <img src="../assets/your-image.jpg" alt="Description" style="border-radius:24px;margin-bottom:4rem;">
  ```
- **Multiple images (gallery):** use the `.media-gallery` pattern (see
  `experience/tesla.html` for a working example with three photos):
  ```html
  <div class="media-gallery reveal">
    <figure>
      <div class="media-thumb"><img src="../assets/tesla/photo.jpg" alt="Description" loading="lazy" /></div>
      <figcaption>Caption text.</figcaption>
    </figure>
    <!-- repeat <figure> for each image -->
  </div>
  ```
  If you're using `generate.py`, set a `media=[(src, alt, caption), ...]` list
  on that entry instead of hand-editing the HTML; the tesla entry shows the
  format, and regenerating will keep the gallery instead of resetting to the
  placeholder frame.

(use `assets/...` with no `../` on `index.html` itself, since it's one level up from `experience/`/`projects/`).

Update the placeholder email/LinkedIn/GitHub/resume links in the footer
(appears on every page) and the hero's "Download resume" button.

## Previewing locally

No build step needed, just open `index.html` in a browser, or run a local
server from this folder so relative links behave exactly like they will on
GitHub Pages:
```
python3 -m http.server 8000
```
then visit `http://localhost:8000`.

## Deploying to GitHub Pages

1. Create a new GitHub repository (e.g. `portfolio` or `<yourusername>.github.io`
   for a root-domain site).
2. From this folder:
   ```
   git init
   git add .
   git commit -m "Initial portfolio site"
   git branch -M main
   git remote add origin https://github.com/<yourusername>/<repo-name>.git
   git push -u origin main
   ```
3. On GitHub: repo **Settings → Pages → Build and deployment → Source:
   Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
4. Your site goes live at `https://<yourusername>.github.io/<repo-name>/`
   (or `https://<yourusername>.github.io/` if you named the repo
   `<yourusername>.github.io`).
5. **Custom domain (optional):** buy a domain, add a `CNAME` file to this
   folder containing just the domain name, and point your domain's DNS at
   GitHub Pages per GitHub's custom-domain docs, then set it in the same
   Pages settings page.

## Notes

- Dark mode follows the visitor's OS setting automatically (see the
  `prefers-color-scheme` block in `styles.css`).
- Motion respects `prefers-reduced-motion`; reveal animations are disabled
  for visitors who've asked for that.
- The accent color is one CSS variable (`--accent` in `styles.css`); change
  it there to re-theme the whole site.
