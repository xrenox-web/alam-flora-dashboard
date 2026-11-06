"""Inject config + parsed data into the static dashboard template."""

import json
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_template.html")

# Only these config sections are needed by the browser.
_PUBLIC_CONFIG_KEYS = ("project", "terms", "statuses", "flags", "group_names")


def _safe_json(obj):
    # Prevent "</script>" (or any "</") inside Excel text from breaking out of the script tag.
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def render_dashboard(cfg, data, output_path):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    public_cfg = {k: cfg[k] for k in _PUBLIC_CONFIG_KEYS if k in cfg}
    # Only the CSV prefix is needed client-side; never expose local folder paths.
    public_cfg["output"] = {"csv_prefix": cfg["output"].get("csv_prefix", "Project_Rollout")}
    page_title = f"{cfg['project']['organization']} - {cfg['project']['name']}"
    html = (template
            .replace("__PAGE_TITLE__", _html_escape(page_title))
            .replace("__CONFIG_JSON__", _safe_json(public_cfg))
            .replace("__DATA_JSON__", _safe_json(data)))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def _html_escape(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))
