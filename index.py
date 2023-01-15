import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime
from app import app
from tabContent.content_tab_one import layout_tab_one
from tabContent.content_tab_two import layout_tab_two

tab_style = {
    'height': '35px',
    'padding': '7.5px',
    'border-top': 'none',
    'border-bottom': 'none',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)'
}

selected_tab_style = {
    'height': '35px',
    'padding': '7.5px',
    'border-top': 'none',
    'border-bottom': '2px solid blue',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'fontWeight': 'bold'
}

app.layout = html.Div([

    dcc.Interval(id='update_value',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([

            html.Div([
                html.Img(src=app.get_asset_url('real-time.png'),
                         className='image'),
                html.Div('Real Time Data Visualizations and Analysis',
                         className='title_text')
            ], className='title_image_row'),

            html.Div([
                html.Div('Sensor location:'),
                html.Div('Walsall, England', className='location_name')
            ], className='location_row'),

            html.Div(id='data_update_time')

        ], className='title_background twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', value='tab_content_one', children=[
                dcc.Tab(label='Real Time',
                        value='tab_content_one',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(label='Humidity',
                        value='tab_content_two',
                        style=tab_style,
                        selected_style=selected_tab_style)
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], className='tabs_container eight columns')
    ], className='display_center_row row'),

    html.Div(id='return_tab_content', children=[])

])


@app.callback(Output('return_tab_content', 'children'),
              [Input('tabs', 'value')])
def update_content(tabs):
    if tabs == 'tab_content_one':
        return layout_tab_one
    elif tabs == 'tab_content_two':
        return layout_tab_two


@app.callback(Output('data_update_time', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/1/last.csv'
    df = pd.read_csv(url)
    date_time = df['created_at'].iloc[0]
    get_date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
    last_date_time = get_date_time.strftime('%Y-%m-%d %H:%M:%S')

    return [
        html.Div([
            html.Div('Last data update time:'),
            html.Div(last_date_time, className='location_name')
        ], className='date_time_row')
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
