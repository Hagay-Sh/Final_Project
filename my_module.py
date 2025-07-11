# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_df_stocks(start_date, end_date, size):
    # Define the date range
    dates = pd.date_range(start=start_date, end=end_date)

    # Select 20 random dates from Q2 2024 (with or without duplicates)
    stock_dates = np.random.choice(dates, size=size, replace=True)

    # Create DataFrame for each stock using the same 20 dates
    df_a = pd.DataFrame({
        'Stock': 'stock_a',
        'Closed': np.abs(np.random.randn(size)),
        'Date': stock_dates
    })

    df_b = pd.DataFrame({
        'Stock': 'stock_b',
        'Closed': np.abs(np.random.randn(size)),
        'Date': stock_dates
    })

    df_c = pd.DataFrame({
        'Stock': 'stock_c',
        'Closed': np.abs(np.random.randn(size)),
        'Date': stock_dates
    })

    # Combine all into one DataFrame
    df_stock = pd.concat([df_a, df_b, df_c], ignore_index=True)
    df_stock = df_stock.set_index('Date')

    # Pivot for visualization or further analysis
    pivot_df_stock = df_stock.pivot_table(
        values='Closed', index=df_stock.index, columns='Stock')

    grouped_df_stock = df_stock.groupby('Stock').Closed.mean()

    return (df_stock, pivot_df_stock, grouped_df_stock)


def create_df_map(base_lat, base_lon, num_points, uf_min, uf_max):
    # Base coordinates for London
    base_lat = base_lat
    base_lon = base_lon

    # Generate small random offsets around the base location
    num_points = num_points
    # uniform distribution
    latitudes = base_lat + np.random.uniform(uf_min, uf_max, size=num_points)
    # uniform distribution
    longitudes = base_lon + np.random.uniform(uf_min, uf_max, size=num_points)

    # Create DataFrame
    df = pd.DataFrame({
        'lat': latitudes,
        'lon': longitudes
    })
    return (df)


def create_mat_plot(pivot_df_stock):
    # Matplotlib Chart
    fig, ax = plt.subplots()
    pivot_df_stock.plot(ax=ax)
    ax.set_title("Matplotlib - Stock Closing Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closed")
    plt.xticks(rotation=45)

    return (fig)

    return (fig)


def create_sns_plot(pivot_df_stock):
    ax2.set_title("Seaborn - Stock Closing Prices")
    plt.xticks(rotation=45)

    return (fig2)


# %%

    return (fig2)


# %%
