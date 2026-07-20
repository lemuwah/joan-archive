# Validation Report

This document tracks validation checks, provenance notes, and audit trails for the Joan Archive.

---

## 1. Repository structure

- **Root files:**  
  - README.md present and up to date.  
  - validation-report.md added and linked from main site.

- **Docs / site:**  
  - All Markdown files render correctly under GitHub Pages.  
  - No orphaned pages detected in navigation.

---

## 2. Links and navigation

- **Internal links:**  
  - All relative links tested (e.g., `validation-report.md`, `/docs/...`) and resolve correctly.  
  - No 404s found in primary navigation paths.

- **External links:**  
  - GitHub issue link uses plain label:
    - `https://github.com/lemuwah/joan-archive/issues/new?labels=discussion&title=Discussion:+Joan+Archive+Note`
  - No emoji in `labels` parameter; label `discussion` exists in the repo.

---

## 3. Issue and discussion flow

- **New issue link:**  
  - Opens the GitHub issue form with:
    - Pre-set label: `discussion`  
    - Pre-set title: `Discussion: Joan Archive Note`

- **Behavior from GitHub Pages:**  
  - Link works when clicked from the published site.  
  - No redirect loops or blank pages observed.

---

## 4. Content validation

- **Markdown syntax:**  
  - Headings, lists, and links conform to GitHub Flavored Markdown.  
  - No broken inline HTML affecting rendering.

- **Provenance notes:**  
  - Interpretive claims are clearly marked as such.  
  - Legal and historical statements are framed conditionally where evidence is limited.

---

## 5. Pending checks

- **Automated link checking:**  
  - Future task: add a GitHub Action to crawl and validate all links on each push.

- **Schema for validation reports:**  
  - Future task: define a standard section layout for all future validation entries.

---

_Last updated: manually by Wendy._
