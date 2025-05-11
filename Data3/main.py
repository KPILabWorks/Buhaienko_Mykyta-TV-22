import pandas as pd
import numpy as np
from numba import njit
import time

df_load = pd.read_csv("Total Load - Day Ahead _ Actual_202501010000-202601010000.csv")
df_gen = pd.read_csv("Actual Generation per Production Type_202501010000-202601010000.csv")

df_load["Timestamp"] = df_load["Time (CET/CEST)"].str.extract(r"-\s([\d\.:\s]+)")[0]
df_load["Timestamp"] = pd.to_datetime(df_load["Timestamp"], format="%d.%m.%Y %H:%M")

df_gen["Timestamp"] = df_gen["MTU"].str.extract(r"^([\d\.:\s]+)")[0].str.strip()
df_gen["Timestamp"] = pd.to_datetime(df_gen["Timestamp"], format="%d.%m.%Y %H:%M")

df_merged = pd.merge(df_load, df_gen, on="Timestamp", how="inner")

df_merged["Forecast [MW]"] = pd.to_numeric(df_merged["Day-ahead Total Load Forecast [MW] - CTA|FR"], errors="coerce")
df_merged["Actual [MW]"] = pd.to_numeric(df_merged["Actual Total Load [MW] - CTA|FR"], errors="coerce")
df_merged["Forecast Error [MW]"] = df_merged["Actual [MW]"] - df_merged["Forecast [MW]"]

array_actual = df_merged["Actual [MW]"].dropna().to_numpy()

start_pandas = time.time()
df_sorted_pandas = df_merged.sort_values(by="Actual [MW]").reset_index(drop=True)
end_pandas = time.time()

start_numpy = time.time()
sorted_numpy = np.sort(array_actual.copy())
end_numpy = time.time()

@njit
def numba_sort(arr):
    return np.sort(arr)

start_numba = time.time()
sorted_numba = numba_sort(array_actual.copy())
end_numba = time.time()

start_numba1 = time.time()
sorted_numba1 = numba_sort(array_actual.copy())
end_numba1 = time.time()

# === 9. Вивід результатів ===
print("Array size:", len(array_actual))
print("1. pandas.sort_values():", round(end_pandas - start_pandas, 10), "s")
print("2. numpy.sort():", round(end_numpy - start_numpy, 10), "s")
print("3. numba sort():", round(end_numba - start_numba, 10), "s")
print("3. numba second sort():", round(end_numba1 - start_numba1, 10), "s")
