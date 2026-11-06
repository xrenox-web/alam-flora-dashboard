"""Excel -> structured project data, driven entirely by the config."""

import datetime as dt
import glob
import os
import re

import openpyxl


# --------------------------------------------------------------------------- helpers

def _norm(text):
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def _clean(value):
    if value is None:
        return ""
    return re.sub(r"[ \t]+", " ", str(value)).strip()


def _to_iso(value):
    """Return an ISO date string for date-like cells, else None."""
    if isinstance(value, (dt.datetime, dt.date)):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, str):
        s = value.strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %b %Y", "%d %B %Y"):
            try:
                return dt.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
            except ValueError:
                pass
    return None


def _to_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def _fmt_no(value):
    """Keep "9.1" as "9.1" and 3.0 as "3"."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return _clean(value)


def _get_sheet(wb, ref):
    if ref is None:
        return None
    if isinstance(ref, int):
        return wb.worksheets[ref] if ref < len(wb.worksheets) else None
    for name in wb.sheetnames:  # tolerant name match
        if _norm(name) == _norm(ref):
            return wb[name]
    return None


def find_latest_excel(directory):
    files = [f for f in glob.glob(os.path.join(directory, "*.xlsx"))
             if not os.path.basename(f).startswith("~$")]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


# --------------------------------------------------------------------------- rules

def _field_text(item, field):
    if field in ("start_date", "end_date"):
        return item.get(field + "_text") or item.get(field) or ""
    return str(item.get(field) if item.get(field) is not None else "")


def _check(cond, item, as_of):
    field = cond["field"]
    text = _norm(_field_text(item, field))
    if "contains" in cond:
        return any(_norm(k) in text for k in cond["contains"])
    if "equals" in cond:
        return any(_norm(k) == text for k in cond["equals"])
    if "empty" in cond:
        return (text == "") == bool(cond["empty"])
    if "on_or_before" in cond or "after" in cond:
        date = item.get(field) if field in ("start_date", "end_date") else _to_iso(item.get(field))
        if not date:
            return False
        ref_raw = cond["on_or_before"] if "on_or_before" in cond else cond["after"]
        ref = as_of if ref_raw == "as_of" else (_to_iso(ref_raw) or ref_raw)
        return date <= ref if "on_or_before" in cond else date > ref
    raise ValueError(f"Unsupported condition: {cond}")


def _matches(rule, item, as_of):
    if "all" in rule:
        return all(_check(c, item, as_of) for c in rule["all"])
    if "any" in rule:
        return any(_check(c, item, as_of) for c in rule["any"])
    return False


# --------------------------------------------------------------------------- sheets

def _detect_header(ws, columns_cfg, header_row):
    aliases = {field: {_norm(a) for a in names} for field, names in columns_cfg.items()}

    def map_row(r):
        mapping = {}
        for c in range(1, ws.max_column + 1):
            cap = _norm(ws.cell(r, c).value)
            if not cap:
                continue
            for field, names in aliases.items():
                if field not in mapping and cap in names:
                    mapping[field] = c
                    break
        return mapping

    if header_row != "auto":
        return int(header_row), map_row(int(header_row))

    best = (None, {})
    for r in range(1, min(ws.max_row, 30) + 1):
        m = map_row(r)
        if len(m) > len(best[1]):
            best = (r, m)
    if best[0] is None or "task" not in best[1] or len(best[1]) < 3:
        raise ValueError(
            f"Could not find a header row in sheet '{ws.title}'. "
            "Set excel.header_row or extend excel.columns with your header captions.")
    return best


def _parse_responsibility(wb, cfg):
    ws = _get_sheet(wb, cfg["excel"].get("responsibility_sheet"))
    if ws is None:
        return {"departments": [], "rows": []}

    true_vals = {_norm(v) for v in cfg["excel"]["responsibility_true_values"]}
    header_r, desc_c = None, None
    for r in range(1, min(ws.max_row, 20) + 1):
        for c in range(1, ws.max_column + 1):
            if _norm(ws.cell(r, c).value) in ("description", "task", "task description", "responsibility"):
                if any(_clean(ws.cell(r, cc).value) for cc in range(c + 1, ws.max_column + 1)):
                    header_r, desc_c = r, c
                    break
        if header_r:
            break
    if not header_r:
        return {"departments": [], "rows": []}

    dept_cols = [(c, _clean(ws.cell(header_r, c).value)) for c in range(desc_c + 1, ws.max_column + 1)
                 if _clean(ws.cell(header_r, c).value)]
    rows = []
    for r in range(header_r + 1, ws.max_row + 1):
        desc = _clean(ws.cell(r, desc_c).value)
        if not desc:
            continue
        no = ws.cell(r, desc_c - 1).value if desc_c > 1 else None
        assigned = [name for c, name in dept_cols
                    if _norm(ws.cell(r, c).value) in true_vals
                    or (_clean(ws.cell(r, c).value) and not true_vals)]
        if no is None and not assigned:  # footnotes / section titles
            continue
        rows.append({
            "no": _fmt_no(no) if no is not None else str(len(rows) + 1),
            "task": desc,
            "assigned": assigned,
        })
    return {"departments": [name for _, name in dept_cols], "rows": rows}


def _read_spares(wb, cfg):
    if cfg.get("spares") is not None:
        return int(cfg["spares"])
    ws = _get_sheet(wb, cfg["excel"].get("summary_sheet"))
    if ws is None:
        return 0
    label = _norm(cfg["excel"].get("spare_label", "spare"))
    for row in ws.iter_rows():
        for i, cell in enumerate(row):
            if label and label in _norm(cell.value):
                for nxt in row[i + 1:]:
                    n = _to_number(nxt.value)
                    if n is not None:
                        return int(n)
    return 0


# --------------------------------------------------------------------------- main

def parse_workbook(cfg, file_path=None):
    xcfg = cfg["excel"]
    if not file_path:
        file_path = xcfg["file"] if xcfg["file"] != "auto" else find_latest_excel(xcfg["input_dir"])
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"No Excel workbook found (looked in {xcfg['input_dir']}).")

    as_of = cfg["project"]["as_of"]
    as_of = dt.date.today().isoformat() if as_of in (None, "", "auto") else _to_iso(as_of) or as_of

    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = _get_sheet(wb, xcfg["timeline_sheet"])
    if ws is None:
        raise ValueError(f"Timeline sheet '{xcfg['timeline_sheet']}' not found. Sheets: {wb.sheetnames}")

    header_row, colmap = _detect_header(ws, xcfg["columns"], xcfg["header_row"])

    meta = {k: _clean(ws[ref].value) for k, ref in (xcfg.get("meta_cells") or {}).items()}

    statuses = {s["key"]: s for s in cfg["statuses"]}
    alias_map = {}
    for key, names in (cfg.get("status_aliases") or {}).items():
        for n in names:
            alias_map[_norm(n)] = key
    for s in cfg["statuses"]:
        alias_map.setdefault(_norm(s["label"]), s["key"])
        alias_map.setdefault(_norm(s["key"]), s["key"])

    skip_words = [_norm(w) for w in xcfg.get("skip_rows_containing", [])]
    sites, milestones = [], []
    fill_down = cfg.get("fill_down") or []
    warnings = []
    last_site = None

    def cell(r, field):
        c = colmap.get(field)
        return ws.cell(r, c).value if c else None

    for r in range(header_row + 1, ws.max_row + 1):
        raw = {f: cell(r, f) for f in colmap}
        no, task = _fmt_no(raw.get("no")), _clean(raw.get("task"))
        if not no and not task:
            continue
        probe = f"{_norm(no)} | {_norm(task)}"
        if any(w and (w == _norm(no) or w == _norm(task) or (len(w) > 6 and w in probe)) for w in skip_words):
            continue

        qty = _to_number(raw.get("quantity"))
        item = {
            "row": r,
            "no": no,
            "task": task,
            "quantity": int(qty) if qty is not None else None,
            "group": _clean(raw.get("group")) or None,
            "region": _clean(raw.get("region")) or None,
            "facility": _clean(raw.get("facility")) or None,
            "days": int(_to_number(raw.get("days"))) if _to_number(raw.get("days")) is not None else None,
            "start_date": _to_iso(raw.get("start_date")),
            "start_date_text": None if _to_iso(raw.get("start_date")) else _clean(raw.get("start_date")),
            "end_date": _to_iso(raw.get("end_date")),
            "end_date_text": None if _to_iso(raw.get("end_date")) else _clean(raw.get("end_date")),
            "activities": _clean(raw.get("activities")),
            "responsibility": _clean(raw.get("responsibility")),
            "remarks": _clean(raw.get("remarks")),
            "status_text": _clean(raw.get("status")),
        }

        # Inherit blank fields (e.g. a forgotten Area cell) from the previous site row,
        # but only for rows that otherwise look like a site (have a facility or region).
        if last_site and (item["facility"] or item["region"]):
            for f in fill_down:
                if item.get(f) in (None, ""):
                    item[f] = last_site.get(f)
                    item.setdefault("filled", []).append(f)

        is_site = all(item.get(f) not in (None, "") for f in cfg["site_requires"])
        if is_site:
            last_site = item
            _check_dates(item, cfg.get("max_span_days"), warnings)
            status = alias_map.get(_norm(item["status_text"])) if item["status_text"] else None
            if not status:
                status = next((rule["status"] for rule in cfg["status_rules"] if _matches(rule, item, as_of)),
                              cfg["default_status"])
            item["status"] = status
            if item["quantity"] is None:
                item["quantity"] = 0 if statuses[status].get("excluded") else cfg["default_quantity"]
            item["flags"] = [f["key"] for f in cfg.get("flags", []) if _matches(f, item, as_of)]
            sites.append(item)
        else:
            override = (cfg.get("milestone_overrides") or {}).get(no)
            if override:
                m_status = override
            elif item["end_date"] and item["end_date"] <= as_of:
                m_status = "Completed"
            elif item["start_date"] and item["start_date"] <= as_of:
                m_status = "In Progress" if item["end_date"] else "Completed"
            else:
                m_status = "Pending"
            item["status"] = m_status
            milestones.append(item)

    for it in sites:
        for f in it.get("filled", []):
            warnings.append(f"Row {it['row']} (No {it['no']}): blank '{f}' filled from previous row -> {it[f]}")
    summary = build_summary(cfg, sites, milestones, _parse_responsibility(wb, cfg), _read_spares(wb, cfg),
                            meta, as_of, os.path.basename(file_path))
    summary["warnings"] = warnings
    return summary


def _check_dates(item, max_span, warnings):
    """Catch typos like an end date a year after the start date."""
    s, e = item["start_date"], item["end_date"]
    if not (s and e):
        return
    span = (dt.date.fromisoformat(e) - dt.date.fromisoformat(s)).days
    if span < 0 or (max_span and span > max_span):
        warnings.append(f"Row {item['row']} (No {item['no']}): end date {e} looks wrong vs start {s}; "
                        f"plotted as a single day")
        item["end_date_original"] = e
        item["end_date"] = s


def build_summary(cfg, sites, milestones, responsibility, spares, meta, as_of, source_file):
    statuses = cfg["statuses"]
    excluded = {s["key"] for s in statuses if s.get("excluded")}
    complete = {s["key"] for s in statuses if s.get("complete")}
    in_scope = [s for s in sites if s["status"] not in excluded]

    total_units = sum(s["quantity"] for s in in_scope)
    done_units = sum(s["quantity"] for s in in_scope if s["status"] in complete)

    by_status = {}
    for st in statuses:
        members = [s for s in sites if s["status"] == st["key"]]
        by_status[st["key"]] = {"sites": len(members), "units": sum(m["quantity"] for m in members)}

    groups = {}
    for s in in_scope:
        g = groups.setdefault(s["group"] or "Other", {"sites": 0, "units": 0, "done_units": 0, "done_sites": 0,
                                                       "region": s["region"] or ""})
        g["sites"] += 1
        g["units"] += s["quantity"]
        if s["status"] in complete:
            g["done_units"] += s["quantity"]
            g["done_sites"] += 1
    for g in groups.values():
        g["pct"] = round(g["done_units"] / g["units"] * 100, 1) if g["units"] else 0.0

    facilities = {}
    for s in in_scope:
        name = s["facility"] or "Other"
        key = next((k for k in facilities if k.lower() == name.lower()), name)  # merge "Site office"/"Site Office"
        f = facilities.setdefault(key, {"sites": 0, "units": 0})
        f["sites"] += 1
        f["units"] += s["quantity"]

    # Planned vs actual cumulative curve, by start date.
    dated = sorted({s["start_date"] for s in in_scope if s["start_date"]})
    curve, cum_plan, cum_done = [], 0, 0
    for d in dated:
        day = [s for s in in_scope if s["start_date"] == d]
        planned = sum(s["quantity"] for s in day)
        done = sum(s["quantity"] for s in day if s["status"] in complete)
        cum_plan += planned
        cum_done += done
        curve.append({"date": d, "planned": planned, "done": done,
                      "cum_planned": cum_plan, "cum_done": cum_done})

    flags = {f["key"]: [s["row"] for s in sites if f["key"] in s["flags"]] for f in cfg.get("flags", [])}

    return {
        "metadata": {
            "source_file": source_file,
            "as_of": as_of,
            "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            **meta,
        },
        "kpis": {
            "total_sites": len(sites),
            "active_sites": len(in_scope),
            "total_units": total_units,
            "spares": spares,
            "total_units_with_spares": total_units + spares,
            "done_units": done_units,
            "done_sites": sum(1 for s in in_scope if s["status"] in complete),
            "done_pct": round(done_units / total_units * 100, 1) if total_units else 0.0,
            "by_status": by_status,
            "flags": {k: len(v) for k, v in flags.items()},
        },
        "groups": groups,
        "facilities": facilities,
        "curve": curve,
        "milestones": milestones,
        "sites": sites,
        "responsibility": responsibility,
    }
