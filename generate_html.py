import json
import os

def generate_html_dashboard(data_json_path, output_html_path):
    with open(data_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    data_str = json.dumps(data, ensure_ascii=False)
    source_file = data.get('metadata', {}).get('source_file', 'Project Time Line Face Reader 20_07_2026 (1).xlsx')
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ubio Face Reader Project Portal</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Plus Jakarta Sans', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }},
                    colors: {{
                        brand: {{
                            50: '#f0fdf4',
                            100: '#dcfce7',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d',
                            800: '#166534',
                            900: '#14532d',
                        }},
                        navy: {{
                            50: '#f8fafc',
                            100: '#f1f5f9',
                            200: '#e2e8f0',
                            700: '#334155',
                            800: '#1e293b',
                            900: '#0f172a',
                            950: '#0b0f19'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #f1f5f9;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}
        .clean-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }}
        .clean-card:hover {{
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
        }}
        .nav-item.active {{
            background-color: #f0fdf4;
            color: #15803d;
            font-weight: 700;
            border-left: 3px solid #16a34a;
        }}
        .nav-item:not(.active) {{
            border-left: 3px solid transparent;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            #sidebar {{ display: none !important; }}
            #sidebar-backdrop {{ display: none !important; }}
            main {{ margin-left: 0 !important; max-width: 100% !important; padding: 0 !important; }}
            body {{ background-color: #fff !important; color: #000 !important; }}
            .clean-card {{ box-shadow: none !important; border: 1px solid #cbd5e1 !important; }}
        }}
    </style>
</head>
<body class="min-h-screen flex bg-slate-50 antialiased relative">

    <!-- Mobile Backdrop Overlay -->
    <div id="sidebar-backdrop" onclick="closeSidebar()" class="fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-40 hidden md:hidden transition-opacity"></div>

    <!-- SIDEBAR NAVIGATION -->
    <aside id="sidebar" class="-translate-x-full md:translate-x-0 w-64 bg-white border-r border-slate-200 flex flex-col justify-between fixed inset-y-0 left-0 z-50 shadow-lg md:shadow-xs transition-transform duration-300 ease-in-out no-print">
        <div class="flex flex-col h-full">
            
            <!-- Brand Header with Mobile Close Button -->
            <div class="p-5 border-b border-slate-100 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-emerald-700 flex items-center justify-center text-white font-extrabold text-lg shadow-md shadow-emerald-700/20">
                        <i class="fa-solid fa-id-card-clip"></i>
                    </div>
                    <div>
                        <h1 class="text-sm font-bold text-slate-900 leading-tight">Project Portal</h1>
                        <p class="text-[11px] text-emerald-700 font-semibold tracking-wide uppercase">Face Reader Rollout</p>
                    </div>
                </div>

                <!-- Mobile Close Button (X) -->
                <button onclick="closeSidebar()" class="md:hidden w-8 h-8 rounded-lg bg-slate-100 text-slate-500 hover:text-slate-900 hover:bg-slate-200 flex items-center justify-center transition" aria-label="Close Sidebar">
                    <i class="fa-solid fa-xmark text-sm"></i>
                </button>
            </div>

            <!-- Navigation Links -->
            <div class="p-3 space-y-1.5 flex-1 overflow-y-auto custom-scrollbar">
                <div class="px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">Main Menu</div>
                
                <button onclick="navigateTo('overview')" id="nav-overview" class="nav-item active w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition">
                    <i class="fa-solid fa-chart-pie w-4 text-center"></i>
                    <span>Executive Overview</span>
                </button>

                <button onclick="navigateTo('analytics')" id="nav-analytics" class="nav-item w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition">
                    <i class="fa-solid fa-chart-column w-4 text-center"></i>
                    <span>Cluster Analytics</span>
                </button>

                <button onclick="navigateTo('sites')" id="nav-sites" class="nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition">
                    <div class="flex items-center gap-3">
                        <i class="fa-solid fa-list-check w-4 text-center"></i>
                        <span>Site Directory</span>
                    </div>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700">47</span>
                </button>

                <button onclick="navigateTo('schedule')" id="nav-schedule" class="nav-item w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition">
                    <i class="fa-solid fa-calendar-days w-4 text-center"></i>
                    <span>Rollout Schedule</span>
                </button>

                <div class="pt-4 px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">Governance & Action</div>

                <button onclick="navigateTo('issues')" id="nav-issues" class="nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition">
                    <div class="flex items-center gap-3">
                        <i class="fa-solid fa-triangle-exclamation w-4 text-center text-amber-500"></i>
                        <span>Action Items & Risks</span>
                    </div>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">4</span>
                </button>

                <button onclick="navigateTo('raci')" id="nav-raci" class="nav-item w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition">
                    <i class="fa-solid fa-users-gear w-4 text-center"></i>
                    <span>RACI Governance</span>
                </button>
            </div>

            <!-- Sidebar Footer -->
            <div class="p-4 border-t border-slate-100 bg-slate-50/70 space-y-2.5 text-xs">
                <div class="flex items-center justify-between text-slate-500 text-[11px]">
                    <span>Revision Date:</span>
                    <span class="font-bold text-slate-700 font-mono">21 Aug 2026</span>
                </div>
                <div class="flex flex-col gap-0.5 text-slate-500 text-[11px]">
                    <span>Vendor Partner:</span>
                    <span class="font-bold text-slate-800 font-mono text-[11px] leading-tight">Implementation Vendor</span>
                </div>
                <div class="pt-2 border-t border-slate-200 flex items-center gap-2">
                    <button onclick="exportToCSV()" class="flex-1 py-1.5 px-2 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded-lg text-[11px] font-semibold flex items-center justify-center gap-1.5 transition shadow-2xs">
                        <i class="fa-solid fa-file-csv text-emerald-600"></i>
                        <span>Export</span>
                    </button>
                    <button onclick="window.print()" class="flex-1 py-1.5 px-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-[11px] font-semibold flex items-center justify-center gap-1.5 transition shadow-2xs">
                        <i class="fa-solid fa-print"></i>
                        <span>Print</span>
                    </button>
                </div>
            </div>

        </div>
    </aside>

    <!-- MAIN CONTENT AREA -->
    <div class="flex-1 flex flex-col ml-0 md:ml-64 min-h-screen">

        <!-- Top Header Bar with Hamburger for Mobile -->
        <header class="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between shadow-2xs">
            <div class="flex items-center gap-3">
                <button onclick="openSidebar()" class="md:hidden w-9 h-9 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700 hover:text-slate-900 hover:bg-slate-200 transition no-print" aria-label="Open Navigation Menu">
                    <i class="fa-solid fa-bars text-sm"></i>
                </button>
                <div>
                    <div class="text-[11px] font-semibold text-emerald-700 uppercase tracking-wider font-mono">Ubio Face Reader Rollout</div>
                    <h2 id="page-title" class="text-sm sm:text-base font-bold text-slate-900 leading-tight">Executive Progress Overview</h2>
                </div>
            </div>

            <div class="flex items-center gap-3 text-xs">
                <div class="flex items-center gap-2 bg-slate-100 px-2.5 py-1.5 rounded-lg border border-slate-200 font-mono">
                    <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span class="text-slate-600 text-[11px] sm:text-xs">Health: <strong class="text-emerald-700 font-bold">86.3% Done</strong></span>
                </div>
                <div class="text-slate-400 font-mono hidden lg:block text-[11px]">
                    As of: 21 Aug 2026
                </div>
            </div>
        </header>

        <!-- Page Views Container -->
        <main class="flex-1 p-4 sm:p-6 lg:p-8 max-w-6xl w-full mx-auto space-y-6">

            <!-- ==================================================================== -->
            <!-- PAGE 1: EXECUTIVE OVERVIEW -->
            <!-- ==================================================================== -->
            <div id="page-overview" class="page-content space-y-6">
                
                <!-- 4 Top Executive KPI Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <!-- Total Scope -->
                    <div onclick="navigateTo('sites')" class="clean-card p-5 border-l-4 border-l-slate-700 flex flex-col justify-between cursor-pointer hover:border-slate-400 hover:shadow-md group transition" title="Click to view Site Directory">
                        <div class="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider">
                            <span>Total Hardware Scope</span>
                            <span class="w-8 h-8 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center text-xs group-hover:bg-slate-200 transition">
                                <i class="fa-solid fa-layer-group"></i>
                            </span>
                        </div>
                        <div class="mt-4 flex items-baseline justify-between">
                            <div class="text-3xl font-extrabold text-slate-900 font-mono" id="ov-total-readers">51</div>
                            <span class="text-xs text-slate-500 font-semibold">47 Sites (+ 2 Spares)</span>
                        </div>
                        <div class="text-[10px] text-slate-400 group-hover:text-slate-700 flex items-center gap-1 mt-2 font-semibold">
                            <span>View Site Directory</span>
                            <i class="fa-solid fa-arrow-right text-[8px] group-hover:translate-x-0.5 transition-transform"></i>
                        </div>
                    </div>

                    <!-- Installed Completion -->
                    <div onclick="navigateTo('sites'); filterByStatus('Installed');" class="clean-card p-5 border-l-4 border-l-emerald-600 bg-emerald-50/20 flex flex-col justify-between cursor-pointer hover:border-emerald-500 hover:shadow-md group transition" title="Click to view Installed Sites">
                        <div class="flex items-center justify-between text-emerald-800 text-xs font-bold uppercase tracking-wider">
                            <span>Installed & Operational</span>
                            <span class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center text-xs group-hover:bg-emerald-200 transition">
                                <i class="fa-solid fa-check"></i>
                            </span>
                        </div>
                        <div class="mt-4 flex items-baseline justify-between">
                            <div class="text-3xl font-extrabold text-emerald-700 font-mono" id="ov-installed-readers">44</div>
                            <span class="text-xs font-bold font-mono text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full" id="ov-installed-pct">86.3% Rate</span>
                        </div>
                        <div class="text-[10px] text-emerald-700 group-hover:text-emerald-900 flex items-center gap-1 mt-2 font-semibold">
                            <span>View 40 Operational Sites</span>
                            <i class="fa-solid fa-arrow-right text-[8px] group-hover:translate-x-0.5 transition-transform"></i>
                        </div>
                    </div>

                    <!-- Upcoming Rollout -->
                    <div onclick="navigateTo('schedule')" class="clean-card p-5 border-l-4 border-l-blue-600 flex flex-col justify-between cursor-pointer hover:border-blue-500 hover:shadow-md group transition" title="Click to view Rollout Schedule">
                        <div class="flex items-center justify-between text-blue-700 text-xs font-bold uppercase tracking-wider">
                            <span>Upcoming Deployments</span>
                            <span class="w-8 h-8 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center text-xs group-hover:bg-blue-100 transition">
                                <i class="fa-solid fa-truck"></i>
                            </span>
                        </div>
                        <div class="mt-4 flex items-baseline justify-between">
                            <div class="text-3xl font-extrabold text-blue-700 font-mono" id="ov-upcoming-readers">3</div>
                            <span class="text-xs text-slate-500 font-medium">Johor Port & Tg. Bin</span>
                        </div>
                        <div class="text-[10px] text-blue-600 group-hover:text-blue-800 flex items-center gap-1 mt-2 font-semibold">
                            <span>View Rollout Schedule</span>
                            <i class="fa-solid fa-arrow-right text-[8px] group-hover:translate-x-0.5 transition-transform"></i>
                        </div>
                    </div>

                    <!-- On Hold / Pending Action (Navigates to Action Items & Risks) -->
                    <div onclick="navigateTo('issues')" class="clean-card p-5 border-l-4 border-l-amber-500 bg-amber-50/20 flex flex-col justify-between cursor-pointer hover:border-amber-500 hover:shadow-md group transition ring-2 ring-amber-400/30" title="Click to view Action Items & Risks page">
                        <div class="flex items-center justify-between text-amber-800 text-xs font-bold uppercase tracking-wider">
                            <span>On Hold / Pending</span>
                            <span class="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center text-xs group-hover:bg-amber-200 transition">
                                <i class="fa-solid fa-triangle-exclamation"></i>
                            </span>
                        </div>
                        <div class="mt-4 flex items-baseline justify-between">
                            <div class="text-3xl font-extrabold text-amber-700 font-mono" id="ov-action-readers">4</div>
                            <span class="text-xs text-amber-800 font-semibold bg-amber-100 px-2 py-0.5 rounded-full">2 Cabin + 2 Pending</span>
                        </div>
                        <div class="text-[10px] text-amber-800 group-hover:text-amber-950 flex items-center justify-between mt-2 pt-2 border-t border-amber-200 font-bold">
                            <span>View Action Items & Risks</span>
                            <i class="fa-solid fa-arrow-right text-[9px] group-hover:translate-x-1 transition-transform"></i>
                        </div>
                    </div>
                </div>

                <!-- Executive Highlights Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

                    <!-- Deployment Breakdown Donut -->
                    <div class="clean-card p-6 flex flex-col justify-between">
                        <div>
                            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                <i class="fa-solid fa-chart-pie text-emerald-600"></i>
                                Overall Deployment Status
                            </h3>
                            <p class="text-xs text-slate-500 mt-0.5">Summary of all 51 site devices</p>
                        </div>
                        
                        <div class="relative h-48 my-3 flex items-center justify-center">
                            <canvas id="ov-chart-donut"></canvas>
                        </div>

                        <div class="grid grid-cols-2 gap-2 text-xs pt-3 border-t border-slate-100 font-medium">
                            <div onclick="navigateTo('sites'); filterByStatus('Installed');" class="flex items-center justify-between p-1.5 rounded bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-transparent hover:border-emerald-200" title="Click to view Installed sites">
                                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-600"></span> Installed</span>
                                <span class="font-bold text-slate-900 font-mono">44</span>
                            </div>
                            <div onclick="navigateTo('schedule')" class="flex items-center justify-between p-1.5 rounded bg-slate-50 hover:bg-blue-50 cursor-pointer transition border border-transparent hover:border-blue-200" title="Click to view Upcoming schedule">
                                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-blue-600"></span> Upcoming</span>
                                <span class="font-bold text-slate-900 font-mono">3</span>
                            </div>
                            <div onclick="navigateTo('issues')" class="flex items-center justify-between p-1.5 rounded bg-slate-50 hover:bg-amber-50 cursor-pointer transition border border-transparent hover:border-amber-200" title="Click to view On Hold Cabin items">
                                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500"></span> On Hold</span>
                                <span class="font-bold text-slate-900 font-mono">2</span>
                            </div>
                            <div onclick="navigateTo('issues')" class="flex items-center justify-between p-1.5 rounded bg-slate-50 hover:bg-purple-50 cursor-pointer transition border border-transparent hover:border-purple-200" title="Click to view Pending items">
                                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-purple-600"></span> Pending</span>
                                <span class="font-bold text-slate-900 font-mono">2</span>
                            </div>
                        </div>
                    </div>

                    <!-- Cluster Completion Progress Bars -->
                    <div class="lg:col-span-2 clean-card p-6 flex flex-col justify-between">
                        <div class="flex items-center justify-between">
                            <div>
                                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                    <i class="fa-solid fa-bars-progress text-blue-600"></i>
                                    Cluster Progress Summary
                                </h3>
                                <p class="text-xs text-slate-500 mt-0.5">Deployment status by geographic area</p>
                            </div>
                            <button onclick="navigateTo('analytics')" class="text-xs font-semibold text-blue-600 hover:text-blue-800 transition flex items-center gap-1">
                                <span>Detailed Charts</span>
                                <i class="fa-solid fa-arrow-right text-[10px]"></i>
                            </button>
                        </div>

                        <div class="space-y-3.5 my-3" id="ov-cluster-bars">
                            <!-- Populated dynamically by JS -->
                        </div>

                        <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                            <span>4 of 7 Clusters Completed / High Completion</span>
                            <span class="font-mono font-semibold text-emerald-700">WPKL (87.5%), PH3 (100%), PH4 (100%), WPPJ (100%)</span>
                        </div>
                    </div>

                </div>

                <!-- Clean Milestone Stepper -->
                <div class="clean-card p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                            <i class="fa-solid fa-diagram-project text-purple-600"></i>
                            Project Milestones Status
                        </h3>
                        <span class="text-xs font-mono text-slate-500">Stage 4 / 6 Active</span>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                        <div class="p-3 rounded-xl bg-emerald-50/70 border border-emerald-200">
                            <div class="flex items-center justify-between text-xs text-emerald-800 font-bold mb-1">
                                <span>1. Initiation</span>
                                <i class="fa-solid fa-check text-emerald-600"></i>
                            </div>
                            <p class="text-xs text-slate-600">PO & Stock Order</p>
                            <p class="text-[10px] text-slate-400 mt-1 font-mono">Completed</p>
                        </div>

                        <div class="p-3 rounded-xl bg-emerald-50/70 border border-emerald-200">
                            <div class="flex items-center justify-between text-xs text-emerald-800 font-bold mb-1">
                                <span>2. Registration</span>
                                <i class="fa-solid fa-check text-emerald-600"></i>
                            </div>
                            <p class="text-xs text-slate-600">12 Staging Readers</p>
                            <p class="text-[10px] text-slate-400 mt-1 font-mono">Completed</p>
                        </div>

                        <div class="p-3 rounded-xl bg-emerald-50/70 border border-emerald-200">
                            <div class="flex items-center justify-between text-xs text-emerald-800 font-bold mb-1">
                                <span>3. HQ Server</span>
                                <i class="fa-solid fa-check text-emerald-600"></i>
                            </div>
                            <p class="text-xs text-slate-600">Alpeta & DB Setup</p>
                            <p class="text-[10px] text-slate-400 mt-1 font-mono">Completed</p>
                        </div>

                        <div class="p-3 rounded-xl bg-blue-50 border-2 border-blue-400">
                            <div class="flex items-center justify-between text-xs text-blue-900 font-bold mb-1">
                                <span>4. Site Rollout</span>
                                <i class="fa-solid fa-spinner fa-spin text-blue-600"></i>
                            </div>
                            <p class="text-xs text-blue-950 font-bold">47 Locations</p>
                            <p class="text-[10px] text-blue-700 mt-1 font-mono font-semibold">86.3% Installed</p>
                        </div>

                        <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                            <div class="flex items-center justify-between text-xs text-slate-700 font-bold mb-1">
                                <span>5. System Test</span>
                                <i class="fa-regular fa-clock text-slate-400"></i>
                            </div>
                            <p class="text-xs text-slate-600">Data Connection</p>
                            <p class="text-[10px] text-slate-400 mt-1 font-mono">In Progress</p>
                        </div>

                        <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                            <div class="flex items-center justify-between text-xs text-slate-700 font-bold mb-1">
                                <span>6. UAT / Sign-off</span>
                                <i class="fa-regular fa-circle text-slate-300"></i>
                            </div>
                            <p class="text-xs text-slate-600">Handover to HR</p>
                            <p class="text-[10px] text-slate-400 mt-1 font-mono">Pending</p>
                        </div>
                    </div>
                </div>

            </div>

            <!-- ==================================================================== -->
            <!-- PAGE 2: CLUSTER ANALYTICS -->
            <!-- ==================================================================== -->
            <div id="page-analytics" class="page-content hidden space-y-6">
                
                <!-- Area Bar Chart -->
                <div class="clean-card p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                <i class="fa-solid fa-chart-column text-emerald-600"></i>
                                Hardware Deployment by Operational Area
                            </h3>
                            <p class="text-xs text-slate-500 mt-0.5">Installed vs Pending readers across 7 clusters</p>
                        </div>
                        <div class="flex items-center gap-3 text-xs font-semibold">
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-emerald-600"></span> Installed</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-blue-600"></span> Pending / Action Req.</span>
                        </div>
                    </div>
                    <div class="relative h-72 w-full">
                        <canvas id="an-chart-area"></canvas>
                    </div>
                </div>

                <!-- Two Column Analytics -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    
                    <!-- Rollout Velocity -->
                    <div class="clean-card p-6 flex flex-col justify-between">
                        <div class="flex items-center justify-between mb-4">
                            <div>
                                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                    <i class="fa-solid fa-chart-line text-blue-600"></i>
                                    Deployment Velocity (S-Curve)
                                </h3>
                                <p class="text-xs text-slate-500 mt-0.5">Cumulative progress pace over time</p>
                            </div>
                        </div>
                        <div class="relative h-64 w-full">
                            <canvas id="an-chart-velocity"></canvas>
                        </div>
                    </div>

                    <!-- Facility Types -->
                    <div class="clean-card p-6 flex flex-col justify-between">
                        <div class="flex items-center justify-between mb-4">
                            <div>
                                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                    <i class="fa-solid fa-building text-purple-600"></i>
                                    Distribution by Facility Type
                                </h3>
                                <p class="text-xs text-slate-500 mt-0.5">Mustering Points, Depots, Offices, Workshops</p>
                            </div>
                        </div>
                        <div class="relative h-64 w-full flex items-center justify-center">
                            <canvas id="an-chart-loctypes"></canvas>
                        </div>
                    </div>

                </div>

            </div>

            <!-- ==================================================================== -->
            <!-- PAGE 3: SITE DIRECTORY (CLEAN SEARCHABLE TABLE) -->
            <!-- ==================================================================== -->
            <div id="page-sites" class="page-content hidden space-y-4">
                
                <!-- Filter Bar -->
                <div class="clean-card p-4 flex flex-wrap items-center justify-between gap-3">
                    <div class="flex-1 min-w-[260px] relative">
                        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                        <input type="text" id="site-search" oninput="filterSites()" placeholder="Search site name, address, cluster, or remarks..." class="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition">
                    </div>

                    <div class="flex flex-wrap items-center gap-2">
                        <select id="filter-area" onchange="filterSites()" class="px-3 py-2 rounded-xl bg-white border border-slate-200 text-xs text-slate-700 font-medium focus:outline-none focus:border-emerald-600">
                            <option value="">All Clusters (7)</option>
                            <option value="WPKL">WPKL (Kuala Lumpur)</option>
                            <option value="WPPJ">WPPJ (Putrajaya)</option>
                            <option value="AFES">AFES (Core / Johor)</option>
                            <option value="PH1">PH1 (Kuantan)</option>
                            <option value="PH2">PH2 (Pekan / Rompin / Tioman)</option>
                            <option value="PH3">PH3 (Temerloh / Bera / Maran)</option>
                            <option value="PH4">PH4 (Bentong / Raub / Cameron)</option>
                        </select>

                        <select id="filter-status" onchange="filterSites()" class="px-3 py-2 rounded-xl bg-white border border-slate-200 text-xs text-slate-700 font-medium focus:outline-none focus:border-emerald-600">
                            <option value="">All Statuses</option>
                            <option value="Installed">Installed (40 sites)</option>
                            <option value="Upcoming">Upcoming (2 sites)</option>
                            <option value="On Hold">On Hold (2 sites)</option>
                            <option value="Pending">Pending (2 sites)</option>
                            <option value="KIV (Replaced)">KIV Replaced (1 site)</option>
                        </select>

                        <button onclick="resetFilters()" class="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-semibold transition">
                            <i class="fa-solid fa-rotate-left mr-1"></i>Reset
                        </button>
                    </div>
                </div>

                <!-- Table Card -->
                <div class="clean-card overflow-hidden">
                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-100 text-slate-700 uppercase font-bold border-b border-slate-200 font-mono tracking-wider">
                                <tr>
                                    <th class="py-3 px-4 w-12 text-center">No</th>
                                    <th class="py-3 px-4 min-w-[280px]">Site Description & Address</th>
                                    <th class="py-3 px-3 text-center">Cluster</th>
                                    <th class="py-3 px-3">Facility</th>
                                    <th class="py-3 px-3 text-center">Qty</th>
                                    <th class="py-3 px-3">Date</th>
                                    <th class="py-3 px-3 text-center">Status</th>
                                    <th class="py-3 px-4 min-w-[200px]">Remarks / Flags</th>
                                </tr>
                            </thead>
                            <tbody id="sites-table-body" class="divide-y divide-slate-100 font-medium text-slate-700">
                                <!-- Populated dynamically by JS -->
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="px-4 py-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600 font-mono">
                        <div>Showing <span id="filtered-sites-count" class="text-slate-900 font-bold">47</span> sites</div>
                        <div>Total Readers: <span id="filtered-readers-count" class="text-emerald-700 font-bold">51</span> Units (+ 2 Spares)</div>
                    </div>
                </div>

            </div>

            <!-- ==================================================================== -->
            <!-- PAGE 4: ROLLOUT SCHEDULE (GANTT) -->
            <!-- ==================================================================== -->
            <div id="page-schedule" class="page-content hidden space-y-4">
                <div class="clean-card p-6">
                    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
                        <div>
                            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                <i class="fa-solid fa-calendar-days text-blue-600"></i>
                                Daily Rollout Timeline (July – August 2026)
                            </h3>
                            <p class="text-xs text-slate-500 mt-0.5">Chronological site deployment mapping</p>
                        </div>

                        <div class="flex flex-wrap items-center gap-3 text-xs font-semibold">
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-emerald-600"></span> Installed</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-blue-600"></span> Upcoming</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-amber-500"></span> On Hold (Cabin)</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-purple-600"></span> Pending</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-xs bg-slate-200"></span> Weekend</span>
                        </div>
                    </div>

                    <div class="overflow-x-auto custom-scrollbar border border-slate-200 rounded-xl bg-white">
                        <div id="gantt-container" class="min-w-[1000px] text-xs">
                            <!-- Populated dynamically by JS -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- ==================================================================== -->
            <!-- PAGE 5: ACTION ITEMS & RISKS -->
            <!-- ==================================================================== -->
            <div id="page-issues" class="page-content hidden space-y-6">
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

                    <!-- Pending Group: Kepong & Tioman -->
                    <div class="clean-card p-5 border-l-4 border-l-purple-600 bg-purple-50/10">
                        <div class="flex items-center gap-3 mb-3">
                            <div class="w-8 h-8 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-clock"></i>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-purple-950">Pending Sites (2 Locations)</h4>
                                <p class="text-[11px] text-slate-500">Locations pending quotation approval or date finalization</p>
                            </div>
                        </div>
                        <div class="space-y-2 text-xs">
                            <div class="p-3 rounded-xl bg-white border border-slate-200 space-y-1 shadow-2xs">
                                <div class="flex items-center justify-between font-bold text-slate-900">
                                    <span>No 14.6: Medan Niaga Kepong Main Office (WPKL)</span>
                                    <span class="px-2 py-0.5 rounded bg-purple-100 text-purple-800 font-mono text-[10px]">Pending</span>
                                </div>
                                <p class="text-slate-600 font-medium">Remarks: <strong class="text-purple-700">Stand Quotation Request</strong></p>
                                <p class="text-[11px] text-slate-500 font-mono">1 Reader. Vendor to provide quotation for mounting stand.</p>
                            </div>

                            <div class="p-3 rounded-xl bg-white border border-slate-200 space-y-1 shadow-2xs">
                                <div class="flex items-center justify-between font-bold text-slate-900">
                                    <span>No 11.6: Pulau Tioman (PH2)</span>
                                    <span class="px-2 py-0.5 rounded bg-purple-100 text-purple-800 font-mono text-[10px]">Pending</span>
                                </div>
                                <p class="text-slate-600 font-medium">Remarks: <strong class="text-purple-700">Date TBC</strong></p>
                                <p class="text-[11px] text-slate-500 font-mono">1 Reader. Mustering Point. Ferry & island transport coordination.</p>
                            </div>
                        </div>
                    </div>

                    <!-- Cabin Not Ready (PH1) -->
                    <div class="clean-card p-5 border-l-4 border-l-amber-500 bg-amber-50/10">
                        <div class="flex items-center gap-3 mb-3">
                            <div class="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-person-digging"></i>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-amber-950">Cabin Not Ready (PH1)</h4>
                                <p class="text-[11px] text-slate-500">2 sites in Kuantan awaiting cabin readiness</p>
                            </div>
                        </div>
                        <div class="space-y-2 text-xs">
                            <div class="p-3 rounded-xl bg-white border border-slate-200 space-y-1 shadow-2xs">
                                <div class="flex items-center justify-between font-bold text-slate-900">
                                    <span>No 10.1: Lorong Sekilau 28@20, Kuantan</span>
                                    <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-mono text-[10px]">On Hold</span>
                                </div>
                                <p class="text-slate-600">Mustering Point (1 Unit). Remark: <strong class="text-amber-800">Cabin Not Ready</strong>.</p>
                            </div>
                            <div class="p-3 rounded-xl bg-white border border-slate-200 space-y-1 shadow-2xs">
                                <div class="flex items-center justify-between font-bold text-slate-900">
                                    <span>No 10.5: Pandan Damai 2/4, Kuantan</span>
                                    <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-mono text-[10px]">On Hold</span>
                                </div>
                                <p class="text-slate-600">Mustering Point (1 Unit). Remark: <strong class="text-amber-800">Cabin Not Ready</strong> (New Installation).</p>
                            </div>
                        </div>
                    </div>

                    <!-- Network Alerts -->
                    <div class="clean-card p-5 border-l-4 border-l-rose-500 bg-rose-50/10 md:col-span-2">
                        <div class="flex items-center gap-3 mb-3">
                            <div class="w-8 h-8 rounded-lg bg-rose-100 text-rose-700 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-wifi"></i>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-rose-950">Network Connectivity Alerts (3 Locations)</h4>
                                <p class="text-[11px] text-slate-500">Remote locations requiring connectivity verification</p>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                            <div class="p-3 rounded-xl bg-white border border-slate-200 space-y-1 shadow-2xs">
                                <div class="flex items-center justify-between font-bold text-slate-900">
                                    <span>No 9.4: Belenggu Sanitary Landfill (AFES)</span>
                                    <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-mono text-[10px]">No Network</span>
                                </div>
                                <p class="text-slate-600">Offline buffer storage operational. MIS 4G router under deployment.</p>
                            </div>
                            <div class="p-3 rounded-xl bg-white border border-slate-200 space-y-1 shadow-2xs">
                                <div class="flex items-center justify-between font-bold text-slate-900">
                                    <span>No 13.6 & 13.7: Depoh Raub & Cameron Highlands (PH4)</span>
                                    <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-mono text-[10px]">Unstable</span>
                                </div>
                                <p class="text-slate-600">Cellular signal booster / SIM telco change under review by MIS.</p>
                            </div>
                        </div>
                    </div>

                </div>

            </div>

            <!-- ==================================================================== -->
            <!-- PAGE 6: RACI GOVERNANCE MATRIX -->
            <!-- ==================================================================== -->
            <div id="page-raci" class="page-content hidden space-y-4">
                <div class="clean-card p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                                <i class="fa-solid fa-users-gear text-emerald-600"></i>
                                RACI Project Governance Matrix
                            </h3>
                            <p class="text-xs text-slate-500 mt-0.5">22 stakeholder duties mapped across departments</p>
                        </div>
                        <div class="flex items-center gap-3 text-xs font-mono font-semibold">
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span> Responsible</span>
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-slate-300"></span> N/A</span>
                        </div>
                    </div>

                    <div class="overflow-x-auto custom-scrollbar border border-slate-200 rounded-xl bg-white">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-100 text-slate-700 uppercase font-bold border-b border-slate-200 font-mono">
                                <tr>
                                    <th class="py-3 px-4 w-12 text-center">No</th>
                                    <th class="py-3 px-4 min-w-[320px]">Responsibility Scope</th>
                                    <th class="py-3 px-4 text-center w-24">Finance</th>
                                    <th class="py-3 px-4 text-center w-24">MIS / IT</th>
                                    <th class="py-3 px-4 text-center w-24">HR</th>
                                    <th class="py-3 px-4 text-center w-24">Engineering</th>
                                </tr>
                            </thead>
                            <tbody id="raci-table-body" class="divide-y divide-slate-100 font-medium text-slate-700">
                                <!-- Populated dynamically by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </main>

        <!-- Footer -->
        <footer class="mt-auto border-t border-slate-200 bg-white py-3.5 px-6 text-center text-xs text-slate-500 font-mono flex flex-wrap items-center justify-between gap-2">
            <div>
                <span class="font-semibold text-slate-700">Project Portal</span>
                <span class="mx-2 text-slate-300">•</span>
                <span>Ubio Face Reader Rollout System</span>
            </div>
            <div>
                <span>Vendor &amp; Client Implementation Team</span>
            </div>
        </footer>

    </div>

    <!-- INJECTED DATA -->
    <script>
        const PROJECT_DATA = {data_str};
    </script>

    <!-- UI & DASHBOARD LOGIC -->
    <script>
        const PAGE_TITLES = {{
            'overview': 'Executive Progress Overview',
            'analytics': 'Cluster & Regional Analytics',
            'sites': 'Site Installation Directory',
            'schedule': 'Daily Rollout Schedule (Gantt)',
            'issues': 'Action Items & Risk Log',
            'raci': 'RACI Responsibility Matrix'
        }};

        function openSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (sidebar) sidebar.classList.remove('-translate-x-full');
            if (backdrop) backdrop.classList.remove('hidden');
        }}

        function closeSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (sidebar) sidebar.classList.add('-translate-x-full');
            if (backdrop) backdrop.classList.add('hidden');
        }}

        function toggleSidebar() {{
            const sidebar = document.getElementById('sidebar');
            if (sidebar && sidebar.classList.contains('-translate-x-full')) openSidebar();
            else closeSidebar();
        }}

        function navigateTo(pageId) {{
            document.querySelectorAll('.page-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

            const targetPage = document.getElementById('page-' + pageId);
            const targetNav = document.getElementById('nav-' + pageId);
            if (targetPage) targetPage.classList.remove('hidden');
            if (targetNav) targetNav.classList.add('active');

            const title = PAGE_TITLES[pageId] || 'Project Dashboard';
            document.getElementById('page-title').innerText = title;

            if (window.innerWidth < 768) closeSidebar();

            if (pageId === 'overview' || pageId === 'analytics') {{
                setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
            }}

            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function formatDate(dateStr) {{
            if (!dateStr || dateStr === 'None') return '-';
            if (dateStr.toLowerCase() === 'on hold') return 'On Hold';
            if (dateStr.toLowerCase() === 'tbc') return 'TBC';
            try {{
                const parts = dateStr.split('-');
                if (parts.length === 3) {{
                    const d = new Date(parts[0], parts[1]-1, parts[2]);
                    return d.toLocaleDateString('en-GB', {{ day: '2-digit', month: 'short', year: 'numeric' }});
                }}
            }} catch(e) {{}}
            return dateStr;
        }}

        function renderOverviewData() {{
            const kpis = PROJECT_DATA.kpis;
            document.getElementById('ov-total-readers').innerText = kpis.total_readers;
            document.getElementById('ov-installed-readers').innerText = kpis.installed_readers;
            document.getElementById('ov-installed-pct').innerText = kpis.installed_pct + '% Rate';
            document.getElementById('ov-upcoming-readers').innerText = kpis.upcoming_readers;
            document.getElementById('ov-action-readers').innerText = kpis.on_hold_readers + kpis.pending_readers;

            const clusterContainer = document.getElementById('ov-cluster-bars');
            clusterContainer.innerHTML = '';
            
            const areaNames = {{
                'WPKL': 'Wilayah Persekutuan KL',
                'WPPJ': 'Putrajaya ISWMF & Offices',
                'AFES': 'AFES Core & Johor',
                'PH1': 'PH1: Kuantan Cluster',
                'PH2': 'PH2: Pekan & Rompin',
                'PH3': 'PH3: Temerloh & Bera',
                'PH4': 'PH4: Bentong & Highland'
            }};

            Object.keys(PROJECT_DATA.areas).forEach(code => {{
                const a = PROJECT_DATA.areas[code];
                const pct = a.total_readers > 0 ? Math.round((a.installed_readers / a.total_readers) * 100) : 0;
                const isFull = pct === 100;
                
                const div = document.createElement('div');
                div.className = 'space-y-1';
                div.innerHTML = `
                    <div class="flex items-center justify-between text-xs font-semibold">
                        <span class="text-slate-800 font-mono">${{code}} <span class="text-slate-500 font-normal">(${{areaNames[code] || code}})</span></span>
                        <span class="font-mono ${{isFull ? 'text-emerald-700' : 'text-slate-700'}}">${{a.installed_readers}}/${{a.total_readers}} Units (${{pct}}%)</span>
                    </div>
                    <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden border border-slate-200">
                        <div class="${{isFull ? 'bg-emerald-600' : 'bg-blue-600'}} h-full transition-all duration-500" style="width: ${{pct}}%"></div>
                    </div>
                `;
                clusterContainer.appendChild(div);
            }});
        }}

        // Charts
        let ovDonutChart, anAreaChart, anVelocityChart, anLocChart;

        function initCharts() {{
            Chart.defaults.color = '#475569';
            Chart.defaults.font.family = 'Plus Jakarta Sans';
            Chart.defaults.font.size = 11;

            const donutCtx = document.getElementById('ov-chart-donut').getContext('2d');
            const kpis = PROJECT_DATA.kpis;
            ovDonutChart = new Chart(donutCtx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Installed', 'Upcoming', 'On Hold', 'Pending'],
                    datasets: [{{
                        data: [
                            kpis.installed_readers,
                            kpis.upcoming_readers,
                            kpis.on_hold_readers,
                            kpis.pending_readers
                        ],
                        backgroundColor: ['#16a34a', '#2563eb', '#d97706', '#9333ea'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '72%',
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            backgroundColor: '#0f172a',
                            padding: 10,
                            callbacks: {{
                                label: (c) => ` ${{c.label}}: ${{c.raw}} Units (${{((c.raw/51)*100).toFixed(1)}}%)`
                            }}
                        }}
                    }}
                }}
            }});

            const areaCtx = document.getElementById('an-chart-area').getContext('2d');
            const areaKeys = Object.keys(PROJECT_DATA.areas);
            const instData = areaKeys.map(k => PROJECT_DATA.areas[k].installed_readers);
            const pendData = areaKeys.map(k => PROJECT_DATA.areas[k].pending_readers);

            anAreaChart = new Chart(areaCtx, {{
                type: 'bar',
                data: {{
                    labels: areaKeys,
                    datasets: [
                        {{ label: 'Installed', data: instData, backgroundColor: '#16a34a', borderRadius: 4 }},
                        {{ label: 'Pending / Action Req.', data: pendData, backgroundColor: '#2563eb', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ stacked: true, grid: {{ color: '#f1f5f9' }} }},
                        y: {{ stacked: true, beginAtZero: true, grid: {{ color: '#f1f5f9' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            const velCtx = document.getElementById('an-chart-velocity').getContext('2d');
            const daily = PROJECT_DATA.daily_rollout;
            anVelocityChart = new Chart(velCtx, {{
                type: 'line',
                data: {{
                    labels: daily.map(d => formatDate(d.date).replace(/ 2026/, '')),
                    datasets: [
                        {{
                            label: 'Cumulative',
                            data: daily.map(d => d.cumulative),
                            borderColor: '#2563eb',
                            backgroundColor: 'rgba(37, 99, 235, 0.08)',
                            borderWidth: 2.5,
                            fill: true,
                            tension: 0.3,
                            yAxisID: 'y'
                        }},
                        {{
                            type: 'bar',
                            label: 'Daily',
                            data: daily.map(d => d.daily),
                            backgroundColor: '#16a34a',
                            borderRadius: 4,
                            yAxisID: 'y1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ grid: {{ color: '#f1f5f9' }} }},
                        y: {{ position: 'left', grid: {{ color: '#f1f5f9' }} }},
                        y1: {{ position: 'right', grid: {{ drawOnChartArea: false }}, ticks: {{ stepSize: 2 }} }}
                    }}
                }}
            }});

            const locCtx = document.getElementById('an-chart-loctypes').getContext('2d');
            const locs = PROJECT_DATA.location_types;
            const locKeys = Object.keys(locs);
            anLocChart = new Chart(locCtx, {{
                type: 'polarArea',
                data: {{
                    labels: locKeys,
                    datasets: [{{
                        data: locKeys.map(k => locs[k].readers),
                        backgroundColor: ['#16a34a', '#2563eb', '#9333ea', '#d97706', '#0284c7', '#e11d48', '#64748b']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 8, font: {{ size: 9 }} }} }} }}
                }}
            }});
        }}

        // Sites Table
        function renderSitesTable(sitesToRender) {{
            const tbody = document.getElementById('sites-table-body');
            tbody.innerHTML = '';

            if (sitesToRender.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400 font-mono">No matching locations found</td></tr>`;
                return;
            }}

            sitesToRender.forEach(s => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition border-b border-slate-100';
                
                let statusBadge = '';
                if (s.status === 'Installed') statusBadge = '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono bg-emerald-50 text-emerald-700 border border-emerald-200">Installed</span>';
                else if (s.status === 'Upcoming') statusBadge = '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono bg-blue-50 text-blue-700 border border-blue-200">Upcoming</span>';
                else if (s.status === 'On Hold') statusBadge = '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono bg-amber-50 text-amber-800 border border-amber-200">On Hold</span>';
                else if (s.status === 'Pending') statusBadge = '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono bg-purple-50 text-purple-700 border border-purple-200">Pending</span>';
                else statusBadge = '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono bg-slate-100 text-slate-600 border border-slate-200">KIV</span>';

                let flagsHtml = '';
                if (s.flags && s.flags.length > 0) {{
                    flagsHtml = s.flags.map(f => `<span class="inline-block px-2 py-0.5 rounded text-[10px] font-semibold font-mono bg-slate-100 text-slate-800 border border-slate-200 mr-1">${{f.label}}</span>`).join('');
                }} else if (s.remarks) {{
                    flagsHtml = `<span class="text-slate-600 font-medium">${{s.remarks}}</span>`;
                }} else {{
                    flagsHtml = `<span class="text-slate-300">-</span>`;
                }}

                tr.innerHTML = `
                    <td class="py-2.5 px-4 text-center font-mono font-bold text-slate-400">${{s.no}}</td>
                    <td class="py-2.5 px-4">
                        <div class="font-bold text-slate-900">${{s.task}}</div>
                        <div class="text-[10px] text-slate-400 font-mono">${{s.region || ''}}</div>
                    </td>
                    <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-slate-100 text-slate-800 font-mono font-bold">${{s.area}}</span></td>
                    <td class="py-2.5 px-3 text-slate-600">${{s.location_type || '-'}}</td>
                    <td class="py-2.5 px-3 text-center font-bold font-mono text-emerald-700">${{s.quantity}}</td>
                    <td class="py-2.5 px-3 font-mono text-slate-600">${{formatDate(s.start_date)}}</td>
                    <td class="py-2.5 px-3 text-center">${{statusBadge}}</td>
                    <td class="py-2.5 px-4">${{flagsHtml}}</td>
                `;
                tbody.appendChild(tr);
            }});

            document.getElementById('filtered-sites-count').innerText = sitesToRender.length;
            const totalQ = sitesToRender.reduce((sum, s) => sum + s.quantity, 0);
            document.getElementById('filtered-readers-count').innerText = totalQ;
        }}

        function filterSites() {{
            const search = document.getElementById('site-search').value.toLowerCase();
            const area = document.getElementById('filter-area').value;
            const status = document.getElementById('filter-status').value;

            const filtered = PROJECT_DATA.sites.filter(s => {{
                const matchesSearch = !search || 
                    (s.task && s.task.toLowerCase().includes(search)) ||
                    (s.area && s.area.toLowerCase().includes(search)) ||
                    (s.no && s.no.toLowerCase().includes(search)) ||
                    (s.remarks && s.remarks.toLowerCase().includes(search));
                
                const matchesArea = !area || s.area === area;
                const matchesStatus = !status || s.status === status;

                return matchesSearch && matchesArea && matchesStatus;
            }});

            renderSitesTable(filtered);
        }}

        function resetFilters() {{
            document.getElementById('site-search').value = '';
            document.getElementById('filter-area').value = '';
            document.getElementById('filter-status').value = '';
            filterSites();
        }}

        function filterByStatus(status) {{
            document.getElementById('site-search').value = '';
            document.getElementById('filter-area').value = '';
            document.getElementById('filter-status').value = status;
            filterSites();
        }}

        // Gantt
        function renderGanttTimeline() {{
            const container = document.getElementById('gantt-container');
            const dates = PROJECT_DATA.gantt_dates;
            const sites = PROJECT_DATA.sites;

            let html = `
                <div class="grid grid-cols-[260px_repeat(${{dates.length}},34px)] bg-slate-100 text-slate-700 font-mono text-[10px] font-bold border-b border-slate-200 sticky top-0 z-20">
                    <div class="p-2 border-r border-slate-200">Site Location</div>
                    ${{dates.map(d => `
                        <div class="p-1 text-center border-r border-slate-200">
                            <div>${{d.display.split(' ')[0]}}</div>
                            <div class="text-[8px] text-slate-400">${{d.display.split(' ')[1]}}</div>
                        </div>
                    `).join('')}}
                </div>
            `;

            sites.forEach(s => {{
                const sDate = s.start_date;
                const eDate = s.end_date || sDate;
                html += `
                    <div class="grid grid-cols-[260px_repeat(${{dates.length}},34px)] border-b border-slate-100 text-[10px] hover:bg-slate-50 items-center">
                        <div class="p-1.5 border-r border-slate-200 flex items-center justify-between gap-1 overflow-hidden bg-white">
                            <span class="truncate font-semibold text-slate-800" title="${{s.task}}">
                                <span class="text-blue-600 font-mono">${{s.no}}</span> ${{s.task}}
                            </span>
                            <span class="px-1 py-0.2 text-[9px] font-mono rounded bg-slate-100 text-slate-500">${{s.area}}</span>
                        </div>
                        ${{dates.map(d => {{
                            const isWeekend = (new Date(d.date).getDay() === 0 || new Date(d.date).getDay() === 6);
                            let cellBg = isWeekend ? 'bg-slate-100/50' : 'bg-white';
                            let marker = '';

                            if (sDate && d.date >= sDate && d.date <= eDate) {{
                                if (s.status === 'Installed') marker = '<div class="w-full h-4 rounded bg-emerald-600 flex items-center justify-center text-white text-[9px]"><i class="fa-solid fa-check"></i></div>';
                                else if (s.status === 'Upcoming') marker = '<div class="w-full h-4 rounded bg-blue-600 flex items-center justify-center text-white text-[9px]"><i class="fa-solid fa-truck"></i></div>';
                                else if (s.status === 'On Hold') marker = '<div class="w-full h-4 rounded bg-amber-500 flex items-center justify-center text-white text-[9px]"><i class="fa-solid fa-hand"></i></div>';
                                else if (s.status === 'Pending') marker = '<div class="w-full h-4 rounded bg-purple-600 flex items-center justify-center text-white text-[9px]"><i class="fa-solid fa-clock"></i></div>';
                            }}

                            return `<div class="h-8 border-r border-slate-100 p-0.5 flex items-center justify-center ${{cellBg}}">${{marker}}</div>`;
                        }}).join('')}}
                    </div>
                `;
            }});

            container.innerHTML = html;
        }}

        // RACI
        function renderRACITable() {{
            const tbody = document.getElementById('raci-table-body');
            tbody.innerHTML = '';
            PROJECT_DATA.responsibility.forEach(r => {{
                const check = '<span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center mx-auto text-[10px]"><i class="fa-solid fa-check"></i></span>';
                const empty = '<span class="text-slate-300">-</span>';
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 border-b border-slate-100';
                tr.innerHTML = `
                    <td class="py-2.5 px-4 text-center font-mono font-bold text-slate-400">${{r.no}}</td>
                    <td class="py-2.5 px-4 text-slate-900 font-semibold">${{r.task}}</td>
                    <td class="py-2.5 px-4 text-center">${{r.finance ? check : empty}}</td>
                    <td class="py-2.5 px-4 text-center">${{r.mis ? check : empty}}</td>
                    <td class="py-2.5 px-4 text-center">${{r.hr ? check : empty}}</td>
                    <td class="py-2.5 px-4 text-center">${{r.engineering ? check : empty}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // CSV Export
        function exportToCSV() {{
            const sites = PROJECT_DATA.sites;
            let csv = "No,Task/Site Name,Area,Region,Facility Type,Quantity,Target Date,Status,Remarks\\n";
            sites.forEach(s => {{
                const cleanTask = (s.task || '').replace(/"/g, '""').replace(/\\n/g, ' ');
                const cleanRem = (s.remarks || '').replace(/"/g, '""');
                csv += `"${{s.no}}","${{cleanTask}}","${{s.area || ''}}","${{s.region || ''}}","${{s.location_type || ''}}",${{s.quantity}},"${{s.start_date || ''}}","${{s.status}}","${{cleanRem}}"\\n`;
            }});

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `Face_Reader_Rollout_${{new Date().toISOString().slice(0,10)}}.csv`;
            link.click();
        }}

        // Initialization
        document.addEventListener('DOMContentLoaded', () => {{
            renderOverviewData();
            initCharts();
            renderSitesTable(PROJECT_DATA.sites);
            renderGanttTimeline();
            renderRACITable();
        }});
    </script>
</body>
</html>
"""
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    # Also create index.html for GitHub Pages root
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated clean multi-page {output_html_path} and index.html (for GitHub Pages) successfully.")

if __name__ == '__main__':
    generate_html_dashboard('project_data.json', 'dashboard.html')
