import pandas as pd

def calculate_rolling_max(df: pd.DataFrame) -> pd.DataFrame:
    df['Rolling1hr'] = df['Reading'].rolling(window=2).sum()
    return df

def enrich_summary_row(start_row, end_row):
    total = start_row['Reading'] + end_row['Reading']
    mpan = start_row['MPAN']
    season = start_row['Season']
    date = str(start_row['DateOnly'])
    time_1 = start_row['DateTime']
    time_2 = end_row['DateTime']

    def calc_buffer(buffer_pct):
        buffer = total * buffer_pct
        diff_kW = round(buffer - total, 3)
        diff_pct = round((buffer - total) / total * 100, 2)
        return round(buffer, 3), diff_pct, diff_kW

    buffer_50, diff_50_pct, diff_50_kW = calc_buffer(1.5)
    buffer_100, diff_100_pct, diff_100_kW = calc_buffer(2.0)
    buffer_125, diff_125_pct, diff_125_kW = calc_buffer(2.25)
    buffer_250, diff_250_pct, diff_250_kW = calc_buffer(3.5)

    return {
        'MPAN': mpan,
        'Season': season,
        'Date': date,
        'First 30 Min Start Time': time_1,
        'Second 30 Min Start Time': time_2,
        'First 30 Min Demand (kW)': round(start_row['Reading'], 3),
        'Second 30 Min Demand (kW)': round(end_row['Reading'], 3),
        'Total Demand (1-hr) in kW': round(total, 3),
        '50% Buffer in kW': buffer_50,
        '50% Buffer Difference in %': diff_50_pct,
        '50% Buffer Difference in kW': diff_50_kW,
        '100% Buffer in kW': buffer_100,
        '100% Buffer Difference in %': diff_100_pct,
        '100% Buffer Difference in kW': diff_100_kW,
        '125% Buffer in kW': buffer_125,
        '125% Buffer Difference in %': diff_125_pct,
        '125% Buffer Difference in kW': diff_125_kW,
        '250% Buffer in kW': buffer_250,
        '250% Buffer Difference in %': diff_250_pct,
        '250% Buffer Difference in kW': diff_250_kW
    }

def summarize_top_days(df: pd.DataFrame) -> pd.DataFrame:
    top_dates = (
        df.groupby('DateOnly')['Rolling1hr']
        .max()
        .sort_values(ascending=False)
        .head(5)
        .index
    )

    summary = []
    for rank, date in enumerate(top_dates, 1):
        day_df = df[df['DateOnly'] == date]
        if day_df.empty or day_df['Rolling1hr'].isnull().all():
            continue
        day_df = day_df.reset_index(drop=True)  # Ensure position-based indexing
        if len(day_df) < 2:
            continue
        max_pos = day_df['Rolling1hr'].idxmax()
        if max_pos > 0:
            start_row = day_df.iloc[max_pos - 1]
            end_row = day_df.iloc[max_pos]
            enriched = enrich_summary_row(start_row, end_row)
            enriched['Rank'] = rank
            summary.append(enriched)
    return pd.DataFrame(summary)

def seasonal_summary(df: pd.DataFrame) -> pd.DataFrame:
    max_idxs = (
        df.groupby('Season')['Rolling1hr']
        .idxmax()
        .dropna()
        .astype(int)
    )
    summary = []
    for idx in max_idxs:
        if idx > 0:
            start_row = df.loc[idx - 1]
            end_row = df.loc[idx]
            enriched = enrich_summary_row(start_row, end_row)
            summary.append(enriched)
    return pd.DataFrame(summary)
