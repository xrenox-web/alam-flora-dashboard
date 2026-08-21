# Alam Flora Sdn Bhd - Ubio Face Reader Project Portal

> **Executive Rollout Tracker for Ubio Face Reader (Ubio X Face & Face Pro) Time Attendance Implementation**  
> **Vendor Partner:** Third Millennium Solutions Sdn Bhd  
> **Revision Date:** 21 August 2026

---

## 📊 Live Dashboard
Open [`index.html`](index.html) or visit the **GitHub Pages URL** to access the interactive web portal.

### Features
- 🏠 **Executive Overview:** High-level KPI pulse, overall status donut, milestone progression, and cluster completion progress bars.
- 📊 **Cluster Analytics:** Area-by-area breakdown across 7 operational clusters (WPKL, WPPJ, AFES, PH1, PH2, PH3, PH4), rollout velocity (S-curve), and facility types.
- 📍 **Site Directory:** Searchable and filterable master directory of all 47 installation sites.
- 📅 **Rollout Schedule:** Visual daily Gantt timeline mapping deployments from July to August 2026.
- ⚠️ **Action Items & Risks:** Detailed tracking for Cabin readiness, stand quotes, and network connectivity.
- 📋 **RACI Governance:** Complete 22-task responsibility matrix across Finance, MIS/IT, HR, and Engineering.

---

## 🚀 How to Run Locally

1. **Prerequisites:** Python 3.8+ with `openpyxl`:
   ```bash
   pip install openpyxl
   ```
2. **Rebuild & View:**
   ```bash
   python app.py
   ```
3. **Launch Local Server:**
   ```bash
   python app.py --serve
   ```

---

## 📁 Repository Structure
```text
├── index.html                                        # GitHub Pages Root Entry (Self-contained interactive dashboard)
├── dashboard.html                                    # Standalone Dashboard Application
├── project_data.json                                 # Structured JSON Database
├── generate_dashboard.py                             # Excel Data Parser & Analyzer
├── generate_html.py                                  # HTML & Charts Generator
├── app.py                                            # Auto-pipeline & Local Web Server
├── Project Time Line Face Reader 20_07_2026 (1).xlsx # Master Excel Workbook
└── README.md                                         # Project Documentation
```
