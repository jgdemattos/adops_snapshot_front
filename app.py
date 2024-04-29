import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values #pip
from supabase import create_client, Client
import plotly.express as px

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


st.set_page_config(page_title="Meu Site Streamlit",layout="wide")

response = supabase.table('client_daily').select("date,cod,health,satisfaction,engagement,budget,spend,projection").lt('date', '2024-04-30').gt('date', '2024-04-01').execute()

df = pd.DataFrame(response.data)
df["date"] = pd.to_datetime(df["date"])
df=df.sort_values("date")

cod=st.sidebar.selectbox("Client", list(set(df["cod"])))

df_filtered = df[df["cod"] == cod]

df_filtered

count_data = df_filtered['health'].value_counts().reset_index()
count_data.columns = ['health', 'count']

st.write("DataFrame showing the count of each category:")
st.write(count_data)

# Plotting using Plotly Express
fig = px.bar(count_data, x='health', y='count',
             labels={'Counts': 'Total Counts'},
             title='Bar Chart of Category Counts')
fig.update_layout(xaxis_title='Category', yaxis_title='Total Counts')

# Display the plot in Streamlit
st.plotly_chart(fig)

#col1,col2=st.columns(2)

#fig_date=px.bar(df_filtered, x="health",y="date", title="Saúde em dias")
#col1.plotly_chart(fig_date)

#print(response)
#print(response.data)



