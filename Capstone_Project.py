
import math
import numpy as np
import matplotlib.pyplot as plt

#The data of different Sites
network_sites = [
    {
        'site_id'      : 'BLR_001',
        'city'         : 'Bengaluru',
        'operator'     : 'Jio',
        'frequency'    : 3500,
        'tx_power'     : 46,
        'antenna_gain' : 18,
        'distance_km'  : 1.2,
        'rsrp_readings': [-72, -78, -81, -75, -69, -83, -77, -74, -80, -76]
    },
    {
        'site_id'      : 'MUM_002',
        'city'         : 'Mumbai',
        'operator'     : 'Airtel',
        'frequency'    : 1800,
        'tx_power'     : 43,
        'antenna_gain' : 17,
        'distance_km'  : 3.5,
        'rsrp_readings': [-85, -88, -91, -84, -93, -89, -87, -92, -86, -90]
    },
    {
        'site_id'      : 'DEL_003',
        'city'         : 'Delhi',
        'operator'     : 'Vi',
        'frequency'    : 1800,
        'tx_power'     : 43,
        'antenna_gain' : 15,
        'distance_km'  : 7.8,
        'rsrp_readings': [-101, -98, -105, -110, -103, -99, -107, -104, -108, -102]
    },
    {
        'site_id'      : 'CHN_004',
        'city'         : 'Chennai',
        'operator'     : 'Jio',
        'frequency'    : 2600,
        'tx_power'     : 44,
        'antenna_gain' : 17,
        'distance_km'  : 2.1,
        'rsrp_readings': [-79, -82, -77, -85, -80, -83, -78, -86, -81, -79]
    },
]

#Function 1 — calculate_fspl(distance_km, frequency_mhz) 

def calculate_fspl(distance_km, frequency_mhz):
    """
    Calculates Free Space Path Loss (FSPL) in dB.
    Formula: FSPL = 20*log10(d) + 20*log10(f) + 32.44
    distance_km   : distance between tower and phone in km
    frequency_mhz : signal frequency in MHz
    """
    fspl = 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz) + 32.44
    return round(fspl, 2)

#Function 2 — classify_rsrp(rsrp_dbm) 

def classify_rsrp(rsrp_dbm):
    """
    Classifies signal quality based on 3GPP RSRP thresholds.
    rsrp_dbm : RSRP value in dBm
    Returns  : quality label string
    """
    if rsrp_dbm >= -80:
        return 'Excellent'
    elif rsrp_dbm >= -90:
        return 'Good'
    elif rsrp_dbm >= -100:
        return 'Fair'
    else:
        return 'Poor'

#Function 3 — analyse_site(site) 

def analyse_site(site):
    """
    Analyses a single site dictionary.
    Returns a results dictionary with:
    avg_rsrp, min_rsrp, max_rsrp, quality, fspl, poor_count, poor_pct
    """
    readings   = site['rsrp_readings']
    avg_rsrp   = round(sum(readings) / len(readings), 1)
    min_rsrp   = min(readings)
    max_rsrp   = max(readings)
    quality    = classify_rsrp(avg_rsrp)
    fspl       = calculate_fspl(site['distance_km'], site['frequency'])
    poor_count = sum(1 for r in readings if r < -100)
    poor_pct   = round(poor_count / len(readings) * 100, 1)

    return {
        'avg_rsrp'  : avg_rsrp,
        'min_rsrp'  : min_rsrp,
        'max_rsrp'  : max_rsrp,
        'quality'   : quality,
        'fspl'      : fspl,
        'poor_count': poor_count,
        'poor_pct'  : poor_pct
    }

#Main Analysis Loop

print('=' * 65)
print('        RF NETWORK SITE ANALYSIS REPORT')
print('=' * 65)

results_list = []   # store all results — used for graphs below

for site in network_sites:
    res = analyse_site(site)
    results_list.append({'site_id': site['site_id'], **res})

    print(f"\nSite ID  : {site['site_id']} ({site['city']})")
    print(f"Operator : {site['operator']}  |  Frequency: {site['frequency']} MHz")
    print(f"Distance : {site['distance_km']} km  |  FSPL: {res['fspl']} dB")
    print(f"Avg RSRP : {res['avg_rsrp']} dBm  |  Quality: {res['quality']}")
    print(f"Min RSRP : {res['min_rsrp']} dBm  |  Max RSRP: {res['max_rsrp']} dBm")
    print(f"Poor readings: {res['poor_count']}/10 ({res['poor_pct']}%)")

    if res['poor_pct'] > 30:
        print('[!] ACTION NEEDED: High poor reading percentage')
    else:
        print('[OK] Site performing within acceptable limits')
    print('-' * 65)


#Graph 1: Average RSRP per Site

site_ids  = [r['site_id']  for r in results_list]
avg_rsrps = [r['avg_rsrp'] for r in results_list]

# Color each bar based on quality

colors = []
for rsrp in avg_rsrps:
    if rsrp >= -80:
        colors.append('#2ecc71')    # green  → Excellent
    elif rsrp >= -90:
        colors.append('#f1c40f')    # yellow → Good
    elif rsrp >= -100:
        colors.append('#e67e22')    # orange → Fair
    else:
        colors.append('#e74c3c')    # red    → Poor

plt.figure(figsize=(10, 6))

#Keep the bar() call on ONE line — no line break in the middle

bars = plt.bar(site_ids, avg_rsrps, color=colors, edgecolor='white', linewidth=1.5)

#Add RSRP value labels inside each bar

for bar, val in zip(bars, avg_rsrps):
    plt.text(bar.get_x() + bar.get_width() / 2, val - 2,
             f'{val} dBm', ha='center', va='top',
             fontweight='bold', color='white', fontsize=10)

# FIX 3: Correct label text — include minus sign
plt.axhline(y=-80,  color='green',  linestyle='--', alpha=0.7, label='Excellent (-80 dBm)')
plt.axhline(y=-90,  color='orange', linestyle='--', alpha=0.7, label='Good (-90 dBm)')
plt.axhline(y=-100, color='red',    linestyle='--', alpha=0.7, label='Fair (-100 dBm)')

plt.title('Average RSRP per Site — Network Health Overview', fontsize=14, fontweight='bold')
plt.xlabel('Site ID', fontsize=12)
plt.ylabel('Average RSRP (dBm)', fontsize=12)
plt.legend(fontsize=9)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

plt.savefig('site_rsrp_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()   # close figure cleanly before starting Graph 2
print('Graph 1 saved: site_rsrp_comparison.png')

#Graph 2: Coverage Curves for All Sites 

distances   = np.linspace(0.1, 12, 200)
line_colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']

plt.figure(figsize=(11, 7))

for i, site in enumerate(network_sites):
    # Calculate RSRP curve across all distances
    fspl = 20 * np.log10(distances) + 20 * np.log10(site['frequency']) + 32.44
    rsrp = site['tx_power'] + site['antenna_gain'] - fspl

    label = f"{site['site_id']} ({site['frequency']} MHz, {site['operator']})"
    plt.plot(distances, rsrp, color=line_colors[i], linewidth=2, label=label)

    # Mark the actual operating point of this site with a dot
    
    actual_fspl = calculate_fspl(site['distance_km'], site['frequency'])
    actual_rsrp = site['tx_power'] + site['antenna_gain'] - actual_fspl
    plt.scatter(site['distance_km'], actual_rsrp,
                color=line_colors[i], s=80, zorder=5)

plt.axhline(y=-80,  color='green', linestyle=':',  alpha=0.6, label='Excellent threshold (-80 dBm)')
plt.axhline(y=-100, color='red',   linestyle='--', alpha=0.6, label='Coverage limit (-100 dBm)')

plt.title('Coverage Curves — All Sites (dots = actual operating point)',
          fontsize=13, fontweight='bold')
plt.xlabel('Distance from Tower (km)', fontsize=12)
plt.ylabel('RSRP (dBm)', fontsize=12)
plt.legend(fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig('coverage_curves_all_sites.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print('Graph 2 saved: coverage_curves_all_sites.png')

print('\n' + '=' * 65)
print('  ANALYSIS COMPLETE — 2 graphs saved to your project folder')
print('=' * 65)
