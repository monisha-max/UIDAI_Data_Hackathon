# 🇮🇳 Aadhaar Operational Intelligence Platform

**UIDAI Aadhaar Hackathon 2025**

Detecting Redistribution Patterns & Optimizing Biometric Operations

---

## 🎯 Executive Summary

Two complementary modules analyzing **4.9M+ Aadhaar records**:

| Module | Purpose | Key Output |
|--------|---------|------------|
| **Mobility Signal Index (MSI)** | Detect redistribution-like patterns | 276 events, 14 wave patterns |
| **Biometric Load Balancer** | Forecast demand & optimize load | 84 overloaded pincodes, 30% reduction |

### Key Metrics

- **Total Records Analyzed:** 4,938,837
- **Districts Covered:** 1,071
- **Pincodes Analyzed:** 31,198
- **Redistribution Events:** 276 (MSI > 0.3)
- **Wave Patterns:** 14
- **Peak MSI Score:** 0.9337
- **Overloaded Pincodes:** 84
- **Max Load Reduction:** 30% (51,551 updates)
- **Interactive Dashboards:** 11

---

## 🎯 Problem Statement

> "Identify meaningful patterns, trends, anomalies, or predictive indicators in Aadhaar enrollment and update data that can support informed decision-making."

### Our Approach

We took a **relational approach** — examining how activity in one district correlates with neighboring districts over time.

**Key Insight:** When District A shows declining activity while neighbors show increasing activity, this signals possible population redistribution.

---

## 🔧 Technical Implementation

### Module 1: Mobility Signal Index (MSI)

**Core Formula:**
```
MSI = inverse_correlation × (1 + spatial_spread) × normalized_z_score
```

**Components:**
- **inverse_corr** = negative correlation between location and neighbors
- **spatial_spread** = proportion of neighbors moving opposite direction
- **z_magnitude** = anomaly score of the change

**Process:**
1. Aggregate data weekly by district
2. Build neighbor graph (districts in same state)
3. Calculate week-over-week changes
4. Compute MSI for each location-time pair
5. Detect wave patterns (3+ districts, 3+ weeks)

### Module 2: Biometric Load Balancer

**Core Formula:**
```
LoadScore = (load_percentile × 0.7) + (spike_risk_percentile × 0.3)
SpareCapacity = 1 - load_percentile
```

**Process:**
1. Forecast next month's load using trend analysis
2. Calculate LoadScore for each pincode
3. Flag top 10% as overloaded
4. Find alternatives in same district with spare capacity
5. Simulate 10-30% redirection scenarios

---

## 🏆 Key Results

### MSI Findings

| Metric | Value |
|--------|-------|
| Redistribution Events | 276 |
| Top Hotspot | Koraput, Orissa (0.680) |
| Wave Patterns | 14 |
| Most Stable State | Kerala (-0.248) |

### Load Balancer Findings

| Metric | Value |
|--------|-------|
| Critical Pincodes | 84 |
| Top Overloaded | Ratlam 457001 (0.903) |
| Avg Alternatives | 4.5 per pincode |
| Max Load Reduction | 30% |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### Quick Start

```bash
# Clone repository
git clone https://github.com/monisha-max/UIDAI_Data_Hackathon.git
cd UIDAI_Data_Hackathon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run MSI Analysis
python mobility_signal_index_analysis.py

# Run Load Balancer
python biometric_load_balancer.py
```

---

## 📁 Project Structure

```
UIDAI_Data_Hackathon/
├── README.md
├── requirements.txt
├── mobility_signal_index_analysis.py    # MSI module
├── biometric_load_balancer.py           # Load balancer module
├── MSI_Analysis_Hackathon.ipynb         # Jupyter notebook
├── api_data_aadhar_enrolment/           # Enrollment data
├── api_data_aadhar_demographic/         # Demographic data
├── api_data_aadhar_biometric/           # Biometric data
├── msi_visualizations/                  # 6 MSI dashboards
└── load_balancer_visualizations/        # 5 Load balancer dashboards
```

---

## 📊 Interactive Dashboards

### MSI Visualizations (6)
- `summary_dashboard.html` - Executive summary
- `msi_heatmap.html` - State × Time heatmap
- `hotspot_ranking.html` - Top redistribution hotspots
- `temporal_analysis.html` - MSI trends over time
- `state_comparison.html` - State-wise comparison
- `wave_visualization.html` - Wave pattern analysis

### Load Balancer Visualizations (5)
- `summary_dashboard.html` - Executive summary
- `load_distribution.html` - Load categories
- `top_overloaded.html` - Top 20 overloaded pincodes
- `simulation.html` - Redirection simulation
- `recommendations_table.html` - Alternative recommendations

---

## 🔄 Reproducibility

```bash
# Run analysis
python mobility_signal_index_analysis.py    # ~2-3 minutes
python biometric_load_balancer.py           # ~1-2 minutes

# Check outputs
ls msi_visualizations/           # 6 HTML files
ls load_balancer_visualizations/ # 5 HTML files
```

### Dependencies
```
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scipy>=1.11.0
```

---

## 🇮🇳 Theme

All visualizations use the **Indian Tricolor** theme:
- 🟠 Saffron (#FF9933)
- ⚪ White (#FFFFFF)
- 🟢 Green (#138808)

---

**Built for UIDAI Aadhaar Hackathon 2025**

*Analysis conducted on publicly available aggregated Aadhaar data. No individual-level information was accessed.*
