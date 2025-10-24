import os, requests, pandas as pd, numpy as np
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("TWELVE_DATA_KEY")

def ema(series, period):
    alpha = 2 / (period + 1)
    out = np.empty_like(series, dtype=float)
    out[0] = series[0]
    for i in range(1, len(series)):
        out[i] = alpha * series[i] + (1 - alpha) * out[i-1]
    return out

def fetch_fx_intraday():
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "EUR/USD",
        "interval": "5min",
        "outputsize": 72,
        "apikey": API_KEY,
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "values" not in data:
        raise RuntimeError(f"APIレスポンス異常: {data}")
    df = pd.DataFrame(data["values"])
    df = df.rename(columns={
        "datetime": "time",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close"
    })
    df = df.astype({"open": float, "high": float, "low": float, "close": float})
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    return df

if __name__ == "__main__":
    df = fetch_fx_intraday()
    df["ema25"] = ema(df["close"].to_numpy(), 25)
    print(df.tail(1))
    df.to_csv("logs_ohlc_5m.csv", index=False)
    print("保存完了")
