from dash import Dash,dcc,html,Input,Output,callback,page_container,page_registry
import plotly.express as px
import pandas as pd
import os

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
    ], use_pages=True)

app.title = "Sales Report retial"
app.layout= html.Div([
   
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in page_registry.values()
    ]),
    page_container
])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
