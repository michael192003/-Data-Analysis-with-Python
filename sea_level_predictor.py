import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

# Import data from CSV file.
df = pd.read_csv("epa-sea-level.csv")

def draw_plot():
    # Create scatter plot.
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df["Year"], df["CSIRO Adjusted Sea Level"], s=10, color="blue", label="Data")
    
    # Create first line of best fit (using all data).
    res_all = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    years_extended = np.arange(df["Year"].min(), 2051)
    line_all = res_all.intercept + res_all.slope * years_extended
    ax.plot(years_extended, line_all, color="red", label="Fit: All Data")
    
    # Create second line of best fit (using data from year 2000 onwards).
    df_recent = df[df["Year"] >= 2000]
    res_recent = linregress(df_recent["Year"], df_recent["CSIRO Adjusted Sea Level"])
    line_recent = res_recent.intercept + res_recent.slope * years_extended
    ax.plot(years_extended, line_recent, color="green", label="Fit: Since 2000")
    
    # Set labels and title.
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")
    ax.legend()
    
    # Save plot.
    fig.savefig("sea_level_plot.png")
    return fig

if __name__ == '__main__':
    draw_plot()
