import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="EUR/USD 5分足 + EMA25", layout="wide")
st.title("EUR/USD 5分足（Candlestick）+ EMA25")

p = Path("logs_ohlc_5m.csv")
if not p.exists():
    st.warning("先に main.py を実行してCSVを用意してください。")
else:
    df = pd.read_csv(p, parse_dates=["time"])

    # ボラ判定
    lo = float(df["low"].min())
    hi = float(df["high"].max())
    span = hi - lo

    # 目標: 縦軸幅を常に 0.01。全足が入るなら適用。入らなければ自動。
    y_range = None
    if span <= 0.01:
        center = (hi + lo) / 2
        y_range = [center - 0.005, center + 0.005]

    fig = go.Figure()

    # ローソク足
    fig.add_trace(go.Candlestick(
        x=df["time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Candles"
    ))
    # EMA25
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["ema25"], mode="lines", name="EMA25"
    ))

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        yaxis=dict(
            range=y_range,            # Noneなら自動
            dtick=0.005,              # 目盛間隔
            tickformat=".4f"
        ),
        height=520,
        margin=dict(l=40, r=40, t=30, b=40),
        legend=dict(x=0, y=1)
    )

    st.plotly_chart(fig, use_container_width=True)
