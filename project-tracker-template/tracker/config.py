"""Configuration loading with sensible defaults.

A project config only needs to override what differs from DEFAULTS below.
Dicts are merged recursively; lists in the user config replace the default list.
"""

import copy
import json
import os

DEFAULTS = {
    "project": {
        "organization": "Your Organization",
        "name": "Project Rollout",
        "subtitle": "Rollout Tracker",
        "vendor": "",
        "icon": "fa-solid fa-diagram-project",
        "brand_color": "#15803d",
        # "auto" = today's date at build time, or a fixed ISO date "YYYY-MM-DD".
        "as_of": "auto",
    },
    # Wording used across the UI, so the dashboard reads naturally for any project
    # (e.g. unit="Reader"/"Camera"/"Device", site="Site"/"Branch", group="Cluster"/"Region").
    "terms": {
        "unit": "Unit",
        "units": "Units",
        "site": "Site",
        "sites": "Sites",
        "group": "Cluster",
        "groups": "Clusters",
        "facility": "Facility",
        "spare": "Spare",
        "spares": "Spares",
    },
    "excel": {
        # "auto" = newest *.xlsx inside input_dir (ignoring Excel lock files ~$*.xlsx).
        "file": "auto",
        "input_dir": ".",
        # Sheet holding the task / site timeline. Name or 0-based index.
        "timeline_sheet": 0,
        # Row number (1-based) of the column headers, or "auto" to detect it.
        "header_row": "auto",
        # Map of logical field -> list of accepted header captions (case-insensitive).
        "columns": {
            "no": ["no", "no.", "#", "item", "ref"],
            "task": ["task description", "task", "description", "site", "site name", "location name"],
            "quantity": ["quantity", "qty", "units", "no of units"],
            "group": ["area", "cluster", "group", "zone", "branch"],
            "region": ["region", "state"],
            "facility": ["location", "location type", "facility", "facility type", "type"],
            "days": ["no of days", "days", "duration"],
            "start_date": ["start date", "start", "date", "planned date", "install date"],
            "end_date": ["end date", "end", "finish", "finish date"],
            "activities": ["activities", "activity", "scope", "work"],
            "responsibility": ["responsibility", "owner", "pic", "assigned to"],
            "remarks": ["remarks", "remark", "notes", "comments", "comment"],
            "status": ["status", "progress"],
        },
        # Optional cells holding document metadata, e.g. {"title": "A2", "revision": "J2"}.
        "meta_cells": {},
        # Rows whose No/Task text contains any of these (case-insensitive) are ignored.
        "skip_rows_containing": ["total", "this time line is a tentative", "constraints"],
        # Optional RACI / responsibility matrix sheet (name, index, or null to disable).
        "responsibility_sheet": "Responsibility",
        # Values in the RACI matrix that count as "responsible".
        "responsibility_true_values": ["ü", "x", "✓", "✔", "yes", "y", "1", "r", "a", "true"],
        # Optional summary sheet to read the spare count from (label search).
        "summary_sheet": "Summary",
        "spare_label": "spare",
    },
    # Number of spare units. null = try the summary sheet, then fall back to 0.
    "spares": None,
    # A row is treated as a site (deployable location) when ALL these fields are filled.
    # Rows that fail the test become project milestones (PO, setup, UAT ...).
    "site_requires": ["group"],
    # Fields copied from the previous site row when blank (only on rows that have a
    # facility or region value), e.g. ["group", "region"]. Handy for merged/forgotten cells.
    "fill_down": [],
    # Site rows whose end date is more than this many days after the start date (or before it)
    # are treated as typos: reported as build warnings and plotted as a single day. null = off.
    "max_span_days": 60,
    # Quantity used for site rows with an empty quantity cell.
    "default_quantity": 1,
    # Status catalogue. Order = display order.
    #   complete: counts as done for progress %.
    #   action:   shown on the "Action Items & Risks" page.
    #   excluded: removed from scope totals (cancelled / replaced / KIV).
    "statuses": [
        {"key": "done", "label": "Completed", "color": "#16a34a", "icon": "fa-solid fa-check", "complete": True,
         "description": "Completed & operational"},
        {"key": "upcoming", "label": "Upcoming", "color": "#2563eb", "icon": "fa-solid fa-truck",
         "description": "Scheduled for rollout"},
        {"key": "on_hold", "label": "On Hold", "color": "#d97706", "icon": "fa-solid fa-hand", "action": True,
         "description": "Blocked - waiting on site readiness"},
        {"key": "pending", "label": "Pending", "color": "#9333ea", "icon": "fa-solid fa-clock", "action": True,
         "description": "Awaiting decision / date confirmation"},
        {"key": "cancelled", "label": "Cancelled / KIV", "color": "#64748b", "icon": "fa-solid fa-ban", "excluded": True,
         "description": "Removed from scope or reallocated"},
    ],
    # Applied in order, first match wins. See README for the condition syntax.
    "status_rules": [
        {"status": "cancelled", "any": [{"field": "remarks", "contains": ["kiv", "cancel", "removed from scope"]}]},
        {"status": "on_hold", "any": [{"field": "start_date", "contains": ["on hold", "hold"]},
                                      {"field": "remarks", "contains": ["on hold", "not ready"]}]},
        {"status": "pending", "any": [{"field": "start_date", "contains": ["tbc", "tba", "pending"]},
                                      {"field": "start_date", "empty": True}]},
        {"status": "done", "any": [{"field": "start_date", "on_or_before": "as_of"}]},
    ],
    "default_status": "upcoming",
    # Values of an explicit "Status" column mapped to status keys (case-insensitive).
    # If a row's Status cell matches, it overrides status_rules.
    "status_aliases": {
        "done": ["done", "completed", "complete", "installed", "finished", "live"],
        "upcoming": ["upcoming", "scheduled", "planned", "not started"],
        "on_hold": ["on hold", "hold", "blocked"],
        "pending": ["pending", "tbc", "waiting"],
        "cancelled": ["cancelled", "canceled", "kiv", "dropped"],
    },
    # Risk / issue flags. Every flag with at least one site gets a card on the Risks page.
    "flags": [
        {"key": "network", "label": "Network Issue", "color": "#e11d48", "icon": "fa-solid fa-wifi",
         "any": [{"field": "remarks", "contains": ["network", "unstable", "no signal", "connectivity"]}]},
        {"key": "scope", "label": "Scope Change", "color": "#0284c7", "icon": "fa-solid fa-plus",
         "any": [{"field": "remarks", "contains": ["not in original list", "additional", "new installation"]}]},
    ],
    # Optional friendly names per group code, e.g. {"KL": "Kuala Lumpur"}.
    "group_names": {},
    # Milestone rows: status derived from dates unless overridden here by "No" value,
    # e.g. {"16": "In Progress"}. Allowed: "Completed", "In Progress", "Pending".
    "milestone_overrides": {},
    "output": {
        "dir": ".",
        "html": "index.html",
        "json": "project_data.json",
        "csv_prefix": "Project_Rollout",
    },
}


def _deep_merge(base, override):
    result = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def load_config(path=None):
    """Load a JSON config file and merge it over DEFAULTS.

    Relative paths inside the config (excel.input_dir, excel.file, output.dir)
    are resolved against the config file's directory.
    """
    user_cfg = {}
    base_dir = os.getcwd()
    if path:
        with open(path, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        base_dir = os.path.dirname(os.path.abspath(path))

    cfg = _deep_merge(DEFAULTS, user_cfg)
    cfg["_base_dir"] = base_dir

    def _resolve(p):
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(base_dir, p))

    cfg["excel"]["input_dir"] = _resolve(cfg["excel"]["input_dir"])
    if cfg["excel"]["file"] != "auto":
        cfg["excel"]["file"] = _resolve(cfg["excel"]["file"])
    cfg["output"]["dir"] = _resolve(cfg["output"]["dir"])

    keys = {s["key"] for s in cfg["statuses"]}
    for rule in cfg["status_rules"]:
        if rule["status"] not in keys:
            raise ValueError(f"status_rules refers to unknown status '{rule['status']}'")
    if cfg["default_status"] not in keys:
        raise ValueError(f"default_status '{cfg['default_status']}' is not defined in statuses")
    return cfg
