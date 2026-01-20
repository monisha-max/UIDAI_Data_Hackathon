"""
Create comprehensive platform architecture diagram - from data to insights
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
import os

# Indian Tricolor Theme
SAFFRON = '#FF9933'
WHITE = '#FFFFFF'
GREEN = '#138808'
NAVY = '#000080'
LIGHT_SAFFRON = '#FFE5CC'
LIGHT_GREEN = '#E5F5E5'
LIGHT_BLUE = '#E5F0FF'
GRAY = '#F5F5F5'

os.makedirs('/Users/lrao/Desktop/aadhar/diagrams', exist_ok=True)

def create_full_architecture():
    """Create comprehensive architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # ============== TITLE ==============
    # Saffron header bar
    ax.add_patch(FancyBboxPatch((0.5, 13), 17, 0.8, boxstyle="round,pad=0.02", 
                                 facecolor=SAFFRON, edgecolor='none'))
    ax.text(9, 13.4, 'AADHAAR OPERATIONAL INTELLIGENCE PLATFORM', 
            fontsize=18, fontweight='bold', ha='center', color=WHITE)
    
    # ============== DATA SOURCES (Top) ==============
    ax.text(9, 12.3, 'DATA SOURCES', fontsize=12, fontweight='bold', ha='center', color=NAVY)
    
    data_sources = [
        (3, 11.2, 'BIOMETRIC\nUPDATES', '1.86M records', SAFFRON),
        (9, 11.2, 'DEMOGRAPHIC\nUPDATES', '2.07M records', WHITE),
        (15, 11.2, 'ENROLLMENT\nDATA', '1.0M records', GREEN),
    ]
    
    for x, y, title, subtitle, color in data_sources:
        box = FancyBboxPatch((x-1.8, y-0.7), 3.6, 1.4, boxstyle="round,pad=0.05",
                             facecolor=color if color != WHITE else GRAY, 
                             edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        text_color = WHITE if color in [SAFFRON, GREEN] else NAVY
        ax.text(x, y+0.2, title, fontsize=9, ha='center', va='center', 
                fontweight='bold', color=text_color)
        ax.text(x, y-0.35, subtitle, fontsize=8, ha='center', color=text_color, alpha=0.8)
    
    # Arrows from data sources down
    for x in [3, 9, 15]:
        ax.annotate('', xy=(9, 9.8), xytext=(x, 10.5),
                   arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    
    # ============== DATA INGESTION & PREPROCESSING ==============
    ingest_box = FancyBboxPatch((5.5, 8.8), 7, 1, boxstyle="round,pad=0.05",
                                 facecolor=LIGHT_BLUE, edgecolor=NAVY, linewidth=2)
    ax.add_patch(ingest_box)
    ax.text(9, 9.5, 'DATA INGESTION & PREPROCESSING', fontsize=10, 
            fontweight='bold', ha='center', color=NAVY)
    ax.text(9, 9.0, 'Cleaning | Aggregation (Weekly/Monthly) | Geographic Mapping', 
            fontsize=8, ha='center', color='#444')
    
    # Arrow down
    ax.annotate('', xy=(9, 8.0), xytext=(9, 8.8),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # ============== LAYER 1: ANALYTICS ENGINE ==============
    # Main box
    layer1_box = FancyBboxPatch((2, 5.8), 14, 2.2, boxstyle="round,pad=0.05",
                                 facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=3)
    ax.add_patch(layer1_box)
    
    # Header
    ax.add_patch(FancyBboxPatch((2, 7.5), 14, 0.5, boxstyle="round,pad=0.02",
                                facecolor=SAFFRON, edgecolor='none'))
    ax.text(9, 7.75, 'LAYER 1: ANALYTICS ENGINE (Foundation)', 
            fontsize=11, fontweight='bold', ha='center', color=WHITE)
    
    # Sub-components
    layer1_items = [
        (4.5, 6.6, 'Rolling Indicators\n(7/14/30 day windows)'),
        (9, 6.6, 'Change-Point Detection\n(ruptures library)'),
        (13.5, 6.6, 'Anomaly Scoring\n(z-score / MAD)'),
    ]
    for x, y, text in layer1_items:
        box = FancyBboxPatch((x-2, y-0.5), 4, 1, boxstyle="round,pad=0.03",
                             facecolor=WHITE, edgecolor=SAFFRON, linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8, ha='center', va='center', color='#333')
    
    ax.text(9, 6.0, 'OUTPUT: Feature tables per area per date', 
            fontsize=9, ha='center', color=NAVY, style='italic', fontweight='bold')
    
    # Arrows down to Layer 2
    ax.annotate('', xy=(5, 5.0), xytext=(7, 5.8),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(13, 5.0), xytext=(11, 5.8),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # ============== LAYER 2a: MSI ANALYSIS ==============
    layer2a_box = FancyBboxPatch((1, 2.8), 7, 2.2, boxstyle="round,pad=0.05",
                                  facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=3)
    ax.add_patch(layer2a_box)
    
    ax.add_patch(FancyBboxPatch((1, 4.5), 7, 0.5, boxstyle="round,pad=0.02",
                                facecolor=GREEN, edgecolor='none'))
    ax.text(4.5, 4.75, 'LAYER 2a: MSI ANALYSIS', 
            fontsize=10, fontweight='bold', ha='center', color=WHITE)
    ax.text(4.5, 4.3, '(Pattern Detection)', fontsize=9, ha='center', color=GREEN)
    
    msi_items = ['Redistribution signals', 'Wave propagation', 'Hotspot ranking']
    for i, item in enumerate(msi_items):
        ax.text(4.5, 3.8 - i*0.35, f'• {item}', fontsize=9, ha='center', color='#333')
    
    ax.text(4.5, 2.95, 'WHERE & WHEN', fontsize=10, ha='center', 
            color=GREEN, fontweight='bold')
    
    # ============== LAYER 2b: LOAD BALANCER ==============
    layer2b_box = FancyBboxPatch((10, 2.8), 7, 2.2, boxstyle="round,pad=0.05",
                                  facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=3)
    ax.add_patch(layer2b_box)
    
    ax.add_patch(FancyBboxPatch((10, 4.5), 7, 0.5, boxstyle="round,pad=0.02",
                                facecolor=SAFFRON, edgecolor='none'))
    ax.text(13.5, 4.75, 'LAYER 2b: LOAD BALANCER', 
            fontsize=10, fontweight='bold', ha='center', color=WHITE)
    ax.text(13.5, 4.3, '(Operations Tool)', fontsize=9, ha='center', color=SAFFRON)
    
    lb_items = ['Demand forecasting', 'Overload identification', 
                'Alternative recommendations', 'Simulation engine']
    for i, item in enumerate(lb_items):
        ax.text(13.5, 3.9 - i*0.32, f'• {item}', fontsize=9, ha='center', color='#333')
    
    ax.text(13.5, 2.95, 'WHAT TO DO', fontsize=10, ha='center', 
            color=SAFFRON, fontweight='bold')
    
    # Arrows down to Layer 3
    ax.annotate('', xy=(7, 2.0), xytext=(4.5, 2.8),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(11, 2.0), xytext=(13.5, 2.8),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # ============== LAYER 3: CHANGE-POINT EXPLAINER ==============
    layer3_box = FancyBboxPatch((4, 0.3), 10, 1.7, boxstyle="round,pad=0.05",
                                 facecolor=LIGHT_BLUE, edgecolor=NAVY, linewidth=3)
    ax.add_patch(layer3_box)
    
    ax.add_patch(FancyBboxPatch((4, 1.5), 10, 0.5, boxstyle="round,pad=0.02",
                                facecolor=NAVY, edgecolor='none'))
    ax.text(9, 1.75, 'LAYER 3: CHANGE-POINT EXPLAINER (Interpretation)', 
            fontsize=10, fontweight='bold', ha='center', color=WHITE)
    
    explainer_items = [
        'What changed (magnitude, age splits)',
        'Where it started (first-affected pincodes)',
        'How long it lasted (persistence)',
        'Pattern matching (similar historical events)'
    ]
    ax.text(6, 1.1, '• ' + explainer_items[0], fontsize=8, ha='left', color='#333')
    ax.text(6, 0.75, '• ' + explainer_items[1], fontsize=8, ha='left', color='#333')
    ax.text(10.5, 1.1, '• ' + explainer_items[2], fontsize=8, ha='left', color='#333')
    ax.text(10.5, 0.75, '• ' + explainer_items[3], fontsize=8, ha='left', color='#333')
    
    ax.text(9, 0.4, 'WHY IT HAPPENED (inferred)', fontsize=10, ha='center', 
            color=NAVY, fontweight='bold')
    
    # ============== SIDE PANELS: OUTPUTS ==============
    # Left side - Dashboards
    ax.add_patch(FancyBboxPatch((0.2, 0.3), 3.5, 4.7, boxstyle="round,pad=0.05",
                                facecolor='#F0F0F0', edgecolor='#CCC', linewidth=1, linestyle='--'))
    ax.text(2, 4.7, 'OUTPUTS', fontsize=9, fontweight='bold', ha='center', color='#666')
    
    outputs = ['11 Dashboards', '6 MSI Visualizations', '5 Load Balancer Charts', 
               'Automated Reports', 'Recommendations']
    for i, item in enumerate(outputs):
        ax.text(2, 4.2 - i*0.4, f'• {item}', fontsize=8, ha='center', color='#555')
    
    # Right side - Key Metrics
    ax.add_patch(FancyBboxPatch((14.3, 0.3), 3.5, 4.7, boxstyle="round,pad=0.05",
                                facecolor='#F0F0F0', edgecolor='#CCC', linewidth=1, linestyle='--'))
    ax.text(16, 4.7, 'KEY METRICS', fontsize=9, fontweight='bold', ha='center', color='#666')
    
    metrics = ['276 Redistribution Events', '14 Wave Patterns', 
               '84 Overloaded Pincodes', '30% Load Reduction', '4.9M Records Analyzed']
    for i, item in enumerate(metrics):
        ax.text(16, 4.2 - i*0.4, f'• {item}', fontsize=8, ha='center', color='#555')
    
    # ============== FOOTER ==============
    ax.add_patch(FancyBboxPatch((0.5, -0.5), 17, 0.4, boxstyle="round,pad=0.02",
                                facecolor=GREEN, edgecolor='none'))
    ax.text(9, -0.3, 'UIDAI Aadhaar Hackathon 2025  |  Theme: Indian Tricolor', 
            fontsize=9, ha='center', color=WHITE)
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/full_platform_architecture.png', 
                dpi=200, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Created: full_platform_architecture.png")

def create_data_flow_diagram():
    """Create a simpler data flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title
    ax.add_patch(FancyBboxPatch((4, 9.2), 8, 0.6, boxstyle="round,pad=0.02",
                                facecolor=SAFFRON, edgecolor='none'))
    ax.text(8, 9.5, 'DATA FLOW: END-TO-END PIPELINE', 
            fontsize=14, fontweight='bold', ha='center', color=WHITE)
    
    # Flow stages (vertical)
    stages = [
        (8, 8.2, 'RAW DATA', 'Biometric + Demographic + Enrollment\n4.9M total records', SAFFRON, WHITE),
        (8, 6.5, 'PREPROCESSING', 'Cleaning, Aggregation, Geographic Mapping', GRAY, NAVY),
        (8, 4.8, 'FEATURE ENGINEERING', 'Rolling stats, Change-points, Anomalies', LIGHT_SAFFRON, NAVY),
        (4, 3.0, 'MSI ANALYSIS', 'Spatial patterns\n276 events detected', GREEN, WHITE),
        (12, 3.0, 'LOAD BALANCER', 'Forecasting & Simulation\n30% reduction possible', SAFFRON, WHITE),
        (8, 1.2, 'INSIGHTS & ACTIONS', 'Dashboards + Reports + Recommendations', NAVY, WHITE),
    ]
    
    for x, y, title, desc, bgcolor, textcolor in stages:
        width = 6 if x == 8 else 5
        box = FancyBboxPatch((x-width/2, y-0.6), width, 1.2, boxstyle="round,pad=0.05",
                             facecolor=bgcolor, edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.15, title, fontsize=10, ha='center', va='center', 
                fontweight='bold', color=textcolor)
        ax.text(x, y-0.25, desc, fontsize=8, ha='center', va='center', color=textcolor, alpha=0.9)
    
    # Arrows
    ax.annotate('', xy=(8, 7.7), xytext=(8, 7.1), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(8, 6.0), xytext=(8, 5.4), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Split arrows
    ax.annotate('', xy=(4, 3.6), xytext=(6.5, 4.2), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(12, 3.6), xytext=(9.5, 4.2), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Merge arrows
    ax.annotate('', xy=(6.5, 1.8), xytext=(4, 2.4), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(9.5, 1.8), xytext=(12, 2.4), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/data_flow.png', 
                dpi=200, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Created: data_flow.png")

# Generate diagrams
print("\nCreating comprehensive architecture diagrams...\n")
create_full_architecture()
create_data_flow_diagram()

print("\nDone! Files saved to /Users/lrao/Desktop/aadhar/diagrams/")
