from dash import Dash,dcc,html,Input,Output,callback
import plotly.express as px
import pandas as pd
import os

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
print(df7.head(10))
df7 = df7.groupby(["year","month","Continent","Country_x"],as_index=False).sum("Amount")
print(df7.head(10))
#df7= df7.reset_index(drop=True)
#print(df7.head(10))

app = Dash(__name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no",
        }
    ],
)
app.title = "Sales Report retial"
app.layout= html.Div([
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
