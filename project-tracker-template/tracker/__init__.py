"""Generic, config-driven rollout / project-tracker dashboard generator.

Pipeline:  Excel workbook  --(parser)-->  project_data.json  --(render)-->  index.html

Everything project-specific (names, branding, column headers, status rules,
risk flags, group names, terminology) lives in a JSON config file, so the same
code can be reused for any multi-site rollout or project timeline.
"""

from .config import load_config
from .parser import parse_workbook
from .render import render_dashboard

__all__ = ["load_config", "parse_workbook", "render_dashboard"]
