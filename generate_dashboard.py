import openpyxl
import json
import datetime
import glob
import os

def find_latest_excel():
    files = glob.glob('*.xlsx')
    valid_files = [f for f in files if not os.path.basename(f).startswith('~$')]
    if not valid_files:
        return None
    valid_files.sort(key=os.path.getmtime, reverse=True)
    return valid_files[0]

def parse_excel(file_path=None):
    if not file_path:
        file_path = find_latest_excel()
        
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"No Excel file found.")
        
    print(f"Reading latest Excel file: {file_path}")
    wb = openpyxl.load_workbook(file_path, data_only=True)
    
    # 1. Parse Summary sheet if available
    summary_sheet_data = {}
    if 'Summary' in wb.sheetnames:
        ws_sum = wb['Summary']
        total_dev = ws_sum.cell(4, 2).value
        total_inst = ws_sum.cell(5, 2).value
        total_spare = ws_sum.cell(6, 2).value
        comp_rate = ws_sum.cell(7, 2).value
        
        summary_sheet_data = {
            'total_device': int(total_dev) if total_dev is not None else 53,
            'total_installed': int(total_inst) if total_inst is not None else 48,
            'total_spare': int(total_spare) if total_spare is not None else 2,
            'completion_pct': round(float(comp_rate) * 100, 1) if comp_rate is not None else 92.5
        }
    
    # 2. Parse Time Line Sheet
    ws_tl = wb['Time Line']
    
    # Extract metadata header
    doc_title = ws_tl.cell(2, 1).value or "Time Line for Ubio Face Reader Installation and Implementation"
    doc_date = ws_tl.cell(2, 7).value or "Date: 26th April 2026"
    revise_date = ws_tl.cell(2, 10).value or "Revise Date: 21st August 2026"
    
    milestones = []
    sites = []
    
    for r in range(7, ws_tl.max_row + 1):
        no_val = ws_tl.cell(r, 1).value
        desc_val = ws_tl.cell(r, 2).value
        qty_val = ws_tl.cell(r, 3).value
        area_val = ws_tl.cell(r, 4).value
        region_val = ws_tl.cell(r, 5).value
        loc_val = ws_tl.cell(r, 6).value
        days_val = ws_tl.cell(r, 7).value
        sdate_val = ws_tl.cell(r, 8).value
        edate_val = ws_tl.cell(r, 9).value
        act_val = ws_tl.cell(r, 10).value
        resp_val = ws_tl.cell(r, 11).value
        rem_val = ws_tl.cell(r, 12).value
        
        if not desc_val and not no_val:
            continue
            
        desc_clean = str(desc_val).strip() if desc_val else ''
        no_clean = str(no_val).strip() if no_val is not None else ''
        
        # Skip total or constraint note rows
        if desc_clean.lower() == 'total' or no_clean.lower() == 'total' or 'this time line is a tentative' in no_clean.lower() or 'constraints' in no_clean.lower():
            continue
        
        # Format dates
        sdate_str = sdate_val.strftime('%Y-%m-%d') if hasattr(sdate_val, 'strftime') else str(sdate_val) if sdate_val is not None else None
        edate_str = edate_val.strftime('%Y-%m-%d') if hasattr(edate_val, 'strftime') else str(edate_val) if edate_val is not None else None
        
        area_str = str(area_val).strip() if area_val else None
        if not area_str and 'maran' in desc_clean.lower() and no_clean == '12.9':
            area_str = 'PH3'
            
        qty_int = int(qty_val) if qty_val is not None and str(qty_val).isdigit() else int(float(qty_val)) if qty_val is not None and isinstance(qty_val, (int, float)) else None
        
        item = {
            'row': r,
            'no': no_clean,
            'task': desc_clean,
            'quantity': qty_int if qty_int is not None else 0 if 'kiv' in str(rem_val).lower() else 1,
            'area': area_str,
            'region': str(region_val).strip() if region_val else None,
            'location_type': str(loc_val).strip() if loc_val else None,
            'no_of_days': int(days_val) if days_val is not None and isinstance(days_val, (int, float)) else None,
            'start_date': sdate_str,
            'end_date': edate_str,
            'activities': str(act_val).strip() if act_val else '',
            'responsibility': str(resp_val).strip() if resp_val else '',
            'remarks': str(rem_val).strip() if rem_val else ''
        }
        
        is_site = (26 <= r <= 72) or (item['area'] is not None and item['no'] not in ('1', '2', '3.1', '3.2', '4', '5', '6', '6.1', '6.2', '7', '8', '16', '17', '16.0', '17.0'))
        
        if is_site and r <= 72:
            st = (item['start_date'] or '').lower()
            rem = (item['remarks'] or '').lower()
            task_lower = item['task'].lower()
            
            # Status classification
            if 'on hold' in st or 'cabin not ready' in rem:
                item['status'] = 'On Hold'
                item['status_badge'] = 'bg-amber-50 text-amber-800 border-amber-200'
                item['status_desc'] = 'Cabin Not Ready'
            elif 'kepong' in task_lower or 'reader stand' in rem:
                # User preference: Put under Pending Group with Stand Quotation Request remarks
                item['status'] = 'Pending'
                item['status_badge'] = 'bg-purple-50 text-purple-700 border-purple-200'
                item['status_desc'] = 'Stand Quotation Request'
                if not item['remarks']:
                    item['remarks'] = 'Stand Quotation Request'
            elif 'tioman' in task_lower or ('tbc' in st and 'bukit kayu hitam' not in task_lower):
                # User preference: Put under Pending Group with Date TBC remarks
                item['status'] = 'Pending'
                item['status_badge'] = 'bg-purple-50 text-purple-700 border-purple-200'
                item['status_desc'] = 'Date TBC'
                if not item['remarks']:
                    item['remarks'] = 'Date TBC'
            elif 'kiv' in rem or (not item['start_date'] and 'pine jerantut' in task_lower) or qty_val is None:
                item['status'] = 'KIV (Replaced)'
                item['status_badge'] = 'bg-slate-100 text-slate-600 border-slate-200'
                item['status_desc'] = 'Slot reallocated to Depoh Jerantut'
                item['quantity'] = 0
            elif item['start_date'] and item['start_date'] <= '2026-08-21':
                item['status'] = 'Installed'
                item['status_badge'] = 'bg-emerald-50 text-emerald-700 border-emerald-200'
                item['status_desc'] = 'Hardware installed & operational'
            else:
                item['status'] = 'Upcoming'
                item['status_badge'] = 'bg-blue-50 text-blue-700 border-blue-200'
                item['status_desc'] = 'Scheduled for rollout'
            
            # Identify specific operational flags / risks
            flags = []
            if 'kepong' in task_lower or 'reader stand' in rem:
                flags.append({'type': 'stand', 'label': 'Stand Quotation Request', 'text': 'Stand Quotation Request'})
            if 'tioman' in task_lower or ('tbc' in st and 'bukit kayu hitam' not in task_lower and 'kepong' not in task_lower):
                flags.append({'type': 'reschedule', 'label': 'Date TBC', 'text': 'Date TBC'})
            if 'cabin' in rem or 'on hold' in st:
                flags.append({'type': 'cabin', 'label': 'Cabin Not Ready', 'text': item['remarks'] or 'Cabin Not Ready'})
            if 'network' in rem or 'no network' in rem or 'unstable' in rem:
                flags.append({'type': 'network', 'label': 'Network Issue', 'text': item['remarks']})
            if 'not in original list' in rem:
                flags.append({'type': 'scope', 'label': 'Scope Addition', 'text': item['remarks']})
            if 'kiv' in rem:
                flags.append({'type': 'kiv', 'label': 'Scope Shift', 'text': item['remarks']})
            item['flags'] = flags
            
            sites.append(item)
        else:
            # Milestone entry
            if item['no'] or item['task']:
                m_no = item['no']
                if m_no in ('1', '2', '3.1', '3.2', '4', '5', '6', '6.1', '6.2', '7', '8'):
                    item['m_status'] = 'Completed'
                    item['m_badge'] = 'bg-emerald-50 text-emerald-700 border-emerald-200'
                elif m_no in ('16', '16.0'):
                    item['m_status'] = 'In Progress / Next'
                    item['m_badge'] = 'bg-blue-50 text-blue-700 border-blue-200'
                elif m_no in ('17', '17.0'):
                    item['m_status'] = 'Pending Final Rollout'
                    item['m_badge'] = 'bg-slate-100 text-slate-600 border-slate-200'
                else:
                    item['m_status'] = 'Completed' if item['start_date'] else 'Pending'
                    item['m_badge'] = 'bg-slate-100 text-slate-600 border-slate-200'
                milestones.append(item)
                
    # 3. Parse Gantt Chart Sheet
    ws_gc = wb['Gnatt Chart']
    gantt_dates = []
    for c in range(6, ws_gc.max_column + 1):
        d_val = ws_gc.cell(3, c).value
        if d_val:
            d_str = d_val.strftime('%Y-%m-%d') if hasattr(d_val, 'strftime') else str(d_val)
            gantt_dates.append({'col': c, 'date': d_str, 'display': d_val.strftime('%d %b') if hasattr(d_val, 'strftime') else d_str})
            
    # 4. Parse Responsibility Sheet
    ws_res = wb['Responsibility']
    responsibility = []
    for r in range(4, ws_res.max_row + 1):
        no_val = ws_res.cell(r, 1).value
        desc_val = ws_res.cell(r, 2).value
        fin_val = ws_res.cell(r, 3).value
        mis_val = ws_res.cell(r, 4).value
        hr_val = ws_res.cell(r, 5).value
        eng_val = ws_res.cell(r, 6).value
        
        if desc_val and (isinstance(no_val, (int, float)) or str(no_val).isdigit()):
            responsibility.append({
                'no': int(no_val) if isinstance(no_val, (int, float)) else str(no_val),
                'task': str(desc_val).strip(),
                'finance': bool(fin_val),
                'mis': bool(mis_val),
                'hr': bool(hr_val),
                'engineering': bool(eng_val)
            })
            
    # Calculate Summary Statistics
    total_site_readers = sum(s['quantity'] for s in sites)
    total_sites = len(sites)
    spare_units = summary_sheet_data.get('total_spare', 2)
    total_readers_with_spare = total_site_readers + spare_units
    
    installed_sites = [s for s in sites if s['status'] == 'Installed']
    installed_readers = sum(s['quantity'] for s in installed_sites)
    
    upcoming_sites = [s for s in sites if s['status'] == 'Upcoming']
    upcoming_readers = sum(s['quantity'] for s in upcoming_sites)
    
    on_hold_sites = [s for s in sites if s['status'] == 'On Hold']
    on_hold_readers = sum(s['quantity'] for s in on_hold_sites)
    
    pending_sites = [s for s in sites if s['status'] == 'Pending']
    pending_readers = sum(s['quantity'] for s in pending_sites)
    
    kiv_sites = [s for s in sites if s['status'] == 'KIV (Replaced)']
    kiv_readers = sum(s['quantity'] for s in kiv_sites)
    
    network_issues = [s for s in sites if any(f['type'] == 'network' for f in s['flags'])]
    
    # Area Breakdown
    areas = {}
    for s in sites:
        a = s['area'] or 'Other'
        if a not in areas:
            areas[a] = {'total_sites': 0, 'total_readers': 0, 'installed_readers': 0, 'installed_sites': 0, 'pending_readers': 0, 'region': s['region'] or ''}
        areas[a]['total_sites'] += 1
        q = s['quantity']
        areas[a]['total_readers'] += q
        if s['status'] == 'Installed':
            areas[a]['installed_readers'] += q
            areas[a]['installed_sites'] += 1
        else:
            areas[a]['pending_readers'] += q
            
    # Location Types Breakdown
    loc_types = {}
    for s in sites:
        lt = s['location_type'] or 'Other'
        if lt not in loc_types:
            loc_types[lt] = {'count': 0, 'readers': 0}
        loc_types[lt]['count'] += 1
        loc_types[lt]['readers'] += s['quantity']
        
    # Timeline Distribution for Cumulative Progress
    all_dates = sorted(list(set(s['start_date'] for s in sites if s['start_date'] and s['start_date'] not in ('On hold', 'TBC', 'None'))))
    cum_readers = 0
    daily_rollout = {}
    for d in all_dates:
        count = sum(s['quantity'] for s in sites if s['start_date'] == d and s['status'] == 'Installed')
        cum_readers += count
        daily_rollout[d] = {'date': d, 'daily': count, 'cumulative': cum_readers}
        
    summary = {
        'metadata': {
            'source_file': os.path.basename(file_path),
            'title': doc_title,
            'initial_date': doc_date,
            'revision_date': revise_date,
            'current_as_of': '21 August 2026'
        },
        'kpis': {
            'total_readers': total_site_readers,
            'total_readers_with_spare': total_readers_with_spare,
            'total_spare': spare_units,
            'total_sites': total_sites,
            'active_sites': total_sites - len(kiv_sites),
            'installed_readers': installed_readers,
            'installed_sites': len(installed_sites),
            'installed_pct': round((installed_readers / total_site_readers) * 100, 1) if total_site_readers else 0,
            'upcoming_readers': upcoming_readers,
            'upcoming_sites': len(upcoming_sites),
            'on_hold_readers': on_hold_readers,
            'on_hold_sites': len(on_hold_sites),
            'pending_readers': pending_readers,
            'pending_sites': len(pending_sites),
            'kiv_readers': kiv_readers,
            'kiv_sites': len(kiv_sites),
            'network_issue_sites': len(network_issues)
        },
        'summary_sheet_data': summary_sheet_data,
        'areas': areas,
        'location_types': loc_types,
        'daily_rollout': list(daily_rollout.values()),
        'milestones': milestones,
        'sites': sites,
        'responsibility': responsibility,
        'gantt_dates': gantt_dates
    }
    
    return summary

def main():
    latest_file = find_latest_excel()
    if not latest_file:
        print("Error: No Excel file found in current directory.")
        return
        
    data = parse_excel(latest_file)
    
    with open('project_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Exported project_data.json successfully from " + latest_file)
    print(f"Summary: {data['kpis']['installed_readers']}/{data['kpis']['total_readers']} site readers installed ({data['kpis']['installed_pct']}%) across {data['kpis']['total_sites']} sites.")
    print(f"Breakdown: Installed={data['kpis']['installed_readers']}, Upcoming={data['kpis']['upcoming_readers']}, On Hold={data['kpis']['on_hold_readers']}, Pending={data['kpis']['pending_readers']}, Spares={data['kpis']['total_spare']}")

if __name__ == '__main__':
    main()
