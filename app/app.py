from dash import Dash,dcc,html,Input,Output,callback,page_container,page_registry
import plotly.express as px
import pandas as pd
import os

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

port = os.environ.get('dash_port')
debug = os.environ.get('dash_debug')=="True"
if __name__ == '__main__':
    app.run(debug=debug ,host="0.0.0.0", port=port)
