import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import os

dash.register_page(__name__,path='/products')

p = os.getcwd()
df1=pd.read_csv(p+"\data\Sales.csv")
df1['Date'] = pd.to_datetime(df1['Order Date'])
df1['year'] = df1['Date'].dt.year
df1['month'] = df1['Date'].dt.month

df2=pd.read_csv(p+"\data\Customers.csv", encoding='unicode_escape')
df3 = df1.merge(df2, on='CustomerKey')

df4=pd.read_csv(p+"\data\Products.csv")
df5=df3.merge(df4,on='ProductKey')

df6=pd.read_csv(p+"\data\Stores.csv")
df7=df5.merge(df6,on='StoreKey')
df7['Price'] = df7['Unit Price USD'].str.split(pat='$',n=1).str[1]
df7['Price'] = df7['Price'].str.replace(r',', '').astype(float)
df7['Amount'] = df7['Price']*df7['Quantity']
df7 = df7.groupby(["year","Continent", "Category", "Product Name"])["Amount"].sum().reset_index()
df7 = df7.sort_values(["Category", "Amount"], ascending=[True, False])
#print(df7.head(20))

title = "Sales Report - product details"
category_options = df7['Category'].unique()
continent_options = df7['Continent'].unique()
layout= html.Div([
    html.H1('Top Products'),
    html.Div([
            dcc.Dropdown(
                category_options,
                value=category_options[0],
                id='category-filter'
                )
            ],style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
            dcc.Dropdown(
                continent_options,
                value=continent_options[0],
                id='continent-filter'
                )
                ], style={'width': '48%', 'display': 'inline-block'}),

         
    dcc.Graph(id='graph-with-slider-product', className="dash-bootstrap",),

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
    Output('graph-with-slider-product','figure'),
    Input('year-slider','value'),
    Input('category-filter', 'value'),
    Input('continent-filter', 'value'))

def update_figure(selected_year,category,continent):
    filtered_df= df7[(df7.year == selected_year)]
    filtered_df= filtered_df[filtered_df.Continent == continent]
    filtered_df= filtered_df[filtered_df.Category == category].head(5)
    fig= px.bar(filtered_df, x="Product Name", y="Amount", color='Product Name') 
    fig.layout.template = "plotly_dark"
    fig.update_layout(transition_duration=500)

    return fig
