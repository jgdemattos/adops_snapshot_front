import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values #pip
from supabase import create_client, Client
import plotly.express as px

from datetime import date
from dateutil.relativedelta import relativedelta

def get_past_date(number_of_months):
        return date.today() - relativedelta(months=number_of_months)

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Meu Site Streamlit",layout="wide")

#fetch data from supabase
response = supabase.table('client_daily').select("date,cod,health,satisfaction,engagement,budget,spend,min_revenue, min_investment, ideal_revenue, real_revenue ").lte('date', date.today()).gte('date', get_past_date(2)).execute()

#creates dataframe with supabase data
df = pd.DataFrame(response.data)

#converts "date" string object to datetime
df["date"] = pd.to_datetime(df["date"])

#oders by date
df=df.sort_values("date")

#creates selectbox and filters results by client indentification code ("cod")
cod=st.sidebar.selectbox("Client", list(set(df["cod"])))
df_filtered = df[df["cod"] == cod]

#creates 2 rows with 2 columns each
col1,col2=st.columns(2)
col3,col4=st.columns(2)
col5=st.columns(1)

#counts number of rows with each "health" type
health_count = df_filtered['health'].value_counts().reset_index()
health_count.columns = ['health', 'count']
# plotting using Plotly Express
health_fig = px.pie(health_count, names='health', values='count',
            labels={'Counts': 'Total Counts'},
            title='Número de dias em cada status de saúde',
            color='health',
            color_discrete_map= {    'Ótima': 'green',
                                      'Regular': 'yellow',
                                      'UTI': 'red'}
                                      )
health_fig.update_layout(xaxis_title='Saúde', yaxis_title='Total de dias')
# Display the plot in Streamlit
col1.plotly_chart(health_fig)

satisfaction_count = df_filtered['satisfaction'].value_counts().reset_index()
satisfaction_count.columns = ['satisfaction', 'count']
satisfaction_fig = px.pie(satisfaction_count, names='satisfaction', values='count',
            labels={'Counts': 'Total Counts'},
            title='Número de dias em cada status de satisfação',
            color='satisfaction',
            color_discrete_map= {    'Tudo bem 💕': 'green',
                                      'Incomodado 😢': 'yellow',
                                      'Fudeu 🥵': 'red'}
             )
satisfaction_fig.update_layout(xaxis_title='Satifação', yaxis_title='Total de dias')
col2.plotly_chart(satisfaction_fig)

engagement_count = df_filtered['engagement'].value_counts().reset_index()
engagement_count.columns = ['engagement', 'count']
engagement_fig = px.pie(engagement_count, names='engagement', values='count',
            labels={'Counts': 'Total Counts'},
            title='Número de dias em cada status de engajamento',
            color='engagement',
            color_discrete_map= {    'Alto': 'green',
                                      'Médio': 'yellow',
                                      'Baixo': 'red'}
             )
engagement_fig.update_layout(xaxis_title='Engajamento', yaxis_title='Total de dias')
col3.plotly_chart(engagement_fig)

spend_fig=px.line(df_filtered,markers=True, x="date", y=["budget","spend"],title='Orçamento diário últimos 3 meses')
col4.plotly_chart(spend_fig)

spend_fig=px.line(df_filtered,markers=True, x="date", y=["min_revenue","min_investment","ideal_revenue","real_revenue"],title='Orçamento diário últimos 3 meses')
st.plotly_chart(spend_fig,use_container_width=True)

df_filtered

#fig_date=px.bar(df_filtered, x="health",y="date", title="Saúde em dias")
#col1.plotly_chart(fig_date)

#print(response)
#print(response.data)



