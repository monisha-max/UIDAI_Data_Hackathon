"""
Create clean architecture diagrams for the hackathon presentation (no emojis)
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

# Indian Tricolor Theme
SAFFRON = '#FF9933'
WHITE = '#FFFFFF'
GREEN = '#138808'
NAVY = '#000080'
LIGHT_SAFFRON = '#FFE5CC'
LIGHT_GREEN = '#E5F5E5'

os.makedirs('/Users/lrao/Desktop/aadhar/diagrams', exist_ok=True)

def create_solution_overview():
    """Create overall solution overview diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title with flag colors
    ax.add_patch(FancyBboxPatch((4, 7.2), 6, 0.6, boxstyle="round,pad=0.02", facecolor=SAFFRON, edgecolor='none'))
    ax.text(7, 7.5, 'COMPLETE SOLUTION ARCHITECTURE', fontsize=16, fontweight='bold', ha='center', color=WHITE)
    ax.text(7, 6.8, 'Aadhaar Operational Intelligence Platform', fontsize=11, ha='center', color=NAVY, style='italic')
    
    # Data Source (top)
    data_box = FancyBboxPatch((5, 5.3), 4, 1.2, boxstyle="round,pad=0.05,rounding_size=0.2",
                               facecolor=SAFFRON, edgecolor=NAVY, linewidth=2)
    ax.add_patch(data_box)
    ax.text(7, 5.95, 'AADHAAR DATA', fontsize=12, fontweight='bold', ha='center', color=WHITE)
    ax.text(7, 5.55, 'Biometric | Demographic | Enrollment', fontsize=9, ha='center', color=WHITE)
    
    # MSI Module (left)
    msi_box = FancyBboxPatch((0.8, 2.3), 5.2, 2.7, boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=3)
    ax.add_patch(msi_box)
    ax.add_patch(FancyBboxPatch((0.8, 4.5), 5.2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=GREEN, edgecolor='none'))
    ax.text(3.4, 4.75, 'MODULE 1: MSI ANALYSIS', fontsize=11, fontweight='bold', ha='center', color=WHITE)
    ax.text(3.4, 4.0, 'Detect redistribution patterns', fontsize=9, ha='center', color='#333')
    ax.text(3.4, 3.5, 'Wave propagation tracking', fontsize=9, ha='center', color='#333')
    ax.text(3.4, 3.0, 'Hotspot identification', fontsize=9, ha='center', color='#333')
    ax.text(3.4, 2.5, '6 Interactive Dashboards', fontsize=9, ha='center', color=GREEN, fontweight='bold')
    
    # Load Balancer Module (right)
    lb_box = FancyBboxPatch((8, 2.3), 5.2, 2.7, boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=3)
    ax.add_patch(lb_box)
    ax.add_patch(FancyBboxPatch((8, 4.5), 5.2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=SAFFRON, edgecolor='none'))
    ax.text(10.6, 4.75, 'MODULE 2: LOAD BALANCER', fontsize=11, fontweight='bold', ha='center', color=WHITE)
    ax.text(10.6, 4.0, 'Forecast biometric load', fontsize=9, ha='center', color='#333')
    ax.text(10.6, 3.5, 'Identify overloaded centers', fontsize=9, ha='center', color='#333')
    ax.text(10.6, 3.0, 'Recommend alternatives', fontsize=9, ha='center', color='#333')
    ax.text(10.6, 2.5, '5 Interactive Dashboards', fontsize=9, ha='center', color=SAFFRON, fontweight='bold')
    
    # Arrows from data
    ax.annotate('', xy=(3.4, 5), xytext=(6, 5.3), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))
    ax.annotate('', xy=(10.6, 5), xytext=(8, 5.3), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))
    
    # Output (bottom)
    output_box = FancyBboxPatch((3.5, 0.4), 7, 1.5, boxstyle="round,pad=0.05,rounding_size=0.2",
                                 facecolor=GREEN, edgecolor=NAVY, linewidth=2)
    ax.add_patch(output_box)
    ax.text(7, 1.4, 'ACTIONABLE INSIGHTS', fontsize=13, fontweight='bold', ha='center', color=WHITE)
    ax.text(7, 0.85, '11 Interactive Dashboards  |  Decision Support  |  30% Load Reduction', 
            fontsize=9, ha='center', color=WHITE)
    
    # Arrows to output
    ax.annotate('', xy=(5, 1.9), xytext=(3.4, 2.3), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))
    ax.annotate('', xy=(9, 1.9), xytext=(10.6, 2.3), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/solution_overview.png', dpi=200, 
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Created: solution_overview.png")

def create_msi_pipeline():
    """Create MSI Analysis Pipeline Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title
    ax.add_patch(FancyBboxPatch((4, 8.2), 8, 0.6, boxstyle="round,pad=0.02", facecolor=GREEN, edgecolor='none'))
    ax.text(8, 8.5, 'MSI ANALYSIS PIPELINE', fontsize=16, fontweight='bold', ha='center', color=WHITE)
    
    # Pipeline stages
    stages = [
        (1.5, 5.5, 'DATA\nINGESTION', SAFFRON, ['1.8M+ Records', 'Biometric Data', 'Multi-state']),
        (4.5, 5.5, 'PREPROCESSING', WHITE, ['Weekly Aggregation', 'State/District/PIN', 'Data Cleaning']),
        (7.5, 5.5, 'MSI\nCALCULATION', GREEN, ['Neighbor Detection', 'Z-Score Analysis', 'Divergence Index']),
        (10.5, 5.5, 'PATTERN\nDETECTION', SAFFRON, ['Wave Propagation', 'Hotspot Ranking', 'Temporal Trends']),
        (13.5, 5.5, 'VISUALIZATION\n& INSIGHTS', GREEN, ['6 Dashboards', 'Heatmaps', 'Rankings']),
    ]
    
    for i, (x, y, title, color, details) in enumerate(stages):
        # Main box
        box = FancyBboxPatch((x-1.2, y-1.2), 2.4, 2.4, boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color if color != WHITE else '#F8F8F8', edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        
        # Stage number
        ax.add_patch(Circle((x-0.8, y+0.9), 0.3, facecolor=NAVY, edgecolor='none'))
        ax.text(x-0.8, y+0.9, str(i+1), fontsize=10, ha='center', va='center', color=WHITE, fontweight='bold')
        
        # Title
        text_color = WHITE if color in [SAFFRON, GREEN] else NAVY
        ax.text(x, y+0.2, title, fontsize=9, ha='center', va='center', fontweight='bold', color=text_color)
        
        # Details box below
        detail_box = FancyBboxPatch((x-1.1, y-2.8), 2.2, 1.3, boxstyle="round,pad=0.03",
                                     facecolor='white', edgecolor='#DDD', linewidth=1)
        ax.add_patch(detail_box)
        for j, detail in enumerate(details):
            ax.text(x, y-1.7-j*0.4, f'• {detail}', fontsize=8, ha='center', color='#444')
        
        # Arrow to next stage
        if i < 4:
            ax.annotate('', xy=(x+1.5, 5.5), xytext=(x+1.2, 5.5),
                       arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Formula box at bottom
    formula_box = FancyBboxPatch((4, 0.5), 8, 1.2, boxstyle="round,pad=0.05,rounding_size=0.2",
                                  facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=2)
    ax.add_patch(formula_box)
    ax.text(8, 1.3, 'MSI FORMULA', fontsize=11, fontweight='bold', ha='center', color=NAVY)
    ax.text(8, 0.8, 'MSI = Neighbor_Divergence × Temporal_Consistency × (1 + Wave_Propagation)', 
            fontsize=9, ha='center', color='#333', family='monospace')
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/msi_pipeline.png', dpi=200, 
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Created: msi_pipeline.png")

def create_load_balancer_pipeline():
    """Create Load Balancer Pipeline Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title
    ax.add_patch(FancyBboxPatch((4, 9.2), 8, 0.6, boxstyle="round,pad=0.02", facecolor=SAFFRON, edgecolor='none'))
    ax.text(8, 9.5, 'LOAD BALANCER PIPELINE', fontsize=16, fontweight='bold', ha='center', color=WHITE)
    
    # Input
    input_box = FancyBboxPatch((0.5, 6), 3, 2.5, boxstyle="round,pad=0.05,rounding_size=0.2",
                                facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=2)
    ax.add_patch(input_box)
    ax.text(2, 8, 'INPUT DATA', fontsize=11, fontweight='bold', ha='center', color=NAVY)
    ax.text(2, 7.3, 'Biometric Updates', fontsize=9, ha='center', color='#333')
    ax.text(2, 6.8, '1.8M Records', fontsize=9, ha='center', color='#333')
    ax.text(2, 6.3, 'State/District/PIN', fontsize=9, ha='center', color='#333')
    
    # Processing stages
    stages = [
        (5.5, 7.25, 'FORECAST\nENGINE', GREEN, 'Seasonal + Trend\nNext Month Load'),
        (9, 7.25, 'LOAD SCORE\nCALCULATOR', SAFFRON, 'Load × 0.7 +\nSpike Risk × 0.3'),
        (12.5, 7.25, 'ALTERNATIVE\nFINDER', GREEN, 'Same District +\nAdjacent PINs'),
    ]
    
    for x, y, title, color, detail in stages:
        box = FancyBboxPatch((x-1.3, y-1.2), 2.6, 2.4, boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color, edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.4, title, fontsize=9, ha='center', va='center', fontweight='bold', color=WHITE)
        ax.text(x, y-0.5, detail, fontsize=8, ha='center', color=WHITE, family='monospace')
    
    # Arrows
    ax.annotate('', xy=(4.2, 7.25), xytext=(3.5, 7.25), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(7.7, 7.25), xytext=(6.8, 7.25), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(11.2, 7.25), xytext=(10.3, 7.25), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Simulation Engine
    sim_box = FancyBboxPatch((5, 3.5), 6, 2, boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=3)
    ax.add_patch(sim_box)
    ax.add_patch(FancyBboxPatch((5, 5), 6, 0.5, boxstyle="round,pad=0.02", facecolor=GREEN, edgecolor='none'))
    ax.text(8, 5.25, 'SIMULATION ENGINE', fontsize=11, fontweight='bold', ha='center', color=WHITE)
    ax.text(8, 4.5, '"If we redirect X% load from overloaded PINs..."', fontsize=9, ha='center', style='italic', color='#333')
    ax.text(8, 3.9, '10% → 10% reduction  |  20% → 20% reduction  |  30% → 30% reduction', 
            fontsize=8, ha='center', color='#666', family='monospace')
    
    ax.annotate('', xy=(8, 5.5), xytext=(9, 6.05), arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Outputs
    ax.text(8, 2.8, 'OUTPUTS', fontsize=12, fontweight='bold', ha='center', color=NAVY)
    
    outputs = [
        (2, 1.2, 'Top 20\nOverloaded', SAFFRON),
        (5.5, 1.2, 'Recommended\nAlternatives', WHITE),
        (9, 1.2, 'Load\nReduction %', GREEN),
        (12.5, 1.2, '5 Interactive\nDashboards', SAFFRON),
    ]
    
    for x, y, text, color in outputs:
        box = FancyBboxPatch((x-1.3, y-0.8), 2.6, 1.6, boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color if color != WHITE else '#F8F8F8', edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        text_color = WHITE if color in [SAFFRON, GREEN] else NAVY
        ax.text(x, y, text, fontsize=9, ha='center', va='center', fontweight='bold', color=text_color)
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/load_balancer_pipeline.png', dpi=200, 
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Created: load_balancer_pipeline.png")

def create_before_after():
    """Create Before/After Load Balancing Comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('LOAD BALANCING IMPACT', fontsize=16, fontweight='bold', color=NAVY, y=1.02)
    
    pincodes = ['PIN A', 'PIN B', 'PIN C', 'PIN D', 'PIN E']
    before_load = [95, 88, 30, 25, 20]
    after_load = [60, 58, 48, 45, 42]
    capacity_line = 70
    
    # BEFORE
    ax1 = axes[0]
    colors1 = ['#CC0000' if v > capacity_line else SAFFRON for v in before_load]
    bars1 = ax1.bar(pincodes, before_load, color=colors1, edgecolor=NAVY, linewidth=2)
    ax1.axhline(y=capacity_line, color='#CC0000', linestyle='--', linewidth=2, label='Capacity Limit')
    ax1.set_ylabel('Load (Biometric Updates)', fontsize=11, fontweight='bold')
    ax1.set_title('BEFORE Load Balancing', fontsize=13, fontweight='bold', color='#CC0000')
    ax1.set_ylim(0, 110)
    ax1.legend(loc='upper right')
    ax1.set_facecolor('#FFF5F5')
    
    for i, v in enumerate(before_load):
        label = 'OVERLOAD!' if v > capacity_line else ''
        ax1.text(i, v + 3, label, ha='center', fontsize=8, color='#CC0000', fontweight='bold')
    
    # AFTER
    ax2 = axes[1]
    bars2 = ax2.bar(pincodes, after_load, color=GREEN, edgecolor=NAVY, linewidth=2)
    ax2.axhline(y=capacity_line, color=GREEN, linestyle='--', linewidth=2, label='Capacity Limit')
    ax2.set_ylabel('Load (Biometric Updates)', fontsize=11, fontweight='bold')
    ax2.set_title('AFTER Load Balancing', fontsize=13, fontweight='bold', color=GREEN)
    ax2.set_ylim(0, 110)
    ax2.legend(loc='upper right')
    ax2.set_facecolor('#F5FFF5')
    
    for i, v in enumerate(after_load):
        ax2.text(i, v + 3, 'OK', ha='center', fontsize=9, color=GREEN, fontweight='bold')
    
    fig.text(0.5, -0.02, '30% of load redirected from overloaded PINs to nearby alternatives', 
             ha='center', fontsize=11, fontweight='bold', color=NAVY,
             bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON))
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/before_after.png', dpi=200, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created: before_after.png")

def create_msi_concept():
    """Create MSI Concept Explanation"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('UNDERSTANDING MOBILITY SIGNAL INDEX (MSI)', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
    
    scenarios = [
        (axes[0], 'LOW MSI\n(Synchronized)', '#FFF5F5', '#CC0000', 
         [1,1,1,1,1], 'All areas increase together\n→ Policy/Camp Effect'),
        (axes[1], 'HIGH MSI\n(Redistribution)', '#F5FFF5', GREEN,
         [-1,1,1,1,1], 'Center drops, neighbors rise\n→ Population Movement'),
        (axes[2], 'MEDIUM MSI\n(Local Event)', '#FFFFF5', SAFFRON,
         [1,0,0,0,0], 'Only one area spikes\n→ Local Camp/Drive'),
    ]
    
    for ax, title, bgcolor, title_color, directions, desc in scenarios:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_facecolor(bgcolor)
        
        ax.text(5, 9, title, fontsize=11, fontweight='bold', ha='center', color=title_color)
        
        positions = [(5, 5), (3, 7), (7, 7), (3, 3), (7, 3)]
        for i, ((x, y), d) in enumerate(zip(positions, directions)):
            if d == 1:
                color = '#66CC66'
                arrow = '↑'
            elif d == -1:
                color = '#CC6666'
                arrow = '↓'
            else:
                color = '#CCCCCC'
                arrow = '—'
            
            circle = plt.Circle((x, y), 0.7, color=color, ec=NAVY, linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, arrow, fontsize=20, ha='center', va='center', color=NAVY, fontweight='bold')
        
        ax.text(5, 1, desc, fontsize=9, ha='center', color='#444',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#DDD'))
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/msi_concept.png', dpi=200, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created: msi_concept.png")

# Generate all diagrams
print("\nCreating architecture diagrams (clean version)...\n")
create_solution_overview()
create_msi_pipeline()
create_load_balancer_pipeline()
create_before_after()
create_msi_concept()

print("\nAll diagrams saved to /Users/lrao/Desktop/aadhar/diagrams/")
print("\nFiles created:")
for f in sorted(os.listdir('/Users/lrao/Desktop/aadhar/diagrams')):
    if f.endswith('.png'):
        print(f"  • {f}")
