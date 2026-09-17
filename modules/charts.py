import plotly.graph_objects as go
from depreciation import depreciation_calculator
import pandas as pd
import plotly.express as px

def render_waterfall(shap_result):
     
    contributions = shap_result['contributions']
    labels = [name for name, _ in contributions]
    deltas = [delta for _, delta in contributions]

    fig = go.Figure(go.Waterfall(
        orientation='v',
        measure=['relative'] * len(deltas),
        x=labels,
        y=deltas,
        base=shap_result['base_price'],
        increasing=dict(marker=dict(color='#2E8B57')),   # green
        decreasing=dict(marker=dict(color='#C0392B')),   # red
        connector=dict(line=dict(color='#C9DCF2', width=1)),
        text=[f'₹{d:,.0f}' for d in deltas],
        textposition='outside'
    ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Roboto, sans-serif', color='#14203A'),
        yaxis=dict(title='Price (₹)', showgrid=True, gridcolor='#C9DCF2'),
        margin=dict(l=40, r=40, t=80, b=40),
    )

    return(fig)
    

def render_depcurve(dep_df):
    fig = px.line(
        dep_df,
        x='index',
        y='price',
        labels={"index": "Year", 0: "Prince (in Rs.)"},
        template="plotly_white", 
    )
    fig.update_traces(
        line=dict(width=2.5),  
        mode="lines", 
    )
    fig.update_xaxes(
        dtick=1,  
        tickformat="d",
    )
    fig.update_layout(
        font_family="Arial, sans-serif",
        hovermode="x unified", 
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        margin=dict(l=40, r=40, t=80, b=40),
    )

    return(fig)