import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt



if __name__ == '__main__':

    df_load = pd.read_csv("Total Load - Day Ahead _ Actual_202501010000-202601010000.csv")
    df_gen = pd.read_csv("Actual Generation per Production Type_202501010000-202601010000.csv")

    df_load["Timestamp"] = df_load["Time (CET/CEST)"].str.extract(r"-\s([\d\.:\s]+)")[0]
    df_load["Timestamp"] = pd.to_datetime(df_load["Timestamp"], format="%d.%m.%Y %H:%M")
    df_gen["Timestamp"] = df_gen["MTU"].str.extract(r"^([\d\.:\s]+)")[0].str.strip()
    df_gen["Timestamp"] = pd.to_datetime(df_gen["Timestamp"], format="%d.%m.%Y %H:%M")

    df_merged = pd.merge(df_load, df_gen, on="Timestamp", how="inner")
    df_merged["Forecast [MW]"] = pd.to_numeric(df_merged["Day-ahead Total Load Forecast [MW] - CTA|FR"], errors="coerce")
    df_merged["Actual [MW]"] = pd.to_numeric(df_merged["Actual Total Load [MW] - CTA|FR"], errors="coerce")

    subset = df_merged.head(500).copy()

    forecast = subset["Forecast [MW]"].ffill().to_numpy()
    cost_per_mw = 45  # $/MW
    bounds = [(0.9 * f, 1.1 * f) for f in forecast]
    initial_guess = forecast.copy()

    def cost_function(load):
        return np.sum(load * cost_per_mw)

    result = minimize(cost_function, initial_guess, bounds=bounds, method='SLSQP', options={'disp': True})

    subset["Optimized Load [MW]"] = result.x

    original_cost = np.sum(forecast * cost_per_mw)
    optimized_cost = np.sum(result.x * cost_per_mw)

    print("Original:", round(original_cost, 2), "$")
    print("Optimized:", round(optimized_cost, 2), "$")
    print("Economy:", round(original_cost - optimized_cost, 2), "$")

    plt.figure(figsize=(14, 6))
    plt.plot(subset["Timestamp"], forecast, label="Predict", linestyle="--")
    plt.plot(subset["Timestamp"], result.x, label="Optimized load", linewidth=2)
    plt.xlabel("Time")
    plt.ylabel("Load (MW)")
    plt.title("Optimised load")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
