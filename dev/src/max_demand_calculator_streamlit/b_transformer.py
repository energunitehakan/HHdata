import pandas as pd

REQUIRED_COLUMNS = {'MPAN', 'Meter Name', 'Description', 'Date'}

def parse_datetime_column(date_series, time_series):
    """Robust parser that handles dd/mm/yy and falls back if needed."""
    datetime_str = date_series + ' ' + time_series
    try:
        # Try specific format first (fast, consistent)
        return pd.to_datetime(datetime_str, format="%d/%m/%y %H:%M", dayfirst=True)
    except Exception:
        # Fallback to flexible parsing with coercion
        return pd.to_datetime(datetime_str, dayfirst=True, errors='coerce')

def transform_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if not REQUIRED_COLUMNS.issubset(df.columns):
        missing = REQUIRED_COLUMNS - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Filter for 'Consumption' readings only
    df = df[df['Description'].str.contains('Consumption', case=False, na=False)]

    # Melt the time columns into long format
    id_vars = ['MPAN', 'Meter Name', 'Description', 'Date']
    time_cols = [col for col in df.columns if col not in id_vars and not col.endswith('Flag')]
    df_melted = df.melt(id_vars=id_vars, value_vars=time_cols,
                        var_name='Time', value_name='Reading')
    df_melted.dropna(subset=['Reading'], inplace=True)

    # Parse and validate datetime
    df_melted['DateTime'] = parse_datetime_column(df_melted['Date'], df_melted['Time'])
    if df_melted['DateTime'].isnull().any():
        raise ValueError("Some DateTime values could not be parsed. Please check input formatting.")

    # Final cleanup
    df_melted.sort_values('DateTime', inplace=True)
    df_melted['DateOnly'] = df_melted['DateTime'].dt.date
    return df_melted
