"""
Ubio Face Reader Project Progress Dashboard
Automated Pipeline & Local Viewer Server
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading
from generate_dashboard import parse_excel, find_latest_excel
from generate_html import generate_html_dashboard
import json

PORT = 8080
DATA_JSON = 'project_data.json'
DASHBOARD_HTML = 'dashboard.html'

def build():
    latest_excel = find_latest_excel()
    if not latest_excel:
        print("Error: No Excel workbook (.xlsx) found in current directory.")
        sys.exit(1)
        
    print(f"[1/2] Parsing latest Excel workbook: {latest_excel}...")
    data = parse_excel(latest_excel)
    
    with open(DATA_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"      Extracted {data['kpis']['total_sites']} sites and {data['kpis']['total_readers']} site readers (+ {data['kpis']['total_spare']} spares).")
    print(f"      Current Progress: {data['kpis']['installed_readers']}/{data['kpis']['total_readers']} units installed ({data['kpis']['installed_pct']}%).")
    
    print(f"[2/2] Generating interactive Corporate Web Dashboard: {DASHBOARD_HTML}...")
    generate_html_dashboard(DATA_JSON, DASHBOARD_HTML)
    print("      Dashboard build completed successfully.")

def serve():
    build()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = http.server.SimpleHTTPRequestHandler
    current_port = PORT
    server = None
    for p in range(PORT, PORT + 20):
        try:
            server = socketserver.TCPServer(("", p), handler)
            current_port = p
            break
        except OSError:
            continue
            
    if not server:
        print(f"Opening {DASHBOARD_HTML} directly in browser...")
        webbrowser.open(os.path.abspath(DASHBOARD_HTML))
        return

    url = f"http://localhost:{current_port}/{DASHBOARD_HTML}"
    print(f"\n========================================================")
    print(f"🚀 Project Dashboard is LIVE at:")
    print(f"   {url}")
    print(f"========================================================\n")
    
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.shutdown()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--serve':
        serve()
    else:
        build()
        print(f"\nTo view the dashboard, open '{DASHBOARD_HTML}' directly in any browser.")
        print(f"Or run 'python app.py --serve' to launch a local server with auto-open browser.")
