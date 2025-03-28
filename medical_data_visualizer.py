import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data from CSV file and assign it to the df variable.
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column. First, calculate BMI: weight (kg) / [height (m)]^2.
# Then, if BMI > 25, mark as overweight (1), else not overweight (0).
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad.
# For 'cholesterol' and 'gluc', if the value is 1, set it to 0; if greater than 1, set it to 1.
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

def draw_cat_plot():
    """
    Create a categorical plot that shows the counts of each feature for patients with and without
    cardiovascular disease. The plot displays counts for:
      - cholesterol, gluc, smoke, alco, active, and overweight
    grouped by the cardio (cardiovascular disease) column.
    """
    # Create DataFrame for cat plot using pd.melt. 'cardio' is used as the id variable.
    df_cat = pd.melt(df, id_vars=['cardio'], 
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # Group and reformat the data. Count the occurrences of each value for every combination of
    # 'cardio', 'variable', and 'value'.
    df_cat = df_cat.value_counts().reset_index(name='total')
    
    # Create a categorical plot using the seaborn catplot method.
    # We set kind='bar' to get a bar plot and use 'col' to create separate panels for cardio=0 and cardio=1.
    fig = sns.catplot(data=df_cat, x='variable', y='total', hue='value', col='cardio', kind='bar').fig
    
    # Return the figure object
    return fig

def draw_heat_map():
    """
    Clean the data by filtering out patients with incorrect data, compute the correlation matrix,
    and then draw a heatmap.
    The following conditions are used for cleaning:
      - Keep only rows where 'ap_lo' <= 'ap_hi'
      - Keep only rows where height is between the 2.5th and 97.5th percentiles
      - Keep only rows where weight is between the 2.5th and 97.5th percentiles
    """
    # Clean the data.
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    
    # Calculate the correlation matrix.
    corr = df_heat.corr()
    
    # Generate a mask for the upper triangle.
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Set up the matplotlib figure.
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Draw the heatmap using seaborn. Adjust parameters for clear formatting.
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    # Return the figure object.
    return fig

# Do not modify the next two lines
if __name__ == '__main__':
    # For testing, you can display the plots:
    cat_fig = draw_cat_plot()
    cat_fig.savefig('catplot.png')
    heat_fig = draw_heat_map()
    heat_fig.savefig('heatmap.png')
