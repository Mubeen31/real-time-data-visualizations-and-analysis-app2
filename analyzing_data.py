import pandas as pd
from datetime import datetime


url = 'https://api.thingspeak.com/channels/2007583/fields/2.csv?results=50'
df = pd.read_csv(url)
df['created_at'] = pd.to_datetime(df['created_at'])
df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime('%Y-%m-%d %H:%M:%S')
# date_time = df['created_at'].iloc[0]
# get_date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S UTC')
# last_date_time = get_date_time.strftime('%Y-%m-%d %H:%M:%S')
print(df)
