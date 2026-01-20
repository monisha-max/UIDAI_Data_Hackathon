<![CDATA[<div align="center">

# 🇮🇳 Aadhaar Operational Intelligence Platform

### **UIDAI Aadhaar Hackathon 2025**
#### *Detecting Redistribution Patterns & Optimizing Biometric Operations*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

---

**🎯 Two complementary modules analyzing 4.9M+ Aadhaar records to detect redistribution patterns and optimize operational load balancing**

</div>

---

## 📋 Table of Contents

- [Executive Summary](#-executive-summary)
- [Problem Statement](#-problem-statement)
- [Technical Implementation](#-technical-implementation)
- [Key Results](#-key-results)
- [Installation & Setup](#-installation--setup)
- [Project Structure](#-project-structure)
- [Reproducibility](#-reproducibility)

---

## 🎯 Executive Summary

We developed an **Aadhaar Operational Intelligence Platform** comprising two analytical modules:

| Module | Purpose | Key Output |
|--------|---------|------------|
| **Mobility Signal Index (MSI)** | Detect redistribution-like patterns in Aadhaar data | 276 redistribution events, 14 wave patterns |
| **Biometric Load Balancer** | Forecast demand & recommend load balancing strategies | 84 overloaded pincodes, 30% load reduction achievable |

### Quick Stats

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYSIS SUMMARY                              │
├─────────────────────────────────────────────────────────────────┤
│  📊 Total Records Analyzed     │  4,938,837                     │
│  🗺️  Districts Covered          │  1,071                         │
│  📍 Pincodes Analyzed          │  31,198                        │
│  🔍 Redistribution Events      │  276 (MSI > 0.3)               │
│  🌊 Wave Patterns Identified   │  14                            │
│  📈 Peak MSI Score             │  0.9337                        │
│  🔥 Overloaded Pincodes        │  84                            │
│  📉 Max Load Reduction         │  30% (51,551 updates)          │
│  📊 Interactive Dashboards     │  11                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Problem Statement

> **"Identify meaningful patterns, trends, anomalies, or predictive indicators in Aadhaar enrollment and update data that can support informed decision-making."**

### Our Approach

Traditional analysis examines absolute numbers. We took a **relational approach** — examining how activity in one district correlates with activity in neighboring districts over time.

**Key Insight:** When District A shows *declining* activity while neighboring districts show *increasing* activity simultaneously, this creates a statistical signal consistent with population redistribution.

---

## 🔧 Technical Implementation

### Module 1: Mobility Signal Index (MSI) Analysis

#### Core Algorithm

The MSI measures **inverse correlation** between a geographic unit and its neighbors:

```python
# MSI Formula
MSI(location, time) = inverse_corr × (1 + spatial_spread) × min(z_magnitude, 3) / 3

Where:
- inverse_corr = -correlation(Δ_activity_location, avg(Δ_activity_neighbors))
- spatial_spread = count(neighbors_opposite_direction) / total_neighbors
- z_magnitude = |z_score| of activity change
```

#### Key Components

| Component | Description |
|-----------|-------------|
| **Data Aggregation** | Weekly aggregation by district across all datasets |
| **Neighbor Graph** | Districts in same state treated as neighbors |
| **Temporal Changes** | Week-over-week percentage changes with rolling z-scores |
| **Wave Detection** | Patterns spreading across 3+ districts over 3+ weeks |

### Module 2: Biometric Load Balancer

#### Core Algorithm

```python
# Load Score Calculation
LoadScore = (load_percentile × 0.7) + (spike_risk_percentile × 0.3)

# Spare Capacity
SpareCapacity = 1 - load_percentile
```

#### Key Components

| Component | Description |
|-----------|-------------|
| **Load Forecasting** | Trend + seasonality based prediction |
| **Overload Detection** | Top 10% by LoadScore flagged as critical |
| **Alternative Finding** | Same district + adjacent pincodes with spare capacity |
| **Simulation Engine** | Test 10-30% redirection scenarios |

---

## 🏆 Key Results

### MSI Analysis Findings

| Finding | Details |
|---------|---------|
| **Redistribution Events** | 276 events detected (MSI > 0.3) |
| **Top Hotspot** | Koraput, Orissa (Score: 0.680) |
| **Wave Patterns** | 14 distinct spatial propagation patterns |
| **Most Stable State** | Kerala (Mean MSI: -0.248) |

### Load Balancer Findings

| Finding | Details |
|---------|---------|
| **Critical Pincodes** | 84 identified |
| **Top Overloaded** | Ratlam 457001 (Load Score: 0.903) |
| **Avg Alternatives** | 4.5 per overloaded pincode |
| **Max Load Reduction** | 30% (51,551 updates redirectable) |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10+
- pip package manager

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/monisha-max/UIDAI_Data_Hackathon.git
cd UIDAI_Data_Hackathon

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run MSI Analysis
python mobility_signal_index_analysis.py

# 5. Run Load Balancer Analysis
python biometric_load_balancer.py

# 6. View visualizations - open any .html file in browser
```

---

## 📁 Project Structure

```
UIDAI_Data_Hackathon/
│
├── 📄 README.md                           # Documentation
├── 📄 requirements.txt                    # Dependencies
│
├── 🐍 mobility_signal_index_analysis.py   # MSI analysis module
├── 🐍 biometric_load_balancer.py          # Load balancer module
├── 📓 MSI_Analysis_Hackathon.ipynb        # Jupyter notebook
│
├── 📊 api_data_aadhar_enrolment/          # Enrollment data (1M records)
├── 📊 api_data_aadhar_demographic/        # Demographic data (2M records)
├── 📊 api_data_aadhar_biometric/          # Biometric data (1.8M records)
│
├── 📈 msi_visualizations/                 # MSI dashboards (6 HTML files)
│   ├── summary_dashboard.html
│   ├── msi_heatmap.html
│   ├── hotspot_ranking.html
│   ├── temporal_analysis.html
│   ├── state_comparison.html
│   └── wave_visualization.html
│
└── 📈 load_balancer_visualizations/       # Load balancer dashboards (5 HTML files)
    ├── summary_dashboard.html
    ├── load_distribution.html
    ├── top_overloaded.html
    ├── simulation.html
    └── recommendations_table.html
```

---

## 🔄 Reproducibility

### Reproduction Steps

```bash
# Verify environment
python --version  # Should be 3.10+

# Run complete analysis
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

## 📊 Interactive Dashboards

### MSI Analysis (6 dashboards)
| File | Description |
|------|-------------|
| `summary_dashboard.html` | Executive summary |
| `msi_heatmap.html` | State × Time heatmap |
| `hotspot_ranking.html` | Top redistribution hotspots |
| `temporal_analysis.html` | MSI trends over time |
| `state_comparison.html` | State-wise comparison |
| `wave_visualization.html` | Wave pattern analysis |

### Load Balancer (5 dashboards)
| File | Description |
|------|-------------|
| `summary_dashboard.html` | Executive summary |
| `load_distribution.html` | Load categories |
| `top_overloaded.html` | Top 20 overloaded pincodes |
| `simulation.html` | Redirection simulation |
| `recommendations_table.html` | Alternative recommendations |

---

<div align="center">

### 🇮🇳 Built for UIDAI Aadhaar Hackathon 2025 🇮🇳

*Analysis conducted on publicly available aggregated Aadhaar data.*

</div>
]]>