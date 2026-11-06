# Project Rollout Tracker (reusable template)

A config-driven version of the original Face Reader rollout dashboard. You can use it for **any** multi-site
rollout or project timeline: equipment installs, CCTV, network upgrades, branch fit-outs, and so on.

```
Excel workbook  ──►  tracker/parser.py  ──►  project_data.json  ──►  tracker/render.py  ──►  index.html
                         ▲                                              ▲
                         └──────────────── config.json ─────────────────┘
```

Everything that was hard-coded for the original project now lives in `config.json`: company name, vendor, branding colour,
wording ("Reader" vs "Device"), Excel column headers, status rules, risk flags and cluster names. The Python code and
the HTML template do not need to change between projects.

The output is a single self-contained `index.html` that you can open directly, email, or host on GitHub Pages.

## Quick start

```bash
pip install openpyxl
python make_sample.py        # (re)creates sample/sample_project.xlsx
python build.py              # reads config.json -> writes index.html + project_data.json
python build.py --serve      # same, then opens it on http://localhost:8080
```

## Starting a new project

1. **Copy this folder** into a new repository. On GitHub: create an empty repo, then copy the contents of
   `project-tracker-template/` to its root. If you want one-click copies later, tick
   *Settings → Template repository* on that new repo.
2. **Add your workbook.** Put your `.xlsx` in `sample/` (or anywhere, then set `excel.input_dir` / `excel.file`).
   Delete `sample/sample_project.xlsx` if you don't need it. If several workbooks are present, the newest one is used.
3. **Edit `config.json`.** At minimum, set `project`, `terms` and `as_of`. See the reference below.
4. **Build:** `python build.py`, then check the summary and any **Data warnings** it prints.
5. **Publish** (optional): commit `index.html` and enable *Settings → Pages → Deploy from branch (root)*.

## Workbook layout

Only one sheet is required: the timeline (`excel.timeline_sheet`, the first sheet by default). The tracker finds the
header row automatically by matching column captions. Column order doesn't matter, and unknown columns are ignored.

| Field (config key) | Accepted header captions (default)                           | Required |
|--------------------|-------------------------------------------------------------|----------|
| `no`               | No, No., #, Item, Ref                                        |          |
| `task`             | Task Description, Task, Description, Site, Site Name         | ✔        |
| `quantity`         | Quantity, Qty, Units                                         |          |
| `group`            | Area, Cluster, Group, Zone, Branch                           | ✔ for sites |
| `region`           | Region, State                                                |          |
| `facility`         | Location, Location Type, Facility, Facility Type, Type       |          |
| `start_date`       | Start Date, Start, Date, Planned Date, Install Date           |          |
| `end_date`         | End Date, End, Finish                                        |          |
| `activities`, `responsibility`, `remarks`, `status`, `days` | (see `tracker/config.py`) |   |

If your headers are worded differently, add them to `excel.columns`, for example
`"columns": {"group": ["Zone Code"]}`. Note that this **replaces** the default list for that field.

**Sites vs milestones.** A row that has every field in `site_requires` (default `["group"]`) is treated as a **site**
(deployable location). Any other numbered row is a **milestone** (PO, setup, UAT…). Milestone status comes from its
dates relative to `as_of`, unless you set `milestone_overrides`, e.g. `{"16": "In Progress"}`.

**Date cells** can be real dates or text such as `On hold` / `TBC`. Status rules can match on either.

**Optional sheets:**
- `Responsibility`: a RACI matrix. It needs a header row with `Description` followed by department names. Any mark
  (`ü`, `x`, `✓`, `yes`…) in a cell means that department is responsible. If this sheet is missing, the page is hidden.
- `Summary`: the spare count is read from the cell to the right of a label that contains "spare". You can also just set
  `"spares": 2` in the config.

## Config reference

Your `config.json` only needs the keys that differ from the defaults in [`tracker/config.py`](tracker/config.py).
Dicts are merged with the defaults, and lists **replace** them.

| Key | Purpose |
|-----|---------|
| `project.organization / name / subtitle / vendor` | Text in the sidebar, header and footer. Leave `vendor` empty to hide it. |
| `project.icon` | Any [Font Awesome 6](https://fontawesome.com/search?o=r&m=free) class, e.g. `fa-solid fa-video`. |
| `project.brand_color` | Accent colour (hex). |
| `project.as_of` | `"auto"` (today) or `"YYYY-MM-DD"`. Sites dated on/before this count as done (with the default rules). |
| `terms.*` | Wording: unit/units, site/sites, group/groups, facility, spare/spares. |
| `excel.*` | Workbook location, sheet names, header row, column captions, metadata cells, rows to skip. |
| `statuses` | Status catalogue: `key`, `label`, `color`, `icon`, `description`, plus the flags `complete`, `action` and `excluded`. |
| `status_rules` | Ordered rules. The **first match wins**; otherwise `default_status` is used. |
| `status_aliases` | If the sheet has a `Status` column, these values map directly to a status key (this overrides the rules). |
| `flags` | Risk tags (network, scope change…). Each flag with at least one match gets a card on the Risks page. |
| `group_names` | Friendly names, e.g. `{"WPKL": "Kuala Lumpur"}`. |
| `fill_down` | Fields to inherit from the previous site row when blank, e.g. `["group"]`. Each fill is reported as a warning. |
| `max_span_days` | End dates more than N days after the start (likely typos) are warned about and plotted as one day. |
| `output.*` | Output folder, file names and CSV export prefix. |

Status meanings:
- `complete`: counts toward the progress %.
- `action`: listed on the *Action Items & Risks* page.
- `excluded`: removed from the scope totals (cancelled/KIV).

Any status with none of these is treated as "open / upcoming".

### Rule & flag condition syntax

```json
{ "status": "on_hold", "any": [ {"field": "start_date", "contains": ["on hold"]},
                                {"field": "remarks",    "contains": ["cabin not ready"]} ] }
```

- `"any": [...]` matches if any condition is true. `"all": [...]` requires all of them.
- Conditions: `contains: [...]`, `equals: [...]`, `empty: true|false`, `on_or_before: "as_of"|"YYYY-MM-DD"`,
  `after: "as_of"|"YYYY-MM-DD"`. All text matching is case-insensitive.
- `field` can be any column key: `task`, `remarks`, `start_date`, `group`, `quantity`, `facility`…

Example: force specific sites to Pending by name:

```json
{ "status": "pending", "any": [ {"field": "task", "contains": ["kepong", "tioman"]} ] }
```

## Worked example: the original Face Reader workbook

This config reproduces the original dashboard's numbers exactly from
`Project Time Line Face Reader 20_07_2026 (1).xlsx`: 47 sites, 44/51 readers installed, 86.3%, and every site's status
matching.

```json
{
  "project": { "organization": "Client Organization", "name": "Ubio Face Reader Rollout",
               "vendor": "Vendor Sdn Bhd", "as_of": "2026-08-21" },
  "terms": { "unit": "Reader", "units": "Readers" },
  "excel": { "file": "Project Time Line Face Reader 20_07_2026 (1).xlsx", "timeline_sheet": "Time Line" },
  "fill_down": ["group"],
  "status_rules": [
    {"status": "on_hold",   "any": [{"field": "start_date", "contains": ["on hold"]}, {"field": "remarks", "contains": ["cabin not ready"]}]},
    {"status": "pending",   "any": [{"field": "task", "contains": ["kepong", "tioman"]}, {"field": "remarks", "contains": ["reader stand"]}]},
    {"status": "cancelled", "any": [{"field": "remarks", "contains": ["kiv"]}, {"field": "quantity", "empty": true}]},
    {"status": "pending",   "any": [{"field": "start_date", "contains": ["tbc"]}]},
    {"status": "done",      "any": [{"field": "start_date", "on_or_before": "as_of"}]}
  ],
  "milestone_overrides": { "16": "In Progress" }
}
```

The build also flags two real data issues in that workbook: rows 13.7 and 13.8 have an end date in 2027, and row
12.9 has a blank Area cell.

## Files

```text
project-tracker-template/
├── build.py                      # CLI: build (+ --serve)
├── config.json                   # per-project settings (edit this)
├── make_sample.py                # generates the sample workbook
├── sample/sample_project.xlsx    # sample input / layout reference
├── index.html, project_data.json # generated output (from the sample)
└── tracker/
    ├── config.py                 # defaults + config loader
    ├── parser.py                 # Excel -> data (rules, flags, KPIs)
    ├── render.py                 # data -> HTML
    └── dashboard_template.html   # the dashboard UI (Tailwind + Chart.js, data-driven)
```
