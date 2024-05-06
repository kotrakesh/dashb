import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import os

dash.register_page(__name__,path='/')

p = "https://raw.githubusercontent.com/kotrakesh/dashb/master/data/"
df1=pd.read_csv(p+"Sales.csv")
df1['Date'] = pd.to_datetime(df1['Order Date'])
df1['year'] = df1['Date'].dt.year
df1['month'] = df1['Date'].dt.month

df2=pd.read_csv(p+"Customers.csv", encoding='unicode_escape')
df3 = df1.merge(df2, on='CustomerKey')

df4=pd.read_csv(p+"Products.csv")
df5=df3.merge(df4,on='ProductKey')

df6=pd.read_csv(p+"Stores.csv")
df7=df5.merge(df6,on='StoreKey')
df7['Price'] = df7['Unit Price USD'].str.split(pat='$',n=1).str[1]
df7['Price'] = df7['Price'].str.replace(r',', '').astype(float)
df7['Amount'] = df7['Price']*df7['Quantity']
df7 = df7.groupby(["year","month","Continent","Country_x"],as_index=False).sum("Amount")



title = "Sales Report retial"
layout= html.Div([
    html.H1('Sales Overview'),
    dcc.Graph(id='graph-with-slider', className="dash-bootstrap",),
    dcc.Slider(
        df7['year'].min(),
        df7['year'].max(),
        step=None,
        value=df7['year'].min(),
        marks={str(year): str(year) for year in df7['year'].unique()},
        id='year-slider'

    )
])

@callback(
    Output('graph-with-slider','figure'),
    Input('year-slider','value'))

def update_figure(selected_year):
    filtered_df= df7[df7.year == selected_year]
    fig= px.line(filtered_df, x="month", y="Amount", color='Country_x') 
    #fig = px.scatter(filtered_df, x="month", y="Amount",
    #                 size="Quantity", color="Continent", hover_name="Country_x",
    #                log_x=True,size_max=55)
    fig.layout.template = "plotly_dark"
    fig.update_layout(transition_duration=500)

    return fig
