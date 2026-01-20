"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MOBILITY SIGNAL INDEX (MSI) ANALYSIS                       ║
║          Detecting Redistribution Patterns in Aadhaar Data                   ║
║                                                                              ║
║  🇮🇳 Theme: Indian Tricolor (Saffron • White • Green)                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Problem Statement:
-----------------
Detect "redistribution-like patterns" in Aadhaar enrollment and update data.
When one area shows declining activity while neighboring areas show increasing 
activity in the same time window, this may indicate population redistribution.

Key Metrics:
- Mobility Signal Index (MSI): Measures inverse correlation between an area and its neighbors
- Wave Propagation Score: Detects spatial spread patterns over time
- Hotspot Ranking: Identifies areas with strongest redistribution signals

Careful Interpretation:
- We cannot prove "people moved"
- We detect statistical patterns consistent with redistribution
- Local camp effects are filtered out (single pincode spikes)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Visualization imports
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Statistical imports
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from collections import defaultdict
from datetime import datetime, timedelta
import json

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 INDIAN TRICOLOR THEME CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

INDIA_COLORS = {
    'saffron': '#FF9933',           # Kesari - Courage & Sacrifice
    'saffron_light': '#FFB366',
    'saffron_dark': '#E67300',
    'white': '#FFFFFF',              # Peace & Truth
    'white_off': '#F8F9FA',
    'green': '#138808',              # Fertility & Prosperity
    'green_light': '#1DB954',
    'green_dark': '#0D5C06',
    'navy': '#000080',               # Ashoka Chakra blue
    'chakra_blue': '#0000CD',
    'background': '#0A0A1A',         # Dark background for contrast
    'text': '#F0F0F0',
    'grid': '#2A2A4A'
}

# Plotly template with Indian theme
def create_india_template():
    """Create a custom Plotly template with Indian tricolor theme"""
    return go.layout.Template(
        layout=go.Layout(
            paper_bgcolor=INDIA_COLORS['background'],
            plot_bgcolor=INDIA_COLORS['background'],
            font=dict(
                family="Segoe UI, Arial, sans-serif",
                color=INDIA_COLORS['text'],
                size=12
            ),
            title=dict(
                font=dict(size=24, color=INDIA_COLORS['saffron']),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                gridcolor=INDIA_COLORS['grid'],
                linecolor=INDIA_COLORS['grid'],
                zerolinecolor=INDIA_COLORS['grid']
            ),
            yaxis=dict(
                gridcolor=INDIA_COLORS['grid'],
                linecolor=INDIA_COLORS['grid'],
                zerolinecolor=INDIA_COLORS['grid']
            ),
            colorway=[
                INDIA_COLORS['saffron'],
                INDIA_COLORS['green'],
                INDIA_COLORS['chakra_blue'],
                INDIA_COLORS['saffron_light'],
                INDIA_COLORS['green_light']
            ]
        )
    )

INDIA_TEMPLATE = create_india_template()

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 DATA LOADING & PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

class AadhaarDataLoader:
    """Load and preprocess Aadhaar datasets"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.enrolment_df = None
        self.demographic_df = None
        self.biometric_df = None
        
    def load_all_data(self):
        """Load all three datasets"""
        print("🔄 Loading Aadhaar datasets...")
        
        # Load Enrolment Data
        enrolment_files = sorted(self.base_path.glob("api_data_aadhar_enrolment/*.csv"))
        self.enrolment_df = pd.concat([pd.read_csv(f) for f in enrolment_files], ignore_index=True)
        print(f"   ✓ Enrolment: {len(self.enrolment_df):,} records")
        
        # Load Demographic Data
        demographic_files = sorted(self.base_path.glob("api_data_aadhar_demographic/*.csv"))
        self.demographic_df = pd.concat([pd.read_csv(f) for f in demographic_files], ignore_index=True)
        print(f"   ✓ Demographic: {len(self.demographic_df):,} records")
        
        # Load Biometric Data
        biometric_files = sorted(self.base_path.glob("api_data_aadhar_biometric/*.csv"))
        self.biometric_df = pd.concat([pd.read_csv(f) for f in biometric_files], ignore_index=True)
        print(f"   ✓ Biometric: {len(self.biometric_df):,} records")
        
        self._preprocess_all()
        return self
    
    def _preprocess_all(self):
        """Preprocess all datasets"""
        print("🔧 Preprocessing data...")
        
        for df_name in ['enrolment_df', 'demographic_df', 'biometric_df']:
            df = getattr(self, df_name)
            
            # Parse dates
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            
            # Clean state names
            df['state'] = df['state'].str.strip().str.title()
            df['district'] = df['district'].str.strip().str.title()
            
            # Extract pincode prefix (first 3 digits - geographic region proxy)
            df['pincode'] = df['pincode'].astype(str).str.zfill(6)
            df['pin_region'] = df['pincode'].str[:3]  # Postal region
            df['pin_subregion'] = df['pincode'].str[:4]  # Sub-region
            
            # Create week and month columns
            df['week'] = df['date'].dt.isocalendar().week
            df['month'] = df['date'].dt.month
            df['year_week'] = df['date'].dt.strftime('%Y-W%V')
            df['year_month'] = df['date'].dt.strftime('%Y-%m')
            
            setattr(self, df_name, df)
        
        # Create total activity column for enrolment
        self.enrolment_df['total_enrolment'] = (
            self.enrolment_df['age_0_5'] + 
            self.enrolment_df['age_5_17'] + 
            self.enrolment_df['age_18_greater']
        )
        
        # Create total activity columns for updates
        self.demographic_df['total_demo_updates'] = (
            self.demographic_df['demo_age_5_17'] + 
            self.demographic_df['demo_age_17_']
        )
        
        self.biometric_df['total_bio_updates'] = (
            self.biometric_df['bio_age_5_17'] + 
            self.biometric_df['bio_age_17_']
        )
        
        print("   ✓ Preprocessing complete!")
        
    def get_combined_activity(self):
        """Combine all datasets into unified activity measure"""
        print("📊 Creating combined activity dataset...")
        
        # Aggregate by date, state, district, pincode
        enrol_agg = self.enrolment_df.groupby(
            ['date', 'state', 'district', 'pincode', 'pin_region', 'year_week']
        )['total_enrolment'].sum().reset_index()
        enrol_agg.columns = ['date', 'state', 'district', 'pincode', 'pin_region', 'year_week', 'enrolment']
        
        demo_agg = self.demographic_df.groupby(
            ['date', 'state', 'district', 'pincode', 'pin_region', 'year_week']
        )['total_demo_updates'].sum().reset_index()
        demo_agg.columns = ['date', 'state', 'district', 'pincode', 'pin_region', 'year_week', 'demo_updates']
        
        bio_agg = self.biometric_df.groupby(
            ['date', 'state', 'district', 'pincode', 'pin_region', 'year_week']
        )['total_bio_updates'].sum().reset_index()
        bio_agg.columns = ['date', 'state', 'district', 'pincode', 'pin_region', 'year_week', 'bio_updates']
        
        # Merge all
        combined = enrol_agg.merge(
            demo_agg, on=['date', 'state', 'district', 'pincode', 'pin_region', 'year_week'], how='outer'
        ).merge(
            bio_agg, on=['date', 'state', 'district', 'pincode', 'pin_region', 'year_week'], how='outer'
        ).fillna(0)
        
        # Total activity score
        combined['total_activity'] = (
            combined['enrolment'] + 
            combined['demo_updates'] + 
            combined['bio_updates']
        )
        
        print(f"   ✓ Combined dataset: {len(combined):,} records")
        return combined


# ═══════════════════════════════════════════════════════════════════════════════
# 🧮 MOBILITY SIGNAL INDEX (MSI) ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class MobilitySignalIndexEngine:
    """
    Core MSI computation engine.
    
    The MSI detects redistribution-like patterns by measuring:
    1. Inverse correlation: Area A drops while neighbors rise
    2. Spatial propagation: Changes spread geographically over time
    3. Local vs distributed: Filter single-pincode operational effects
    """
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.district_neighbors = {}
        self.pincode_neighbors = {}
        self.msi_results = None
        self.wave_patterns = None
        
    def build_neighbor_graph(self, level='district'):
        """
        Build geographic neighbor relationships.
        
        Since we don't have coordinates, we use:
        1. Same state = potential neighbors
        2. Pincode prefix similarity = geographic proximity
        3. Co-occurrence patterns in data
        """
        print(f"🗺️  Building {level}-level neighbor graph...")
        
        if level == 'district':
            # Districts in same state are neighbors
            state_districts = self.data.groupby('state')['district'].unique().to_dict()
            
            for state, districts in state_districts.items():
                districts = list(districts)
                for i, d1 in enumerate(districts):
                    key = f"{state}|{d1}"
                    self.district_neighbors[key] = [
                        f"{state}|{d2}" for d2 in districts if d2 != d1
                    ]
            
            print(f"   ✓ {len(self.district_neighbors)} district nodes")
            
        elif level == 'pincode':
            # Pincodes with same 4-digit prefix are neighbors
            pin_regions = self.data.groupby('pin_region')['pincode'].unique().to_dict()
            
            for region, pincodes in pin_regions.items():
                pincodes = list(set(pincodes))
                for pin in pincodes:
                    # Neighbors = same 4-digit prefix OR adjacent 3-digit prefix
                    same_region = [p for p in pincodes if p != pin and p[:4] == pin[:4]]
                    adjacent_region = [p for p in pincodes if p != pin and abs(int(p[:3]) - int(pin[:3])) <= 1]
                    self.pincode_neighbors[pin] = list(set(same_region + adjacent_region))
            
            print(f"   ✓ {len(self.pincode_neighbors)} pincode nodes")
    
    def compute_temporal_changes(self, time_col='year_week', value_col='total_activity', 
                                  geo_col='district', state_col='state'):
        """Compute week-over-week changes for each geographic unit"""
        print("📈 Computing temporal changes...")
        
        # Aggregate by time and geography
        geo_key = f"{state_col}|{geo_col}" if state_col else geo_col
        
        agg = self.data.groupby([time_col, state_col, geo_col])[value_col].sum().reset_index()
        agg['geo_key'] = agg[state_col] + '|' + agg[geo_col]
        
        # Pivot to get time series per location
        pivot = agg.pivot(index=time_col, columns='geo_key', values=value_col).fillna(0)
        
        # Compute percentage changes
        pct_change = pivot.pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
        
        # Compute rolling z-scores (anomaly detection)
        rolling_mean = pivot.rolling(window=4, min_periods=1).mean()
        rolling_std = pivot.rolling(window=4, min_periods=1).std().replace(0, 1)
        z_scores = (pivot - rolling_mean) / rolling_std
        
        self.temporal_pivot = pivot
        self.temporal_changes = pct_change
        self.temporal_zscores = z_scores
        
        print(f"   ✓ {len(pivot.columns)} locations × {len(pivot)} time periods")
        return pct_change
    
    def compute_msi(self, window_size=3):
        """
        Compute Mobility Signal Index for each location and time.
        
        MSI Formula:
        MSI(A, t) = -corr(Δ_activity_A, avg(Δ_activity_neighbors)) × spatial_spread_factor
        
        High MSI indicates:
        - Area A decreasing while neighbors increasing (or vice versa)
        - Changes spreading spatially (not isolated)
        """
        print("🧮 Computing Mobility Signal Index...")
        
        msi_records = []
        
        locations = list(self.temporal_changes.columns)
        time_periods = list(self.temporal_changes.index)
        
        for loc in locations:
            # Get neighbors
            neighbors = self.district_neighbors.get(loc, [])
            valid_neighbors = [n for n in neighbors if n in locations]
            
            if len(valid_neighbors) < 2:
                continue
            
            for t_idx in range(window_size, len(time_periods)):
                t = time_periods[t_idx]
                t_window = time_periods[t_idx - window_size:t_idx + 1]
                
                # Get changes for this location
                loc_changes = self.temporal_changes.loc[t_window, loc].values
                
                # Get average neighbor changes
                neighbor_changes = self.temporal_changes.loc[t_window, valid_neighbors].mean(axis=1).values
                
                # Compute inverse correlation (MSI core)
                if len(loc_changes) > 2 and np.std(loc_changes) > 0 and np.std(neighbor_changes) > 0:
                    correlation = np.corrcoef(loc_changes, neighbor_changes)[0, 1]
                    inverse_corr = -correlation  # Negative correlation = redistribution signal
                else:
                    inverse_corr = 0
                
                # Spatial spread factor: how many neighbors are changing in opposite direction?
                loc_direction = np.sign(loc_changes[-1])
                neighbor_directions = np.sign(self.temporal_changes.loc[t, valid_neighbors].values)
                opposite_count = np.sum(neighbor_directions != loc_direction) if loc_direction != 0 else 0
                spatial_spread = opposite_count / len(valid_neighbors) if valid_neighbors else 0
                
                # Z-score magnitude (how unusual is this change?)
                z_magnitude = abs(self.temporal_zscores.loc[t, loc]) if t in self.temporal_zscores.index else 0
                
                # Final MSI
                msi = inverse_corr * (1 + spatial_spread) * min(z_magnitude, 3) / 3
                
                # Activity levels
                loc_activity = self.temporal_pivot.loc[t, loc] if t in self.temporal_pivot.index else 0
                neighbor_activity = self.temporal_pivot.loc[t, valid_neighbors].mean() if t in self.temporal_pivot.index else 0
                
                state, district = loc.split('|')
                
                msi_records.append({
                    'time_period': t,
                    'state': state,
                    'district': district,
                    'geo_key': loc,
                    'msi_score': msi,
                    'inverse_correlation': inverse_corr,
                    'spatial_spread': spatial_spread,
                    'z_magnitude': z_magnitude,
                    'activity_change_pct': self.temporal_changes.loc[t, loc] * 100 if t in self.temporal_changes.index else 0,
                    'neighbor_change_pct': self.temporal_changes.loc[t, valid_neighbors].mean() * 100 if t in self.temporal_changes.index else 0,
                    'activity_level': loc_activity,
                    'neighbor_activity': neighbor_activity,
                    'num_neighbors': len(valid_neighbors),
                    'neighbors_opposite': opposite_count
                })
        
        self.msi_results = pd.DataFrame(msi_records)
        print(f"   ✓ Computed {len(self.msi_results):,} MSI measurements")
        return self.msi_results
    
    def detect_wave_patterns(self, min_duration=3, min_spread=3):
        """
        Detect wave-like propagation patterns.
        
        A wave pattern is:
        1. Change starts in one district
        2. Spreads to neighbors in subsequent periods
        3. Shows clear start → peak → fade progression
        """
        print("🌊 Detecting wave propagation patterns...")
        
        waves = []
        
        # Find high-MSI events as potential wave origins
        high_msi = self.msi_results[self.msi_results['msi_score'] > 0.3].copy()
        
        # Group by state and time to find propagating events
        for state in high_msi['state'].unique():
            state_data = high_msi[high_msi['state'] == state].copy()
            state_data = state_data.sort_values('time_period')
            
            # Track which districts show activity over time
            time_periods = sorted(state_data['time_period'].unique())
            
            for start_idx, start_time in enumerate(time_periods[:-min_duration]):
                # Get initial districts with high MSI
                initial_districts = set(
                    state_data[state_data['time_period'] == start_time]['district'].unique()
                )
                
                if len(initial_districts) == 0:
                    continue
                
                # Track spread over subsequent periods
                affected_districts = {start_time: initial_districts}
                cumulative = initial_districts.copy()
                
                for t in time_periods[start_idx + 1:start_idx + min_duration + 2]:
                    if t in state_data['time_period'].values:
                        new_districts = set(
                            state_data[state_data['time_period'] == t]['district'].unique()
                        )
                        new_spread = new_districts - cumulative
                        affected_districts[t] = new_districts
                        cumulative = cumulative | new_districts
                
                # Check if this is a wave (spreading pattern)
                district_counts = [len(d) for d in affected_districts.values()]
                
                if len(cumulative) >= min_spread and max(district_counts) > district_counts[0]:
                    # Found a potential wave
                    peak_time = list(affected_districts.keys())[np.argmax(district_counts)]
                    
                    waves.append({
                        'state': state,
                        'start_time': start_time,
                        'peak_time': peak_time,
                        'duration': len(affected_districts),
                        'origin_districts': list(initial_districts),
                        'total_affected': len(cumulative),
                        'all_districts': list(cumulative),
                        'spread_sequence': {str(k): list(v) for k, v in affected_districts.items()},
                        'peak_count': max(district_counts),
                        'wave_score': len(cumulative) * max(district_counts) / (len(initial_districts) + 1)
                    })
        
        self.wave_patterns = sorted(waves, key=lambda x: x['wave_score'], reverse=True)
        print(f"   ✓ Detected {len(self.wave_patterns)} wave patterns")
        return self.wave_patterns
    
    def get_redistribution_hotspots(self, top_n=20):
        """Get ranked list of potential redistribution hotspots"""
        print("🎯 Ranking redistribution hotspots...")
        
        # Aggregate MSI by location
        hotspots = self.msi_results.groupby(['state', 'district', 'geo_key']).agg({
            'msi_score': ['mean', 'max', 'std', 'count'],
            'inverse_correlation': 'mean',
            'spatial_spread': 'mean',
            'z_magnitude': 'mean',
            'activity_change_pct': 'mean',
            'activity_level': 'mean'
        }).reset_index()
        
        hotspots.columns = [
            'state', 'district', 'geo_key',
            'msi_mean', 'msi_max', 'msi_std', 'event_count',
            'avg_inverse_corr', 'avg_spatial_spread', 'avg_z_magnitude',
            'avg_activity_change', 'avg_activity_level'
        ]
        
        # Composite hotspot score
        hotspots['hotspot_score'] = (
            hotspots['msi_mean'] * 0.3 +
            hotspots['msi_max'] * 0.3 +
            hotspots['avg_spatial_spread'] * 0.2 +
            np.log1p(hotspots['event_count']) * 0.1 +
            hotspots['avg_z_magnitude'] / 3 * 0.1
        )
        
        hotspots = hotspots.sort_values('hotspot_score', ascending=False)
        
        print(f"   ✓ Top hotspot: {hotspots.iloc[0]['district']}, {hotspots.iloc[0]['state']}")
        return hotspots.head(top_n)


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 VISUALIZATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class MSIVisualizer:
    """Create stunning Indian tricolor themed visualizations"""
    
    def __init__(self, msi_engine: MobilitySignalIndexEngine):
        self.engine = msi_engine
        self.figures = {}
        
    def create_msi_heatmap(self):
        """Create temporal heatmap of MSI scores by state"""
        print("📊 Creating MSI heatmap...")
        
        # Aggregate by state and time
        heatmap_data = self.engine.msi_results.groupby(
            ['time_period', 'state']
        )['msi_score'].mean().reset_index()
        
        pivot = heatmap_data.pivot(
            index='state', 
            columns='time_period', 
            values='msi_score'
        ).fillna(0)
        
        # Sort states by total MSI
        state_order = pivot.sum(axis=1).sort_values(ascending=True).index
        pivot = pivot.loc[state_order]
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=[
                [0, INDIA_COLORS['green_dark']],
                [0.3, INDIA_COLORS['green']],
                [0.5, INDIA_COLORS['white']],
                [0.7, INDIA_COLORS['saffron']],
                [1, INDIA_COLORS['saffron_dark']]
            ],
    colorbar=dict(
        title=dict(text="MSI Score", font=dict(color=INDIA_COLORS['text'])),
        tickfont=dict(color=INDIA_COLORS['text'])
    )
        ))
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title=dict(
                text="🇮🇳 Mobility Signal Index by State & Time",
                font=dict(size=22, color=INDIA_COLORS['saffron'])
            ),
            xaxis_title="Time Period",
            yaxis_title="State",
            height=800
        )
        
        self.figures['msi_heatmap'] = fig
        return fig
    
    def create_hotspot_ranking(self, top_n=15):
        """Create horizontal bar chart of top redistribution hotspots"""
        print("📊 Creating hotspot ranking chart...")
        
        hotspots = self.engine.get_redistribution_hotspots(top_n)
        
        fig = go.Figure()
        
        # Create gradient colors based on score
        colors = [
            f"rgba({int(255*0.6 + 255*0.4*i/len(hotspots))}, " + 
            f"{int(153*0.6 - 100*i/len(hotspots))}, " +
            f"{int(51)}, 0.9)"
            for i in range(len(hotspots))
        ]
        
        fig.add_trace(go.Bar(
            y=[f"{row['district']}, {row['state']}" for _, row in hotspots.iterrows()],
            x=hotspots['hotspot_score'],
            orientation='h',
            marker=dict(
                color=hotspots['hotspot_score'],
                colorscale=[
                    [0, INDIA_COLORS['green']],
                    [0.5, INDIA_COLORS['white']],
                    [1, INDIA_COLORS['saffron']]
                ],
                line=dict(color=INDIA_COLORS['saffron_dark'], width=1)
            ),
            text=[f"Score: {s:.3f}" for s in hotspots['hotspot_score']],
            textposition='inside',
            textfont=dict(color=INDIA_COLORS['background'], size=11, family='Arial Black')
        ))
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title=dict(
                text="🎯 Top Redistribution Hotspots (Ranked by MSI)",
                font=dict(size=22, color=INDIA_COLORS['saffron'])
            ),
            xaxis_title="Hotspot Score",
            yaxis_title="",
            height=600,
            showlegend=False,
            yaxis=dict(autorange="reversed")
        )
        
        self.figures['hotspot_ranking'] = fig
        return fig
    
    def create_wave_visualization(self, wave_idx=0):
        """Create visualization of wave propagation pattern"""
        print("📊 Creating wave propagation visualization...")
        
        if not self.engine.wave_patterns:
            print("   ⚠️ No wave patterns detected")
            return None
        
        wave = self.engine.wave_patterns[wave_idx]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                f"Wave Origin: {wave['state']}",
                "District Spread Over Time",
                "Activity Levels During Wave",
                "Wave Intensity Map"
            ),
            specs=[
                [{"type": "indicator"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "heatmap"}]
            ]
        )
        
        # Indicator for wave score
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=wave['wave_score'],
                title={'text': "Wave Score", 'font': {'color': INDIA_COLORS['text']}},
                gauge={
                    'axis': {'range': [0, max(wave['wave_score'] * 1.5, 10)]},
                    'bar': {'color': INDIA_COLORS['saffron']},
                    'bgcolor': INDIA_COLORS['background'],
                    'borderwidth': 2,
                    'bordercolor': INDIA_COLORS['saffron'],
                    'steps': [
                        {'range': [0, wave['wave_score']/3], 'color': INDIA_COLORS['green']},
                        {'range': [wave['wave_score']/3, wave['wave_score']*2/3], 'color': INDIA_COLORS['white']},
                        {'range': [wave['wave_score']*2/3, wave['wave_score']*1.5], 'color': INDIA_COLORS['saffron']}
                    ]
                },
                number={'font': {'color': INDIA_COLORS['saffron']}}
            ),
            row=1, col=1
        )
        
        # Bar chart of districts over time
        spread_data = wave['spread_sequence']
        times = list(spread_data.keys())
        counts = [len(spread_data[t]) for t in times]
        
        fig.add_trace(
            go.Bar(
                x=times,
                y=counts,
                marker=dict(
                    color=counts,
                    colorscale=[[0, INDIA_COLORS['green']], [1, INDIA_COLORS['saffron']]]
                ),
                text=counts,
                textposition='outside',
                textfont=dict(color=INDIA_COLORS['text'])
            ),
            row=1, col=2
        )
        
        # Timeline of spread
        for i, (t, districts) in enumerate(spread_data.items()):
            fig.add_trace(
                go.Scatter(
                    x=[t] * len(districts),
                    y=list(range(len(districts))),
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color=INDIA_COLORS['saffron'] if i == 0 else INDIA_COLORS['green'],
                        symbol='circle'
                    ),
                    text=districts,
                    textposition='middle right',
                    textfont=dict(size=10, color=INDIA_COLORS['text']),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title=dict(
                text=f"🌊 Wave Pattern Analysis: {wave['state']} ({wave['start_time']} → {wave['peak_time']})",
                font=dict(size=20, color=INDIA_COLORS['saffron'])
            ),
            height=700,
            showlegend=False
        )
        
        self.figures['wave_visualization'] = fig
        return fig
    
    def create_temporal_analysis(self):
        """Create temporal analysis of MSI trends"""
        print("📊 Creating temporal analysis...")
        
        # Aggregate MSI over time
        temporal = self.engine.msi_results.groupby('time_period').agg({
            'msi_score': ['mean', 'std', 'max'],
            'activity_level': 'sum',
            'geo_key': 'nunique'
        }).reset_index()
        temporal.columns = ['time_period', 'msi_mean', 'msi_std', 'msi_max', 'total_activity', 'active_locations']
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("MSI Trend Over Time", "Activity Volume & Active Locations"),
            shared_xaxes=True,
            vertical_spacing=0.1
        )
        
        # MSI trend with confidence band
        fig.add_trace(
            go.Scatter(
                x=temporal['time_period'],
                y=temporal['msi_mean'] + temporal['msi_std'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=temporal['time_period'],
                y=temporal['msi_mean'] - temporal['msi_std'],
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor=f"rgba(255, 153, 51, 0.2)",
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=temporal['time_period'],
                y=temporal['msi_mean'],
                mode='lines+markers',
                name='Mean MSI',
                line=dict(color=INDIA_COLORS['saffron'], width=3),
                marker=dict(size=8, color=INDIA_COLORS['saffron'])
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=temporal['time_period'],
                y=temporal['msi_max'],
                mode='lines+markers',
                name='Max MSI',
                line=dict(color=INDIA_COLORS['green'], width=2, dash='dash'),
                marker=dict(size=6, color=INDIA_COLORS['green'])
            ),
            row=1, col=1
        )
        
        # Activity volume
        fig.add_trace(
            go.Bar(
                x=temporal['time_period'],
                y=temporal['total_activity'],
                name='Total Activity',
                marker=dict(color=INDIA_COLORS['green'], opacity=0.7)
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=temporal['time_period'],
                y=temporal['active_locations'] * temporal['total_activity'].max() / temporal['active_locations'].max(),
                mode='lines+markers',
                name='Active Locations (scaled)',
                line=dict(color=INDIA_COLORS['saffron'], width=2),
                marker=dict(size=6),
                yaxis='y3'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title=dict(
                text="📈 Temporal MSI Analysis: When Did Redistribution Patterns Occur?",
                font=dict(size=20, color=INDIA_COLORS['saffron'])
            ),
            height=600,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            )
        )
        
        self.figures['temporal_analysis'] = fig
        return fig
    
    def create_state_comparison(self):
        """Create state-level MSI comparison"""
        print("📊 Creating state comparison...")
        
        state_stats = self.engine.msi_results.groupby('state').agg({
            'msi_score': ['mean', 'max', 'std'],
            'activity_level': 'mean',
            'spatial_spread': 'mean',
            'district': 'nunique'
        }).reset_index()
        state_stats.columns = ['state', 'msi_mean', 'msi_max', 'msi_std', 'avg_activity', 'avg_spread', 'num_districts']
        state_stats = state_stats.sort_values('msi_mean', ascending=True)
        
        fig = go.Figure()
        
        # Horizontal bar for mean MSI
        fig.add_trace(go.Bar(
            y=state_stats['state'],
            x=state_stats['msi_mean'],
            orientation='h',
            name='Mean MSI',
            marker=dict(
                color=state_stats['msi_mean'],
                colorscale=[
                    [0, INDIA_COLORS['green']],
                    [0.5, INDIA_COLORS['white']],
                    [1, INDIA_COLORS['saffron']]
                ]
            ),
            text=[f"{v:.3f}" for v in state_stats['msi_mean']],
            textposition='outside',
            textfont=dict(color=INDIA_COLORS['text'], size=10)
        ))
        
        # Error bars for variability
        fig.add_trace(go.Scatter(
            y=state_stats['state'],
            x=state_stats['msi_max'],
            mode='markers',
            name='Max MSI',
            marker=dict(
                size=10,
                color=INDIA_COLORS['chakra_blue'],
                symbol='diamond'
            )
        ))
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title=dict(
                text="🗺️ State-wise Mobility Signal Index Comparison",
                font=dict(size=20, color=INDIA_COLORS['saffron'])
            ),
            xaxis_title="MSI Score",
            yaxis_title="",
            height=900,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            barmode='overlay'
        )
        
        self.figures['state_comparison'] = fig
        return fig
    
    def create_summary_dashboard(self):
        """Create executive summary dashboard"""
        print("📊 Creating summary dashboard...")
        
        msi = self.engine.msi_results
        hotspots = self.engine.get_redistribution_hotspots(10)
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                "🎯 Redistribution Events (MSI > 0.3)",
                "🗺️ Locations Analyzed",
                "📈 Max MSI Score",
                "🏆 States with Most Redistribution Events",
                "📊 MSI Distribution",
                "🌐 Spatial Spread Distribution"
            ),
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                [{"type": "bar"}, {"type": "histogram"}, {"type": "histogram"}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Indicators - focus on POSITIVE MSI (redistribution signals)
        high_msi_events = msi[msi['msi_score'] > 0.3]
        high_msi_count = len(high_msi_events)
        unique_locations = msi['geo_key'].nunique()
        max_msi = msi['msi_score'].max()  # Show max instead of avg
        
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=high_msi_count,
                title={'text': "High-MSI Events", 'font': {'color': INDIA_COLORS['text'], 'size': 14}},
                number={'font': {'color': INDIA_COLORS['saffron'], 'size': 36}},
                delta={'reference': high_msi_count * 0.8, 'relative': True}
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=unique_locations,
                title={'text': "Locations Analyzed", 'font': {'color': INDIA_COLORS['text'], 'size': 14}},
                number={'font': {'color': INDIA_COLORS['green'], 'size': 36}}
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=max_msi,
                title={'text': "Peak MSI Score", 'font': {'color': INDIA_COLORS['text'], 'size': 14}},
                number={'font': {'color': INDIA_COLORS['saffron'], 'size': 36}, 'valueformat': '.4f'}
            ),
            row=1, col=3
        )
        
        # Top states BY REDISTRIBUTION EVENT COUNT (not mean MSI)
        state_event_counts = high_msi_events.groupby('state').size().sort_values(ascending=False).head(10)
        fig.add_trace(
            go.Bar(
                x=state_event_counts.index,
                y=state_event_counts.values,
                marker=dict(
                    color=state_event_counts.values,
                    colorscale=[[0, INDIA_COLORS['green']], [1, INDIA_COLORS['saffron']]]
                ),
                text=state_event_counts.values,
                textposition='outside',
                textfont=dict(color=INDIA_COLORS['text'], size=10)
            ),
            row=2, col=1
        )
        
        # MSI distribution
        fig.add_trace(
            go.Histogram(
                x=msi['msi_score'],
                nbinsx=50,
                marker=dict(color=INDIA_COLORS['saffron'], line=dict(color=INDIA_COLORS['saffron_dark'], width=1))
            ),
            row=2, col=2
        )
        
        # Spatial spread distribution
        fig.add_trace(
            go.Histogram(
                x=msi['spatial_spread'],
                nbinsx=30,
                marker=dict(color=INDIA_COLORS['green'], line=dict(color=INDIA_COLORS['green_dark'], width=1))
            ),
            row=2, col=3
        )
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title=dict(
                text="🇮🇳 MOBILITY SIGNAL INDEX - EXECUTIVE SUMMARY",
                font=dict(size=24, color=INDIA_COLORS['saffron'])
            ),
            height=700,
            showlegend=False
        )
        
        self.figures['summary_dashboard'] = fig
        return fig
    
    def save_all_figures(self, output_dir: str = "msi_visualizations"):
        """Save all figures as HTML files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n💾 Saving visualizations to {output_dir}/")
        
        for name, fig in self.figures.items():
            if fig is not None:
                filepath = output_path / f"{name}.html"
                fig.write_html(str(filepath))
                print(f"   ✓ Saved {name}.html")
        
        print(f"\n✅ All visualizations saved!")
        return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def run_msi_analysis(data_path: str = "."):
    """Run complete MSI analysis pipeline"""
    
    print("=" * 80)
    print("🇮🇳 MOBILITY SIGNAL INDEX (MSI) ANALYSIS")
    print("   Detecting Redistribution Patterns in Aadhaar Data")
    print("=" * 80)
    print()
    
    # 1. Load Data
    loader = AadhaarDataLoader(data_path)
    loader.load_all_data()
    combined_data = loader.get_combined_activity()
    
    print()
    
    # 2. Initialize MSI Engine
    engine = MobilitySignalIndexEngine(combined_data)
    
    # 3. Build neighbor relationships
    engine.build_neighbor_graph(level='district')
    
    # 4. Compute temporal changes
    engine.compute_temporal_changes()
    
    # 5. Compute MSI
    engine.compute_msi(window_size=3)
    
    # 6. Detect wave patterns
    engine.detect_wave_patterns(min_duration=3, min_spread=3)
    
    print()
    
    # 7. Create visualizations
    viz = MSIVisualizer(engine)
    
    viz.create_summary_dashboard()
    viz.create_msi_heatmap()
    viz.create_hotspot_ranking()
    viz.create_temporal_analysis()
    viz.create_state_comparison()
    
    if engine.wave_patterns:
        viz.create_wave_visualization(wave_idx=0)
    
    # 8. Save outputs
    viz.save_all_figures()
    
    # 9. Print key findings
    print("\n" + "=" * 80)
    print("📋 KEY FINDINGS")
    print("=" * 80)
    
    hotspots = engine.get_redistribution_hotspots(10)
    print("\n🎯 TOP 10 REDISTRIBUTION HOTSPOTS:")
    print("-" * 50)
    for i, (_, row) in enumerate(hotspots.iterrows(), 1):
        print(f"   {i:2d}. {row['district']}, {row['state']}")
        print(f"       MSI: {row['msi_mean']:.4f} (max: {row['msi_max']:.4f})")
        print(f"       Events: {row['event_count']:.0f} | Spatial Spread: {row['avg_spatial_spread']:.2%}")
    
    if engine.wave_patterns:
        print(f"\n🌊 WAVE PATTERNS DETECTED: {len(engine.wave_patterns)}")
        print("-" * 50)
        for i, wave in enumerate(engine.wave_patterns[:5], 1):
            print(f"   {i}. {wave['state']}: {wave['start_time']} → {wave['peak_time']}")
            print(f"      Origin: {', '.join(wave['origin_districts'][:3])}")
            print(f"      Affected: {wave['total_affected']} districts | Score: {wave['wave_score']:.2f}")
    
    print("\n" + "=" * 80)
    print("✅ Analysis Complete!")
    print("   Open msi_visualizations/*.html to view interactive dashboards")
    print("=" * 80)
    
    return engine, viz


if __name__ == "__main__":
    engine, viz = run_msi_analysis("/Users/lrao/Desktop/aadhar")
