import pandas as pd

# Display historical data as str

# Trim column headers
view_df = pd.read_json('sesh.json')
view_df['Timestamp'] = pd.to_datetime(view_df['Timestamp'].str[0]).dt.strftime('%Y-%m-%d %H:%M:%S')
view_df['MAC'] = view_df['MAC'].str[0]
view_df['Moisture'] = view_df['Moisture'].str[0]
view_df['Light'] = view_df['Light'].str[0]
view_df['Temperature'] = view_df['Temperature'].str[0]
view_df['Conductivity'] = view_df['Conductivity'].str[0]
print(view_df)
