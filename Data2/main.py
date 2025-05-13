import yfinance as yf
import pandas as pd


def to_mb(bytes):
    return round(bytes / (1024 * 1024), 4)


if __name__ == '__main__':
    df = yf.download("AAPL", start="2015-01-01", end="2024-12-31")
    print(df)
    df = df.reset_index()
    print(df)

    df['Date_str'] = df['Date'].astype(str)
    date_in_str = df['Date_str'].memory_usage(deep=True)

    df['Date_dt'] = pd.to_datetime(df['Date_str'])
    date_in_pd = df['Date_dt'].memory_usage(deep=True)

    df['Date_py'] = df['Date_dt'].dt.date
    date_in_py = df['Date_py'].memory_usage(deep=True)

    print(f"Memory in string: {date_in_str} bytes ({to_mb(date_in_str)} MB)")
    print(f"Memory in pandas datetime64[ns]: {date_in_pd} bytes ({to_mb(date_in_pd)} MB)")
    print(f"Memory in python datetime.date: {date_in_py} bytes ({to_mb(date_in_py)} MB)")

    print(f"\nMemory saved str to pd: {date_in_str - date_in_pd} bytes ({to_mb(date_in_str - date_in_pd)} MB)")
    print(f"Memory saved str to py:  {date_in_str - date_in_py} bytes ({to_mb(date_in_str - date_in_py)} MB)")
