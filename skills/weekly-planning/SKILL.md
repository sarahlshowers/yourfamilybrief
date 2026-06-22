---
name: weekly-planning
description: >
  Plan next week by pulling tasks from the Blue Sky dashboard and carryovers from the
  prior week, checking Google Calendar for scheduling constraints, and creating the
  weekly planning doc in Notion. Trigger whenever Sarah says "plan next week", "let's
  do weekly planning", "set up next week", "create the week doc", or any variation of
  wanting to plan or prep for the upcoming week. Always invoke this skill — Sarah uses
  it every Sunday evening or Monday morning as her weekly planning ritual.
---

# Weekly Planning Skill

This skill builds the upcoming week's Notion planning page by reading what Sarah has already
queued on the Blue Sky dashboard, pulling carryovers from last week, and checking Google
Calendar for scheduling constraints.

The hub lives at https://app.notion.com/p/947e7abcffbf83ccbbcc8128e08d68aa.

---

## Step 1: Read the Blue Sky Dashboard

Navigate to the Blue Sky hub using `mcp__Claude_in_Chrome__navigate` (tabId optional — let
it auto-select), then read the full page with `mcp__Claude_in_Chrome__get_page_text`.

From the page text, extract two things:

**A. This Week's Goals per bucket** — they appear in the "This Week" section under the
Buckets table. The format is:
```
Bucket Name
This Week's Goal: [text]
```
Grab the goal text for each bucket: Job Search, AI Learning, Content, Admin, FamilyOS.
If Blue Sky/Wildcard shows "N/A" or is replaced by FamilyOS, note that.

**B. Tasks on the "This Week" board** — the Task Breakdown board shows cards grouped by
status (Todo, Working On, Paused/Waiting, Done). Under each status group, task names appear
as plain text lines. Read all visible tasks under Todo and Working On — these are what's
been scheduled. Group them mentally by their bucket prefix or context (Admin, Job Search,
AI Learning, Content, FamilyOS/YFB). Ignore Done tasks.

---

## Step 2: Pull Carryovers from Last Week

Use `notion-search` with query "Week of" to find the most recent weekly planning page.
Fetch it with `notion-fetch`.

From that page extract:
- **Unchecked tasks** (lines starting with `- [ ]`) in the Tasks section — these didn't
  get done and may need to carry forward
- **"What's Carrying Over"** paragraph from the Wrap-Up section — this is Sarah's own
  explicit list of what needs to follow her into next week

Cross-reference with the dashboard board: if a carryover task is already on the board
(step 1B), it's covered and you don't need to add it again. Only surface things that
aren't already queued.

---

## Step 3: Check Google Calendar for Next Week

Navigate to next week's Google Calendar view:
`https://calendar.google.com/calendar/r/week/YYYY/M/D`

Use the correct Monday date for next week. Then read with `get_page_text`.

The calendar week view in Google Calendar runs Monday through Sunday — read all 7 days.

**Only read events from Sarah's calendars:** The Showers Fam, Baby Showers, Sophie's
Calendar, Holidays, and events marked Personal. Completely ignore anything from:
- **Welcome Compass** calendar — that's Derrick's work, not relevant to Sarah's week
- **Derrick** calendar — his personal events are not Sarah's scheduling constraints

Look for:
- **Doctor/medical appointments** (OB, echo, pediatrician, any health event on Baby Showers or Personal)
- **Sophie school schedule anomalies** — half days (school ends before 3pm), no school,
  last day of school, first day of summer camp
- **Summer camp or childcare events** — especially in summer when school is out
- **Extracurriculars** — dance, Girl Scouts, sports, anything on The Showers Fam or Sophie's Calendar
- **Travel** — road trips, flights, "Florida", "away", multi-day events on The Showers Fam
- **Family events** — anything on The Showers Fam that affects Sarah's day

Ignore routine recurring events (bus dropoff, evening routine, FAMILY TODO LIST reminders,
school 8:50–3pm on a normal day). Focus on what's different from a typical week.

Synthesize the calendar into a "Calendar Watch" section: one bullet per day that has
something noteworthy. Skip days that are completely normal.

---

## Step 4: Determine Realistic Hours

Based on the calendar anomalies, estimate total usable work hours for the week. A full
normal week is ~35–40 hrs. Adjust down for:
- Medical appointments: subtract 2–3 hrs per appointment day
- Sophie half days (pickup at 11:15am): subtract ~3 hrs from that day
- Last day of school (early pickup): very short day
- Travel prep days (packing, loading car): subtract 2–3 hrs from that day

**Travel on the calendar does not mean time off.** Do not reduce hours or deprioritize
work just because there's a road trip or multi-day travel event. Sarah works remotely and
may be traveling while working a full week. Only reduce hours if the calendar shows
explicitly blocked time (e.g., "driving all day", "no work this week") or Sarah says so.

When travel is detected, note it briefly in Calendar Watch (e.g., "Florida trip in
progress — working remotely") and otherwise plan the week normally.

**Job applications are a standing weekly requirement for unemployment insurance.** Even
in travel weeks or weeks when other priorities are high, job apps must appear in the
Job Search task list. Don't drop them.

State the estimated total as a callout in the page so the goals feel grounded.

---

## Step 5: Build the Goals Table

Using the dashboard bucket goals (Step 1A) as background context, construct the goals
table. Adjust "This week" hour targets proportionally if it's a short week. The normal
targets are:

| Bucket | Normal target |
|--------|--------------|
| 🎯 Job Search & Pipeline | 14 hrs |
| 🧠 AI Learning & Building | 12 hrs |
| 🌤️ FamilyOS / Your Family Brief | 4 hrs |
| 📱 Content & Social Media | 8 hrs |
| 🔁 Admin & Reflection | 2 hrs |

**Write the "This week's outcome" column fresh for each week — do not copy the dashboard
goal text.** The dashboard goals are standing directional targets; the outcome column
should say what success looks like *specifically this week* given the tasks queued, the
carryovers, and the calendar. Think: if Sarah looks back on Friday, what would make her
say this week was a win for each bucket?

Good outcomes are concrete and completable:
- Bad: "Find your north star and talk about it on Friday" (vague, dashboard copy)
- Good: "10 applications out the door (5 dev + 5 dev-adjacent). North star written down before Friday wrap-up."

- Bad: "Have something interesting to share" (generic)
- Good: "One topic chosen and a LinkedIn post or walk-and-talk recorded by Friday."

- Bad: "Research and pitch 10 emails. Post every day." (task list, not outcome)
- Good: "Daily posting streak holds Mon–Fri. 3 World Cup scripts cleared. Testimonial post live once Laura or Andi responds."

---

## Step 6: Build the Tasks Section

Organize tasks by bucket with checkbox format. Sources in priority order:
1. **Dashboard board tasks** (Step 1B) — already queued by Sarah, include them as-is
2. **Carryovers not on the board** (Step 2) — add with a "(carries from last week)" note

Within each bucket, lead with the most time-sensitive or blocking item. Admin items that
have been carrying multiple weeks (like COBRA) get a nudge note.

Use this structure:
```
### 🔁 Admin — Do First
- [ ] **COBRA** — action it the day the letter arrives (call 1-855-783-4772)

### 🌤️ FamilyOS / Your Family Brief
- [ ] [tasks]

### 🎯 Job Search
- [ ] [tasks]

### 🧠 AI Learning & Building
- [ ] [tasks]

### 📱 Content & Social Media
- [ ] [tasks]
```

---

## Step 7: Create the Notion Page

Create a new sub-page under the Blue Sky Hub (page_id: `947e7abcffbf83ccbbcc8128e08d68aa`)
using `notion-create-pages`.

**Title format:** `📅 Week of [Month Day]` using the Monday date (e.g., "📅 Week of June 22")

Weeks run **Monday through Sunday**. All date references, calendar coverage, and daily
wrap-up slots should span the full 7 days — Mon through Sun.

**Page structure:**

```
## 🎯 This Week's Goals
[goals table]

> ⚠️ [Short week / travel note if applicable — estimated usable hours]

---
## 🗓️ Calendar Watch
[one bullet per notable day — Mon through Sun]

---
## ✅ This Week's Tasks
[tasks by bucket]

---
## 🗓️ Daily Wrap-Ups

### Mon [Date]

### Tue [Date]

### Wed [Date]

### Thu [Date]

### Fri [Date]

### Sat [Date]

### Sun [Date]

---
## 📋 Wrap-Up (Friday)

**The Goals**

**What Got Done**

**What's Carrying Over**

**Side Quests / Emergent Work**
```

---

## Step 8: Confirm

After creating the page, share the Notion link and give Sarah a two-sentence summary:
what the week looks like at a glance and the one thing most likely to make or break it.

---

## Notes

- Do NOT pull from the Family Planning page — that's a separate system.
- The weekly page lives as a sub-page of the Blue Sky Hub, not inside any database.
- If the prior week's Wrap-Up hasn't been filled in yet, the unchecked tasks section
  is your best signal for carryovers.
- Chrome extension tools: use `mcp__Claude_in_Chrome__navigate` and
  `mcp__Claude_in_Chrome__get_page_text`. The tabId is optional on standalone navigate.
- Notion tools: `notion-search`, `notion-fetch`, `notion-create-pages`.
- Style: no em dashes, no AI filler openers, warm and direct, past/present tense as
  appropriate. Tasks are imperative. The weekly plan should feel like Sarah wrote it.
