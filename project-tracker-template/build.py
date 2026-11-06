#!/usr/bin/env python3
"""Build (and optionally serve) the project dashboard.

Usage:
    python build.py                          # uses ./config.json
    python build.py --config my_project.json
    python build.py --excel path/to/workbook.xlsx
    python build.py --serve [--port 8080]    # build, then open in a local web server
"""

import argparse
import functools
import http.server
import json
import os
import socketserver
import sys
import threading
import webbrowser

from tracker import load_config, parse_workbook, render_dashboard

HERE = os.path.dirname(os.path.abspath(__file__))


def build(config_path, excel=None):
    cfg = load_config(config_path)
    data = parse_workbook(cfg, excel)
    out = cfg["output"]
    os.makedirs(out["dir"], exist_ok=True)

    json_path = os.path.join(out["dir"], out["json"])
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    html_path = render_dashboard(cfg, data, os.path.join(out["dir"], out["html"]))

    k = data["kpis"]
    print(f"Source workbook : {data['metadata']['source_file']}  (as of {data['metadata']['as_of']})")
    print(f"Sites           : {k['total_sites']} ({k['active_sites']} in scope)")
    print(f"Units           : {k['done_units']}/{k['total_units']} complete ({k['done_pct']}%), spares {k['spares']}")
    print("By status       : " + ", ".join(f"{s['label']}={k['by_status'][s['key']]['units']}" for s in cfg["statuses"]))
    print(f"Milestones      : {len(data['milestones'])}")
    print(f"Wrote           : {html_path}\n                  {json_path}")
    if data.get("warnings"):
        print(f"\nData warnings ({len(data['warnings'])}) - please check the workbook:")
        for w in data["warnings"]:
            print("  - " + w)
    return cfg, html_path


def serve(directory, filename, port):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    for p in range(port, port + 20):
        try:
            httpd = socketserver.TCPServer(("", p), handler)
            break
        except OSError:
            continue
    else:
        sys.exit(f"No free port found in {port}-{port + 19}")
    url = f"http://localhost:{p}/{filename}"
    print(f"\nDashboard live at {url}  (Ctrl+C to stop)")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"), help="project config JSON")
    ap.add_argument("--excel", help="workbook to parse (overrides config excel.file)")
    ap.add_argument("--serve", action="store_true", help="start a local web server after building")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args()

    cfg, html_path = build(args.config, args.excel)
    if args.serve:
        serve(cfg["output"]["dir"], cfg["output"]["html"], args.port)


if __name__ == "__main__":
    main()
