import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px


'''
Questions:
Which site has the largest successful launches?
Which site has the highest launch success rate?
Which payload range(s) has the highest launch success rate?
Which payload range(s) has the lowest launch success rate?
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?'''

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)


sites = [{'label':item, 'value':item} for item in spacex_df['Launch Site'].unique()]
k = [i for i in range(0, 10001, 500)]
v = [{'label': f"{j} (kg)"} for j in k]
marks = {j: v[i] for i, j in enumerate(k)}
app.layout = html.Div(children=[ html.H1('SpaceX - Launch Records', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40,
                                'font-family': 'Montserrat, sans-serif'}),
                                # TASK 1: Add a Launch Site Drop-down Input Component
                                  dcc.Dropdown(id='dropdown',options=sites,
                                    value='All Sites',
                                    placeholder="Launch Sites",
                                    searchable=True,
                                    style={'width':'200px',
                                    'font-size':'20px',
                                    'color':'#333333'}
                                    ),
                                #TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                #TASK 3: Add a Range Slider to Select Payload
                                html.H2('Payload Range'),
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, step = 500, 
                                                value = [min_payload, max_payload], 
                                                marks=marks),
                                html.Br(),
                                #TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))     
                                # html.Br(),
                                # html.Div(dcc.Graph(id='line-plot')),
                                ])
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='dropdown', component_property='value'))

# Task 2 Function
def get_pie_chart(select):
    if select == 'All Sites':
        data = spacex_df[spacex_df['class']==1].groupby('Launch Site').count()
        fig = px.pie(data, values='class', names=data.index, title='Success Launches by Site')
        return fig
    else:
        new_df = spacex_df[spacex_df["Launch Site"] == select]["class"].value_counts()
        fig1 = px.pie(new_df, values=new_df, names=new_df.index, title='Total Success Launches for ' + select)
        return fig1
#Task 4 function
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def scatter(input1, input2):
    if input1 == 'All Sites':
        new_df2 = spacex_df[spacex_df["Payload Mass (kg)"] >= input2[0]]
        new_df3 = new_df2[new_df2["Payload Mass (kg)"] <= input2[1]]
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", color="Booster Version Category")
    else:
        new_df = spacex_df[spacex_df["Launch Site"] == input1]
        new_df2 = new_df[new_df["Payload Mass (kg)"] >= input2[0]]
        new_df3 = new_df2[new_df2["Payload Mass (kg)"] <= input2[1]]
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", color="Booster Version Category")
    return fig2



if __name__ == '__main__':
    app.run_server()