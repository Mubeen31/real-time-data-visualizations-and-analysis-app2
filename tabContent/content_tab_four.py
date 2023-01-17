from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from app import app
import plotly.graph_objs as go

layout_tab_four = html.Div([
    dcc.Interval(id='update_value4',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id='line_chart4',
                      config={'displayModeBar': False})
        ], className='tab_page eight columns')

    ], className='tab_content_row row')
])


@app.callback(Output('line_chart4', 'figure'),
              [Input('update_value4', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/3.csv?days=2'
    df = pd.read_csv(url)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['Date'] = pd.to_datetime(df['created_at']).dt.date
    df['Hour'] = pd.to_datetime(df['created_at']).dt.hour
    unique = df['Date'].unique()
    filter_today_date = df[df['Date'] == unique[-1]][['Date', 'Hour', 'field3']]
    today_hourly_values = filter_today_date.groupby(['Date', 'Hour'])['field3'].mean().reset_index()

    return {
        'data': [go.Scatter(
            x=today_hourly_values['Hour'],
            y=today_hourly_values['field3'],
            mode='markers+lines',
            line=dict(width=3, color='rgb(214, 32, 32)'),
            marker=dict(size=7, symbol='circle', color='rgb(214, 32, 32)',
                        line=dict(width=2, color='rgb(214, 32, 32)')),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + today_hourly_values['Date'].astype(str) + '<br>' +
            '<b>Hour</b>: ' + today_hourly_values['Hour'].astype(str) + '<br>' +
            '<b>Light Intensity (lux)</b>: ' + [f'{x:.2f} lux' for x in today_hourly_values['field3']] + '<br>'

        )],
        'layout': go.Layout(
            margin=dict(t=50, l=50, r=40),
            hovermode='closest',
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={'text': '<b>Today Light Intensity (lux)</b>',
                   'y': 0.95,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'size': 17,
                       'color': 'rgb(214, 32, 32)'},
            xaxis=dict(
                tick0=0,
                dtick=1,
                zeroline=False,
                showline=True,
                showgrid=False,
                linecolor='#666666',
                linewidth=1,
                ticks='outside',
                tickfont=dict(family='Arial',
                              size=12,
                              color='#666666')
            ),
            yaxis=dict(
                       zeroline=False,
                       showline=False,
                       showgrid=True,
                       gridcolor='#e6e6e6',
                       tickfont=dict(family='Arial',
                                     size=12,
                                     color='#666666')
                       ),
        )
    }
