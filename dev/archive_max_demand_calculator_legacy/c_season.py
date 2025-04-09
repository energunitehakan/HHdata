def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

def apply_season(df):
    df['Season'] = df['DateTime'].dt.date.map(lambda d: get_season(d))
    return df
