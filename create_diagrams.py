"""
Create architecture diagrams for the hackathon presentation
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Indian Tricolor Theme
SAFFRON = '#FF9933'
WHITE = '#FFFFFF'
GREEN = '#138808'
NAVY = '#000080'
LIGHT_SAFFRON = '#FFE5CC'
LIGHT_GREEN = '#E5F5E5'

def create_msi_architecture():
    """Create MSI Analysis Pipeline Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title
    ax.text(8, 9.5, '🇮🇳 Mobility Signal Index (MSI) Analysis Pipeline', 
            fontsize=20, fontweight='bold', ha='center', color=NAVY)
    
    # Stage boxes - horizontal flow
    stages = [
        (1, 6, 'Data\nIngestion', SAFFRON, '📊'),
        (4, 6, 'Preprocessing\n& Aggregation', WHITE, '⚙️'),
        (7, 6, 'MSI\nCalculation', GREEN, '📈'),
        (10, 6, 'Pattern\nDetection', SAFFRON, '🔍'),
        (13, 6, 'Insights &\nVisualization', GREEN, '📊')
    ]
    
    for x, y, text, color, emoji in stages:
        box = FancyBboxPatch((x-1, y-1), 2.5, 2,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color if color != WHITE else '#F5F5F5',
                             edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        ax.text(x+0.25, y+0.5, emoji, fontsize=24, ha='center', va='center')
        ax.text(x+0.25, y-0.3, text, fontsize=10, ha='center', va='center', 
                fontweight='bold', color=NAVY)
    
    # Arrows between stages
    for i in range(4):
        ax.annotate('', xy=(stages[i+1][0]-1, 6), xytext=(stages[i][0]+1.5, 6),
                   arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Details below each stage
    details = [
        (1.25, 3.5, '• Biometric Data\n• Enrollment Data\n• 1.8M+ Records'),
        (4.25, 3.5, '• Weekly Aggregation\n• State/District/PIN\n• Missing Data Fill'),
        (7.25, 3.5, '• Neighbor Detection\n• Z-Score Calculation\n• Divergence Index'),
        (10.25, 3.5, '• Wave Propagation\n• Hotspot Ranking\n• Temporal Patterns'),
        (13.25, 3.5, '• 6 Dashboards\n• Heatmaps\n• Rankings')
    ]
    
    for x, y, text in details:
        ax.text(x, y, text, fontsize=9, ha='center', va='top', 
                color='#333', family='monospace',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#DDD', alpha=0.8))
    
    # Formula box
    formula_box = FancyBboxPatch((4, 0.5), 8, 1.5,
                                  boxstyle="round,pad=0.05,rounding_size=0.2",
                                  facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=2)
    ax.add_patch(formula_box)
    ax.text(8, 1.5, 'MSI Formula', fontsize=12, fontweight='bold', ha='center', color=NAVY)
    ax.text(8, 0.9, 'MSI = Neighbor_Divergence × Temporal_Consistency × (1 + Wave_Propagation)', 
            fontsize=10, ha='center', color='#333', family='monospace')
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/msi_architecture.png', dpi=150, 
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("✓ Created MSI Architecture Diagram")

def create_load_balancer_architecture():
    """Create Load Balancer Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title
    ax.text(8, 11.5, '🇮🇳 Biometric Load Balancer Architecture', 
            fontsize=20, fontweight='bold', ha='center', color=NAVY)
    
    # Input Data (left side)
    input_box = FancyBboxPatch((0.5, 7), 3, 3,
                                boxstyle="round,pad=0.05,rounding_size=0.2",
                                facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=2)
    ax.add_patch(input_box)
    ax.text(2, 9.5, '📊 Input Data', fontsize=12, fontweight='bold', ha='center', color=NAVY)
    ax.text(2, 8.5, '• Biometric Updates\n• 1.8M Records\n• State/District/PIN\n• Date/Time', 
            fontsize=9, ha='center', va='center', family='monospace')
    
    # Processing Pipeline (center)
    pipeline_stages = [
        (5.5, 9, 'Forecast\nEngine', '🔮', 'Seasonal + Trend\nNext Month Load'),
        (9, 9, 'Load Score\nCalculator', '📊', 'Percentile × 0.7 +\nSpike Risk × 0.3'),
        (12.5, 9, 'Alternative\nFinder', '🔍', 'Same District +\nAdjacent PINs'),
    ]
    
    for x, y, title, emoji, detail in pipeline_stages:
        box = FancyBboxPatch((x-1.3, y-1.2), 2.6, 2.4,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=WHITE, edgecolor=GREEN, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.7, emoji, fontsize=20, ha='center')
        ax.text(x, y, title, fontsize=10, fontweight='bold', ha='center', color=NAVY)
        ax.text(x, y-0.7, detail, fontsize=8, ha='center', color='#666', family='monospace')
    
    # Arrows
    ax.annotate('', xy=(4.2, 8.5), xytext=(3.5, 8.5),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(7.7, 9), xytext=(6.8, 9),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(11.2, 9), xytext=(10.3, 9),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Simulation Engine (bottom center)
    sim_box = FancyBboxPatch((5.5, 4), 5, 2.5,
                              boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
    ax.add_patch(sim_box)
    ax.text(8, 5.8, '⚡ Simulation Engine', fontsize=12, fontweight='bold', ha='center', color=NAVY)
    ax.text(8, 4.8, '"If we redirect X% load → Peak drops by Y%"', 
            fontsize=10, ha='center', style='italic', color='#333')
    ax.text(8, 4.3, '10% → 10% reduction  |  20% → 20% reduction  |  30% → 30% reduction', 
            fontsize=9, ha='center', color='#666', family='monospace')
    
    # Arrow to simulation
    ax.annotate('', xy=(8, 6.5), xytext=(9, 7.8),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Output (bottom)
    outputs = [
        (2, 1.5, '📋 Top 20\nOverloaded', SAFFRON),
        (6, 1.5, '🎯 Recommended\nAlternatives', WHITE),
        (10, 1.5, '📉 Load\nReduction %', GREEN),
        (14, 1.5, '📊 5 Interactive\nDashboards', SAFFRON),
    ]
    
    ax.text(8, 3.2, '📤 Outputs', fontsize=14, fontweight='bold', ha='center', color=NAVY)
    
    for x, y, text, color in outputs:
        box = FancyBboxPatch((x-1.3, y-1), 2.6, 1.8,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color if color != WHITE else '#F5F5F5',
                             edgecolor=NAVY, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=10, ha='center', va='center', 
                fontweight='bold', color=NAVY)
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/load_balancer_architecture.png', dpi=150, 
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("✓ Created Load Balancer Architecture Diagram")

def create_before_after_diagram():
    """Create Before/After Load Balancing Comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Data for visualization
    pincodes = ['PIN A', 'PIN B', 'PIN C', 'PIN D', 'PIN E']
    before_load = [85, 95, 30, 25, 20]  # Overloaded at A and B
    after_load = [60, 65, 45, 40, 35]   # Balanced
    
    capacity_line = 70  # Capacity threshold
    
    # Before Load Balancing
    ax1 = axes[0]
    bars1 = ax1.bar(pincodes, before_load, color=[
        '#FF4444' if v > capacity_line else SAFFRON for v in before_load
    ], edgecolor=NAVY, linewidth=2)
    ax1.axhline(y=capacity_line, color='red', linestyle='--', linewidth=2, label='Capacity Limit')
    ax1.set_ylabel('Load (Biometric Updates)', fontsize=12, fontweight='bold')
    ax1.set_title('❌ BEFORE Load Balancing', fontsize=14, fontweight='bold', color='#CC0000')
    ax1.set_ylim(0, 110)
    ax1.legend()
    ax1.set_facecolor('#FFF5F5')
    
    # Add overload labels
    for i, v in enumerate(before_load):
        if v > capacity_line:
            ax1.text(i, v + 3, '⚠️ OVERLOAD', ha='center', fontsize=9, color='red', fontweight='bold')
    
    # After Load Balancing
    ax2 = axes[1]
    bars2 = ax2.bar(pincodes, after_load, color=GREEN, edgecolor=NAVY, linewidth=2)
    ax2.axhline(y=capacity_line, color='green', linestyle='--', linewidth=2, label='Capacity Limit')
    ax2.set_ylabel('Load (Biometric Updates)', fontsize=12, fontweight='bold')
    ax2.set_title('✅ AFTER Load Balancing', fontsize=14, fontweight='bold', color=GREEN)
    ax2.set_ylim(0, 110)
    ax2.legend()
    ax2.set_facecolor('#F5FFF5')
    
    # Add balanced labels
    for i, v in enumerate(after_load):
        ax2.text(i, v + 3, '✓', ha='center', fontsize=12, color=GREEN, fontweight='bold')
    
    # Add arrows showing redistribution
    fig.text(0.5, 0.02, '🔄 30% of load redirected from overloaded PINs to nearby alternatives', 
             ha='center', fontsize=12, fontweight='bold', color=NAVY)
    
    plt.suptitle('🇮🇳 Load Balancing Impact Visualization', fontsize=16, fontweight='bold', color=NAVY, y=1.02)
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/before_after_comparison.png', dpi=150, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created Before/After Comparison Diagram")

def create_msi_concept_diagram():
    """Create MSI Concept Explanation Diagram"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Scenario 1: Synchronized (Low MSI)
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_facecolor('#FFF5F5')
    
    # Center and neighbors all going up
    ax1.text(5, 9, '📉 Low MSI (Synchronized)', fontsize=12, fontweight='bold', ha='center', color='#CC0000')
    
    # Draw pincodes as circles
    circle_positions = [(5, 5), (3, 7), (7, 7), (3, 3), (7, 3)]
    for i, (x, y) in enumerate(circle_positions):
        circle = plt.Circle((x, y), 0.8, color='#FF6666', ec=NAVY, linewidth=2)
        ax1.add_patch(circle)
        ax1.annotate('', xy=(x, y+0.5), xytext=(x, y-0.3),
                    arrowprops=dict(arrowstyle='->', color='green', lw=2))
    
    ax1.text(5, 1, 'All areas increase together\n→ Likely: Policy/Camp Effect', 
             fontsize=9, ha='center', color='#666')
    
    # Scenario 2: Redistribution (High MSI)
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_facecolor('#F5FFF5')
    
    ax2.text(5, 9, '📈 High MSI (Redistribution)', fontsize=12, fontweight='bold', ha='center', color=GREEN)
    
    # Center going down, neighbors going up
    for i, (x, y) in enumerate(circle_positions):
        if i == 0:  # Center
            color = '#FF6666'
            arrow_dir = -1  # Down
        else:
            color = '#66FF66'
            arrow_dir = 1  # Up
        
        circle = plt.Circle((x, y), 0.8, color=color, ec=NAVY, linewidth=2)
        ax2.add_patch(circle)
        ax2.annotate('', xy=(x, y + 0.5*arrow_dir), xytext=(x, y - 0.3*arrow_dir),
                    arrowprops=dict(arrowstyle='->', color='green' if arrow_dir > 0 else 'red', lw=2))
    
    ax2.text(5, 1, 'Center drops, neighbors rise\n→ Likely: Population Movement', 
             fontsize=9, ha='center', color='#666')
    
    # Scenario 3: Isolated Spike (Medium MSI)
    ax3 = axes[2]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    ax3.set_facecolor('#FFFFF5')
    
    ax3.text(5, 9, '➡️ Medium MSI (Local Event)', fontsize=12, fontweight='bold', ha='center', color=SAFFRON)
    
    # Only center spiking
    for i, (x, y) in enumerate(circle_positions):
        if i == 0:  # Center
            color = '#66FF66'
            circle = plt.Circle((x, y), 0.8, color=color, ec=NAVY, linewidth=2)
            ax3.add_patch(circle)
            ax3.annotate('', xy=(x, y+0.5), xytext=(x, y-0.3),
                        arrowprops=dict(arrowstyle='->', color='green', lw=2))
        else:
            color = '#DDDDDD'
            circle = plt.Circle((x, y), 0.8, color=color, ec=NAVY, linewidth=2)
            ax3.add_patch(circle)
            ax3.text(x, y, '—', fontsize=16, ha='center', va='center', color='#666')
    
    ax3.text(5, 1, 'Only one area spikes\n→ Likely: Local Camp/Drive', 
             fontsize=9, ha='center', color='#666')
    
    plt.suptitle('🇮🇳 Understanding Mobility Signal Index (MSI)', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/msi_concept.png', dpi=150, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created MSI Concept Diagram")

def create_solution_overview():
    """Create overall solution overview diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')
    
    # Title
    ax.text(7, 7.5, '🇮🇳 Complete Solution Architecture', 
            fontsize=18, fontweight='bold', ha='center', color=NAVY)
    ax.text(7, 7, 'Aadhaar Operational Intelligence Platform', 
            fontsize=12, ha='center', color='#666', style='italic')
    
    # Data Source (top)
    data_box = FancyBboxPatch((5, 5.5), 4, 1.2,
                               boxstyle="round,pad=0.05,rounding_size=0.2",
                               facecolor=SAFFRON, edgecolor=NAVY, linewidth=2)
    ax.add_patch(data_box)
    ax.text(7, 6.1, '📊 Aadhaar Data', fontsize=12, fontweight='bold', ha='center', color=NAVY)
    ax.text(7, 5.7, 'Biometric • Demographic • Enrollment', fontsize=9, ha='center', color='#333')
    
    # Two modules
    # MSI Module (left)
    msi_box = FancyBboxPatch((1, 2.5), 5, 2.5,
                              boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
    ax.add_patch(msi_box)
    ax.text(3.5, 4.5, '🔍 Module 1: MSI Analysis', fontsize=11, fontweight='bold', ha='center', color=NAVY)
    ax.text(3.5, 3.8, '• Detect redistribution patterns', fontsize=9, ha='center', color='#333')
    ax.text(3.5, 3.3, '• Wave propagation tracking', fontsize=9, ha='center', color='#333')
    ax.text(3.5, 2.8, '• Hotspot identification', fontsize=9, ha='center', color='#333')
    
    # Load Balancer Module (right)
    lb_box = FancyBboxPatch((8, 2.5), 5, 2.5,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=LIGHT_SAFFRON, edgecolor=SAFFRON, linewidth=2)
    ax.add_patch(lb_box)
    ax.text(10.5, 4.5, '⚖️ Module 2: Load Balancer', fontsize=11, fontweight='bold', ha='center', color=NAVY)
    ax.text(10.5, 3.8, '• Forecast biometric load', fontsize=9, ha='center', color='#333')
    ax.text(10.5, 3.3, '• Identify overloaded centers', fontsize=9, ha='center', color='#333')
    ax.text(10.5, 2.8, '• Recommend alternatives', fontsize=9, ha='center', color='#333')
    
    # Arrows from data
    ax.annotate('', xy=(3.5, 5), xytext=(6, 5.5),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(10.5, 5), xytext=(8, 5.5),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    # Output (bottom)
    output_box = FancyBboxPatch((4, 0.5), 6, 1.5,
                                 boxstyle="round,pad=0.05,rounding_size=0.2",
                                 facecolor=GREEN, edgecolor=NAVY, linewidth=2)
    ax.add_patch(output_box)
    ax.text(7, 1.5, '📈 Actionable Insights', fontsize=12, fontweight='bold', ha='center', color=WHITE)
    ax.text(7, 0.9, '11 Interactive Dashboards • Decision Support • 30% Load Reduction', 
            fontsize=9, ha='center', color=WHITE)
    
    # Arrows to output
    ax.annotate('', xy=(5.5, 2), xytext=(3.5, 2.5),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    ax.annotate('', xy=(8.5, 2), xytext=(10.5, 2.5),
               arrowprops=dict(arrowstyle='->', color=NAVY, lw=2))
    
    plt.tight_layout()
    plt.savefig('/Users/lrao/Desktop/aadhar/diagrams/solution_overview.png', dpi=150, 
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("✓ Created Solution Overview Diagram")

# Create diagrams directory
import os
os.makedirs('/Users/lrao/Desktop/aadhar/diagrams', exist_ok=True)

# Generate all diagrams
print("Creating architecture diagrams...")
create_solution_overview()
create_msi_architecture()
create_msi_concept_diagram()
create_load_balancer_architecture()
create_before_after_diagram()

print("\n✅ All diagrams created in /Users/lrao/Desktop/aadhar/diagrams/")
print("Files:")
for f in os.listdir('/Users/lrao/Desktop/aadhar/diagrams'):
    print(f"  • {f}")
