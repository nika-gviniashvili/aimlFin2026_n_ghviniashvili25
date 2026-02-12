import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Analyzing the log file
times = []
with open("D:/n_ghviniashvili25_15289_server.log", "r",) as f:
    for line in f:
        m = re.search(r'\[(.*?)\]', line)
        if m:
            times.append(datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S%z"))

# Creating dataframe and count requests per minute
df = pd.DataFrame(times, columns=["time"])
df["time"] = df["time"].dt.floor("min")
traffic = df.groupby("time").size().reset_index(name="count")

# We are using the Linear regression
traffic["x"] = range(len(traffic))
model = LinearRegression().fit(traffic[["x"]], traffic["count"])
pred = model.predict(traffic[["x"]])

# Detect DDoS pattern
res = traffic["count"] - pred
limit = res.mean() + 3 * res.std()
attack = traffic[res > limit]

#Generating the graph to show DDos spike
plt.figure(figsize=(12,6))
plt.plot(traffic["time"], traffic["count"], label="Actual Traffic")
plt.plot(traffic["time"], pred, label="Predicted Traffic")
plt.legend()
plt.xticks(rotation=45)
plt.title("Actual Traffic vs Predicted Traffic")
plt.show()

#Printing the results
if not attack.empty:
    print("Attention DDos was Detected")
    print("Start:", attack["time"].min())
    print("End:", attack["time"].max())
else:
    print("No DDoS was detected")

