# CLAUDE.md — AI Assistant Guide for demo_website

This file provides guidance for AI assistants working on the `catsoc/demo_website` repository.

## Project Overview

A static personal brand landing page for **文科橘貓 (Cat Soc)** — a Taiwanese creator who teaches an Obsidian AI note-taking workshop. The site is a single-page marketing/sales page written in Traditional Chinese (zh-TW).

- **Live URL**: https://catsoc.github.io/demo_website/
- **Hosting**: GitHub Pages
- **Language**: Traditional Chinese (zh-TW)
- **No build step**: pure HTML + CSS + JavaScript, no package manager, no bundler

---

## Repository Structure

```
demo_website/
├── index.html                  # Main landing page (the entire site)
├── style.css                   # Primary stylesheet (active, linked by index.html)
├── style-new.css               # Alternate/newer stylesheet (NOT linked yet)
├── og-image.html               # Open Graph preview image page
├── google-verification.html    # Google site ownership verification file
├── sitemap.xml                 # XML sitemap for search engines
├── robots.txt                  # Search crawler rules
├── README.md                   # Minimal project description
│
├── # Python utility scripts (developer tooling, not part of the site)
├── google_index_checker.py     # Checks Google/Bing/DuckDuckGo indexing status
├── complete_solution.py        # One-click Google indexing setup orchestrator
├── google_indexing_checker.py  # Empty placeholder
│
├── # PowerShell scripts (Windows-only developer tooling)
├── auto-google-check.ps1       # Automated Google indexing check
├── gsc-auto-setup.ps1          # Google Search Console automated setup
├── gsc-setup.ps1               # GSC setup helper
├── auto-indexing-checker.ps1   # Auto indexing checker
├── google-indexing-checker.ps1 # Empty placeholder
├── simple-check.ps1            # Empty placeholder
│
├── # Batch files (Windows-only developer tooling)
├── monitor-indexing.bat        # Runs google_index_checker.py every 24 hours
├── quick-check.bat             # One-shot indexing check shortcut
│
├── # Data / docs
├── google_index_report.json    # Output report from google_index_checker.py
├── gsc-quicklinks.md           # Google Search Console reference links
├── gsc-setup-guide.txt         # Auto-generated GSC setup instructions
├── AI員工主動性更新.md           # Empty file
└── desktop.ini                 # Windows system metadata (ignore)
```

---

## Core Files: What They Do

### `index.html` (~520 lines)

The entire website in one file. Page sections (each marked with HTML comments):

| Section | ID / Class | Description |
|---|---|---|
| Navbar | `.navbar` | Logo + anchor links |
| Hero | `.hero-section` | Main headline and CTA |
| Pain resonance | `#why-this-works` | Problem awareness section |
| Workshop content | `.pain-points` | What the workshop teaches |
| Solution story | `.solution` | Personal backstory + benefits |
| Course modules | `#course` | 2-hour curriculum breakdown |
| Instructor bio | `.instructor` | About 文科橘貓 |
| FAQ | `.faq` | 4 common questions |
| Final CTA | `.final-cta` | Purchase call-to-action |
| Footer | `footer` | Contact info + legal |

**Embedded JavaScript** (bottom of `<body>`):
- `trackExploreClick()` — fires GA4 `click` event on hero CTA
- `openPayment()` — fires GA4 `begin_checkout` event, opens PayUni popup window
- Smooth scroll for anchor links
- Navbar scroll shadow effect
- IntersectionObserver animation for `.pain-item`, `.benefit-item`, `.module`

**Analytics integrations** (in `<head>`):
- Google Analytics 4: `G-Q6PYXJFR8T`
- Google Tag Manager: `GTM-NPJRRWPW`

**Payment**: PayUni gateway — `https://api.payuni.com.tw/api/su/store_info/AJAJ1751374909/...`

### `style.css` (~700+ lines)

CSS-only, no preprocessor. Uses CSS custom properties extensively:

```css
/* Design tokens defined in :root */
--primary-color: #F97316;    /* orange — brand colour */
--primary-hover: #EA580C;
--secondary-color: #FED7AA;
--accent-color: #FB923C;
--dark-color: #1F2937;
--medium-gray: #6B7280;
--light-gray: #F9FAFB;
--font-family: 'Noto Sans TC', -apple-system, ...;
```

Spacing uses `--space-N` tokens (0.25rem increments). Shadows use `--shadow-sm/md/lg/xl`. Border-radius uses `--radius-sm/md/lg/xl/2xl`. All transitions use `--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`.

**Font**: Noto Sans TC (Google Fonts, weights 300/400/500/700).

### `style-new.css`

An alternative, more recent stylesheet. **Not currently linked** in `index.html`. Do not link it without verifying it does not break the layout.

### Python Scripts

These are standalone developer utilities for checking Google Search Console indexing status. They do **not** need to be deployed with the site.

- `google_index_checker.py` — `GoogleIndexChecker` class: checks site accessibility, sitemap/robots.txt, scrapes Google/Bing/DuckDuckGo for `site:` results, saves report to `google_index_report.json`
- `complete_solution.py` — calls `google_index_checker.py` as subprocess, opens GSC in browser, writes `gsc-setup-guide.txt`, creates `monitor-indexing.bat` and `quick-check.bat`

---

## SEO Configuration

| File | Purpose |
|---|---|
| `sitemap.xml` | Lists `index.html` (priority 1.0, weekly) and `og-image.html` (priority 0.3, monthly) |
| `robots.txt` | Allows all crawlers; disallows `/.git/` and `/README.md`; points to sitemap |
| `google-verification.html` | Google Search Console HTML-file ownership verification |
| `<head>` meta tags | Full Open Graph, Twitter Card, JSON-LD (Course schema), canonical URL |

**Canonical URL**: `https://catsoc.github.io/demo_website/`

**JSON-LD Schema**: `Course` type — name, description, provider (Person), offer (NT$3,600 TWD), online mode.

---

## Development Workflow

### Making Changes

There is no build process. Edit files directly and push to GitHub. GitHub Pages auto-deploys from the `master` branch.

```bash
# Make your changes, then:
git add <files>
git commit -m "descriptive message"
git push origin master
```

### Editing the Stylesheet

Always edit `style.css` (the active stylesheet). Use the existing CSS variable tokens rather than hardcoded values. Do not introduce a CSS preprocessor or framework without explicit request.

### Editing the Landing Page

- Keep all section HTML comments (e.g., `<!-- ====== Hero Section Start ====== -->`) so sections are easy to locate.
- Preserve the `id` attributes used for anchor navigation (`#course`, `#why-this-works`).
- GA4 event functions (`trackExploreClick`, `openPayment`) must remain in the inline `<script>` block. Do not move them to an external file without also updating the `onclick` attributes.
- The payment URL in `openPayment()` is a live PayUni endpoint — do not modify it unless explicitly instructed.

### Running the Python Indexing Tools

```bash
# Check indexing status (requires: pip install requests)
python google_index_checker.py

# Full one-click setup + monitoring (Windows)
python complete_solution.py
```

These tools only need to be run on a developer machine, not in CI.

---

## Key Conventions

1. **Language**: All user-facing content is Traditional Chinese (zh-TW). Code comments may be in Chinese or English.
2. **No framework**: This is plain HTML/CSS/JS. Do not introduce npm, React, Vue, Tailwind, etc. without explicit request.
3. **Single page**: The entire site is one HTML file. There are no routes, pages, or components.
4. **CSS variables first**: When adding or changing styles, use the design tokens in `:root` rather than hardcoded values.
5. **Section comments**: Maintain the `<!-- ====== Section Start/End ====== -->` comment pattern so the file remains easy to navigate.
6. **GA4 tracking**: Any new CTA buttons should fire a `gtag('event', ...)` call consistent with the existing pattern.
7. **No `.git/` in web root**: The `robots.txt` disallows it; never add files that expose git internals.
8. **`desktop.ini`**: This Windows metadata file is tracked in git but irrelevant to the site. Leave it alone.

---

## Pricing & Business Context

| Item | Current Value |
|---|---|
| Workshop price | NT$3,600 (special price) |
| Original price | NT$7,200 |
| Template bonus | NT$3,600 value |
| Satisfaction guarantee | 7 days full refund |
| Post-purchase support | 30 days Q&A |
| Contact email | catsoc.org@gmail.com |
| Instagram | @cat__soc |

When editing copy, keep these figures consistent across all sections (solution CTA, course bonus, final CTA, footer).

---

## Branch Strategy

- **`master`**: Production branch, auto-deployed to GitHub Pages
- **`claude/*`**: AI assistant working branches (e.g., `claude/add-claude-documentation-lj5eA`)

Always develop on a `claude/` branch and push there. Do not push directly to `master` unless explicitly instructed.
