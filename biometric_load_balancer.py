"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               BIOMETRIC LOAD BALANCER - OPS IMPACT MODULE                    ║
║                                                                              ║
║  🎯 Purpose: Forecast biometric load & recommend redirection strategies      ║
║  🇮🇳 Theme: Indian Tricolor (Saffron • White • Green)                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Features:
1. Forecast next-month biometric updates per district/pincode
2. Calculate LoadScore and SpareCapacity metrics
3. Identify overloaded areas
4. Recommend redirection to nearby alternatives
5. Simulate load balancing scenarios
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 INDIAN TRICOLOR THEME
# ═══════════════════════════════════════════════════════════════════════════════

INDIA_COLORS = {
    'saffron': '#FF9933',
    'saffron_light': '#FFB366',
    'saffron_dark': '#E67300',
    'white': '#FFFFFF',
    'green': '#138808',
    'green_light': '#1DB954',
    'green_dark': '#0D5C06',
    'chakra_blue': '#0000CD',
    'background': '#0A0A1A',
    'text': '#F0F0F0',
    'grid': '#2A2A4A',
    'red': '#DC3545',
    'yellow': '#FFC107'
}

INDIA_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor=INDIA_COLORS['background'],
        plot_bgcolor=INDIA_COLORS['background'],
        font=dict(family="Segoe UI, Arial", color=INDIA_COLORS['text'], size=12),
        title=dict(font=dict(size=22, color=INDIA_COLORS['saffron']), x=0.5),
        xaxis=dict(gridcolor=INDIA_COLORS['grid'], linecolor=INDIA_COLORS['grid']),
        yaxis=dict(gridcolor=INDIA_COLORS['grid'], linecolor=INDIA_COLORS['grid']),
        colorway=[INDIA_COLORS['saffron'], INDIA_COLORS['green'], INDIA_COLORS['chakra_blue']]
    )
)


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 DATA LOADING & PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

class BiometricLoadForecaster:
    """Forecast biometric load and identify overloaded areas"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.bio_df = None
        self.district_forecast = None
        self.pincode_forecast = None
        self.load_scores = None
        
    def load_data(self):
        """Load biometric update data"""
        print("🔄 Loading biometric update data...")
        
        bio_files = sorted(self.base_path.glob("api_data_aadhar_biometric/*.csv"))
        self.bio_df = pd.concat([pd.read_csv(f) for f in bio_files], ignore_index=True)
        
        # Preprocess
        self.bio_df['date'] = pd.to_datetime(self.bio_df['date'], format='%d-%m-%Y')
        self.bio_df['state'] = self.bio_df['state'].str.strip().str.title()
        self.bio_df['district'] = self.bio_df['district'].str.strip().str.title()
        self.bio_df['pincode'] = self.bio_df['pincode'].astype(str).str.zfill(6)
        
        # Total biometric updates
        self.bio_df['total_bio'] = self.bio_df['bio_age_5_17'] + self.bio_df['bio_age_17_']
        
        # Time features
        self.bio_df['year_month'] = self.bio_df['date'].dt.to_period('M')
        self.bio_df['week'] = self.bio_df['date'].dt.isocalendar().week
        self.bio_df['month'] = self.bio_df['date'].dt.month
        self.bio_df['day_of_week'] = self.bio_df['date'].dt.dayofweek
        
        print(f"   ✓ Loaded {len(self.bio_df):,} biometric records")
        print(f"   ✓ Date range: {self.bio_df['date'].min().strftime('%d-%b-%Y')} to {self.bio_df['date'].max().strftime('%d-%b-%Y')}")
        
        return self
    
    def compute_historical_stats(self):
        """Compute historical load statistics by district and pincode"""
        print("📊 Computing historical load statistics...")
        
        # Monthly aggregation by district
        self.district_monthly = self.bio_df.groupby(
            ['year_month', 'state', 'district']
        )['total_bio'].sum().reset_index()
        self.district_monthly['year_month'] = self.district_monthly['year_month'].astype(str)
        
        # Monthly aggregation by pincode
        self.pincode_monthly = self.bio_df.groupby(
            ['year_month', 'state', 'district', 'pincode']
        )['total_bio'].sum().reset_index()
        self.pincode_monthly['year_month'] = self.pincode_monthly['year_month'].astype(str)
        
        print(f"   ✓ {self.district_monthly['district'].nunique()} districts")
        print(f"   ✓ {self.pincode_monthly['pincode'].nunique()} pincodes")
        
        return self
    
    def forecast_next_month(self):
        """Forecast next month's biometric load using trend + seasonality"""
        print("🔮 Forecasting next month's biometric load...")
        
        # === DISTRICT LEVEL FORECAST ===
        district_stats = self.bio_df.groupby(['state', 'district']).agg({
            'total_bio': ['sum', 'mean', 'std', 'count'],
            'date': ['min', 'max']
        }).reset_index()
        district_stats.columns = ['state', 'district', 'total_load', 'daily_mean', 
                                   'daily_std', 'record_count', 'first_date', 'last_date']
        
        # Calculate trend (simple linear)
        district_trends = []
        for (state, district), group in self.bio_df.groupby(['state', 'district']):
            monthly = group.groupby('year_month')['total_bio'].sum().reset_index()
            monthly['month_num'] = range(len(monthly))
            
            if len(monthly) >= 3:
                # Simple trend: difference between last 3 months and first 3 months
                recent_avg = monthly['total_bio'].tail(3).mean()
                early_avg = monthly['total_bio'].head(3).mean()
                trend = (recent_avg - early_avg) / max(early_avg, 1)
            else:
                trend = 0
            
            # Seasonality: use last month as baseline
            last_month_load = monthly['total_bio'].iloc[-1] if len(monthly) > 0 else 0
            
            # Forecast: last month + trend adjustment
            forecast = last_month_load * (1 + trend * 0.3)  # Damped trend
            
            # Spike risk: high std relative to mean indicates volatility
            spike_risk = group['total_bio'].std() / max(group['total_bio'].mean(), 1)
            
            district_trends.append({
                'state': state,
                'district': district,
                'last_month_load': last_month_load,
                'trend': trend,
                'forecast_load': forecast,
                'spike_risk': min(spike_risk, 2),  # Cap at 2
                'historical_mean': group['total_bio'].sum() / max(len(monthly), 1),
                'historical_max': monthly['total_bio'].max() if len(monthly) > 0 else 0
            })
        
        self.district_forecast = pd.DataFrame(district_trends)
        
        # === PINCODE LEVEL FORECAST ===
        pincode_trends = []
        for (state, district, pincode), group in self.bio_df.groupby(['state', 'district', 'pincode']):
            monthly = group.groupby('year_month')['total_bio'].sum().reset_index()
            
            if len(monthly) >= 2:
                recent_avg = monthly['total_bio'].tail(2).mean()
                early_avg = monthly['total_bio'].head(2).mean()
                trend = (recent_avg - early_avg) / max(early_avg, 1)
            else:
                trend = 0
            
            last_month_load = monthly['total_bio'].iloc[-1] if len(monthly) > 0 else 0
            forecast = last_month_load * (1 + trend * 0.3)
            spike_risk = group['total_bio'].std() / max(group['total_bio'].mean(), 1)
            
            pincode_trends.append({
                'state': state,
                'district': district,
                'pincode': pincode,
                'last_month_load': last_month_load,
                'trend': trend,
                'forecast_load': forecast,
                'spike_risk': min(spike_risk, 2),
                'historical_mean': monthly['total_bio'].mean() if len(monthly) > 0 else 0,
                'historical_max': monthly['total_bio'].max() if len(monthly) > 0 else 0
            })
        
        self.pincode_forecast = pd.DataFrame(pincode_trends)
        
        print(f"   ✓ Forecasted {len(self.district_forecast)} districts")
        print(f"   ✓ Forecasted {len(self.pincode_forecast)} pincodes")
        
        return self
    
    def calculate_load_scores(self):
        """Calculate LoadScore and SpareCapacity for each pincode"""
        print("📈 Calculating LoadScore and SpareCapacity...")
        
        # LoadScore = forecast_load + spike_risk_weighted
        # Higher = more overloaded
        
        df = self.pincode_forecast.copy()
        
        # Normalize forecast load to percentile
        df['load_percentile'] = df['forecast_load'].rank(pct=True)
        
        # LoadScore: combines expected load and volatility risk
        df['load_score'] = (
            df['load_percentile'] * 0.7 +  # Base load contribution
            df['spike_risk'].rank(pct=True) * 0.3  # Spike risk contribution
        )
        
        # SpareCapacity: inverse of load (lower load = more spare capacity)
        df['spare_capacity'] = 1 - df['load_percentile']
        
        # Categorize load levels
        df['load_category'] = pd.cut(
            df['load_score'],
            bins=[0, 0.5, 0.75, 0.9, 1.0],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        # Identify overloaded (top 10%)
        df['is_overloaded'] = df['load_score'] >= 0.9
        
        self.load_scores = df
        
        overloaded_count = df['is_overloaded'].sum()
        print(f"   ✓ Identified {overloaded_count} overloaded pincodes (top 10%)")
        
        return self


# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 LOAD BALANCING RECOMMENDER
# ═══════════════════════════════════════════════════════════════════════════════

class LoadBalancingRecommender:
    """Recommend redirection strategies for overloaded areas"""
    
    def __init__(self, load_scores: pd.DataFrame):
        self.load_scores = load_scores
        self.recommendations = []
        self.simulation_results = None
        
    def find_alternatives(self, top_n_overloaded=20, alternatives_per_pincode=5):
        """Find alternative pincodes for overloaded areas"""
        print(f"🔍 Finding alternatives for top {top_n_overloaded} overloaded pincodes...")
        
        # Get overloaded pincodes
        overloaded = self.load_scores[self.load_scores['is_overloaded']].nlargest(
            top_n_overloaded, 'load_score'
        )
        
        recommendations = []
        
        for _, row in overloaded.iterrows():
            pincode = row['pincode']
            district = row['district']
            state = row['state']
            
            # Find alternatives within same district with spare capacity
            same_district = self.load_scores[
                (self.load_scores['district'] == district) & 
                (self.load_scores['state'] == state) &
                (self.load_scores['pincode'] != pincode) &
                (self.load_scores['spare_capacity'] > 0.5)  # At least 50% spare
            ].nlargest(alternatives_per_pincode, 'spare_capacity')
            
            # If not enough in district, look at adjacent pincodes (similar prefix)
            if len(same_district) < alternatives_per_pincode:
                pin_prefix = pincode[:4]  # First 4 digits
                adjacent = self.load_scores[
                    (self.load_scores['pincode'].str[:4] == pin_prefix) &
                    (self.load_scores['pincode'] != pincode) &
                    (self.load_scores['spare_capacity'] > 0.3)
                ].nlargest(alternatives_per_pincode - len(same_district), 'spare_capacity')
                same_district = pd.concat([same_district, adjacent])
            
            alternatives = []
            for _, alt in same_district.head(alternatives_per_pincode).iterrows():
                alternatives.append({
                    'alt_pincode': alt['pincode'],
                    'alt_district': alt['district'],
                    'spare_capacity': alt['spare_capacity'],
                    'current_load': alt['forecast_load']
                })
            
            recommendations.append({
                'pincode': pincode,
                'district': district,
                'state': state,
                'load_score': row['load_score'],
                'forecast_load': row['forecast_load'],
                'spike_risk': row['spike_risk'],
                'alternatives': alternatives,
                'num_alternatives': len(alternatives)
            })
        
        self.recommendations = recommendations
        
        print(f"   ✓ Generated recommendations for {len(recommendations)} overloaded pincodes")
        
        return self
    
    def simulate_load_balancing(self, redirect_percentages=[10, 15, 20, 25, 30]):
        """Simulate impact of redirecting load to alternatives"""
        print("🎮 Simulating load balancing scenarios...")
        
        simulations = []
        
        for pct in redirect_percentages:
            total_original_peak = 0
            total_new_peak = 0
            total_redirected = 0
            
            for rec in self.recommendations:
                original_load = rec['forecast_load']
                total_original_peak += original_load
                
                # Amount to redirect
                redirect_amount = original_load * (pct / 100)
                
                # Distribute among alternatives
                if rec['alternatives']:
                    per_alt = redirect_amount / len(rec['alternatives'])
                    
                    # New load for overloaded pincode
                    new_load = original_load - redirect_amount
                    total_new_peak += new_load
                    total_redirected += redirect_amount
                else:
                    total_new_peak += original_load
            
            reduction_pct = ((total_original_peak - total_new_peak) / total_original_peak * 100) if total_original_peak > 0 else 0
            
            simulations.append({
                'redirect_percentage': pct,
                'original_peak_load': total_original_peak,
                'new_peak_load': total_new_peak,
                'total_redirected': total_redirected,
                'peak_reduction_pct': reduction_pct
            })
        
        self.simulation_results = pd.DataFrame(simulations)
        
        print(f"   ✓ Simulated {len(redirect_percentages)} scenarios")
        
        return self
    
    def get_summary_stats(self):
        """Get summary statistics"""
        total_overloaded = len(self.recommendations)
        avg_alternatives = np.mean([r['num_alternatives'] for r in self.recommendations])
        total_forecast_load = sum([r['forecast_load'] for r in self.recommendations])
        
        # Best scenario
        if self.simulation_results is not None:
            best_scenario = self.simulation_results.loc[
                self.simulation_results['peak_reduction_pct'].idxmax()
            ]
        else:
            best_scenario = None
        
        return {
            'total_overloaded': total_overloaded,
            'avg_alternatives': avg_alternatives,
            'total_forecast_load': total_forecast_load,
            'best_scenario': best_scenario
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 VISUALIZATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class LoadBalancerVisualizer:
    """Create visualizations for load balancing analysis"""
    
    def __init__(self, forecaster, recommender):
        self.forecaster = forecaster
        self.recommender = recommender
        self.figures = {}
    
    def create_load_distribution_chart(self):
        """Create chart showing load distribution across categories"""
        print("📊 Creating load distribution chart...")
        
        df = self.forecaster.load_scores
        category_counts = df['load_category'].value_counts().reindex(['Low', 'Medium', 'High', 'Critical'])
        
        colors = [INDIA_COLORS['green'], INDIA_COLORS['green_light'], 
                  INDIA_COLORS['saffron'], INDIA_COLORS['red']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=category_counts.index,
                y=category_counts.values,
                marker=dict(color=colors),
                text=category_counts.values,
                textposition='outside',
                textfont=dict(color=INDIA_COLORS['text'], size=14)
            )
        ])
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title="📊 Pincode Load Distribution by Category",
            xaxis_title="Load Category",
            yaxis_title="Number of Pincodes",
            height=500
        )
        
        self.figures['load_distribution'] = fig
        return fig
    
    def create_top_overloaded_chart(self, top_n=20):
        """Create chart of top overloaded pincodes"""
        print("📊 Creating top overloaded pincodes chart...")
        
        recs = self.recommender.recommendations[:top_n]
        
        pincodes = [f"{r['pincode']}<br>({r['district'][:15]})" for r in recs]
        load_scores = [r['load_score'] for r in recs]
        forecast_loads = [r['forecast_load'] for r in recs]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Load Score (Overload Risk)", "Forecast Load (Updates/Month)"),
            horizontal_spacing=0.15
        )
        
        # Load Score bars
        fig.add_trace(
            go.Bar(
                y=pincodes,
                x=load_scores,
                orientation='h',
                marker=dict(
                    color=load_scores,
                    colorscale=[[0, INDIA_COLORS['saffron']], [1, INDIA_COLORS['red']]],
                ),
                text=[f"{s:.2f}" for s in load_scores],
                textposition='outside',
                textfont=dict(color=INDIA_COLORS['text']),
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Forecast Load bars
        fig.add_trace(
            go.Bar(
                y=pincodes,
                x=forecast_loads,
                orientation='h',
                marker=dict(color=INDIA_COLORS['saffron']),
                text=[f"{int(f):,}" for f in forecast_loads],
                textposition='outside',
                textfont=dict(color=INDIA_COLORS['text']),
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title="🔥 Top 20 Overloaded Pincodes (Next Month Forecast)",
            height=700,
            yaxis=dict(autorange="reversed"),
            yaxis2=dict(autorange="reversed")
        )
        
        self.figures['top_overloaded'] = fig
        return fig
    
    def create_simulation_chart(self):
        """Create chart showing simulation results"""
        print("📊 Creating simulation results chart...")
        
        sim = self.recommender.simulation_results
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Peak Load Comparison", "Peak Load Reduction %"),
            horizontal_spacing=0.12
        )
        
        # Original vs New Peak
        fig.add_trace(
            go.Bar(
                name='Original Peak',
                x=sim['redirect_percentage'].astype(str) + '%',
                y=sim['original_peak_load'],
                marker=dict(color=INDIA_COLORS['red']),
                text=[f"{int(v):,}" for v in sim['original_peak_load']],
                textposition='outside'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                name='After Redirection',
                x=sim['redirect_percentage'].astype(str) + '%',
                y=sim['new_peak_load'],
                marker=dict(color=INDIA_COLORS['green']),
                text=[f"{int(v):,}" for v in sim['new_peak_load']],
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Reduction percentage
        fig.add_trace(
            go.Scatter(
                x=sim['redirect_percentage'].astype(str) + '%',
                y=sim['peak_reduction_pct'],
                mode='lines+markers+text',
                marker=dict(size=15, color=INDIA_COLORS['saffron']),
                line=dict(width=3, color=INDIA_COLORS['saffron']),
                text=[f"{v:.1f}%" for v in sim['peak_reduction_pct']],
                textposition='top center',
                textfont=dict(size=14, color=INDIA_COLORS['saffron']),
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title="🎮 Load Balancing Simulation: Impact of Redirection",
            height=500,
            barmode='group',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.25)
        )
        
        fig.update_yaxes(title_text="Total Load (Updates)", row=1, col=1)
        fig.update_yaxes(title_text="Reduction %", row=1, col=2)
        fig.update_xaxes(title_text="Redirection %", row=1, col=1)
        fig.update_xaxes(title_text="Redirection %", row=1, col=2)
        
        self.figures['simulation'] = fig
        return fig
    
    def create_recommendations_table(self, top_n=10):
        """Create visual recommendations table"""
        print("📊 Creating recommendations visualization...")
        
        recs = self.recommender.recommendations[:top_n]
        
        # Create table data
        header_values = ['Overloaded Pincode', 'District', 'Load Score', 
                         'Forecast Load', 'Alternatives', 'Top Alternative']
        
        cell_values = [
            [r['pincode'] for r in recs],
            [r['district'][:20] for r in recs],
            [f"{r['load_score']:.2f}" for r in recs],
            [f"{int(r['forecast_load']):,}" for r in recs],
            [r['num_alternatives'] for r in recs],
            [r['alternatives'][0]['alt_pincode'] if r['alternatives'] else 'None' for r in recs]
        ]
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=header_values,
                fill_color=INDIA_COLORS['saffron'],
                font=dict(color=INDIA_COLORS['background'], size=13),
                align='center',
                height=40
            ),
            cells=dict(
                values=cell_values,
                fill_color=[
                    [INDIA_COLORS['background']] * len(recs),
                    [INDIA_COLORS['background']] * len(recs),
                    [[INDIA_COLORS['red'] if float(v) > 0.95 else INDIA_COLORS['saffron'] 
                      for v in cell_values[2]]],
                    [INDIA_COLORS['background']] * len(recs),
                    [[INDIA_COLORS['green'] if v >= 3 else INDIA_COLORS['saffron'] 
                      for v in cell_values[4]]],
                    [INDIA_COLORS['green_dark']] * len(recs)
                ],
                font=dict(color=INDIA_COLORS['text'], size=12),
                align='center',
                height=35
            )
        )])
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title="📋 Top 10 Overloaded Pincodes with Recommended Alternatives",
            height=500
        )
        
        self.figures['recommendations_table'] = fig
        return fig
    
    def create_summary_dashboard(self):
        """Create executive summary dashboard"""
        print("📊 Creating summary dashboard...")
        
        stats = self.recommender.get_summary_stats()
        load_df = self.forecaster.load_scores
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                "🔥 Critical Pincodes",
                "📦 Avg Alternatives Found",
                "📉 Max Load Reduction",
                "Load Category Distribution",
                "Forecast vs Historical",
                "Spike Risk Distribution"
            ),
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                [{"type": "pie"}, {"type": "histogram"}, {"type": "histogram"}]
            ],
            vertical_spacing=0.15
        )
        
        # Indicators
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=stats['total_overloaded'],
                number={'font': {'color': INDIA_COLORS['red'], 'size': 48}}
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=stats['avg_alternatives'],
                number={'font': {'color': INDIA_COLORS['green'], 'size': 48}, 'valueformat': '.1f'}
            ),
            row=1, col=2
        )
        
        best_reduction = stats['best_scenario']['peak_reduction_pct'] if stats['best_scenario'] is not None else 0
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=best_reduction,
                number={'font': {'color': INDIA_COLORS['saffron'], 'size': 48}, 'suffix': '%'}
            ),
            row=1, col=3
        )
        
        # Pie chart - load categories
        cat_counts = load_df['load_category'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=cat_counts.index,
                values=cat_counts.values,
                marker=dict(colors=[INDIA_COLORS['green'], INDIA_COLORS['green_light'],
                                   INDIA_COLORS['saffron'], INDIA_COLORS['red']]),
                hole=0.4
            ),
            row=2, col=1
        )
        
        # Histogram - forecast distribution
        fig.add_trace(
            go.Histogram(
                x=load_df['forecast_load'],
                nbinsx=50,
                marker=dict(color=INDIA_COLORS['saffron'])
            ),
            row=2, col=2
        )
        
        # Histogram - spike risk
        fig.add_trace(
            go.Histogram(
                x=load_df['spike_risk'],
                nbinsx=30,
                marker=dict(color=INDIA_COLORS['green'])
            ),
            row=2, col=3
        )
        
        fig.update_layout(
            template=INDIA_TEMPLATE,
            title="🇮🇳 BIOMETRIC LOAD BALANCER - EXECUTIVE SUMMARY",
            height=650,
            showlegend=False
        )
        
        self.figures['summary_dashboard'] = fig
        return fig
    
    def save_all_figures(self, output_dir="load_balancer_visualizations"):
        """Save all figures as HTML"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n💾 Saving visualizations to {output_dir}/")
        
        for name, fig in self.figures.items():
            filepath = output_path / f"{name}.html"
            fig.write_html(str(filepath))
            print(f"   ✓ Saved {name}.html")
        
        return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def run_load_balancer_analysis(data_path: str = "."):
    """Run complete load balancer analysis"""
    
    print("=" * 80)
    print("🇮🇳 BIOMETRIC LOAD BALANCER - OPS IMPACT MODULE")
    print("=" * 80)
    print()
    
    # 1. Load and forecast
    forecaster = BiometricLoadForecaster(data_path)
    forecaster.load_data()
    forecaster.compute_historical_stats()
    forecaster.forecast_next_month()
    forecaster.calculate_load_scores()
    
    print()
    
    # 2. Generate recommendations
    recommender = LoadBalancingRecommender(forecaster.load_scores)
    recommender.find_alternatives(top_n_overloaded=20, alternatives_per_pincode=5)
    recommender.simulate_load_balancing([10, 15, 20, 25, 30])
    
    print()
    
    # 3. Create visualizations
    visualizer = LoadBalancerVisualizer(forecaster, recommender)
    visualizer.create_summary_dashboard()
    visualizer.create_load_distribution_chart()
    visualizer.create_top_overloaded_chart()
    visualizer.create_simulation_chart()
    visualizer.create_recommendations_table()
    visualizer.save_all_figures()
    
    # 4. Print summary
    print("\n" + "=" * 80)
    print("📋 LOAD BALANCER SUMMARY")
    print("=" * 80)
    
    stats = recommender.get_summary_stats()
    
    print(f"\n🔥 OVERLOADED PINCODES: {stats['total_overloaded']}")
    print(f"📦 AVG ALTERNATIVES FOUND: {stats['avg_alternatives']:.1f} per pincode")
    
    if stats['best_scenario'] is not None:
        print(f"\n🎮 BEST SIMULATION SCENARIO:")
        print(f"   Redirect: {stats['best_scenario']['redirect_percentage']}% of load")
        print(f"   Peak Reduction: {stats['best_scenario']['peak_reduction_pct']:.1f}%")
        print(f"   Load Redirected: {int(stats['best_scenario']['total_redirected']):,} updates")
    
    print("\n🎯 TOP 10 OVERLOADED PINCODES:")
    print("-" * 70)
    for i, rec in enumerate(recommender.recommendations[:10], 1):
        alt_str = ", ".join([a['alt_pincode'] for a in rec['alternatives'][:3]]) if rec['alternatives'] else "None"
        print(f"   {i:2d}. {rec['pincode']} ({rec['district'][:20]})")
        print(f"       Load Score: {rec['load_score']:.3f} | Forecast: {int(rec['forecast_load']):,}")
        print(f"       Alternatives: {alt_str}")
    
    print("\n" + "=" * 80)
    print("✅ Analysis Complete!")
    print("   Open load_balancer_visualizations/*.html to view dashboards")
    print("=" * 80)
    
    return forecaster, recommender, visualizer


if __name__ == "__main__":
    forecaster, recommender, visualizer = run_load_balancer_analysis("/Users/lrao/Desktop/aadhar")
