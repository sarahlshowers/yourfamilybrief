---
name: family-brief-report
description: Generate a Your Family Brief client report from a Notion session transcript. Use this skill whenever Sarah provides a Notion link to a client interview/intake session, mentions writing up a "Family Brief", "client report", "household report", or "session report", or says a client session needs its report. Also trigger when she pastes a Notion meeting-notes URL after a Family Brief advisory session, even if she doesn't name the deliverable — the 48-hour report turnaround is the standard follow-up to every session.
---

# Family Brief Report Generator

Turn a recorded client session in Notion into a finished, client-ready Family Brief PDF.

## What this is

Your Family Brief is Sarah's paid family advisory service: a ~45-minute interview about how a client's household runs, followed within 48 hours by a written report. The report's single most important quality, in Sarah's words, is that the client should feel *"almost scared — like, oh, she got it. Somebody hears me and understands."* Every choice below serves that goal.

## Workflow

### 1. Fetch the session from Notion

Fetch the provided Notion URL with the Notion MCP `fetch` tool. Meeting-notes pages return an AI summary but **omit the raw transcript by default** — the response will say "Transcript omitted" with a meeting-note URL. Re-fetch that URL with `include_transcript: true` to get the verbatim conversation.

Use **both** layers:
- The **summary** gives you reliable structure (themes, action items, facts like pickup schedules).
- The **raw transcript** gives you the client's exact words. Mine it for verbatim quotes, vivid details, and emotional moments — these are what make the report feel heard rather than processed. (e.g., "How is our life so chaotic when I'm trying so hard?" lands harder than any paraphrase.)

While reading, collect: client + family names (kids' names and ages matter — use them), session date, the dominant pain ("primary focus"), specific routines and failures, tools already tried and why they died, what the client said freed mental capacity would mean to them, and any raw numbers (times, frequencies, costs).

### 2. Read the writing guide

Read `references/writing-guide.md` for voice, section-by-section guidance, and how to make estimates. Do this before drafting — the tone is the product. Pay particular attention to the "Sounding human" section: Sarah has flagged em dashes and snappy AI-style phrasing as giveaways that undermine client trust, so a de-tell pass over the finished copy is part of the job, not a nice-to-have.

### 3. Populate the template

Copy `assets/family-brief-report-template.html` to a working file. It is a 13-page, 1920×1080-per-page HTML deck (Linen/Espresso/Deep Rose/Warm Taupe palette — never alter the CSS, fonts, or palette; they are the brand). Three of the pages (At a Glance, The Invisible Load, What You've Already Tried) are deliberately prose-dense: they carry the "she got it" half of the report's value, so give them full, specific, verbatim-grounded content rather than compressing them to slide fragments.

Replace the fill placeholders with real content:
- `<span class="fill">&nbsp;</span>` / `.fill.wide` → inline text. **Remove the `fill` class** when populating (otherwise the dashed underline renders under finished text). Same for `.fill-block` → replace with the same element minus the `fill-block` class, containing the text.
- Every page's contents are specified in the writing guide. Fill every placeholder — a client-ready report has no dashed blanks left.

Content must fit the fixed 1920×1080 pages. Keep entries within the length budgets in the writing guide; flexbox does not save you from a 60-word quick-win that belongs at 15.

### 4. Render to PDF

Use the bundled script:

```bash
python3 scripts/render_pdf.py populated.html output.pdf
```

It renders via Playwright/Chromium at exact page size. If Playwright isn't installed, the script prints install instructions (`pip install playwright --break-system-packages && python3 -m playwright install chromium --with-deps`).

Visually verify before delivering: the script also writes per-page PNGs next to the PDF when passed `--preview`. Read a few of them to check for overflowing text, empty placeholders, or layout breaks, and fix the HTML if found.

### 5. Save and deliver

Save both the populated HTML and the PDF to the workspace folder under `reports/<client-first-last>/`, e.g. `reports/laura-langston/family-brief-laura-langston-2026-06-11.pdf`. Present the PDF to Sarah for review — she reviews every report before it goes to a client. Summarize the judgment calls you made (hours estimate, tool picks) so she can adjust them quickly.

## Things that protect the client relationship

- **Never invent facts.** Routines, names, ages, tools tried, quotes — all must come from the session. If the transcript doesn't name something (e.g., a child's age), leave it general rather than guessing.
- **Estimates are drafts.** Hours-back and cost figures are Claude's reasoned drafts for Sarah to confirm, built bottom-up from things the client actually described (see writing guide). Keep them conservative — an inflated promise damages trust.
- **No shame, ever.** Clients in these sessions often describe feeling like bad parents. The report reframes struggles as system problems, not character problems. Recommendations respect constraints the client stated (e.g., if they're hesitant about screens, don't lead with a wall display).
- **Recommend with their grain, not against it.** Strongly prefer tools the client already half-uses (their "almost working" systems) over new apps. A tool that died once (paper calendar, whiteboard) doesn't come back unless the failure reason is addressed.
