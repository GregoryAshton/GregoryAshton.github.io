# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Gregory Ashton's personal academic website, built with [MkDocs](https://www.mkdocs.org/) using the Cinder theme. It is deployed to GitHub Pages via a GitHub Actions workflow on push to `master`.

## Build Commands

- **Install dependencies:** `pip install -r requirements.txt`
- **Build site:** `mkdocs build` (outputs to `docs/`)
- **Local dev server:** `mkdocs serve` (live-reload at http://127.0.0.1:8000)
- **Spellcheck:** `codespell source/` (runs in CI before deploy)

## Architecture

- `mkdocs.yml` — Site configuration, navigation structure, theme, and plugins
- `source/` — All Markdown content and assets (configured as `docs_dir`)
- `source/index.md` — Homepage with news/updates (uses `mkdocs-macros-plugin` for templating, e.g. `{{ git.date.strftime(...) }}`)
- `source/img/` — Images referenced by pages
- `source/js/` — JavaScript (GoatCounter analytics)
- `source/pdfs/` — PDF files (talks, CV, etc.)
- `source/notes/` and `source/old_notes/` — Technical notes, including Jupyter notebooks
- `docs/` — Built output (committed to repo, served by GitHub Pages)
- `.github/workflows/deploy.yml` — CI/CD: runs codespell, builds with mkdocs, deploys to GitHub Pages

## Key Details

- **Branch:** `master` is the main/deploy branch
- **Markdown extensions in use:** `attr_list`, `pymdownx.highlight`, `pymdownx.superfences`, `md_in_html` — content uses these features (e.g. `<figure markdown>` blocks, fenced code highlighting)
- **Templating:** The `mkdocs-macros-plugin` is enabled, so Jinja2 expressions like `{{ git.date }}` are evaluated at build time
- **CI spellcheck:** `codespell source/` runs as a separate job in CI — ensure new content passes before pushing
