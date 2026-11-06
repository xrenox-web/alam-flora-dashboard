#!/usr/bin/env python3
"""Generate sample/sample_project.xlsx: a starter workbook showing the expected layout.

Copy it, replace the rows with your own project, and point config.json at it.
Only the "Time Line" sheet is required; "Responsibility" and "Summary" are optional.
"""

import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample", "sample_project.xlsx")
D = dt.datetime

HEADERS = ["No", "Task Description", "Quantity", "Area", "Region", "Location", "No of Days",
           "Start Date", "End Date", "Activities", "Responsibility", "Remarks"]

MILESTONES = [
    (1, "Receive Purchase Order", D(2026, 6, 1), D(2026, 6, 1), "Client"),
    (2, "Vendor stock order & delivery", D(2026, 6, 3), D(2026, 6, 20), "Vendor"),
    (3, "Server & software setup at HQ", D(2026, 6, 22), D(2026, 6, 26), "Vendor & IT"),
    (4, "Staff enrolment / registration", D(2026, 6, 29), D(2026, 7, 10), "HR"),
]

# no, site, qty, area, region, facility, start, remarks
SITES = [
    ("5.1", "North Hub Main Office", 2, "NORTH", "Northern", "Main Office", D(2026, 7, 20), ""),
    ("5.2", "North Hub Warehouse A", 1, "NORTH", "Northern", "Warehouse", D(2026, 7, 21), ""),
    ("5.3", "Riverside Depot", 1, "NORTH", "Northern", "Depot", D(2026, 7, 22), "Unstable network - 4G router requested"),
    ("5.4", "Hilltop Site Office", 1, "NORTH", "Northern", "Site Office", "On hold", "Site cabin not ready"),
    ("6.1", "Central Office Tower", 3, "CENTRAL", "Central", "Main Office", D(2026, 7, 27), ""),
    ("6.2", "Central Workshop", 1, "CENTRAL", "Central", "Workshop", D(2026, 7, 28), ""),
    ("6.3", "Central Mustering Point", 1, "CENTRAL", "Central", "Mustering Point", D(2026, 7, 29), "Additional site, not in original list"),
    ("6.4", "City Parking Depot", 1, "CENTRAL", "Central", "Depot", D(2026, 8, 3), ""),
    ("7.1", "South Port Office", 2, "SOUTH", "Southern", "Office", D(2026, 8, 5), ""),
    ("7.2", "South Landfill Gate", 1, "SOUTH", "Southern", "Site Office", D(2026, 8, 6), "No network connection"),
    ("7.3", "Coastal Depot", 1, "SOUTH", "Southern", "Depot", D(2026, 8, 18), ""),
    ("7.4", "Harbour Mustering Point", 1, "SOUTH", "Southern", "Mustering Point", D(2026, 8, 20), ""),
    ("8.1", "Island Outpost", 1, "EAST", "Eastern", "Mustering Point", "TBC", "Ferry schedule to be confirmed"),
    ("8.2", "East Valley Office", 1, "EAST", "Eastern", "Office", D(2026, 8, 24), ""),
    ("8.3", "East Valley Old Depot", None, "EAST", "Eastern", "Depot", None, "KIV - unit reallocated to East Valley Office"),
]

LATE_MILESTONES = [
    (9, "System Test", D(2026, 8, 26), D(2026, 8, 28), "Vendor & IT"),
    (10, "User Acceptance Test & Project Hand Over", D(2026, 9, 1), D(2026, 9, 4), "All"),
]

RACI_DEPTS = ["Finance", "IT", "HR", "Operations"]
RACI = [
    ("Purchase order and payments", "Finance"),
    ("Network / IP address provisioning", "IT"),
    ("Server and database setup", "IT"),
    ("Staff enrolment data", "HR"),
    ("Site readiness (power, cabin, mounting)", "Operations"),
    ("User acceptance sign-off", "HR,Operations"),
]


def main():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Time Line"
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DDEBF7")

    ws["A2"] = "Time Line for Sample Equipment Installation and Implementation"
    ws["A2"].font = Font(bold=True, size=13)
    ws["G2"] = "Date: 1st June 2026"
    ws["J2"] = "Revise Date: 15th August 2026"
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(4, c, h)
        cell.font, cell.fill = bold, head_fill

    r = 5
    for no, task, start, end, resp in MILESTONES:
        ws.append([no, task, None, None, None, None, (end - start).days + 1, start, end, None, resp, None])
        r += 1
    for no, site, qty, area, region, fac, start, remarks in SITES:
        end = start if isinstance(start, dt.datetime) else None
        ws.append([float(no), site, qty, area, region, fac, 1 if end else None, start, end,
                   "Install and commission unit", "Vendor & Client", remarks or None])
    for no, task, start, end, resp in LATE_MILESTONES:
        ws.append([no, task, None, None, None, None, (end - start).days + 1, start, end, None, resp, None])
    ws.append([None, "Total"])

    for row in ws.iter_rows(min_row=5):
        for cell in row:
            if isinstance(cell.value, dt.datetime):
                cell.number_format = "dd-mmm-yy"
            cell.alignment = Alignment(vertical="top", wrap_text=cell.column == 2)
    for col, width in zip("ABCDEFGHIJKL", (6, 42, 9, 10, 11, 16, 9, 12, 12, 28, 18, 38)):
        ws.column_dimensions[col].width = width

    rs = wb.create_sheet("Responsibility")
    rs["B1"] = "Core Responsibilities"
    rs["B1"].font = bold
    rs.cell(2, 2, "Description").font = bold
    for i, d in enumerate(RACI_DEPTS):
        rs.cell(2, 3 + i, d).font = bold
    for i, (task, owners) in enumerate(RACI, 1):
        rs.cell(3 + i, 1, i)
        rs.cell(3 + i, 2, task)
        for o in owners.split(","):
            rs.cell(3 + i, 3 + RACI_DEPTS.index(o), "x")
    rs.column_dimensions["B"].width = 44

    ss = wb.create_sheet("Summary")
    ss["A2"] = "Summary"
    ss["A4"], ss["B4"] = "Total Spare:", 2

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wb.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
