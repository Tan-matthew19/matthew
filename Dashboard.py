import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the air quality data
try:
    df_wanliu = pd.read_csv('DATA/PRSA_Data_Wanliu_20130301-20170228.csv')
    df_wanshouxigong = pd.read_csv('DATA/PRSA_Data_Wanshouxigong_20130301-20170228.csv')
except Exception as e:
    st.error("Error loading data: {}".format(e))
    st.stop()  # Stop execution if data loading fails

# Fill missing values and process datetime
df_wanliu.fillna(method='ffill', inplace=True)
df_wanshouxigong.fillna(method='ffill', inplace=True)
df_wanliu.dropna(subset=['PM2.5', 'PM10'], inplace=True)
df_wanshouxigong.dropna(subset=['PM2.5', 'PM10'], inplace=True)
df_wanliu['datetime'] = pd.to_datetime(df_wanliu[['year', 'month', 'day', 'hour']])
df_wanshouxigong['datetime'] = pd.to_datetime(df_wanshouxigong[['year', 'month', 'day', 'hour']])

# Daily averages
df_wanliu_daily = df_wanliu.groupby(df_wanliu['datetime'].dt.date)[['PM2.5', 'PM10']].mean()
df_wanshouxigong_daily = df_wanshouxigong.groupby(df_wanshouxigong['datetime'].dt.date)[['PM2.5', 'PM10']].mean()

# Combine data
df_combined = pd.concat([df_wanliu_daily, df_wanshouxigong_daily], axis=1, keys=['Wanliu', 'Wanshouxigong'])
df_combined.columns = ['Wanliu_PM2.5', 'Wanliu_PM10', 'Wanshouxigong_PM2.5', 'Wanshouxigong_PM10']

# Streamlit UI
st.title("Air Quality Dashboard: PM2.5 & PM10 Comparison")

# Sidebar for date selection
st.sidebar.header("Filter by Date")
start_date = st.sidebar.date_input("Start date", df_combined.index.min())
end_date = st.sidebar.date_input("End date", df_combined.index.max())

# Filter data by date range
mask = (pd.to_datetime(df_combined.index) >= pd.to_datetime(start_date)) & (pd.to_datetime(df_combined.index) <= pd.to_datetime(end_date))
df_filtered = df_combined.loc[mask]

# PM2.5 Comparison
st.header("PM2.5 Levels Over Time")
fig, ax = plt.subplots(figsize=(14, 6))
df_filtered[['Wanliu_PM2.5', 'Wanshouxigong_PM2.5']].plot(ax=ax)
plt.title("PM2.5 Levels")
plt.xlabel("Date")
plt.ylabel("PM2.5 Concentration")
st.pyplot(fig)
st.write("This chart illustrates the variation of PM2.5 levels over time in Wanliu and Wanshouxigong. Significant spikes indicate days with poor air quality, which may correlate with local pollution events.")

# PM10 Comparison
st.header("PM10 Levels Over Time")
fig, ax = plt.subplots(figsize=(14, 6))
df_filtered[['Wanliu_PM10', 'Wanshouxigong_PM10']].plot(ax=ax)
plt.title("PM10 Levels")
plt.xlabel("Date")
plt.ylabel("PM10 Concentration")
st.pyplot(fig)
st.write("This chart compares PM10 levels in both locations. Higher PM10 levels suggest more coarse particulate matter, which can arise from dust, construction, and other activities.")

# Correlation heatmap for Wanliu
st.subheader("Correlation Heatmap - Wanliu")
corr_wanliu = df_wanliu[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'TEMP', 'PRES', 'DEWP', 'RAIN']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_wanliu, annot=True, cmap='coolwarm', center=0, ax=ax)
plt.title('Correlation Matrix - Wanliu')
st.pyplot(fig)
st.write("The heatmap displays correlations among various air quality parameters in Wanliu. Strong correlations indicate potential relationships between pollutants and environmental factors.")

# Correlation heatmap for Wanshouxigong
st.subheader("Correlation Heatmap - Wanshouxigong")
corr_wanshouxigong = df_wanshouxigong[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'TEMP', 'PRES', 'DEWP', 'RAIN']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_wanshouxigong, annot=True, cmap='coolwarm', center=0, ax=ax)
plt.title('Correlation Matrix - Wanshouxigong')
st.pyplot(fig)
st.write("Similar to Wanliu, this heatmap shows the correlation between air quality variables in Wanshouxigong, helping identify relationships that may influence pollution levels.")

# Scatter plot showing the relationship between temperature and NO2 levels
st.subheader("Temperature vs NO2 Levels")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_wanliu, x='TEMP', y='NO2', label='Wanliu', alpha=0.5, ax=ax)
sns.scatterplot(data=df_wanshouxigong, x='TEMP', y='NO2', label='Wanshouxigong', alpha=0.5, ax=ax)
plt.title("Temperature vs NO2")
st.pyplot(fig)
st.write("This scatter plot examines the relationship between temperature and NO2 levels. It can help understand how temperature variations may impact air quality, particularly in urban areas.")

# Sidebar information
st.sidebar.header("About")
st.sidebar.text("This dashboard compares air quality (PM2.5 & PM10) across two locations: Wanliu and Wanshouxigong.")
