import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

FILENAME = "slow stable.csv"
THRESHOLD = 3
RELATIVE_CHANGE_THRESHOLD = 0.2

df = pd.read_csv(FILENAME)

time = df["Time (s)"]
angular_velocity = df["Absolute (rad/s)"]

over_threshold = angular_velocity > THRESHOLD

delta = angular_velocity.pct_change().abs()
rapid_change = delta > RELATIVE_CHANGE_THRESHOLD

unstable_combined = over_threshold | rapid_change
unstable_times = time[unstable_combined]

output_df = df[unstable_combined]
output_df.to_csv("unstable_movements.csv", index=False)
print(f"found {len(output_df)} unstable points. saved in 'unstable_movements.csv'.")

plt.figure(figsize=(12, 6))
plt.plot(time, angular_velocity, label="angular velocity (rad/s)")
plt.axhline(y=THRESHOLD, color='red', linestyle='--', label=f"threshold {THRESHOLD} rad/s")
plt.scatter(unstable_times, angular_velocity[unstable_combined], color='red', s=10, label="unstable points")
plt.xlabel("Time (s)")
plt.ylabel("Absolute angular velocity (рад/с)")
plt.title("unstable movement: threshold and sudden movements (>20%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
