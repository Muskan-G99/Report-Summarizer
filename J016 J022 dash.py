import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('C:/Users/Ojasvi/Desktop/final.csv')

summary = {}
table = {}
for index, row in df.iterrows():
    if len(row['tables']) == 13:
        summary[row['subtopics']] = row['summary']
    else:
        table[row['subtopics']] = row['tables']


fnameDict = {}
topi = df.groupby(['topics'])
for t,d in topi:
    fnameDict[t] = list(d['subtopics'])



app = dash.Dash()

names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

app.layout = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label':name, 'value':name} for name in names],
            value = list(fnameDict.keys())[0]
            ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='opt-dropdown',
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Hr(),
        html.Div(id='display-selected-values')
    ]
)

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('name-dropdown', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in fnameDict[name]]

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('opt-dropdown', 'value')])
def set_display_children(selected_value):
    if selected_value in summary.keys():
        return summary[selected_value]
    else:
        return 'table'


if __name__ == '__main__':
    app.run_server()