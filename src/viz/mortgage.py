import streamlit as st
import plotly.graph_objects as go
import numpy as np

def plot_cashflow_comparison(# region
    base: np.ndarray,
    extended: np.ndarray,
    metric_name,
    unit: str = "zł",
    value_format: str = ",.0f"
) -> go.Figure:
    title = f"Porównanie: {metric_name}"
    unit_str = f" {unit}" if unit else ""
    yaxis_title = f"{metric_name}{f' [{unit}]' if unit else ''}"
    hovertemplate = (
        "Miesiąc: %{x}<br>"
        f"{metric_name}: %{{y:{value_format}}}{unit_str}"
        "<extra></extra>"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(base) + 1)),
            y=base,
            mode="lines",
            name="Bazowa",
            line=dict(width=3, dash="dot"),
            hovertemplate=hovertemplate,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(extended) + 1)),
            y=extended,
            mode="lines",
            name="Łączna",
            line=dict(width=3, dash="dot"),
            hovertemplate=hovertemplate,
        )
    )

    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, x=0.5, xanchor="center"),
        xaxis_title="Miesiąc",
        yaxis_title=yaxis_title,
        hovermode="x unified",
        legend=dict(
            title="Wariant",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=60, r=20, t=80, b=50),
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False, tickformat=value_format)

    st.plotly_chart(fig, use_container_width=True)
# endregion

def cashflows(mortgage_name):
    mrt_dict = st.session_state[mortgage_name]

    metric_name = st.selectbox(
        "Wybierz zmienną",
        options=["Rata całkowita", "Kwota do spłaty"],)

    if metric_name == "Rata całkowita":
        plot_cashflow_comparison(
            base = mrt_dict["summaries"]["base_total_monthly_payment"],
            extended = mrt_dict["summaries"]["extended_total_monthly_payment"],
            metric_name = metric_name
        )
    elif metric_name == "Kwota do spłaty":
        plot_cashflow_comparison(
            base = mrt_dict["details"]["base"]["cashflows"]["exposure"],
            extended = mrt_dict["details"]["extended"]["cashflows"]["exposure"],
            metric_name = metric_name
        )

