import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Import data (set date as index)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data by removing the top and bottom 2.5% of page views
lower_bound = df["value"].quantile(0.025)
upper_bound = df["value"].quantile(0.975)
df = df[(df["value"] >= lower_bound) & (df["value"] <= upper_bound)]

def draw_line_plot():
    """
    Draws a line chart of daily freeCodeCamp Forum page views.
    Title: "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    x-label: "Date"
    y-label: "Page Views"
    Returns the Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    plt.tight_layout()
    return fig

def draw_bar_plot():
    """
    Draws a bar chart that shows the average daily page views for each month grouped by year.
    - x-label: "Years"
    - y-label: "Average Page Views"
    - Legend: Months (with title "Months")
    Returns the Matplotlib figure object.
    """
    # Create a copy and add 'year' and 'month' columns
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Pivot table: rows = years, columns = months, values = average page views
    df_pivot = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(12, 8))
    # Plot each month as a separate series on the same axis.
    df_pivot.plot(kind="bar", ax=ax)
    
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])
    plt.tight_layout()
    return fig

def draw_box_plot():
    """
    Draws two adjacent box plots:
      1) Year-wise Box Plot (Trend): Shows the distribution of page views for each year.
      2) Month-wise Box Plot (Seasonality): Shows the distribution of page views for each month.
         The month names should start at Jan.
    Returns the Matplotlib figure object.
    """
    # Prepare data for box plots: create a copy and add year and month columns
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    # For proper ordering of months
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Create subplots with 1 row and 2 columns
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))
    
    # Year-wise Box Plot (Trend)
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    plt.tight_layout()
    return fig

# For testing purposes:
if __name__ == '__main__':
    # Draw and save line plot
    line_fig = draw_line_plot()
    line_fig.savefig("line_plot.png")

    # Draw and save bar plot
    bar_fig = draw_bar_plot()
    bar_fig.savefig("bar_plot.png")

    # Draw and save box plot
    box_fig = draw_box_plot()
    box_fig.savefig("box_plot.png")
