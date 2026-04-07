import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# External CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z',
        'crossorigin': 'anonymous'
    }
]

patients=pd.read_csv('IndividualDetails.csv')
total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Sample data for Day by Day Analysis
days = np.arange(1, 61)
cases = np.array([5 * (1.1 ** i) for i in days])

# Sample data for Age Distribution
age_data = {
    'Age Group': ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+', '0-19', 'Missing'],
    'Percentage': [24.9, 21.4, 15.6, 11.8, 8.9, 6.4, 4.2, 5.1, 1.7],
    'Color': ['#3498db', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c', '#34495e', '#95a5a6', '#16a085', '#7f8c8d']
}
age_df = pd.DataFrame(age_data)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("CoronaVirus - India'a Perspective", 
                style={
                    'color': '#2c3e50',
                    'text-align': 'center',
                    'padding': '20px',
                    'background-color': '#5a7a99',
                    'margin': '0',
                    'font-weight': 'bold',
                    'border-radius': '5px'
                })
    ]),
    
    # Stats Cards Row
    html.Div([
        # Total Cases Card
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Cases', style={'color': '#ffffff', 'margin-bottom': '10px'}),
                    html.H2(total, style={'color': '#ffffff', 'font-weight': 'bold'})
                ], className='card-body', style={'text-align': 'center'})
            ], className='card', style={'background-color': '#e74c3c', 'border': 'none', 'border-radius': '10px'})
        ], className='col-md-3'),
        
        # Active Cases Card
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Active', style={'color': '#ffffff', 'margin-bottom': '10px'}),
                    html.H2(active, style={'color': '#ffffff', 'font-weight': 'bold'})
                ], className='card-body', style={'text-align': 'center'})
            ], className='card', style={'background-color': '#3498db', 'border': 'none', 'border-radius': '10px'})
        ], className='col-md-3'),
        
        # Recovered Cases Card
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Recovered', style={'color': '#ffffff', 'margin-bottom': '10px'}),
                    html.H2(recovered, style={'color': '#ffffff', 'font-weight': 'bold'})
                ], className='card-body', style={'text-align': 'center'})
            ], className='card', style={'background-color': '#f1c40f', 'border': 'none', 'border-radius': '10px'})
        ], className='col-md-3'),
        
        # Deaths Card
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Deaths', style={'color': '#ffffff', 'margin-bottom': '10px'}),
                    html.H2(deaths, style={'color': '#ffffff', 'font-weight': 'bold'})
                ], className='card-body', style={'text-align': 'center'})
            ], className='card', style={'background-color': '#2ecc71', 'border': 'none', 'border-radius': '10px'})
        ], className='col-md-3')
    ], className='row', style={'margin-top': '30px', 'margin-bottom': '30px'}),
    
    # Charts Row
    html.Div([
        # Day by Day Analysis Chart
        html.Div([
            html.Div([
                html.Div([
                    html.H5('Day by Day Analysis', style={'text-align': 'center', 'color': '#7f8c8d', 'padding': '15px'}),
                    dcc.Graph(
                        id='day-by-day-chart',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=days,
                                    y=cases,
                                    mode='lines',
                                    line=dict(color='#3498db', width=2),
                                    fill='tonexty',
                                    fillcolor='rgba(52, 152, 219, 0.1)'
                                )
                            ],
                            'layout': go.Layout(
                                xaxis={'title': 'Days', 'showgrid': False},
                                yaxis={'title': 'Number of Cases', 'showgrid': True, 'gridcolor': '#ecf0f1'},
                                margin={'l': 60, 'r': 20, 't': 20, 'b': 60},
                                plot_bgcolor='#ffffff',
                                paper_bgcolor='#ffffff',
                                hovermode='closest'
                            )
                        },
                        config={'displayModeBar': False}
                    )
                ], className='card-body')
            ], className='card', style={'border': 'none', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], className='col-md-7'),
        
        # Age Distribution Chart
        html.Div([
            html.Div([
                html.Div([
                    html.H5('Age Distribution', style={'text-align': 'center', 'color': '#7f8c8d', 'padding': '15px'}),
                    dcc.Graph(
                        id='age-distribution-chart',
                        figure={
                            'data': [
                                go.Pie(
                                    labels=age_df['Age Group'],
                                    values=age_df['Percentage'],
                                    marker=dict(colors=age_df['Color']),
                                    textinfo='label+percent',
                                    textposition='outside',
                                    hole=0.3,
                                    hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>'
                                )
                            ],
                            'layout': go.Layout(
                                margin={'l': 20, 'r': 20, 't': 20, 'b': 20},
                                plot_bgcolor='#ffffff',
                                paper_bgcolor='#ffffff',
                                showlegend=False,
                                height=400
                            )
                        },
                        config={'displayModeBar': False}
                    )
                ], className='card-body')
            ], className='card', style={'border': 'none', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], className='col-md-5')
    ], className='row')
    
], className='container-fluid', style={
    'background-color': '#34495e',
    'min-height': '100vh',
    'padding': '20px'
})

if __name__ == "__main__":
    app.run(debug=True)


