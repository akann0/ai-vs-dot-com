import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Nasdaq 100 Valuation Analysis",
    page_icon="📈",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Space Mono', monospace !important;
        color: #00d4ff !important;
    }
    
    p, div, span, label {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #1e1e2f 0%, #2a2a4a 100%);
        border: 1px solid #3a3a5a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.1);
    }
    
    .metric-value {
        font-family: 'Space Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4ff;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #8a8aa3;
        margin-top: 5px;
    }
    
    .era-dotcom {
        color: #ff6b6b !important;
    }
    
    .era-modern {
        color: #4ecdc4 !important;
    }
    
    /* Style the radio buttons */
    .stRadio > div {
        flex-direction: row !important;
        gap: 20px;
    }
    
    .stRadio label {
        background: linear-gradient(145deg, #1e1e2f 0%, #2a2a4a 100%);
        border: 1px solid #3a3a5a;
        border-radius: 8px;
        padding: 10px 20px !important;
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 📈 Nasdaq 100 Valuation Metrics")
st.markdown("### Comparing the Dot-Com Bubble (1996-2000) vs Modern AI Era (2022-2025)")
st.markdown("---")

# Expected file paths
DATA_FILES = {
    "pe_dotcom": "nasdaq100_pe_1996_2000.csv",
    "pe_modern": "nasdaq100_pe_2022_2025.csv",
    "ps_dotcom": "nasdaq100_ps_1996_2000.csv",
    "ps_modern": "nasdaq100_ps_2022_2025.csv",
}


def load_csv_if_exists(filepath):
    """Load a CSV file if it exists, return None otherwise."""
    if not os.path.exists(filepath):
        return None
    
    try:
        df = pd.read_csv(filepath, index_col=0, parse_dates=True)
        # Handle both Series saved as CSV (single column) formats
        if isinstance(df, pd.DataFrame) and len(df.columns) >= 1:
            return df.iloc[:, 0]
        return df
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return None


def check_data_availability():
    """Check which data files are available."""
    available = {}
    for key, filepath in DATA_FILES.items():
        data = load_csv_if_exists(filepath)
        available[key] = data
    return available


def generate_aligned_quarter_labels(start_year, num_quarters):
    """
    Generate quarter labels starting from a given year.
    Returns labels like ['1996 Q1', '1996 Q2', '1996 Q3', '1996 Q4', '1997 Q1', ...]
    """
    labels = []
    year = start_year
    quarter = 1
    for _ in range(num_quarters):
        labels.append(f"{year} Q{quarter}")
        quarter += 1
        if quarter > 4:
            quarter = 1
            year += 1
    return labels


# Check what data is available
data = check_data_availability()

pe_dotcom = data.get("pe_dotcom")
pe_modern = data.get("pe_modern")
ps_dotcom = data.get("ps_dotcom")
ps_modern = data.get("ps_modern")

has_pe_data = pe_dotcom is not None and pe_modern is not None
has_ps_data = ps_dotcom is not None and ps_modern is not None
has_any_data = has_pe_data or has_ps_data

# If no data, show a simple message
if not has_any_data:
    st.warning("No data files found. Please run `python fetch_qqq_data.py` to generate the data.")
    st.stop()

# ============================================================
# METRIC SELECTOR
# ============================================================
st.markdown("### Select Valuation Metric")

# Determine available options
metric_options = []
if has_pe_data:
    metric_options.append("P/E Ratio (Price-to-Earnings)")
if has_ps_data:
    metric_options.append("P/S Ratio (Price-to-Sales)")

if len(metric_options) == 0:
    st.error("No data available.")
    st.stop()

selected_metric = st.radio(
    "Choose metric to display:",
    metric_options,
    horizontal=True,
    label_visibility="collapsed"
)

# Determine which data to use based on selection
if "P/E" in selected_metric:
    dotcom_data = pe_dotcom
    modern_data = pe_modern
    metric_name = "P/E"
    metric_full_name = "Price-to-Earnings (P/E) Ratio"
    value_format = ".1f"
else:
    dotcom_data = ps_dotcom
    modern_data = ps_modern
    metric_name = "P/S"
    metric_full_name = "Price-to-Sales (P/S) Ratio"
    value_format = ".2f"

st.markdown("---")

# ============================================================
# METRICS DISPLAY
# ============================================================
st.markdown(f"## 📊 {metric_full_name}")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    peak_dotcom = dotcom_data.max()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value era-dotcom">{peak_dotcom:{value_format}}</div>
        <div class="metric-label">Peak {metric_name} (Dot-Com)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    peak_modern = modern_data.max()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value era-modern">{peak_modern:{value_format}}</div>
        <div class="metric-label">Peak {metric_name} (Modern)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_dotcom = dotcom_data.mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value era-dotcom">{avg_dotcom:{value_format}}</div>
        <div class="metric-label">Avg {metric_name} (Dot-Com)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_modern = modern_data.mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value era-modern">{avg_modern:{value_format}}</div>
        <div class="metric-label">Avg {metric_name} (Modern)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SIDE-BY-SIDE CHARTS
# ============================================================
fig_side = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Dot-Com Era (1999-2000)", "Modern AI Era (2022-2024)"),
    horizontal_spacing=0.1
)

fig_side.add_trace(
    go.Scatter(
        x=dotcom_data.index,
        y=dotcom_data.values,
        mode='lines+markers',
        name='Dot-Com Era',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=8, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)',
    ),
    row=1, col=1
)

fig_side.add_trace(
    go.Scatter(
        x=modern_data.index,
        y=modern_data.values,
        mode='lines+markers',
        name='Modern Era',
        line=dict(color='#4ecdc4', width=3),
        marker=dict(size=8, symbol='diamond'),
        fill='tozeroy',
        fillcolor='rgba(78, 205, 196, 0.2)',
    ),
    row=1, col=2
)

fig_side.update_layout(
    height=450,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(color='#e0e0e0')
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26, 26, 46, 0.8)',
    font=dict(color='#e0e0e0', family='DM Sans'),
)

fig_side.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#8a8aa3'))
fig_side.update_yaxes(title_text=f"{metric_name} Ratio", showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#8a8aa3'))

st.plotly_chart(fig_side, use_container_width=True)

# ============================================================
# OVERLAY COMPARISON - ALIGNED BY PEAK
# ============================================================
st.markdown(f"### {metric_name} Overlay Comparison (Aligned by Peak)")
st.markdown("*Both eras aligned so their peak valuations overlap.*")

# Find the peak index for each series
dotcom_peak_idx = int(dotcom_data.values.argmax())
modern_peak_idx = int(modern_data.values.argmax())

# We'll use a common x-axis centered around 0 at the peak
# Dot-com positions: peak is at 0, others relative to that
dotcom_x_positions = [i - dotcom_peak_idx for i in range(len(dotcom_data))]

# Modern positions: peak is at 0, others relative to that  
modern_x_positions = [i - modern_peak_idx for i in range(len(modern_data))]

# Find the range we need for the x-axis
min_x = min(min(dotcom_x_positions), min(modern_x_positions))
max_x = max(max(dotcom_x_positions), max(modern_x_positions))

fig_overlay = go.Figure()

# Dot-com data
fig_overlay.add_trace(
    go.Scatter(
        x=dotcom_x_positions,
        y=dotcom_data.values,
        mode='lines+markers',
        name='Dot-Com Era (1999-2000)',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=10),
        connectgaps=True,
    )
)

# Modern data
fig_overlay.add_trace(
    go.Scatter(
        x=modern_x_positions,
        y=modern_data.values,
        mode='lines+markers',
        name='Modern AI Era (2022-2024)',
        line=dict(color='#4ecdc4', width=3),
        marker=dict(size=10),
    )
)

# Create tick labels showing quarters before/after peak
tick_positions = list(range(min_x, max_x + 1))
tick_labels = []
for pos in tick_positions:
    if pos < 0:
        tick_labels.append(f"{abs(pos)}Q before peak")
    elif pos == 0:
        tick_labels.append("PEAK")
    else:
        tick_labels.append(f"{pos}Q after peak")

# Add a vertical line at the peak
fig_overlay.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.5)", line_width=2)

fig_overlay.update_layout(
    height=450,
    xaxis=dict(
        tickmode='array',
        tickvals=tick_positions,
        ticktext=tick_labels,
        tickangle=45,
    ),
    yaxis_title=f"{metric_name} Ratio",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color='#e0e0e0')),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26, 26, 46, 0.8)',
    font=dict(color='#e0e0e0', family='DM Sans'),
    margin=dict(b=120),
)

fig_overlay.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
fig_overlay.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')

st.plotly_chart(fig_overlay, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #8a8aa3;'>Data 511 Final Project | University of Washington</p>",
    unsafe_allow_html=True
)
