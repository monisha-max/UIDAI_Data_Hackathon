

### UIDAI Data Hackathon 2026

---

## 💥 What We Built

An AI-powered analytics platform that processes **4.9 MILLION Aadhaar records** to:

🔍 **Detect population movement patterns** before they become visible in census data

⚡ **Predict & prevent service bottlenecks** at biometric update centers

📊 **Generate actionable recommendations** for operational optimization

---

## 🚀 Impact Numbers

| 🎯 Metric | 📈 Result |
|-----------|-----------|
| Records Processed | **4,938,837** |
| Districts Analyzed | **1,071** |
| Pincodes Covered | **31,198** |
| Migration Patterns Found | **276** |
| Wave Movements Detected | **14** |
| Overloaded Centers Identified | **84** |
| **Potential Load Reduction** | **30%** |
| **Updates Redistributable** | **51,551** |

---

## 🧠 Modules

### 📡 Module 2a: Mobility Signal Index (MSI)

> *"Where are people moving? When? How fast is it spreading?"*

**What it does:** Detects when one area's activity drops while neighbors increase — a signature pattern of population redistribution.

**Peak Signal Detected:** `0.9337` (extremely strong)

**Top Hotspots Identified:**
| Rank | Location | Signal Strength |
|------|----------|-----------------|
| 🥇 | Koraput, Orissa | 0.680 |
| 🥈 | Dharashiv, Maharashtra | 0.673 |
| 🥉 | Karaikal, Pondicherry | 0.665 |

---

### ⚖️ Module 2b: Biometric Load Balancer

> *"Which centers will be overloaded next month? Where should we redirect people?"*

**What it does:** Forecasts demand at 31,198 pincodes and recommends load balancing strategies.

**Critical Finding:** Chhattisgarh has 6 of top 10 overloaded pincodes!

**Top Overloaded Centers:**
| Pincode | District | Forecast Load |
|---------|----------|---------------|
| 457001 | Ratlam | 12,589 |
| 491995 | Kawardha | 11,957 |
| 492001 | Raipur | 11,061 |

**Solution:** Redirect 30% load → **51,551 fewer bottlenecked updates**

---

## Interactive Dashboards

All dashboards are **fully interactive** with hover details, zoom, and filtering.

**MSI Dashboards:**
- Executive Summary
- State × Time Heatmap
- Hotspot Rankings
- Temporal Trends
- State Comparisons
- Wave Propagation Viewer

**Load Balancer Dashboards:**
- Demand Forecast Summary
- Load Distribution
- Top Overloaded Centers
- Redirection Simulator
- Recommendation Engine

---

## ⚡ Quick Start

```bash
git clone https://github.com/monisha-max/UIDAI_Data_Hackathon.git
cd UIDAI_Data_Hackathon
pip install -r requirements.txt

# Run analysis
python mobility_signal_index_analysis.py
python biometric_load_balancer.py

# Open any HTML file in browser to view dashboards
```

---

## 🛠️ Tech Stack

```
Python 3.10+ | Plotly
```
---

